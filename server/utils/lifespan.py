from contextlib import asynccontextmanager

from fastapi import FastAPI
from src.storage.postgres.models_business import TaskRecord # noqa: F401
from src.services.task_service import tasker
from src.storage.postgres.manager import pg_manager
from src.knowledge import knowledge_base
from src.utils import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI lifespan事件管理器"""
    # 初始化数据库连接
    try:
        pg_manager.initialize()
        await pg_manager.create_business_tables()
        await pg_manager.ensure_knowledge_schema()
    except Exception as e:
        logger.error(f"Failed to initialize database during startup: {e}")

# 初始化知识库管理器
    try:
        await knowledge_base.initialize()
    except Exception as e:
        logger.error(f"Failed to initialize knowledge base manager: {e}")

    await tasker.start()
    yield
    await tasker.shutdown()
    await pg_manager.close()
