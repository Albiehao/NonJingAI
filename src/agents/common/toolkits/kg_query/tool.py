"""Knowledge graph query tool."""

import logging
import traceback
from typing import Annotated, Any

from langchain.tools import tool

from src import graph_base

logger = logging.getLogger(__name__)

KG_QUERY_DESCRIPTION = """
使用这个工具可以查询知识图谱中包含的三元组信息。
关键词（query），使用可能帮助回答这个问题的关键词进行查询，不要直接使用用户的原始输入去查询。
"""


@tool(name_or_callable="查询知识图谱", description=KG_QUERY_DESCRIPTION)
def query_knowledge_graph(query: Annotated[str, "The keyword to query knowledge graph."]) -> Any:
    """查询知识图谱中包含的三元组信息。

    Args:
        query: 查询关键词，应使用可能帮助回答问题的关键词，而非用户原始输入

    Returns:
        知识图谱查询结果，包含三元组信息
    """
    try:
        logger.debug(f"Querying knowledge graph with: {query}")
        result = graph_base.query_node(query, hops=2, return_format="triples")
        logger.debug(
            f"Knowledge graph query returned "
            f"{len(result.get('triples', [])) if isinstance(result, dict) else 'N/A'} triples"
        )
        return result
    except Exception as e:
        logger.error(f"Knowledge graph query error: {e}, {traceback.format_exc()}")
        return f"知识图谱查询失败：{str(e)}"
