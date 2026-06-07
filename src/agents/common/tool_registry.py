"""Tool registry and utilities for getting tools."""

import asyncio
import logging
import traceback
from typing import Any

from src import config
from src.agents.common.toolkits.agrochemicals import get_agrochemical_by_name
from src.agents.common.toolkits.yolo import yolo
from src.agents.common.toolkits.kg_query import query_knowledge_graph
from src.agents.common.toolkits.graph_search import query_subgraph
from src.agents.common.toolkits.knowledge_base.tool import get_kb_based_tools
from src.agents.common.toolkits.weather_v2.tools import weather_forecast
from src.agents.common.toolkits.web_search.tool import get_tavily_search


logger = logging.getLogger(__name__)


def gen_tool_info(tools) -> list[dict[str, Any]]:
    """获取所有工具的信息（用于前端展示）。

    Args:
        tools: 工具列表

    Returns:
        工具信息列表，包含 id, name, description, metadata, args 等
    """
    tools_info = []

    try:
        for tool_obj in tools:
            try:
                metadata = getattr(tool_obj, "metadata", {}) or {}
                info = {
                    "id": tool_obj.name,
                    "name": metadata.get("name", tool_obj.name),
                    "description": tool_obj.description,
                    "metadata": metadata,
                    "args": [],
                }

                if hasattr(tool_obj, "args_schema") and tool_obj.args_schema:
                    if isinstance(tool_obj.args_schema, dict):
                        schema = tool_obj.args_schema
                    else:
                        schema = tool_obj.args_schema.schema()

                    for arg_name, arg_info in schema.get("properties", {}).items():
                        info["args"].append(
                            {
                                "name": arg_name,
                                "type": arg_info.get("type", ""),
                                "description": arg_info.get("description", ""),
                            }
                        )

                tools_info.append(info)

            except Exception as e:
                logger.error(
                    f"Failed to process tool {getattr(tool_obj, 'name', 'unknown')}: {e}\n"
                    f"{traceback.format_exc()}. Details: {dict(tool_obj.__dict__)}"
                )
                continue

    except Exception as e:
        logger.error(f"Failed to get tools info: {e}\n{traceback.format_exc()}")
        return []

    logger.info(f"Successfully extracted info for {len(tools_info)} tools")
    return tools_info


def get_buildin_tools() -> list:
    """注册静态工具。

    Returns:
        内置工具列表
    """
    static_tools = [
        query_knowledge_graph,
        query_subgraph,
        weather_forecast,
        yolo,
        get_agrochemical_by_name,
    ]

    # 检查是否启用网页搜索
    if config.enable_web_search:
        tavily_search = get_tavily_search()
        if tavily_search:
            static_tools.append(tavily_search)

    return static_tools


async def get_tools_from_context(context, extra_tools=None) -> list:
    """从上下文配置中获取工具列表。

    Args:
        context: 上下文对象，包含 tools, knowledges 配置
        extra_tools: 额外的工具列表

    Returns:
        工具列表
    """
    # 1. 基础工具
    all_basic_tools = get_buildin_tools() + (extra_tools or [])
    selected_tools = []

    if context.tools:
        tools_map = {t.name: t for t in all_basic_tools}
        for tool_name in context.tools:
            if tool_name in tools_map:
                selected_tools.append(tools_map[tool_name])

    # 2. 知识库工具
    if context.knowledges:
        kb_tools = get_kb_based_tools(db_names=context.knowledges)
        selected_tools.extend(kb_tools)

    return selected_tools
