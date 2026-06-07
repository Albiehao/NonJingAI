"""用户数据访问层 - Repository"""

from typing import Annotated, Any

from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from src.storage.postgres.manager import pg_manager
from src.storage.postgres.models_business import User, UserAddress
from src.storage.postgres.models_crop import Crop, UserCrop
from src.utils.check_geo_util import get_geo_location
from src.utils.datetime_utils import utc_now_naive


class UserRepository:
    """用户数据访问层"""

    async def get_by_id(self, id: int) -> User | None:
        """根据 ID 获取用户"""
        async with pg_manager.get_async_session_context() as session:
            result = await session.execute(
                select(User).options(selectinload(User.user_address)).where(User.id == id)
            )
            return result.scalar_one_or_none()

    async def get_by_user_id(self, user_id: str) -> User | None:
        """根据 user_id 获取用户"""
        async with pg_manager.get_async_session_context() as session:
            result = await session.execute(
                select(User).options(selectinload(User.user_address)).where(User.user_id == user_id)
            )
            return result.scalar_one_or_none()

    async def get_by_phone(self, phone: str) -> User | None:
        """根据手机号获取用户"""
        async with pg_manager.get_async_session_context() as session:
            result = await session.execute(
                select(User).options(selectinload(User.user_address)).where(User.phone_number == phone)
            )
            return result.scalar_one_or_none()

    async def list_users(
        self, skip: int = 0, limit: int = 100, role: str | None = None
    ) -> list[User]:
        """获取用户列表"""
        async with pg_manager.get_async_session_context() as session:
            query = select(User).options(selectinload(User.user_address)).where(User.is_deleted == 0)
            if role is not None:
                query = query.where(User.role == role)
            query = query.order_by(User.id.asc()).offset(skip).limit(limit)
            result = await session.execute(query)
            return list(result.scalars().all())


    async def create(self, data: dict[str, Any]) -> User:
        """创建用户"""
        async with pg_manager.get_async_session_context() as session:
            user = User(**data)
            session.add(user)
            await session.commit()
            await session.refresh(user)
        return user


    async def update(self, id: int, data: dict[str, Any]) -> User | None:
        """更新用户"""
        async with pg_manager.get_async_session_context() as session:
            result = await session.execute(
                select(User).options(selectinload(User.user_address)).where(User.id == id, User.is_deleted == 0)
            )
            user = result.scalar_one_or_none()
            if user is None:
                return None
            for key, value in data.items():
                if key != "id":
                    setattr(user, key, value)
        return user

    async def geo_context_update(self, id: int, geo_context: dict[str, Any]) -> User | None:
        """更新用户地理位置信息"""
        async with pg_manager.get_async_session_context() as session:
            result = await session.execute(
                select(User).options(selectinload(User.user_address)).where(User.id == id, User.is_deleted == 0)
            )
            user = result.scalar_one_or_none()
            if user is None:
                return None
            if user.user_address is None:
                ua = UserAddress(user_id=user.id, geo_context=geo_context)
                session.add(ua)
                user.user_address = ua
            else:
                user.user_address.geo_context = geo_context
        return user

    async def soft_delete(self, id: int, username: str | None = None, phone_number: str | None = None) -> bool:
        """软删除用户"""
        async with pg_manager.get_async_session_context() as session:
            result = await session.execute(select(User).where(User.id == id, User.is_deleted == 0))
            user = result.scalar_one_or_none()
            if user is None:
                return False
            user.is_deleted = 1

            user.deleted_at = utc_now_naive()
            if username:
                import hashlib

                hash_suffix = hashlib.sha256(user.user_id.encode()).hexdigest()[:4]
                user.username = f"已注销用户-{hash_suffix}"
            if phone_number:
                user.phone_number = None
        return True

    async def exists_by_user_id(self, user_id: str) -> bool:
        """检查 user_id 是否存在"""
        async with pg_manager.get_async_session_context() as session:
            result = await session.execute(select(User.id).where(User.user_id == user_id))
            return result.scalar_one_or_none() is not None

    async def exists_by_phone(self, phone: str) -> bool:
        """检查手机号是否存在"""
        async with pg_manager.get_async_session_context() as session:
            result = await session.execute(select(User.id).where(User.phone_number == phone))
            return result.scalar_one_or_none() is not None

    async def count(self) -> int:
        """统计用户数量"""
        async with pg_manager.get_async_session_context() as session:
            query = select(func.count(User.id)).where(User.is_deleted == 0)
            result = await session.execute(query)
            return result.scalar() or 0

    async def get_all_user_ids(self) -> list[str]:
        """获取所有用户 ID"""
        async with pg_manager.get_async_session_context() as session:
            result = await session.execute(select(User.user_id))
            return [uid for (uid,) in result.all()]

    async def get_users_by_crop_names(self, crop_names: list[str]) -> list[User]:
        """根据农作物名称查找用户"""
        if not crop_names:
            return []
        async with pg_manager.get_async_session_context() as session:
            crop_ids_result = await session.execute(
                select(Crop.id).where(Crop.name.in_(crop_names), Crop.deleted_at.is_(None))
            )
            crop_ids = [row[0] for row in crop_ids_result.all()]
            if not crop_ids:
                return []
            user_ids_result = await session.execute(
                select(UserCrop.user_id)
                .where(UserCrop.crop_id.in_(crop_ids), UserCrop.deleted_at.is_(None))
                .distinct()
            )
            user_pk_ids = [row[0] for row in user_ids_result.all()]
            if not user_pk_ids:
                return []
            result = await session.execute(
                select(User)
                .options(selectinload(User.user_address))
                .where(User.id.in_(user_pk_ids), User.is_deleted == 0)
            )
            return list(result.scalars().all())

    async def get_users_by_address_contains(self, text: str) -> list[User]:
        """根据地址模糊查找用户"""
        if not text:
            return []
        async with pg_manager.get_async_session_context() as session:
            result = await session.execute(
                select(User)
                .options(selectinload(User.user_address))
                .join(UserAddress, User.id == UserAddress.user_id)
                .where(
                    User.is_deleted == 0,
                    UserAddress.address.ilike(f"%{text}%"),
                )
            )
            return list(result.unique().scalars().all())

    async def get_user_in_geo(self, geo_context: dict[str, float], radius_km: float = 10) -> list[User]:
        """获取用户在 radius_km 公里范围内"""
        async with pg_manager.get_async_session_context() as session:
            center = get_geo_location(geo_context)
            if not center:
                return []

            from sqlalchemy.orm import contains_eager

            result = await session.execute(
                select(User)
                .join(UserAddress, User.id == UserAddress.user_id)
                .options(contains_eager(User.user_address))
                .where(
                    User.is_deleted == 0,
                    UserAddress.geo_context.is_not(None)
                )
            )
            users = result.unique().scalars().all()

            # 应用层过滤
            radius_meters = radius_km * 1000
            return [
                user for user in users
                if (user_loc := get_geo_location(user.user_address.geo_context))
                   and center.distance_to(user_loc) <= radius_meters
            ]

