"""邮件推送服务 - 发送验证码和系统通知"""

import asyncio
import os
import random
import smtplib
import string
from email.message import EmailMessage
from email.utils import formataddr

from src.utils.logging_config import logger


def _get_smtp_config() -> dict:
    """获取 SMTP 配置，优先从 Config 读取，其次从环境变量"""
    try:
        from src import config as app_config
        cfg = app_config
        return {
            "host": cfg.smtp_host or os.getenv("SMTP_HOST", "smtp.qq.com"),
            "port": cfg.smtp_port or int(os.getenv("SMTP_PORT", "465")),
            "user": cfg.smtp_user or os.getenv("SMTP_USER", ""),
            "password": cfg.smtp_password or os.getenv("SMTP_PASSWORD", ""),
            "from_name": cfg.smtp_from_name or os.getenv("SMTP_FROM_NAME", "千寻农业助手"),
            "from_email": cfg.smtp_from_email or os.getenv("SMTP_FROM_EMAIL", ""),
        }
    except Exception:
        return {
            "host": os.getenv("SMTP_HOST", "smtp.qq.com"),
            "port": int(os.getenv("SMTP_PORT", "465")),
            "user": os.getenv("SMTP_USER", ""),
            "password": os.getenv("SMTP_PASSWORD", ""),
            "from_name": os.getenv("SMTP_FROM_NAME", "千寻农业助手"),
            "from_email": os.getenv("SMTP_FROM_EMAIL", ""),
        }


def _send_sync(config: dict, to_email: str, subject: str, body: str):
    """同步发送单封邮件（在 executor 中运行）"""
    if not config["user"] or not config["password"]:
        logger.warning("SMTP 配置不完整，跳过邮件发送")
        return

    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = formataddr((config["from_name"], config["from_email"] or config["user"]))
    msg["To"] = to_email

    with smtplib.SMTP_SSL(config["host"], config["port"]) as smtp:
        smtp.login(config["user"], config["password"])
        smtp.send_message(msg)

    logger.info("邮件已发送到 {}", to_email)


async def send_email(to_email: str, subject: str, body: str):
    """异步发送单封邮件到指定地址"""
    config = _get_smtp_config()
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, _send_sync, config, to_email, subject, body)


def generate_verification_code(length: int = 6) -> str:
    """生成纯数字验证码"""
    return "".join(random.choices(string.digits, k=length))


async def send_verification_code_email(to_email: str, code: str):
    """发送邮箱验证码"""
    subject = "千寻农业助手 - 邮箱验证"
    body = f"""您好！

您的邮箱验证码为：{code}

验证码有效期为 10 分钟，请勿泄露给他人。

如果这不是您的操作，请忽略此邮件。

千寻农业助手"""
    await send_email(to_email, subject, body)
