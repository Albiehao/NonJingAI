"""农作物管理 API - Crop Agent 的农作物字典和用户关联管理"""

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from server.utils.auth_middleware import get_admin_user, get_db, get_required_user
from src.storage.postgres.models_business import User, UserAddress
from src.storage.postgres.models_crop import Crop, UserCrop
from src.utils import geohash_util
from src.utils import logger

crop_mgr = APIRouter(prefix="/crops", tags=["crop-management"])


# =============================================================================
# === Pydantic Schemas ===
# =============================================================================


class CropCreate(BaseModel):
    name: str
    scientific_name: str | None = None
    category: str | None = None
    icon: str | None = None
    description: str | None = None


class CropUpdate(BaseModel):
    name: str | None = None
    scientific_name: str | None = None
    category: str | None = None
    icon: str | None = None
    description: str | None = None


class CropResponse(BaseModel):
    id: int
    name: str
    scientific_name: str | None = None
    category: str | None = None
    icon: str | None = None
    description: str | None = None
    created_at: str | None = None
    updated_at: str | None = None


class UserCropCreate(BaseModel):
    crop_id: int
    nickname: str | None = None
    planted_at: str | None = None
    area: float | None = None
    notes: str | None = None


class UserCropResponse(BaseModel):
    id: int
    crop_id: int
    crop_name: str
    nickname: str | None = None
    planted_at: str | None = None
    area: float | None = None
    status: str
    notes: str | None = None
    created_at: str | None = None


class AddressUpdate(BaseModel):
    address: str
    latitude: float
    longitude: float


# =============================================================================
# === 用户地址管理（必须在 /{crop_id} 之前定义，避免路由冲突） ===
# =============================================================================


@crop_mgr.put("/address")
async def update_address(
    data: AddressUpdate,
    current_user: User = Depends(get_required_user),
    db: AsyncSession = Depends(get_db),
):
    """更新当前用户的地址和地理位置信息"""
    gh_10km, gh_20km = geohash_util.encode_precisions(data.latitude, data.longitude)
    gh_full = geohash_util.encode(data.latitude, data.longitude, 8)

    ua = current_user.user_address
    if ua is None:
        ua = UserAddress(user_id=current_user.id)
        db.add(ua)
        current_user.user_address = ua

    ua.address = data.address
    ua.latitude = data.latitude
    ua.longitude = data.longitude
    ua.geohash_10km = gh_10km
    ua.geohash_20km = gh_20km
    ua.geohash = gh_full
    ua.geo_context = {"latitude": data.latitude, "longitude": data.longitude}

    await db.commit()
    logger.info(f"User {current_user.id} address updated: {data.address} ({gh_full})")

    return {
        "success": True,
        "address": ua.address,
        "latitude": ua.latitude,
        "longitude": ua.longitude,
        "geohash": gh_full,
        "geohash_10km": gh_10km,
        "geohash_20km": gh_20km,
    }


# =============================================================================
# === 农作物字典 CRUD（管理员）===
# =============================================================================


@crop_mgr.get("", response_model=list[CropResponse])
async def list_crops(
    category: str | None = None,
    current_user: User = Depends(get_required_user),
    db: AsyncSession = Depends(get_db),
):
    """获取农作物列表（已登录用户可用）"""
    query = select(Crop).where(Crop.deleted_at.is_(None))
    if category:
        query = query.where(Crop.category == category)
    query = query.order_by(Crop.name)
    result = await db.execute(query)
    crops = result.scalars().all()
    return [
        CropResponse(
            id=c.id,
            name=c.name,
            scientific_name=c.scientific_name,
            category=c.category,
            icon=c.icon,
            description=c.description,
            created_at=str(c.created_at) if c.created_at else None,
            updated_at=str(c.updated_at) if c.updated_at else None,
        )
        for c in crops
    ]


