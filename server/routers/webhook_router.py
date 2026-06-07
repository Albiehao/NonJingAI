"""Webhook 推送服务路由 - 接收外部推送和管理配置"""

import json
import uuid

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field

from server.utils.auth_middleware import get_admin_user, get_current_user
from src.repositories.webhook_repository import WebhookRepository
from src.services.webhook_service import webhook_service
from src.storage.postgres.models_business import User
from src.utils.logging_config import logger

webhook = APIRouter(prefix="/webhook", tags=["webhook"])

repo = WebhookRepository()


# ===== Schema =====

class WebhookSourceCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    agent_id: str = Field(default="WebhookAgent", max_length=64)
    prompt_template: str = Field(..., min_length=1)
    extra_prompt: str | None = None
    is_active: bool = True
    secret_token: str | None = None  # 自动生成


class WebhookSourceUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    agent_id: str | None = None
    prompt_template: str | None = None
    extra_prompt: str | None = None
    is_active: bool | None = None
    send_to_all: bool | None = None


class WebhookTestPayload(BaseModel):
    mock_body: str = Field(default="{}", description="模拟的 webhook 请求体 JSON 字符串")


# ===== 管理员接口：内部快速推送 =====

class QuickPushRequest(BaseModel):
    """内部快速推送"""
    source_id: int | None = Field(None, description="推送源 ID，不传则使用第一个活跃源")
    message: str = Field(..., min_length=1, description="推送消息内容")
    crops: list[str] | None = Field(None, description="按农作物筛选")
    address_contains: str | None = Field(None, description="按地址筛选")
    lat: float | None = Field(None, description="纬度")
    lng: float | None = Field(None, description="经度")
    geo_radius_km: float = Field(default=10, description="筛选半径(公里)")


