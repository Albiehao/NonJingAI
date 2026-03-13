from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.storage.postgres.models_business import AgentConfig
from src.utils.datetime_utils import utc_now_naive

# 默认配置名称
DEFAULT_CONFIG_NAME = "默认配置"


class AgentConfigRepository:
    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    async def get_by_id(self, config_id: int) -> AgentConfig | None:
        result = await self.db.execute(select(AgentConfig).where(AgentConfig.id == config_id))
        return result.scalar_one_or_none()

    async def list_by_agent(self, agent_id: str) -> list[AgentConfig]:
        """获取指定智能体的所有配置"""
        result = await self.db.execute(
            select(AgentConfig)
            .where(AgentConfig.agent_id == agent_id)
            .order_by(AgentConfig.is_default.desc(), AgentConfig.created_at)
        )
        return result.scalars().all()

    async def get_or_create_default(self, agent_id: str, created_by: str | None = None) -> AgentConfig:
        """获取或创建默认配置"""
        # 先尝试获取默认配置
        result = await self.db.execute(
            select(AgentConfig).where(AgentConfig.agent_id == agent_id, AgentConfig.is_default.is_(True))
        )
        default_config = result.scalar_one_or_none()

        if default_config is not None:
            return default_config

        # 如果没有默认配置，检查是否有任何配置
        result = await self.db.execute(
            select(AgentConfig).where(AgentConfig.agent_id == agent_id).order_by(AgentConfig.created_at)
        )
        first_config = result.scalar_one_or_none()

        if first_config is not None:
            return first_config

        # 创建默认配置
        return await self.create(
            agent_id=agent_id,
            name=DEFAULT_CONFIG_NAME,
            description="系统自动创建的默认配置",
            is_default=True,
            created_by=created_by,
        )

    async def _name_exists(self, *, agent_id: str, name: str, exclude_id: int | None) -> bool:
        stmt = select(AgentConfig.id).where(
            AgentConfig.agent_id == agent_id,
            AgentConfig.name == name,
        )
        if exclude_id is not None:
            stmt = stmt.where(AgentConfig.id != exclude_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none() is not None

    async def ensure_unique_name(
        self,
        *,
        agent_id: str,
        desired_name: str,
        exclude_id: int | None = None,
    ) -> str:
        candidate = desired_name.strip() or "未命名配置"
        if not await self._name_exists(
            agent_id=agent_id, name=candidate, exclude_id=exclude_id
        ):
            return candidate

        base = f"{candidate}-副本"
        if not await self._name_exists(
            agent_id=agent_id, name=base, exclude_id=exclude_id
        ):
            return base

        idx = 2
        while True:
            candidate2 = f"{base}{idx}"
            if not await self._name_exists(
                agent_id=agent_id, name=candidate2, exclude_id=exclude_id
            ):
                return candidate2
            idx += 1

    async def create(
        self,
        *,
        agent_id: str,
        name: str,
        description: str | None = None,
        icon: str | None = None,
        pics: list[str] | None = None,
        examples: list[str] | None = None,
        config_json: dict | None = None,
        is_default: bool = False,
        created_by: str | None = None,
    ) -> AgentConfig:
        unique_name = await self.ensure_unique_name(
            agent_id=agent_id,
            desired_name=name,
            exclude_id=None,
        )
        config = AgentConfig(
            agent_id=agent_id,
            name=unique_name,
            description=description,
            icon=icon,
            pics=pics or [],
            examples=examples or [],
            config_json=config_json or {},
            is_default=bool(is_default),
            created_by=created_by,
            updated_by=created_by,
            created_at=utc_now_naive(),
            updated_at=utc_now_naive(),
        )
        self.db.add(config)
        await self.db.commit()
        await self.db.refresh(config)
        return config

    async def update(
        self,
        config: AgentConfig,
        *,
        name: str | None = None,
        description: str | None = None,
        icon: str | None = None,
        pics: list[str] | None = None,
        examples: list[str] | None = None,
        config_json: dict | None = None,
        updated_by: str | None = None,
    ) -> AgentConfig:
        if name is not None:
            config.name = await self.ensure_unique_name(
                agent_id=config.agent_id,
                desired_name=name,
                exclude_id=config.id,
            )
        if description is not None:
            config.description = description
        if icon is not None:
            config.icon = icon
        if pics is not None:
            config.pics = pics
        if examples is not None:
            config.examples = examples
        if config_json is not None:
            config.config_json = config_json

        config.updated_by = updated_by
        config.updated_at = utc_now_naive()
        await self.db.commit()
        await self.db.refresh(config)
        return config

    async def set_default(self, *, config: AgentConfig, updated_by: str | None = None) -> AgentConfig:
        """设置某个配置为默认，同时将其他配置取消默认"""
        from sqlalchemy import update as sa_update

        # 先将所有该 agent_id 的配置取消默认
        await self.db.execute(
            sa_update(AgentConfig)
            .where(AgentConfig.agent_id == config.agent_id)
            .values(is_default=False, updated_by=updated_by, updated_at=utc_now_naive())
        )

        # 然后设置当前配置为默认
        config.is_default = True
        config.updated_by = updated_by
        config.updated_at = utc_now_naive()
        await self.db.commit()
        await self.db.refresh(config)
        return config

    async def delete(self, *, config: AgentConfig, updated_by: str | None = None) -> None:
        await self.db.delete(config)
        await self.db.commit()