@crop_mgr.post("", response_model=CropResponse)
async def create_crop(
    data: CropCreate,
    current_user: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """新增农作物（管理员）"""
    existing = await db.execute(select(Crop).where(Crop.name == data.name, Crop.deleted_at.is_(None)))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="该作物名称已存在")

    crop = Crop(
        name=data.name,
        scientific_name=data.scientific_name,
        category=data.category,
        icon=data.icon,
        description=data.description,
        created_by=current_user.id,
    )
    db.add(crop)
    await db.commit()
    await db.refresh(crop)
    return CropResponse(
        id=crop.id,
        name=crop.name,
        scientific_name=crop.scientific_name,
        category=crop.category,
        icon=crop.icon,
        description=crop.description,
        created_at=str(crop.created_at) if crop.created_at else None,
        updated_at=str(crop.updated_at) if crop.updated_at else None,
    )


@crop_mgr.put("/{crop_id}", response_model=CropResponse)
async def update_crop(
    crop_id: int,
    data: CropUpdate,
    current_user: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """更新农作物（管理员）"""
    result = await db.execute(select(Crop).where(Crop.id == crop_id, Crop.deleted_at.is_(None)))
    crop = result.scalar_one_or_none()
    if not crop:
        raise HTTPException(status_code=404, detail="农作物不存在")

    if data.name is not None:
        dup = await db.execute(
            select(Crop).where(Crop.name == data.name, Crop.id != crop_id, Crop.deleted_at.is_(None))
        )
        if dup.scalar_one_or_none():
            raise HTTPException(status_code=409, detail="该作物名称已存在")
        crop.name = data.name
    if data.scientific_name is not None:
        crop.scientific_name = data.scientific_name
    if data.category is not None:
        crop.category = data.category
    if data.icon is not None:
        crop.icon = data.icon
    if data.description is not None:
        crop.description = data.description

    await db.commit()
    await db.refresh(crop)
    return CropResponse(
        id=crop.id,
        name=crop.name,
        scientific_name=crop.scientific_name,
        category=crop.category,
        icon=crop.icon,
        description=crop.description,
        created_at=str(crop.created_at) if crop.created_at else None,
        updated_at=str(crop.updated_at) if crop.updated_at else None,
    )


@crop_mgr.delete("/{crop_id}")
async def delete_crop(
    crop_id: int,
    current_user: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """删除农作物（管理员，软删除）"""
    result = await db.execute(select(Crop).where(Crop.id == crop_id, Crop.deleted_at.is_(None)))
    crop = result.scalar_one_or_none()
    if not crop:
        raise HTTPException(status_code=404, detail="农作物不存在")

    crop.deleted_at = datetime.now()
    await db.commit()
    return {"success": True}


# =============================================================================
# === 用户作物关联 ===
# =============================================================================


@crop_mgr.get("/nearby")
async def find_nearby_users(
    latitude: float,
    longitude: float,
    precision: int = 4,
    limit: int = 50,
    current_user: User = Depends(get_required_user),
    db: AsyncSession = Depends(get_db),
):
    """根据 geohash 多级前缀匹配查找附近的用户。

    precision 参数控制搜索精度:
      1: ±2500km,  2: ±630km,  3: ±78km,  4: ±20km,
      5: ±2.4km,   6: ±610m,   7: ±76m,   8: ±19m
    """
    from sqlalchemy.orm import contains_eager
    query_prefix = geohash_util.encode(latitude, longitude, min(precision, 8))

    result = await db.execute(
        select(User)
        .join(UserAddress, User.id == UserAddress.user_id)
        .options(contains_eager(User.user_address))
        .where(
            UserAddress.geohash.isnot(None),
            UserAddress.geohash.startswith(query_prefix),
        )
        .limit(limit)
    )
    users = result.unique().scalars().all()

    # 附带农作物信息
    user_ids = [u.id for u in users]
    crops_map = {}
    if user_ids:
        uc_result = await db.execute(
            select(UserCrop).where(
                UserCrop.user_id.in_(user_ids),
                UserCrop.deleted_at.is_(None),
            )
        )
        user_crops = uc_result.scalars().all()
        for uc in user_crops:
            crops_map.setdefault(uc.user_id, []).append({
                "crop_id": uc.crop_id,
                "nickname": uc.nickname,
            })

    return [
        {
            "id": u.id,
            "username": u.username,
            "address": u.user_address.address if u.user_address else None,
            "latitude": u.user_address.latitude if u.user_address else None,
            "longitude": u.user_address.longitude if u.user_address else None,
            "geohash": u.user_address.geohash if u.user_address else None,
            "crops": crops_map.get(u.id, []),
        }
        for u in users
    ]


@crop_mgr.get("/my", response_model=list[UserCropResponse])
async def list_my_crops(
    current_user: User = Depends(get_required_user),
    db: AsyncSession = Depends(get_db),
):
    """获取当前用户关联的农作物"""
    query = (
        select(UserCrop)
        .where(UserCrop.user_id == current_user.id, UserCrop.deleted_at.is_(None))
        .order_by(UserCrop.created_at.desc())
    )
    result = await db.execute(query)
    user_crops = result.scalars().all()

    # Fetch crop names
    crop_ids = [uc.crop_id for uc in user_crops]
    if crop_ids:
        crops_result = await db.execute(select(Crop).where(Crop.id.in_(crop_ids)))
        crop_map = {c.id: c.name for c in crops_result.scalars().all()}
    else:
        crop_map = {}

    return [
        UserCropResponse(
            id=uc.id,
            crop_id=uc.crop_id,
            crop_name=crop_map.get(uc.crop_id, "未知"),
            nickname=uc.nickname,
            planted_at=str(uc.planted_at) if uc.planted_at else None,
            area=uc.area,
            status=uc.status,
            notes=uc.notes,
            created_at=str(uc.created_at) if uc.created_at else None,
        )
        for uc in user_crops
    ]


@crop_mgr.post("/my", response_model=UserCropResponse)
async def add_my_crop(
    data: UserCropCreate,
    current_user: User = Depends(get_required_user),
    db: AsyncSession = Depends(get_db),
):
    """添加农作物关联"""
    # Check crop exists
    result = await db.execute(select(Crop).where(Crop.id == data.crop_id, Crop.deleted_at.is_(None)))
    crop = result.scalar_one_or_none()
    if not crop:
        raise HTTPException(status_code=404, detail="农作物不存在")

    # Check duplicate
    existing = await db.execute(
        select(UserCrop).where(
            UserCrop.user_id == current_user.id,
            UserCrop.crop_id == data.crop_id,
            UserCrop.deleted_at.is_(None),
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="已关联该农作物")

    planted_at = None
    if data.planted_at:
        planted_at = datetime.strptime(data.planted_at, "%Y-%m-%d").date()

    uc = UserCrop(
        user_id=current_user.id,
        crop_id=data.crop_id,
        nickname=data.nickname,
        planted_at=planted_at,
        area=data.area,
        notes=data.notes,
    )
    db.add(uc)
    await db.commit()
    await db.refresh(uc)

    return UserCropResponse(
        id=uc.id,
        crop_id=uc.crop_id,
        crop_name=crop.name,
        nickname=uc.nickname,
        planted_at=str(uc.planted_at) if uc.planted_at else None,
        area=uc.area,
        status=uc.status,
        notes=uc.notes,
        created_at=str(uc.created_at) if uc.created_at else None,
    )


@crop_mgr.delete("/my/{uc_id}")
async def remove_my_crop(
    uc_id: int,
    current_user: User = Depends(get_required_user),
    db: AsyncSession = Depends(get_db),
):
    """删除农作物关联"""
    result = await db.execute(
        select(UserCrop).where(
            UserCrop.id == uc_id, UserCrop.user_id == current_user.id, UserCrop.deleted_at.is_(None)
        )
    )
    uc = result.scalar_one_or_none()
    if not uc:
        raise HTTPException(status_code=404, detail="关联不存在")

    uc.deleted_at = datetime.now()
    await db.commit()
    return {"success": True}
