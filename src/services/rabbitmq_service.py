"""RabbitMQ 消息队列服务 - 接收外部系统通过 RabbitMQ 推送的 webhook 消息"""

import json

import aio_pika

from src.services.webhook_service import webhook_service
from src.utils.logging_config import logger


class RabbitMQService:
    """RabbitMQ 消费者服务"""

    def __init__(self):
        self._connection: aio_pika.RobustConnection | None = None
        self._channel: aio_pika.RobustChannel | None = None
        self._consumer_tag: str | None = None
        self._running = False

    @property
    def is_connected(self) -> bool:
        return self._connection is not None and not self._connection.is_closed

    async def connect(self, amqp_url: str = "amqp://guest:guest@localhost:5672/"):
        """连接到 RabbitMQ"""
        self._connection = await aio_pika.connect_robust(amqp_url)
        self._channel = await self._connection.channel()
        logger.info("RabbitMQ 连接成功: {}", amqp_url)

    async def start_consuming(
        self,
        queue_name: str = "webhook_push",
        prefetch_count: int = 10,
    ):
        """启动消费，监听 webhook 推送队列"""
        if not self._channel:
            raise RuntimeError("RabbitMQ 未连接，请先调用 connect()")

        queue = await self._channel.declare_queue(queue_name, durable=True)
        await self._channel.set_qos(prefetch_count=prefetch_count)

        self._consumer_tag = await queue.consume(self._on_message)
        self._running = True
        logger.info("开始监听 RabbitMQ 队列: {}", queue_name)

    async def stop_consuming(self):
        """停止消费"""
        if self._consumer_tag and self._channel:
            await self._channel.cancel(self._consumer_tag)
        self._running = False
        logger.info("RabbitMQ 消费已停止")

    async def close(self):
        """关闭连接"""
        await self.stop_consuming()
        if self._connection and not self._connection.is_closed:
            await self._connection.close()
        self._connection = None
        self._channel = None
        logger.info("RabbitMQ 连接已关闭")

    async def _on_message(self, message: aio_pika.IncomingMessage):
        """处理接收到的 RabbitMQ 消息"""
        async with message.process(ignore_processed=True):
            try:
                body = message.body.decode("utf-8")
                data = json.loads(body)

                # 消息体中必须包含 secret_token
                secret_token = data.pop("secret_token", None)
                if not secret_token:
                    logger.error("RabbitMQ 消息缺少 secret_token，已丢弃: {}", message.message_id)
                    await message.reject(requeue=False)
                    return

                # 剩余内容作为 raw_body
                raw_body = json.dumps(data, ensure_ascii=False)

                # 复用电面有的 webhook 处理逻辑
                result = await webhook_service.receive_webhook(secret_token, raw_body)
                logger.info(
                    "RabbitMQ webhook 处理完成: event_id={}", result.get("event_id")
                )
                await message.ack()

            except json.JSONDecodeError:
                logger.error("RabbitMQ 消息 JSON 解析失败: {}", message.body[:500])
                await message.reject(requeue=False)
            except ValueError as e:
                logger.error("RabbitMQ webhook 处理失败: {}", e)
                await message.reject(requeue=False)
            except Exception as e:
                logger.exception("RabbitMQ 消息处理异常: {}", e)
                # 网络抖动等问题，重新入队
                await message.reject(requeue=True)


rabbitmq_service = RabbitMQService()

__all__ = ["rabbitmq_service", "RabbitMQService"]
