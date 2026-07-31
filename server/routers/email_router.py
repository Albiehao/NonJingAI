"""邮箱绑定路由"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy import text

from server.utils.auth_middleware import get_required_user
from src.services.email_service import generate_verification_code, send_verification_code_email
from src.storage.postgres.manager import pg_manager
from src.storage.postgres.models_business import User
from src.utils.datetime_utils import utc_now_naive
from src.utils.logging_config import logger
from datetime import timedelta

email_router = APIRouter(prefix="/email", tags=["email"])


class SendCodeRequest(BaseModel):
    email: EmailStr


class VerifyRequest(BaseModel):
    email: EmailStr
    code: str


@email_router.post("/binding/send-code")
async def send_verification_code(
    req: SendCodeRequest,
    current_user: User = Depends(get_required_user),
):
    """发送邮箱验证码"""
    email = req.email.lower().strip()

    # 检查邮箱是否已被其他用户绑定
    async with pg_manager.get_async_session_context() as db:
        result = await db.execute(
            text("SELECT id FROM users WHERE email = :email AND id != :uid AND email_verified = TRUE"),
            {"email": email, "uid": current_user.id},
        )
        if result.fetchone():
            raise HTTPException(status_code=409, detail="该邮箱已被其他用户绑定")

        # 生成验证码
        code = generate_verification_code()
        expires_at = utc_now_naive() + timedelta(minutes=10)

        await db.execute(
            text(
                "UPDATE users SET email = :email, email_verification_code = :code,"
                " email_verification_expires_at = :expires WHERE id = :uid"
            ),
            {"email": email, "code": code, "expires": expires_at, "uid": current_user.id},
        )
        await db.commit()

    # 发送验证码邮件
    await send_verification_code_email(email, code)
    logger.info("验证码已发送到 {} (user_id={})", email, current_user.id)

    return {"code": 0, "message": "验证码已发送"}


@email_router.post("/binding/verify")
async def verify_and_bind(
    req: VerifyRequest,
    current_user: User = Depends(get_required_user),
):
    """验证验证码并绑定邮箱"""
    email = req.email.lower().strip()
    code = req.code.strip()

    async with pg_manager.get_async_session_context() as db:
        result = await db.execute(
            text(
                "SELECT email, email_verification_code, email_verification_expires_at, email_verified"
                " FROM users WHERE id = :uid"
            ),
            {"uid": current_user.id},
        )
        row = result.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="用户不存在")

        if row.email != email:
            raise HTTPException(status_code=400, detail="邮箱不匹配，请重新发送验证码")

        if row.email_verified:
            return {"code": 0, "message": "邮箱已验证"}

        if not row.email_verification_code:
            raise HTTPException(status_code=400, detail="请先发送验证码")

        if row.email_verification_expires_at and row.email_verification_expires_at < utc_now_naive():
            raise HTTPException(status_code=400, detail="验证码已过期，请重新发送")

        if row.email_verification_code != code:
            raise HTTPException(status_code=400, detail="验证码错误")

        # 验证通过，绑定邮箱
        await db.execute(
            text(
                "UPDATE users SET email_verified = TRUE, email_verification_code = NULL,"
                " email_verification_expires_at = NULL WHERE id = :uid"
            ),
            {"uid": current_user.id},
        )
        await db.commit()

    logger.info("邮箱绑定成功: {} (user_id={})", email, current_user.id)
    return {"code": 0, "message": "邮箱绑定成功"}


@email_router.get("/binding/status")
async def get_email_binding_status(
    current_user: User = Depends(get_required_user),
):
    """查询邮箱绑定状态"""
    async with pg_manager.get_async_session_context() as db:
        result = await db.execute(
            text("SELECT email, email_verified FROM users WHERE id = :uid"),
            {"uid": current_user.id},
        )
        row = result.fetchone()
        if row and row.email and row.email_verified:
            # 脱敏显示
            email_str = row.email
            masked = email_str[0] + "****" + email_str[email_str.index("@"):]
            return {
                "code": 0,
                "data": {
                    "is_bound": True,
                    "email": masked,
                    "full_email": email_str,
                },
            }
        return {
            "code": 0,
            "data": {
                "is_bound": False,
                "email": None,
            },
        }


@email_router.post("/binding/unbind")
async def unbind_email(
    current_user: User = Depends(get_required_user),
):
    """解绑邮箱"""
    async with pg_manager.get_async_session_context() as db:
        await db.execute(
            text(
                "UPDATE users SET email = NULL, email_verified = FALSE,"
                " email_verification_code = NULL, email_verification_expires_at = NULL"
                " WHERE id = :uid"
            ),
            {"uid": current_user.id},
        )
        await db.commit()

    return {"code": 0, "message": "邮箱已解绑"}


@email_router.post("/test")
async def test_email(
    current_user: User = Depends(get_required_user),
):
    """发送测试邮件到当前用户邮箱"""
    async with pg_manager.get_async_session_context() as db:
        result = await db.execute(
            text("SELECT email, email_verified FROM users WHERE id = :uid"),
            {"uid": current_user.id},
        )
        row = result.fetchone()
        if not row or not row.email or not row.email_verified:
            raise HTTPException(status_code=400, detail="当前用户未绑定邮箱")

    from src.services.email_service import send_email

    await send_email(
        to_email=row.email,
        subject="千寻农业助手 - 测试邮件",
        body="这是一封测试邮件，表明您的邮件服务配置正确。",
    )
    return {"code": 0, "message": "测试邮件已发送"}
