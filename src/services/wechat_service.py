"""微信公众号集成服务 - 消息处理、绑定、客服消息推送"""

import asyncio
import base64
import hashlib
import os
import struct
import time
import uuid
import xml.etree.ElementTree as ET
from datetime import timedelta

import httpx
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from langchain.messages import HumanMessage
from sqlalchemy import text

from src.agents import agent_manager
from src.repositories.conversation_repository import ConversationRepository
from src.storage.postgres.manager import pg_manager
from src.utils.datetime_utils import utc_now_naive
from src.utils.logging_config import logger


# =============================================================================
# XML 工具函数
# =============================================================================


def _parse_wechat_xml(xml_body: str) -> dict:
    """解析微信 XML 消息为扁平字典"""
    try:
        root = ET.fromstring(xml_body)
        return {child.tag: child.text or "" for child in root}
    except ET.ParseError as e:
        logger.error("解析微信 XML 失败: {}", e)
        return {}


def _build_text_reply(to_user: str, from_user: str, content: str) -> str:
    """构建微信文本回复 XML"""
    timestamp = int(time.time())
    return f"""<xml>
<ToUserName><![CDATA[{to_user}]]></ToUserName>
<FromUserName><![CDATA[{from_user}]]></FromUserName>
<CreateTime>{timestamp}</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[{content}]]></Content>
</xml>"""


def _build_success_reply() -> str:
    """构建空回复（微信不显示任何消息）"""
    return "success"


def check_signature(signature: str, timestamp: str, nonce: str, token: str) -> bool:
    """微信服务器验证签名"""
    tmp_list = sorted([token, timestamp, nonce])
    tmp_str = "".join(tmp_list)
    digest = hashlib.sha1(tmp_str.encode("utf-8")).hexdigest()
    return digest == signature


# =============================================================================
# AES 加解密（安全模式）
# =============================================================================


def _get_aes_key() -> bytes:
    """从 EncodingAESKey 推导 AES 密钥（Base64 解码后 32 字节）"""
    encoding_aes_key = os.getenv("WECHAT_ENCODING_AES_KEY", "")
    if not encoding_aes_key:
        raise ValueError("缺少 WECHAT_ENCODING_AES_KEY")
    return base64.b64decode(encoding_aes_key + "=")


def _decrypt_aes(ciphertext: str, encoding_aes_key: str | None = None) -> str:
    """AES-256-CBC 解密微信消息，返回原始 XML"""
    aes_key = _get_aes_key()
    iv = aes_key[:16]

    raw = base64.b64decode(ciphertext)
    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    decrypted = decryptor.update(raw) + decryptor.finalize()

    # 去除 PKCS7 填充
    pad_len = decrypted[-1]
    if pad_len < 1 or pad_len > 32:
        raise ValueError("无效的 PKCS7 填充")
    decrypted = decrypted[:-pad_len]

    # 解析：random(16) + msg_len(4字节大端) + msg_xml + app_id
    msg_len = struct.unpack(">I", decrypted[16:20])[0]
    msg_xml = decrypted[20 : 20 + msg_len].decode("utf-8")
    return msg_xml


def _encrypt_aes(reply_xml: str, app_id: str) -> str:
    """AES-256-CBC 加密回复消息"""
    aes_key = _get_aes_key()
    iv = aes_key[:16]

    random_bytes = os.urandom(16)
    msg_bytes = reply_xml.encode("utf-8")
    msg_len = struct.pack(">I", len(msg_bytes))
    full_plaintext = random_bytes + msg_len + msg_bytes + app_id.encode("utf-8")

    # PKCS7 填充
    block_size = 32
    pad_len = block_size - (len(full_plaintext) % block_size)
    full_plaintext += bytes([pad_len] * pad_len)

    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    return base64.b64encode(encryptor.update(full_plaintext) + encryptor.finalize()).decode("utf-8")


def _build_encrypted_reply(reply_xml: str, from_user: str, to_user: str, timestamp: str, nonce: str) -> str:
    """构建安全模式下的加密回复 XML"""
    app_id = os.getenv("WECHAT_APP_ID", "")
    encrypt = _encrypt_aes(reply_xml, app_id)
    token = os.getenv("WECHAT_TOKEN", "")

    # msg_signature = SHA1(token, timestamp, nonce, Encrypt)
    msg_signature = hashlib.sha1(
        "".join(sorted([token, timestamp, nonce, encrypt])).encode("utf-8")
    ).hexdigest()

    return f"""<xml>
<Encrypt><![CDATA[{encrypt}]]></Encrypt>
<MsgSignature><![CDATA[{msg_signature}]]></MsgSignature>
<TimeStamp>{timestamp}</TimeStamp>
<Nonce><![CDATA[{nonce}]]></Nonce>
</xml>"""


