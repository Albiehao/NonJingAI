import os
import traceback

from langchain.chat_models import BaseChatModel, init_chat_model
from langchain_core.messages import AIMessage
from pydantic import SecretStr

from src import config
from src.utils import get_docker_safe_url
from src.utils.logging_config import logger


class _PatchedDeepSeekMixin:
    """Send reasoning_content back to DeepSeek for thinking-mode tool loops."""

    def _get_request_payload(self, input_, *args, stop=None, **kwargs) -> dict:
        messages = self._convert_input(input_).to_messages()
        payload = super()._get_request_payload(input_, *args, stop=stop, **kwargs)

        for message, payload_message in zip(messages, payload.get("messages", []), strict=False):
            if not isinstance(message, AIMessage):
                continue

            reasoning_content = message.additional_kwargs.get("reasoning_content")
            if reasoning_content:
                payload_message["reasoning_content"] = reasoning_content

        return payload


def _normalize_thinking_effort(thinking_effort: str | None) -> str | None:
    if thinking_effort in {"low", "medium"}:
        return "high"
    if thinking_effort == "xhigh":
        return "max"
    return thinking_effort


def _get_thinking_config(
    supports_thinking: bool,
    thinking_effort: str,
    thinking_enabled: bool | None = None,
    thinking_effort_override: str | None = None,
) -> dict:
    # 模型不支持思考，直接返回空
    if not supports_thinking:
        return {}

    # 用户显式关闭思考模式 - 需要传递禁用参数（DeepSeek 默认开启）
    if thinking_enabled is False:
        return {"extra_body": {"thinking": {"type": "disabled"}}}

    # 用户未设置或显式开启思考模式
    if thinking_enabled is True:
        normalized_effort = _normalize_thinking_effort(thinking_effort_override or thinking_effort) or thinking_effort
        return {
            "reasoning_effort": normalized_effort,
            "extra_body": {"thinking": {"type": "enabled"}},
        }

    # thinking_enabled 为 None（未设置）时，默认不开启
    return {}


def _merge_model_kwargs(kwargs: dict, extra_kwargs: dict) -> dict:
    if not extra_kwargs:
        return kwargs

    merged = dict(kwargs)
    extra_body = dict(merged.get("extra_body") or {})
    thinking_extra_body = dict(extra_kwargs.get("extra_body") or {})
    if thinking_extra_body:
        extra_body.update(thinking_extra_body)
        merged["extra_body"] = extra_body

    for key, value in extra_kwargs.items():
        if key == "extra_body":
            continue
        merged[key] = value

    return merged


def load_chat_model(fully_specified_name: str, **kwargs) -> BaseChatModel:
    """Load a chat model from a fully specified provider/model name."""
    thinking_enabled = kwargs.pop("thinking_enabled", None)
    thinking_effort_override = kwargs.pop("thinking_effort", None)
    logger.debug(f"load_chat_model: model={fully_specified_name}, thinking_enabled={thinking_enabled}, thinking_effort={thinking_effort_override}")

    if not isinstance(fully_specified_name, str):
        logger.error(f"Invalid model name type: {type(fully_specified_name)}, value: {fully_specified_name}")
        if isinstance(fully_specified_name, dict):
            model_name = (
                fully_specified_name.get("model_id")
                or fully_specified_name.get("id")
                or fully_specified_name.get("name")
            )
            if model_name:
                logger.warning(f"Extracted model name from dict: {model_name}")
                fully_specified_name = str(model_name)
            else:
                raise ValueError(f"Cannot extract model name from dict: {fully_specified_name}")
        else:
            logger.warning(f"Converting model name to string: {fully_specified_name}")
            fully_specified_name = str(fully_specified_name)

    provider, model = fully_specified_name.split("/", maxsplit=1)

    assert provider != "custom", "[弃用] 自定义模型已移除，请在 src/config/static/models.py 中配置"

    model_info = config.model_names.get(provider)
    if not model_info:
        raise ValueError(f"Unknown model provider: {provider}")

    env_var = model_info.env
    api_key = os.getenv(env_var) or env_var
    base_url = get_docker_safe_url(model_info.base_url)

    model_config = model_info.models.get(model)
    if isinstance(model_config, dict):
        supports_thinking = model_config.get("supports_thinking", False)
        thinking_effort = model_config.get("default_thinking_effort", "medium") or "medium"
    elif model_config:
        supports_thinking = model_config.supports_thinking
        thinking_effort = model_config.default_thinking_effort or "medium"
    else:
        supports_thinking = False
        thinking_effort = "medium"

    thinking_kwargs = _get_thinking_config(
        supports_thinking,
        thinking_effort,
        thinking_enabled=thinking_enabled,
        thinking_effort_override=thinking_effort_override,
    )
    logger.debug(f"thinking_kwargs: {thinking_kwargs}, supports_thinking={supports_thinking}")
    kwargs = _merge_model_kwargs(kwargs, thinking_kwargs)

    if provider == "openai":
        model_spec = f"{provider}:{model}"
        logger.debug(f"[official] Loading model {model_spec} with kwargs {kwargs}")
        return init_chat_model(model_spec, **kwargs)

    if provider == "deepseek":
        from langchain_deepseek import ChatDeepSeek

        class PatchedChatDeepSeek(_PatchedDeepSeekMixin, ChatDeepSeek):
            pass

        logger.debug(f"[official] Loading model deepseek:{model} with kwargs {kwargs}")
        return PatchedChatDeepSeek(
            model=model,
            api_key=SecretStr(api_key),
            base_url=base_url,
            api_base=base_url,
            stream_usage=True,
            **kwargs,
        )

    if provider == "dashscope":
        from langchain_deepseek import ChatDeepSeek

        return ChatDeepSeek(
            model=model,
            api_key=SecretStr(api_key),
            base_url=base_url,
            api_base=base_url,
            stream_usage=True,
            **kwargs,
        )

    try:
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(
            model=model,
            api_key=SecretStr(api_key),
            base_url=base_url,
            stream_usage=True,
            **kwargs,
        )
    except Exception as e:
        raise ValueError(f"Model provider {provider} load failed, {e} \n {traceback.format_exc()}")
