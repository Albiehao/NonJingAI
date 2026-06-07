"""Webhook 推送服务 - 接收外部 Webhook 并主动发起对话"""

import json

from langchain.messages import HumanMessage
from sqlalchemy import select

from src.agents import agent_manager
from src.repositories.conversation_repository import ConversationRepository
from src.repositories.user_repository import UserRepository
from src.repositories.webhook_repository import WebhookRepository
from src.services.task_service import TaskContext, tasker
from src.storage.postgres.manager import pg_manager
from src.storage.postgres.models_business import UserAddress
from src.storage.postgres.models_crop import Crop, UserCrop
from src.utils.logging_config import logger


class WebhookService:
    """Webhook 推送服务"""

    def __init__(self):
        self.repo = WebhookRepository()

    async def receive_webhook(self, secret_token: str, raw_body: str) -> dict:
        """接收外部 Webhook 推送，入队处理"""
        source = await self.repo.get_source_by_token(secret_token)
        if not source:
            raise ValueError("无效的 webhook 令牌")
        if not source.is_active:
            raise ValueError("该 webhook 源已停用")

        event = await self.repo.create_event({
            "source_id": source.id,
            "raw_body": raw_body,
            "status": "pending",
        })

        # 通过消息队列异步处理
        await tasker.enqueue(
            name=f"webhook-{source.name}",
            task_type="webhook_process",
            payload={"event_id": event.id, "source_id": source.id, "raw_body": raw_body},
            coroutine=self._process_webhook_task,
        )

        return {"event_id": event.id, "status": "pending"}

    async def _process_webhook_task(self, ctx: TaskContext) -> dict:
        """消息队列工作线程：处理 webhook 事件"""
        payload = ctx._tasker._tasks[ctx.task_id].payload
        event_id = payload["event_id"]
        source_id = payload["source_id"]
        raw_body = payload["raw_body"]

        try:
            source = await self.repo.get_source_by_id(source_id)
            if not source:
                raise ValueError(f"Webhook 源 {source_id} 不存在")

            await ctx.set_message("正在处理 webhook 事件...")

            await self.repo.update_event(event_id, {"status": "processing"})

            # 解析 webhook 数据
            try:
                webhook_data = json.loads(raw_body) if raw_body else {}
            except json.JSONDecodeError:
                webhook_data = {"raw": raw_body}

            await ctx.set_progress(10, "正在获取目标用户...")

            # 获取目标用户
            user_repo = UserRepository()
            filters = webhook_data.get("filters", {})
            target_ids = webhook_data.get("user_ids", [])

            if target_ids:
                # 按指定 user_id 列表
                users = []
                for uid in target_ids:
                    user = await user_repo.get_by_user_id(str(uid))
                    if user:
                        users.append(user)
            elif filters:
                # 按筛选条件：农作物、地理位置
                users = []
                crop_names = filters.get("crops", [])

                if crop_names:
                    crop_users = await user_repo.get_users_by_crop_names(crop_names)
                    users = self._merge_users(users, crop_users)

                geo = filters.get("geo") or filters.get("location")
                if geo and isinstance(geo, dict):
                    lat = geo.get("lat") or geo.get("latitude")
                    lng = geo.get("lng") or geo.get("longitude")
                    radius = filters.get("geo_radius_km", 10)
                    if lat is not None and lng is not None:
                        geo_users = await user_repo.get_user_in_geo(
                            {"latitude": float(lat), "longitude": float(lng)},
                            radius_km=float(radius),
                        )
                        users = self._merge_users(users, geo_users)
                elif filters.get("address_contains"):
                    addr_users = await user_repo.get_users_by_address_contains(
                        filters["address_contains"]
                    )
                    users = self._merge_users(users, addr_users)

                # 如果没有指定任何筛选条件，返回所有用户
                if not crop_names and not geo and not filters.get("address_contains"):
                    users = await user_repo.list_users(limit=9999)
            else:
                users = await user_repo.list_users(limit=9999)

            total = len(users)
            if total == 0:
                await ctx.set_message("没有目标用户")
                await self.repo.update_event(event_id, {"status": "completed"})
                return {"sent": 0, "total": 0}

            await ctx.set_message(f"开始向 {total} 个用户推送消息...")

            sent = 0
            fail = 0

            for idx, user in enumerate(users):
                if ctx.is_cancel_requested():
                    await self.repo.update_event(event_id, {
                        "status": "failed",
                        "error_message": "任务被取消",
                    })
                    return {"sent": sent, "total": total, "failed": fail}

                try:
                    await self._send_to_user(
                        user=user,
                        source=source,
                        webhook_data=webhook_data,
                    )
                    sent += 1
                except Exception as e:
                    logger.exception("发送 webhook 消息给用户 {} 失败: {}", user.user_id, e)
                    fail += 1

                progress = 10 + int((idx + 1) / total * 80)
                await ctx.set_progress(progress, f"已发送 {sent}/{total}，失败 {fail}")

            await self.repo.update_event(event_id, {
                "status": "completed",
                "error_message": None,
            })

            await ctx.set_progress(100, f"完成：成功 {sent}，失败 {fail}，共 {total}")
            return {"sent": sent, "total": total, "failed": fail}

        except Exception as e:
            logger.exception("Webhook 处理失败: {}", e)
            await self.repo.update_event(event_id, {
                "status": "failed",
                "error_message": str(e),
            })
            raise

    def _merge_users(self, existing: list, new_users: list) -> list:
        """合并用户列表，去重"""
        seen = {u.id for u in existing}
        for u in new_users:
            if u.id not in seen:
                existing.append(u)
                seen.add(u.id)
        return existing

    async def _send_to_user(self, user, source, webhook_data: dict):
        """向单个用户发送推送——WebhookAgent 生成内容后直接注入到最近对话"""
        agent = agent_manager.get_agent("WebhookAgent")
        if not agent:
            raise ValueError("智能体 WebhookAgent 不存在")

        # 推送原始消息
        raw_message = webhook_data.get("message", webhook_data.get("title", ""))

        # 构建用户信息供 WebhookAgent 个性化
        user_profile_parts = [f"用户名称：{user.username or '未设置'}"]
        if user.phone_number:
            user_profile_parts.append(f"手机号：{user.phone_number}")

        async with pg_manager.get_async_session_context() as db:
            try:
                addr_result = await db.execute(
                    select(UserAddress).where(UserAddress.user_id == user.id)
                )
                ua = addr_result.scalar_one_or_none()
                if ua and ua.address:
                    user_profile_parts.append(f"地址：{ua.address}")

                crop_result = await db.execute(
                    select(UserCrop).where(
                        UserCrop.user_id == user.id, UserCrop.deleted_at.is_(None)
                    )
                )
                user_crops = crop_result.scalars().all()
                if user_crops:
                    crop_ids = [uc.crop_id for uc in user_crops]
                    crop_names_res = await db.execute(
                        select(Crop).where(Crop.id.in_(crop_ids))
                    )
                    crop_map = {c.id: c.name for c in crop_names_res.scalars().all()}
                    crop_list = "、".join(
                        f"{crop_map.get(uc.crop_id, '未知')}" for uc in user_crops
                    )
                    user_profile_parts.append(f"种植农作物：{crop_list}")
            except Exception:
                pass

            conv_repo = ConversationRepository(db)
            user_id_str = str(user.id)

            # 查找用户最近的 ChatbotAgent 对话，没有则跳过
            conversations = await conv_repo.list_conversations(
                user_id=user_id_str, agent_id="ChatbotAgent", status="active"
            )
            if not conversations:
                logger.info("用户 {} 没有 ChatbotAgent 对话，跳过推送", user.user_id)
                return

            conversation = conversations[0]
            thread_id = conversation.thread_id

            # 调用 WebhookAgent 生成推送内容（完全独立，不依赖 ChatbotAgent 上下文）
            try:
                user_profile_str = "；".join(user_profile_parts)
                agent_input = f"{raw_message}\n\n用户信息：{user_profile_str}" if raw_message else user_profile_str

                agent_config = {}
                if source.extra_prompt:
                    agent_config["system_prompt"] = source.extra_prompt

                input_context = {
                    "user_id": user_id_str,
                    "thread_id": thread_id,
                    "agent_config_id": None,
                    "agent_config": agent_config,
                }
                result = await agent.invoke_messages(
                    [HumanMessage(content=agent_input)], input_context=input_context
                )

                response_content = raw_message or agent_input
                if isinstance(result, dict):
                    for msg in reversed(result.get("messages", [])):
                        if hasattr(msg, "type") and msg.type == "ai":
                            response_content = msg.content if hasattr(msg, "content") else str(msg)
                            break

                # 直接注入 assistant 消息到 ChatbotAgent 对话
                await conv_repo.add_message_by_thread_id(
                    thread_id=thread_id,
                    role="assistant",
                    content=response_content,
                    message_type="text",
                    extra_metadata={"source": "webhook", "source_name": source.name},
                )

                # 同步推送到微信（如果用户已绑定）
                try:
                    from src.services.wechat_service import wechat_service

                    await wechat_service.push_to_user(user.id, response_content)
                except Exception as we:
                    logger.warning("推送微信消息失败: {}", we)

                # 邮件推送（取用户绑定的邮箱）
                if getattr(user, "email", None) and getattr(user, "email_verified", False):
                    try:
                        from src.services.email_service import send_email

                        await send_email(
                            to_email=user.email,
                            subject=f"千寻农业通知 - {source.name}",
                            body=response_content,
                        )
                    except Exception as e:
                        logger.warning("发送邮件通知失败: {}", e)
            except Exception as e:
                logger.exception("WebhookAgent 调用失败: {}", e)


webhook_service = WebhookService()

__all__ = ["webhook_service", "WebhookService"]
