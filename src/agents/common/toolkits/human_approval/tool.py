"""Human-in-the-loop approval tool."""

import logging

from langchain.tools import tool
from langgraph.types import interrupt

logger = logging.getLogger(__name__)


@tool(name_or_callable="human_in_the_loop_debug", description="请求人工审批工具，用于在执行重要操作前获得人类确认。")
def get_approved_user_goal(operation_description: str) -> dict:
    """请求人工审批，用于在执行重要操作前获得人类确认。

    Args:
        operation_description: 需要审批的操作描述

    Returns:
        包含审批结果的字典，格式为 {"approved": bool, "message": str}
    """
    interrupt_info = {
        "question": "是否批准以下操作？",
        "operation": operation_description,
    }

    is_approved = interrupt(interrupt_info)

    if is_approved:
        result = {
            "approved": True,
            "message": f"✅ 操作已批准：{operation_description}",
        }
        logger.info(f"✅ 人工审批通过：{operation_description}")
    else:
        result = {
            "approved": False,
            "message": f"❌ 操作被拒绝：{operation_description}",
        }
        logger.info(f"❌ 人工审批被拒绝：{operation_description}")

    return result