def check_msg_signature(signature: str, timestamp: str, nonce: str, encrypt: str, token: str) -> bool:
    """验证安全模式的消息签名"""
    tmp_list = sorted([token, timestamp, nonce, encrypt])
    tmp_str = "".join(tmp_list)
    digest = hashlib.sha1(tmp_str.encode("utf-8")).hexdigest()
    return digest == signature


# =============================================================================
# WeChatService
# =============================================================================


class WechatService:
    """微信公众号集成核心服务"""

    def __init__(self):
        self._access_token: str | None = None
        self._token_expires_at: float = 0
        self._token_lock = asyncio.Lock()
        # 订阅号无法主动推送，AI 回复暂存等用户下次主动取
        self._pending_responses: dict[str, str] = {}

    # ---- 配置 ----

    def _get_config(self, key: str) -> str:
        return os.getenv(key, "")

    @property
    def _proxy_url(self) -> str | None:
        url = os.getenv("WECHAT_PROXY_URL", "")
        return url if url else None

    @property
    def app_id(self) -> str:
        return self._get_config("WECHAT_APP_ID")

    @property
    def app_secret(self) -> str:
        return self._get_config("WECHAT_APP_SECRET")

    @property
    def token(self) -> str:
        return self._get_config("WECHAT_TOKEN")

    def is_configured(self) -> bool:
        """检查微信配置是否完整"""
        return bool(self.app_id and self.app_secret and self.token)

    # ---- Access Token 管理 ----

    async def _get_access_token(self) -> str:
        """获取有效的微信 access_token（带缓存和锁）"""
        if self._access_token and time.time() < self._token_expires_at - 60:
            return self._access_token

        async with self._token_lock:
            if self._access_token and time.time() < self._token_expires_at - 60:
                return self._access_token

            if not self.app_id or not self.app_secret:
                raise ValueError("微信配置不完整：缺少 APP_ID 或 APP_SECRET")

            async with httpx.AsyncClient(proxy=self._proxy_url) as client:
                resp = await client.get(
                    "https://api.weixin.qq.com/cgi-bin/token",
                    params={
                        "grant_type": "client_credential",
                        "appid": self.app_id,
                        "secret": self.app_secret,
                    },
                )
                data = resp.json()
                if "access_token" in data:
                    self._access_token = data["access_token"]
                    self._token_expires_at = time.time() + data.get("expires_in", 7200)
                    logger.info("微信 access_token 已刷新")
                    return self._access_token
                logger.error("获取微信 access_token 失败: {}", data)
                raise ValueError(f"获取 access_token 失败: {data}")

    # ---- 客服消息推送 ----

    async def push_custom_message(self, open_id: str, content: str) -> dict:
        """通过微信客服消息接口推送文本消息"""
        access_token = await self._get_access_token()
        async with httpx.AsyncClient(proxy=self._proxy_url) as client:
            resp = await client.post(
                "https://api.weixin.qq.com/cgi-bin/message/custom/send",
                params={"access_token": access_token},
                json={
                    "touser": open_id,
                    "msgtype": "text",
                    "text": {"content": content},
                },
            )
            result = resp.json()
            if result.get("errcode") != 0:
                logger.warning("推送微信客服消息失败: {} (open_id={})", result, open_id[:8] + "****")
            return result

    # ---- 绑定逻辑 ----

    async def generate_binding_token(self, user_id: int) -> str:
        """生成绑定令牌（16位hex，30分钟有效）"""
        token = uuid.uuid4().hex[:16]
        async with pg_manager.get_async_session_context() as db:
            # 使用原始 SQL 操作更直接，避免新表不在 model 映射中的问题
            # 先过期的所有待绑定令牌
            await db.execute(
                text(
                    "UPDATE wechat_bindings SET token_expires_at = NOW() "
                    "WHERE user_id = :uid AND is_bound = FALSE"
                ),
                {"uid": user_id},
            )
            # 插入新记录
            await db.execute(
                text(
                    "INSERT INTO wechat_bindings (user_id, binding_token, token_expires_at, is_bound)"
                    " VALUES (:uid, :token, :expires, FALSE)"
                ),
                {
                    "uid": user_id,
                    "token": token,
                    "expires": utc_now_naive() + timedelta(days=36500),  # 永久有效
                },
            )
            await db.commit()
        return token

    async def verify_binding_token(self, token: str, open_id: str) -> tuple[bool, str]:
        """验证并完成绑定"""
        async with pg_manager.get_async_session_context() as db:
            result = await db.execute(
                text(
                    "SELECT id, token_expires_at FROM wechat_bindings "
                    "WHERE binding_token = :token AND is_bound = FALSE"
                ),
                {"token": token},
            )
            row = result.fetchone()
            if not row:
                return False, "绑定令牌无效，请检查后重试"

            now = utc_now_naive()
            if row.token_expires_at < now:
                return False, "绑定令牌已过期，请在个人中心重新生成"

            # 检查 open_id 是否已被其他用户绑定
            existing = await db.execute(
                text("SELECT id FROM wechat_bindings WHERE open_id = :oid AND is_bound = TRUE"),
                {"oid": open_id},
            )
            if existing.fetchone():
                return False, "该微信账号已被其他用户绑定"

            # 完成绑定
            await db.execute(
                text(
                    "UPDATE wechat_bindings SET open_id = :oid, is_bound = TRUE,"
                    " bound_at = NOW(), updated_at = NOW() WHERE id = :id"
                ),
                {"oid": open_id, "id": row.id},
            )
            await db.commit()
            return True, "绑定成功！您现在可以直接发送消息与我对话了。"

    async def get_user_by_open_id(self, open_id: str) -> dict | None:
        """通过 OpenID 获取绑定的用户信息"""
        async with pg_manager.get_async_session_context() as db:
            result = await db.execute(
                text(
                    "SELECT wb.user_id, u.username FROM wechat_bindings wb"
                    " JOIN users u ON u.id = wb.user_id"
                    " WHERE wb.open_id = :oid AND wb.is_bound = TRUE"
                ),
                {"oid": open_id},
            )
            row = result.fetchone()
            if row:
                return {"user_id": row.user_id, "username": row.username}
            return None

    async def get_binding_by_user_id(self, user_id: int) -> dict | None:
        """查询用户的绑定状态"""
        async with pg_manager.get_async_session_context() as db:
            result = await db.execute(
                text(
                    "SELECT open_id, is_bound, bound_at FROM wechat_bindings"
                    " WHERE user_id = :uid ORDER BY id DESC LIMIT 1"
                ),
                {"uid": user_id},
            )
            row = result.fetchone()
            if row:
                return {"open_id": row.open_id, "is_bound": row.is_bound, "bound_at": row.bound_at}
            return None

    async def unbind(self, user_id: int) -> bool:
        """解绑微信账号"""
        async with pg_manager.get_async_session_context() as db:
            result = await db.execute(
                text(
                    "UPDATE wechat_bindings SET open_id = NULL, is_bound = FALSE,"
                    " updated_at = NOW() WHERE user_id = :uid AND is_bound = TRUE"
                ),
                {"uid": user_id},
            )
            await db.commit()
            return result.rowcount > 0

    async def get_bound_open_id(self, user_id: int) -> str | None:
        """获取用户绑定的微信 OpenID"""
        async with pg_manager.get_async_session_context() as db:
            result = await db.execute(
                text(
                    "SELECT open_id FROM wechat_bindings"
                    " WHERE user_id = :uid AND is_bound = TRUE LIMIT 1"
                ),
                {"uid": user_id},
            )
            row = result.fetchone()
            return row.open_id if row else None

    # ---- 线程管理 ----

    async def _save_wechat_conversation(self, db, open_id: str, user_id: int | None, thread_id: str):
        """保存微信对话记录"""
        await db.execute(
            text(
                "INSERT INTO wechat_conversations (open_id, user_id, thread_id, last_message_at)"
                " VALUES (:oid, :uid, :tid, NOW())"
            ),
            {"oid": open_id, "uid": user_id, "tid": thread_id},
        )
        await db.commit()

    async def get_or_create_thread(self, open_id: str, user_id: int | None) -> str:
        """获取或创建对话线程。1小时无活动则自动创建新线程。"""
        async with pg_manager.get_async_session_context() as db:
            result = await db.execute(
                text(
                    "SELECT wc.thread_id, wc.last_message_at FROM wechat_conversations wc"
                    " WHERE wc.open_id = :oid ORDER BY wc.last_message_at DESC LIMIT 1"
                ),
                {"oid": open_id},
            )
            row = result.fetchone()

            now = utc_now_naive()
            if row:
                last_time = row.last_message_at
                if (now - last_time).total_seconds() < 3600:
                    # 1小时内，复用现有线程
                    await db.execute(
                        text(
                            "UPDATE wechat_conversations SET last_message_at = :now WHERE open_id = :oid"
                        ),
                        {"now": now, "oid": open_id},
                    )
                    await db.commit()
                    return row.thread_id

            # 创建新线程
            thread_id = str(uuid.uuid4())
            user_id_str = str(user_id) if user_id else f"wechat_{open_id}"
            conv_repo = ConversationRepository(db)
            await conv_repo.create_conversation(
                user_id=user_id_str,
                agent_id="ChatbotAgent",
                thread_id=thread_id,
                title=f"微信对话 - {open_id[:8]}",
            )

            await self._save_wechat_conversation(db, open_id, user_id, thread_id)
            return thread_id

    async def create_new_thread(self, open_id: str, user_id: int | None) -> str:
        """强制创建新线程（"新对话"命令）"""
        thread_id = str(uuid.uuid4())
        async with pg_manager.get_async_session_context() as db:
            user_id_str = str(user_id) if user_id else f"wechat_{open_id}"
            conv_repo = ConversationRepository(db)
            await conv_repo.create_conversation(
                user_id=user_id_str,
                agent_id="ChatbotAgent",
                thread_id=thread_id,
                title=f"微信对话 - {open_id[:8]}",
            )
            await self._save_wechat_conversation(db, open_id, user_id, thread_id)
        return thread_id

    # ---- 消息处理 ----

    def _is_binding_token(self, content: str) -> bool:
        """判断内容是否为16位hex绑定令牌"""
        if len(content) != 16:
            return False
        try:
            int(content, 16)
            return True
        except ValueError:
            return False

    async def process_message(self, xml_body: str) -> str:
        """处理微信发来的消息，返回 XML 回复"""
        msg = _parse_wechat_xml(xml_body)
        from_user = msg.get("FromUserName", "")
        to_user = msg.get("ToUserName", "")
        msg_type = msg.get("MsgType", "")
        content = msg.get("Content", "").strip()

        logger.info("收到微信消息: type={}, content={}", msg_type, content[:100])

        # ---- 事件消息 ----
        if msg_type == "event":
            event = msg.get("Event", "")
            if event == "subscribe":
                reply = (
                    "感谢您的关注！\n\n"
                    "使用步骤：\n"
                    "1. 登录系统，进入个人中心\n"
                    "2. 点击「生成绑定令牌」\n"
                    "3. 将生成的令牌发送到此公众号\n"
                    "4. 绑定成功后即可开始对话"
                )
                return _build_text_reply(from_user, to_user, reply)
            if event == "unsubscribe":
                logger.info("用户取消关注: {}", from_user)
                return _build_success_reply()
            return _build_success_reply()

        # ---- 非文本消息 ----
        if msg_type != "text":
            return _build_text_reply(from_user, to_user, "暂不支持此类型的消息，请发送文字消息。")

        # ---- 绑定令牌处理 ----
        if self._is_binding_token(content):
            success, message = await self.verify_binding_token(content, from_user)
            return _build_text_reply(from_user, to_user, message)

        # ---- 新对话命令 ----
        if content == "新对话":
            user_info = await self.get_user_by_open_id(from_user)
            user_id = user_info["user_id"] if user_info else None
            await self.create_new_thread(from_user, user_id)
            self._pending_responses.pop(from_user, None)
            return _build_text_reply(from_user, to_user, "已创建新对话，请发送您的问题。")

        # ---- 领取待处理回复 ----
        pending = self._pending_responses.pop(from_user, None)
        if pending:
            return _build_text_reply(from_user, to_user, pending)

        # ---- 检查绑定状态 ----


        user_info = await self.get_user_by_open_id(from_user)
        if not user_info:
            reply = (
                "您还没有绑定账号。\n\n"
                "请按以下步骤操作：\n"
                "1. 登录系统，进入个人中心\n"
                "2. 点击「生成绑定令牌」\n"
                "3. 将生成的16位令牌发送到此公众号"
            )
            return _build_text_reply(from_user, to_user, reply)

        # ---- 正常消息：保存 + 异步AI回复 ----
        thread_id = await self.get_or_create_thread(from_user, user_info["user_id"])

        async with pg_manager.get_async_session_context() as db:
            conv_repo = ConversationRepository(db)
            await conv_repo.add_message_by_thread_id(
                thread_id=thread_id,
                role="user",
                content=content,
                message_type="text",
                extra_metadata={"source": "wechat", "open_id": from_user},
            )

        # 异步生成 AI 回复
        asyncio.create_task(
            self._generate_and_push_response(
                from_user=from_user,
                thread_id=thread_id,
                user_info=user_info,
                query=content,
            )
        )

        return _build_text_reply(from_user, to_user, "AI正在思考，请稍后发送任意消息查看回复。")

    async def _generate_and_push_response(
        self,
        from_user: str,
        thread_id: str,
        user_info: dict,
        query: str,
    ):
        """异步生成 AI 回复，存入待处理队列等用户主动取（订阅号无法主动推送）"""
        try:
            agent = agent_manager.get_agent("ChatbotAgent")
            if not agent:
                logger.error("ChatbotAgent 不存在，无法处理微信消息")
                return

            user_id_str = str(user_info["user_id"])
            # 加载默认 agent 配置（含工具列表）
            agent_config_dict: dict = {}
            try:
                from src.repositories.agent_config_repository import AgentConfigRepository

                async with pg_manager.get_async_session_context() as db:
                    config_repo = AgentConfigRepository(db)
                    config_item = await config_repo.get_or_create_default(
                        agent_id="ChatbotAgent", created_by=user_id_str
                    )
                    agent_config_dict = (config_item.config_json or {}).get("context", config_item.config_json or {})
            except Exception:
                logger.warning("加载 ChatbotAgent 配置失败，使用空配置")

            input_context = {
                "user_id": user_id_str,
                "thread_id": thread_id,
                "agent_config_id": None,
                "agent_config": agent_config_dict,
            }

            result = await agent.invoke_messages(
                [HumanMessage(content=query)], input_context=input_context
            )

            response_content = ""
            if isinstance(result, dict):
                for msg in reversed(result.get("messages", [])):
                    if hasattr(msg, "type") and msg.type == "ai":
                        response_content = msg.content if hasattr(msg, "content") else str(msg)
                        break

            if not response_content:
                response_content = "抱歉，我暂时无法回答这个问题。"

            # 保存 assistant 消息
            async with pg_manager.get_async_session_context() as db:
                conv_repo = ConversationRepository(db)
                await conv_repo.add_message_by_thread_id(
                    thread_id=thread_id,
                    role="assistant",
                    content=response_content,
                    message_type="text",
                    extra_metadata={"source": "wechat"},
                )

            # 存入待处理队列，等用户下次发消息时推送
            self._pending_responses[from_user] = response_content
            logger.info("微信 AI 回复已就绪，等待用户取走 (open_id={})", from_user[:8] + "****")

        except Exception as e:
            logger.exception("微信异步 AI 回复生成失败: {}", e)
            self._pending_responses[from_user] = "抱歉，处理您的消息时出现错误，请稍后再试。"

    # ---- 系统推送 ----

    async def push_to_user(self, user_id: int, content: str) -> bool:
        """向用户推送消息（微信客服消息 + 邮件通知）"""
        pushed = False

        if self.is_configured():
            open_id = await self.get_bound_open_id(user_id)
            if open_id:
                await self.push_custom_message(open_id, content)
                pushed = True

        # 同步推送邮件
        try:
            async with pg_manager.get_async_session_context() as db:
                result = await db.execute(
                    text("SELECT email, email_verified FROM users WHERE id = :uid"),
                    {"uid": user_id},
                )
                row = result.fetchone()
                if row and row.email and row.email_verified:
                    from src.services.email_service import send_email
                    await send_email(
                        to_email=row.email,
                        subject="千寻农业通知",
                        body=content,
                    )
                    pushed = True
        except Exception as e:
            logger.warning("推送邮件通知失败: {}", e)

        return pushed


# 全局实例
wechat_service = WechatService()

__all__ = ["wechat_service", "WechatService", "check_signature", "_build_text_reply"]
