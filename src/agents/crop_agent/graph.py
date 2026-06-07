"""Crop Agent - 农作物病虫害防治诊疗智能体"""

from deepagents.backends import StateBackend
from deepagents.middleware.filesystem import FilesystemMiddleware
from deepagents.middleware.patch_tool_calls import PatchToolCallsMiddleware
from deepagents.middleware.subagents import SubAgentMiddleware
from langchain.agents import create_agent
from langchain.agents.middleware import (
    TodoListMiddleware,
)

from src.agents.common import BaseAgent, load_chat_model
from src.agents.common.middlewares import RuntimeConfigMiddleware, SummaryOffloadMiddleware, image_interceptor, save_attachments_to_fs
from src.agents.common.toolkits.web_search.tool import get_tavily_search
from src.utils import logger

from .context import CropContext


def _create_fs_backend(rt):
    """创建文件存储后端"""
    return StateBackend(rt)


def _get_research_sub_agent(search_tools: list) -> dict:
    """获取农业研究子智能体配置。"""
    return {
        "name": "research-agent",
        "description": "利用搜索工具，用于研究农作物病虫害问题，查找防治资料和用药信息。将调研结果写入到主题研究文件中。",
        "system_prompt": (
            "你是一位专注的农业研究员。你的工作是根据用户遇到的农作物病虫害问题进行研究。"
            "进行彻底的研究，然后用详细的答案回复用户的问题，只有你的最终答案会被传递给用户。"
            "除了你的最终信息，他们不会知道任何其他事情，所以你的最终报告应该就是你的最终信息！"
            "将调研结果保存到主题研究文件中 /sub_research/xxx.md 中。"
            "研究内容包括：病害/虫害的识别特征、发生规律、防治方法、推荐药剂及用法用量。"
        ),
        "tools": search_tools,
    }


critique_sub_agent = {
    "name": "critique-agent",
    "description": "用于评审最终报告。给这个代理一些关于你希望它如何评审报告的信息。",
    "system_prompt": (
        "你是一位资深的植保专家和编辑。你的任务是评审一份农作物防治诊疗报告。\n\n"
        "你可以在 `final_report.md` 找到这份报告。\n\n"
        "你可以在 `question.txt` 找到这份报告的问题/主题。\n\n"
        "用户可能会要求评审报告的特定方面。请用详细的评论回复用户，指出报告中可以改进的地方。\n\n"
        "如果有助于你评审报告，你可以使用搜索工具来搜索信息。\n\n"
        "不要自己写入 `final_report.md`。\n\n"
        "需要检查的事项：\n"
        "- 诊断是否准确：症状描述与病害/虫害判断是否匹配\n"
        "- 报告结构是否完整：是否包含基本信息、症状识别、病因诊断、防治方案、预防措施等必要章节\n"
        "- 防治方案是否实用：农业防治、物理防治、生物防治、化学防治是否全面\n"
        "- 化学药剂推荐是否合理：是否包含有效成分、用法用量、安全间隔期和抗性管理建议\n"
        "- 报告内容是否专业严谨：术语使用是否准确，建议是否可操作\n"
        "- 是否引用了可靠的来源\n"
        "- 报告是否紧扣用户问题并直接回答\n"
        "- 报告是否结构清晰、语言流畅、易于理解"
    ),
}


class CropAgent(BaseAgent):
    name = "千寻有方"
    description = "专业的农作物病虫害诊断与防治智能体，可以识别作物病虫害、分析病因、提供防治方案和用药建议"
    context_schema = CropContext
    capabilities = [
        "file_upload",
        "todo",
        "files",
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.graph = None
        self.checkpointer = None

    async def get_tools(self):
        """返回 Crop Agent 的专用工具"""
        tavily_search = get_tavily_search()
        if tavily_search:
            return [tavily_search]

        logger.warning("No search tools configured, CropAgent will work without web search")
        return []

    async def get_graph(self, **kwargs):
        """构建 Crop Agent 的图"""
        context = self.context_schema.from_file(module_name=self.module_name)

        model = load_chat_model(context.model)
        sub_model = load_chat_model(context.subagents_model)
        search_tools = await self.get_tools()

        research_sub_agent = _get_research_sub_agent(search_tools)

        summary_middleware = SummaryOffloadMiddleware(
            model=model,
            trigger=("tokens", 160000),
            trim_tokens_to_summarize=None,
            summary_offload_threshold=1000,
            max_retention_ratio=0.6,
        )

        subagents_middleware = SubAgentMiddleware(
            default_model=sub_model,
            default_tools=search_tools,
            subagents=[critique_sub_agent, research_sub_agent],
            default_middleware=[
                RuntimeConfigMiddleware(
                    model_context_name="subagents_model",
                    enable_model_override=True,
                    enable_system_prompt_override=False,
                    enable_tools_override=False,
                ),
                PatchToolCallsMiddleware(),
                summary_middleware,
            ],
            general_purpose_agent=True,
        )

        graph = create_agent(
            model=model,
            system_prompt=context.system_prompt,
            middleware=[
                FilesystemMiddleware(backend=_create_fs_backend),
                RuntimeConfigMiddleware(extra_tools=search_tools),
                save_attachments_to_fs,
                image_interceptor,
                TodoListMiddleware(),
                PatchToolCallsMiddleware(),
                subagents_middleware,
                summary_middleware,
            ],
            checkpointer=await self._get_checkpointer(),
        )

        return graph
