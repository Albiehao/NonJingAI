"""Webhook 数据访问层"""

from datetime import datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.storage.postgres.manager import pg_manager
from src.storage.postgres.models_business import WebhookEvent, WebhookSource
from src.utils.datetime_utils import utc_now_naive


class WebhookRepository:
    """Webhook 推送源配置数据访问"""

    # ---- WebhookSource ----

    async def list_sources(self, skip: int = 0, limit: int = 100) -> list[WebhookSource]:
        async with pg_manager.get_async_session_context() as session:
            result = await session.execute(
                select(WebhookSource).order_by(WebhookSource.id.desc()).offset(skip).limit(limit)
            )
            return list(result.scalars().all())

    async def get_source_by_id(self, source_id: int) -> WebhookSource | None:
        async with pg_manager.get_async_session_context() as session:
            result = await session.execute(
                select(WebhookSource).where(WebhookSource.id == source_id)
            )
            return result.scalar_one_or_none()

    async def get_source_by_token(self, secret_token: str) -> WebhookSource | None:
        async with pg_manager.get_async_session_context() as session:
            result = await session.execute(
                select(WebhookSource).where(WebhookSource.secret_token == secret_token)
            )
            return result.scalar_one_or_none()

    async def create_source(self, data: dict[str, Any]) -> WebhookSource:
        async with pg_manager.get_async_session_context() as session:
            source = WebhookSource(**data)
            session.add(source)
            await session.commit()
            await session.refresh(source)
            return source

    async def update_source(self, source_id: int, data: dict[str, Any]) -> WebhookSource | None:
        async with pg_manager.get_async_session_context() as session:
            result = await session.execute(
                select(WebhookSource).where(WebhookSource.id == source_id)
            )
            source = result.scalar_one_or_none()
            if source is None:
                return None
            data.pop("id", None)
            for key, value in data.items():
                setattr(source, key, value)
            source.updated_at = utc_now_naive()
            await session.commit()
            await session.refresh(source)
            return source

    async def delete_source(self, source_id: int) -> bool:
        async with pg_manager.get_async_session_context() as session:
            result = await session.execute(
                select(WebhookSource).where(WebhookSource.id == source_id)
            )
            source = result.scalar_one_or_none()
            if source is None:
                return False
            await session.delete(source)
            await session.commit()
            return True

    # ---- WebhookEvent ----

    async def list_events(
        self, source_id: int | None = None, skip: int = 0, limit: int = 50
    ) -> list[WebhookEvent]:
        async with pg_manager.get_async_session_context() as session:
            query = select(WebhookEvent).order_by(WebhookEvent.id.desc())
            if source_id is not None:
                query = query.where(WebhookEvent.source_id == source_id)
            query = query.offset(skip).limit(limit)
            result = await session.execute(query)
            return list(result.scalars().all())

    async def get_event_by_id(self, event_id: int) -> WebhookEvent | None:
        async with pg_manager.get_async_session_context() as session:
            result = await session.execute(
                select(WebhookEvent).where(WebhookEvent.id == event_id)
            )
            return result.scalar_one_or_none()

    async def create_event(self, data: dict[str, Any]) -> WebhookEvent:
        async with pg_manager.get_async_session_context() as session:
            event = WebhookEvent(**data)
            session.add(event)
            await session.commit()
            await session.refresh(event)
            return event

    async def update_event(
        self, event_id: int, data: dict[str, Any]
    ) -> WebhookEvent | None:
        async with pg_manager.get_async_session_context() as session:
            result = await session.execute(
                select(WebhookEvent).where(WebhookEvent.id == event_id)
            )
            event = result.scalar_one_or_none()
            if event is None:
                return None
            data.pop("id", None)
            for key, value in data.items():
                setattr(event, key, value)
            if data.get("status") in ("completed", "failed"):
                event.processed_at = datetime.utcnow()
            await session.commit()
            await session.refresh(event)
            return event
