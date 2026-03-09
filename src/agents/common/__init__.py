"""
Common utilities and base classes for agents.

This module provides a unified namespace for commonly used base classes and utilities,
allowing simplified imports like:
    from src.agents.common import BaseAgent, BaseContext, BaseState

For tools, use the tool_registry module:
    from src.agents.common import get_buildin_tools, gen_tool_info, get_tools_from_context
"""

# Base classes - 核心基类
from src.agents.common.base import BaseAgent
from src.agents.common.context import BaseContext

# Model utilities - 模型加载
from src.agents.common.models import load_chat_model
from src.agents.common.state import BaseState

# Tools - 工具注册和获取
from src.agents.common.tool_registry import gen_tool_info, get_buildin_tools, get_tools_from_context

# MCP - Agent 层统一入口（自动过滤 disabled_tools）
from src.services.mcp_service import get_enabled_mcp_tools

__all__ = [
    # Base classes
    "BaseAgent",
    "BaseContext",
    "BaseState",
    # Model utilities
    "load_chat_model",
    # Core tools
    "get_buildin_tools",
    "gen_tool_info",
    "get_tools_from_context",
    # Core MCP
    "get_enabled_mcp_tools",
]
