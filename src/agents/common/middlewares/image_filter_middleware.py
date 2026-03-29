from typing import Any, override

from langchain.agents import AgentState
from langchain.agents.middleware import AgentMiddleware
from langchain_core.messages import HumanMessage
from langgraph.runtime import Runtime
from langgraph.typing import ContextT


class ImageFilterMiddleware(AgentMiddleware):
    """图片过滤中间件

    功能：
    - 检测 HumanMessage 中的图片内容
    - 拦截url,并且把 url 组装入提示词（为后期可能使用多模态模型预留）
    """
    IMAGE_BLOCKED_HINT ="[用户传入了一张图片，需要调用图像识别工具]"


    def __init__(self,enabled:bool = True,hint_text:str = None):
        """初始化中间件
          Args:
              enabled: 是否启用图片过滤，默认 True
              hint_text: 自定义提示文本，默认使用IMAGE_BLOCKED_HINT
        """
        self.enabled = enabled
        self.hint_text = hint_text or self.IMAGE_BLOCKED_HINT

    @override
    def before_model(self, state: AgentState[Any], runtime: Runtime[ContextT]) -> dict[str, Any] | None:
        """在模型调用前处理消息"""
        pass

    @override
    async def abefore_model(self, state: AgentState[Any],runtime: Runtime) -> dict[str, Any] | None:
        """在模型调用前处理消息异步版"""
        pass


    def _filter_image(self,msg:HumanMessage) -> HumanMessage:
        """过滤单条 HumanMessage 中的图片内容
            Args:
                msg: 原始 HumanMessage
            Returns:过滤后的
                HumanMessage（如果有图片）或原始消息
        """
        content = msg.content

        if isinstance(content,str):
            return msg

        if isinstance(content,list):
            has_image = False
            new_content = []

            for item in content:
                if isinstance(item,dict):
                    if item.get("type") == "image_url":
                        has_image = True
                        continue
                    new_content.append(item)
                else:
                    new_content.append(item)

            if has_image:
                text_parts = [
                    item.get("text","")
                    for item in new_content
                    if isinstance(item,dict) and item.get("type") == "text"
                ]

                final_text = " ".join(text_parts)
                if final_text:
                    final_text=f"{final_text}{self.hint_text}"
                else:
                    final_text=self.hint_text

                return HumanMessage(
                    content=final_text,
                    additional_kwargs=msg.additional_kwargs,
                )

        return HumanMessage()


