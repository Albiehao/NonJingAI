from fastapi import APIRouter

from server.routers.auth_router import auth
from server.routers.chat_router import chat
from server.routers.crop_router import crop_mgr
from server.routers.dashboard_router import dashboard
from server.routers.graph_router import graph
from server.routers.knowledge_router import knowledge
from server.routers.evaluation_router import evaluation
from server.routers.mindmap_router import mindmap
from server.routers.system_router import system
from server.routers.task_router import tasks
from server.routers.webhook_router import webhook
from server.routers.wechat_router import wechat_router
from server.routers.storage_router import storage_router
from server.routers.device_router import router as device_router
from .cart_router import router as cart_router
from .orders_router import router as orders_router
from .payment_router import router as payment_router
try:
    from server.routers.email_router import email_router
except ImportError:
    import logging as _logging

    _logging.warning("email-validator 未安装，电子邮件功能不可用。")
    email_router = None  # type: ignore[assignment]

router = APIRouter()

# 注册路由结构
router.include_router(system)  # /api/system/*
router.include_router(auth)  # /api/auth/*
router.include_router(chat)  # /api/chat/*
router.include_router(crop_mgr)  # /api/crops/*
router.include_router(dashboard)  # /api/dashboard/*
router.include_router(knowledge)  # /api/knowledge/*
router.include_router(evaluation)  # /api/evaluation/*
router.include_router(mindmap)  # /api/mindmap/*
router.include_router(graph)  # /api/graph/*
router.include_router(tasks)  # /api/tasks/*
router.include_router(webhook)  # /api/webhook/*
router.include_router(wechat_router)  # /api/wechat/*
router.include_router(storage_router)  # /api/storage/*
router.include_router(device_router)  # /api/devices/*
router.include_router(cart_router)
router.include_router(orders_router)
router.include_router(payment_router)
if email_router is not None:
    router.include_router(email_router)  # /api/email/*
