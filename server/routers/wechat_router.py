"""微信公众号集成路由"""

import os

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import PlainTextResponse, Response

from server.utils.auth_middleware import get_required_user
from src.services.wechat_service import (
    _decrypt_aes,
    _build_encrypted_reply,
    check_msg_signature,
    check_signature,
    wechat_service,
)
from src.storage.postgres.models_business import User
from src.utils.logging_config import logger

wechat_router = APIRouter(prefix="/wechat", tags=["wechat"])


# =============================================================================
# 公开接口（微信服务器调用）
# =============================================================================


@wechat_router.get("/receive")
async def verify_server(
    signature: str,
    timestamp: str,
    nonce: str,
    echostr: str,
):
    """微信服务器验证（GET）"""
    token = os.getenv("WECHAT_TOKEN", "")
    if check_signature(signature, timestamp, nonce, token):
        return PlainTextResponse(content=echostr)
    logger.warning("微信服务器验证失败: signature={}", signature)
    raise HTTPException(status_code=403, detail="验证失败")


@wechat_router.post("/receive")
async def receive_message(
    request: Request,
    signature: str | None = None,
    timestamp: str | None = None,
    nonce: str | None = None,
    openid: str | None = None,
    encrypt_type: str | None = None,
    msg_signature: str | None = None,
):
    """接收微信用户消息（POST XML），同时支持明文和安全模式"""
    if not wechat_service.is_configured():
        logger.error("微信配置不完整，无法处理消息")
        raise HTTPException(status_code=500, detail="微信服务未配置")

    xml_body = (await request.body()).decode("utf-8")
    logger.debug("收到微信 POST, encrypt_type={}, xml_len={}", encrypt_type, len(xml_body))

    # 安全模式：先解密 Encrypt 字段
    if encrypt_type == "aes":
        token = os.getenv("WECHAT_TOKEN", "")
        msg = {"Encrypt": ""}
        import xml.etree.ElementTree as ET
        root = ET.fromstring(xml_body)
        for child in root:
            msg[child.tag] = child.text or ""

        # 验证消息签名
        if msg_signature and not check_msg_signature(msg_signature, timestamp or "", nonce or "", msg["Encrypt"], token):
            logger.warning("消息签名验证失败")
            raise HTTPException(status_code=403, detail="签名验证失败")

        # AES 解密
        decrypted_xml = _decrypt_aes(msg["Encrypt"])
        logger.debug("解密后 XML: {}...", decrypted_xml[:200])
        reply_xml = await wechat_service.process_message(
            decrypted_xml, encrypt_type="aes", timestamp=timestamp, nonce=nonce
        )
        # 加密回复
        encrypted_reply = _build_encrypted_reply(reply_xml, "", "", timestamp or "", nonce or "")
        return Response(content=encrypted_reply, media_type="application/xml")
    else:
        # 明文模式
        reply_xml = await wechat_service.process_message(xml_body)
        return Response(content=reply_xml, media_type="application/xml")


# =============================================================================
# 用户绑定接口（需登录）
# =============================================================================


@wechat_router.get("/binding/token")
async def generate_binding_token(
    current_user: User = Depends(get_required_user),
):
    """生成微信绑定令牌"""
    if not wechat_service.is_configured():
        raise HTTPException(status_code=503, detail="微信服务未配置，请联系管理员")

    token = await wechat_service.generate_binding_token(current_user.id)
    return {
        "code": 0,
        "data": {
            "token": token,
            "expires_in_minutes": 21600,  # 15天
        },
    }


@wechat_router.post("/binding/unbind")
async def unbind_wechat(
    current_user: User = Depends(get_required_user),
):
    """解绑微信账号"""
    if not wechat_service.is_configured():
        raise HTTPException(status_code=503, detail="微信服务未配置，请联系管理员")

    success = await wechat_service.unbind(current_user.id)
    return {
        "code": 0,
        "data": {"unbound": success},
    }


@wechat_router.get("/binding/status")
async def get_binding_status(
    current_user: User = Depends(get_required_user),
):
    """查询微信绑定状态"""
    binding = await wechat_service.get_binding_by_user_id(current_user.id)
    if binding and binding["is_bound"]:
        return {
            "code": 0,
            "data": {
                "is_bound": True,
                "open_id": binding["open_id"],
                "bound_at": str(binding["bound_at"]) if binding.get("bound_at") else None,
            },
        }
    return {
        "code": 0,
        "data": {
            "is_bound": False,
            "open_id": None,
            "bound_at": None,
        },
    }
