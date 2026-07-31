"""Webhook 推送消息智能体 - 处理系统推送通知并以友好方式传达给用户"""

from src.agents.common import BaseAgent, load_chat_model

WEBHOOK_BASE_PROMPT = """你是一个农业推送消息助手。你的任务是将系统推送的农业相关消息以清晰、友好的方式传达给用户。

## 核心职责
1. 把收到的推送消息用自然友好的语气转达给用户
2. 根据推送内容类型（通知、提醒、预警、营销等），使用恰当的语气
3. 保持回复简洁明了，突出关键信息
4. 不要询问用户是否需要帮助，直接传达消息即可
5. 严格遵守：只处理农业相关信息（农事提醒、气象预警、种植建议、政策通知等），非农业内容直接转发原文

## 回复格式要求
- 开头用一句话概括推送内容
- 中间呈现关键信息
- 结尾可以加一句友好的结束语
- 整体不超过 200 字"""


class WebhookAgent(BaseAgent):
    name = "推送消息助手"
    description = "将系统推送的消息以友好的方式传达给用户，支持个性化提醒。"
    capabilities: list[str] = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def get_graph(self, **kwargs):
        from deepagents.middleware.filesystem import FilesystemMiddleware
        from langchain.agents import create_agent
        from langchain.agents.middleware import ModelRetryMiddleware

        from src.agents.common.middlewares.runtime_config_middleware import RuntimeConfigMiddleware

        graph = create_agent(
            model=load_chat_model(self.context_schema().model),
            system_prompt=WEBHOOK_BASE_PROMPT,
            middleware=[
                RuntimeConfigMiddleware(
                    enable_tools_override=False,
                ),
                ModelRetryMiddleware(),
            ],
            checkpointer=await self._get_checkpointer(),
        )

        return graph
