"""Define the configurable parameters for the agent."""

import os
import uuid
from dataclasses import MISSING, dataclass, field, fields
from pathlib import Path
from typing import Annotated, get_args, get_origin

import yaml

from src import config as sys_config
from src.services.mcp_service import get_mcp_server_names
from src.utils import logger

from .tool_registry import gen_tool_info, get_buildin_tools


@dataclass(kw_only=True)
class BaseContext:

    """Base configurable context for all agents."""

    thread_id: str = field(
        default_factory=lambda: str(uuid.uuid4()),
        metadata={"name": "线程ID", "configurable": False, "description": "用于唯一标识一个对话线程"},
    )

    user_id: str = field(
        default_factory=lambda: str(uuid.uuid4()),
        metadata={"name": "用户ID", "configurable": False, "description": "用于唯一标识一个用户"},
    )

    system_prompt: Annotated[str, {"__template_metadata__": {"kind": "prompt"}}] = field(
        default="You are a helpful assistant.",
        metadata={"name": "系统提示词", "description": "用于描述智能体的角色和行为"},
    )

    model: Annotated[str, {"__template_metadata__": {"kind": "llm"}}] = field(
        default=sys_config.default_model,
        metadata={
            "name": "智能体模型",
            "options": [],
            "description": "智能体的驱动模型，建议选择 Agent 能力较强的模型。",
        },
    )

    thinking_enabled: Annotated[bool, {"__template_metadata__": {"kind": "llm"}}] = field(
        default=False,
        metadata={
            "name": "开启思考模式",
            "description": "仅对支持思考模式的模型生效。",
        },
    )

    thinking_effort: Annotated[str, {"__template_metadata__": {"kind": "llm"}}] = field(
        default="medium",
        metadata={
            "name": "思考强度",
            "options": ["low", "medium", "high", "xhigh"],
            "description": "仅对支持思考模式的模型生效。",
        },
    )

    tools: Annotated[list[dict], {"__template_metadata__": {"kind": "tools"}}] = field(
        default_factory=list,
        metadata={
            "name": "工具",
            "options": lambda: gen_tool_info(get_buildin_tools()),
            "description": "内置工具列表。",
        },
    )

    knowledges: Annotated[list[str], {"__template_metadata__": {"kind": "knowledges"}}] = field(
        default_factory=list,
        metadata={
            "name": "知识库",
            "description": "知识库列表，可在知识库页面中创建和管理。",
            "type": "list",
        },
    )

    mcps: Annotated[list[str], {"__template_metadata__": {"kind": "mcps"}}] = field(
        default_factory=list,
        metadata={
            "name": "MCP服务器",
            "options": lambda: get_mcp_server_names(),
            "description": "MCP 服务器列表。",
        },
    )

    def update(self, data: dict):
        """Update known fields from a dict."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)

    @classmethod
    def from_file(cls, module_name: str, input_context: dict = None) -> "BaseContext":
        """Load configuration from YAML."""
        context = cls()
        config_file_path = Path(sys_config.save_dir) / "agents" / module_name / "config.yaml"

        if module_name is not None and os.path.exists(config_file_path):
            file_config = {}
            try:
                with open(config_file_path, encoding="utf-8") as f:
                    file_config = yaml.safe_load(f) or {}
            except Exception as e:
                logger.error(f"加载智能体配置文件出错: {e}")

            context.update(file_config)

        if input_context:
            context.update(input_context)

        return context

    @classmethod
    def save_to_file(cls, config: dict, module_name: str) -> bool:
        """Save configurable fields to YAML."""
        configurable_items = cls.get_configurable_items()
        configurable_config = {k: v for k, v in config.items() if k in configurable_items}

        try:
            config_file_path = Path(sys_config.save_dir) / "agents" / module_name / "config.yaml"
            os.makedirs(os.path.dirname(config_file_path), exist_ok=True)
            with open(config_file_path, "w", encoding="utf-8") as f:
                yaml.dump(configurable_config, f, indent=2, allow_unicode=True)
            return True
        except Exception as e:
            logger.error(f"保存智能体配置文件出错: {e}")
            return False

    @classmethod
    def get_configurable_items(cls):
        """Return configurable fields for UI rendering."""
        configurable_items = {}
        for f in fields(cls):
            if not f.init or f.metadata.get("hide", False):
                continue
            if not f.metadata.get("configurable", True):
                continue

            field_type = f.type
            type_name = cls._get_type_name(field_type)
            template_metadata = cls._extract_template_metadata(field_type)

            options = f.metadata.get("options", [])
            if callable(options):
                options = options()

            configurable_items[f.name] = {
                "type": type_name,
                "name": f.metadata.get("name", f.name),
                "options": options,
                "default": (
                    f.default
                    if f.default is not MISSING
                    else f.default_factory()
                    if f.default_factory is not MISSING
                    else None
                ),
                "description": f.metadata.get("description", ""),
                "template_metadata": template_metadata,
            }

        return configurable_items

    @classmethod
    def _get_type_name(cls, field_type) -> str:
        """Get display type name, handling Annotated and generics."""
        origin = get_origin(field_type)
        if origin is not None:
            if hasattr(origin, "__name__") and origin.__name__ == "Annotated":
                args = get_args(field_type)
                if args:
                    return cls._get_type_name(args[0])
            return origin.__name__ if hasattr(origin, "__name__") else str(origin)
        return field_type.__name__ if hasattr(field_type, "__name__") else str(field_type)

    @classmethod
    def _extract_template_metadata(cls, field_type) -> dict:
        """Extract template metadata from Annotated fields."""
        origin = get_origin(field_type)
        if origin is not None and hasattr(origin, "__name__") and origin.__name__ == "Annotated":
            args = get_args(field_type)
            for metadata in args[1:]:
                if isinstance(metadata, dict) and "__template_metadata__" in metadata:
                    return metadata["__template_metadata__"]
        return {}
