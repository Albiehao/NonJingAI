from collections.abc import Callable

from langchain.agents.middleware import AgentMiddleware, ModelRequest, ModelResponse
from langchain_core.messages import HumanMessage


class ImageFilterMiddleware(AgentMiddleware):
    """图片过滤中间件

    功能：
    - 检测 HumanMessage 中的图片内容
    - 拦截url,并且把 url 组装入提示词（为后期可能使用多模态模型预留）
    """

    IMAGE_BLOCKED_HINT = "[用户传入了一张图片，需要调用图像识别工具，图片url为：]"

    def __init__(self, enabled: bool = True, hint_text: str | None = None):
        super().__init__()
        self.enabled = enabled
        self.hint_text = hint_text or self.IMAGE_BLOCKED_HINT

    async def awrap_model_call(
        self, request: ModelRequest, handler: Callable[[ModelRequest], ModelResponse]
    ) -> ModelResponse:
        """包装模型调用，过滤图片"""
        if not self.enabled:
            return await handler(request)

        # 过滤消息中的图片
        new_messages = []
        for msg in request.messages:
            if isinstance(msg, HumanMessage):
                new_msg = self._filter_image_content(msg)
                new_messages.append(new_msg)
            else:
                new_messages.append(msg)

        # 创建新的 request
        request = request.override(messages=new_messages)
        return await handler(request)

    def _filter_image_content(self, msg: HumanMessage) -> HumanMessage:
        """过滤单条 HumanMessage 中的图片内容

        Args:
            msg: 原始 HumanMessage

        Returns:
            过滤后的 HumanMessage（如果有图片）或原始消息
        """
        content = msg.content
        img_url = None

        # 纯文本，直接返回
        if isinstance(content, str):
            return msg

        # 列表格式，检测图片
        if isinstance(content, list):
            has_image = False
            new_content = []

            for item in content:
                if isinstance(item, dict):
                    if item.get("type") == "image_url":
                        has_image = True
                        img_url = item.get("image_url", {}).get("url")
                        continue
                    new_content.append(item)
                else:
                    new_content.append(item)

            if has_image:
                text_parts = [
                    item.get("text", "")
                    for item in new_content
                    if isinstance(item, dict) and item.get("type") == "text"
                ]

                final_text = " ".join(text_parts)
                hint = f"{self.hint_text}{img_url}" if img_url else self.hint_text
                if final_text:
                    final_text = f"{final_text}\n{hint}"
                else:
                    final_text = hint

                return HumanMessage(
                    content=final_text,
                    additional_kwargs=msg.additional_kwargs,
                )

        return msg


def create_image_filter_middleware(enabled: bool = True, hint_text: str | None = None) -> ImageFilterMiddleware:
    """创建 ImageFilterMiddleware 实例"""
    return ImageFilterMiddleware(enabled=enabled, hint_text=hint_text)
