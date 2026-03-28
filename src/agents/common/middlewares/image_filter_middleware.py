from typing import Any, override

from langchain.agents import AgentState
from langchain.agents.middleware import AgentMiddleware
from langgraph.runtime import Runtime
from langgraph.typing import ContextT


class ImageFilterMiddleware(AgentMiddleware):
    """图片过滤中间件

    功能：
    - 检测 HumanMessage 中的图片内容
    - 拦截url,并且把 url 组装入提示词（为后期可能使用多模态模型预留）
    """
    IMAGE_BLOCKED_HINT ="[图片内容已屏蔽：当前模型不支持多模态输入]"


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