@webhook.post("/quick-push", tags=["webhook-admin"])
async def quick_push(
    body: QuickPushRequest,
    current_user: User = Depends(get_admin_user),
):
    """内部快速推送 - 无需配置外部 Webhook，直接推送给用户"""
    # 确定推送源
    if body.source_id:
        source = await repo.get_source_by_id(body.source_id)
    else:
        sources = await repo.list_sources(limit=10)
        source = next((s for s in sources if s.is_active), None)

    if not source:
        # 自动创建默认推送源
        source = await repo.create_source({
            "name": "系统默认推送",
            "description": "系统自动创建的默认推送源",
            "secret_token": uuid.uuid4().hex,
            "agent_id": "WebhookAgent",
            "prompt_template": "您有一条新的系统推送消息",
            "extra_prompt": None,
            "is_active": True,
            "send_to_all": True,
            "created_by": "system",
        })

    # 构建 webhook_data
    webhook_data: dict = {"message": body.message}
    filters: dict = {}
    if body.crops:
        filters["crops"] = body.crops
    if body.address_contains:
        filters["address_contains"] = body.address_contains
    if body.lat is not None and body.lng is not None:
        filters["geo"] = {"lat": body.lat, "lng": body.lng}
        filters["geo_radius_km"] = body.geo_radius_km
    if filters:
        webhook_data["filters"] = filters

    raw_body = json.dumps(webhook_data, ensure_ascii=False)
    try:
        result = await webhook_service.receive_webhook(source.secret_token, raw_body)
        return {
            "code": 0,
            "message": f"推送任务已提交，使用推送源「{source.name}」",
            "data": {
                "event_id": result["event_id"],
                "status": result["status"],
                "source_name": source.name,
            },
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ===== 公开接口：接收 Webhook 推送 =====

@webhook.post("/receive/{secret_token}")
async def receive_webhook(secret_token: str, request: Request):
    """接收外部 Webhook 推送（公开接口，无需认证）"""
    try:
        raw_body = (await request.body()).decode("utf-8")
    except Exception:
        raw_body = "{}"

    if not raw_body:
        raw_body = "{}"

    try:
        result = await webhook_service.receive_webhook(secret_token, raw_body)
        return {"code": 0, "message": "received", "data": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ===== 管理员接口：Webhook 源管理 =====

@webhook.get("/sources", tags=["webhook-admin"])
async def list_sources(current_user: User = Depends(get_admin_user)):
    """获取所有 Webhook 源配置"""
    sources = await repo.list_sources()
    return {"code": 0, "data": [s.to_dict() for s in sources]}


@webhook.post("/sources", tags=["webhook-admin"])
async def create_source(
    body: WebhookSourceCreate,
    current_user: User = Depends(get_admin_user),
):
    """创建 Webhook 源"""
    data = body.model_dump()
    if not data.get("secret_token"):
        data["secret_token"] = uuid.uuid4().hex
    data["created_by"] = str(current_user.id)
    data.pop("secret_token", None)  # 用下面这行传
    source = await repo.create_source({
        "name": data["name"],
        "description": data.get("description"),
        "secret_token": data["secret_token"],
        "agent_id": data["agent_id"],
        "prompt_template": data["prompt_template"],
        "extra_prompt": data.get("extra_prompt"),
        "is_active": data.get("is_active", True),
        "send_to_all": data.get("send_to_all", True),
        "created_by": data.get("created_by"),
    })
    return {"code": 0, "message": "创建成功", "data": source.to_dict()}


@webhook.get("/sources/{source_id}", tags=["webhook-admin"])
async def get_source(source_id: int, current_user: User = Depends(get_admin_user)):
    """获取 Webhook 源详情"""
    source = await repo.get_source_by_id(source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Webhook 源不存在")
    return {"code": 0, "data": source.to_dict()}


@webhook.put("/sources/{source_id}", tags=["webhook-admin"])
async def update_source(
    source_id: int,
    body: WebhookSourceUpdate,
    current_user: User = Depends(get_admin_user),
):
    """更新 Webhook 源"""
    data = {k: v for k, v in body.model_dump().items() if v is not None}
    if not data:
        raise HTTPException(status_code=400, detail="没有需要更新的字段")
    data["updated_by"] = str(current_user.id)
    source = await repo.update_source(source_id, data)
    if not source:
        raise HTTPException(status_code=404, detail="Webhook 源不存在")
    return {"code": 0, "message": "更新成功", "data": source.to_dict()}


@webhook.delete("/sources/{source_id}", tags=["webhook-admin"])
async def delete_source(source_id: int, current_user: User = Depends(get_admin_user)):
    """删除 Webhook 源"""
    ok = await repo.delete_source(source_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Webhook 源不存在")
    return {"code": 0, "message": "删除成功"}


@webhook.post("/sources/{source_id}/test", tags=["webhook-admin"])
async def test_source(
    source_id: int,
    body: WebhookTestPayload,
    current_user: User = Depends(get_admin_user),
):
    """测试 Webhook 源：模拟接收推送"""
    source = await repo.get_source_by_id(source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Webhook 源不存在")

    # 使用当前管理员作为测试目标用户
    try:
        mock_body = body.mock_body
        if isinstance(mock_body, str):
            webhook_data = json.loads(mock_body)
        else:
            webhook_data = mock_body
    except json.JSONDecodeError:
        webhook_data = {"raw": body.mock_body}

    msg = source.prompt_template or ""
    webhook_msg = webhook_data.get("message", webhook_data.get("title", ""))
    if webhook_msg and webhook_msg != msg:
        msg = f"{msg}\n\n{webhook_msg}" if msg else webhook_msg

    user_profile = (
        f"用户名称：{current_user.username or '未设置'}\n"
        f"手机号：{current_user.phone_number or '未设置'}"
    )
    preview = f"{msg}\n\n--- 用户信息 ---\n{user_profile}"

    return {
        "code": 0,
        "data": {
            "preview": preview,
            "webhook_data": webhook_data,
            "user_info": {"name": current_user.username, "phone": current_user.phone_number},
            "agent_id": source.agent_id,
            "extra_prompt": source.extra_prompt or "",
            "agent_base_prompt": "推送消息助手基础提示词：将推送消息以友好方式传达给用户",
        },
        "message": "测试成功",
    }


# ===== 管理员接口：Webhook 事件日志 =====

@webhook.get("/events", tags=["webhook-admin"])
async def list_events(
    source_id: int | None = None,
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(get_admin_user),
):
    """获取 Webhook 事件记录"""
    events = await repo.list_events(source_id=source_id, skip=skip, limit=limit)
    return {"code": 0, "data": [e.to_dict() for e in events]}


@webhook.get("/events/{event_id}", tags=["webhook-admin"])
async def get_event(event_id: int, current_user: User = Depends(get_admin_user)):
    """获取 Webhook 事件详情"""
    event = await repo.get_event_by_id(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="事件不存在")
    return {"code": 0, "data": event.to_dict()}
