import os
import traceback

from langchain.chat_models import BaseChatModel, init_chat_model
from pydantic import SecretStr

from src import config
from src.utils import get_docker_safe_url
from src.utils.logging_config import logger


def load_chat_model(fully_specified_name: str, **kwargs) -> BaseChatModel:
    """
    Load a chat model from a fully specified name.
    
    Args:
        fully_specified_name: 模型名称，格式为 provider/model
        **kwargs: 额外的模型配置参数
    
    Returns:
        BaseChatModel: 加载的聊天模型实例
    """
    provider, model = fully_specified_name.split("/", maxsplit=1)

    assert provider != "custom", "[弃用] 自定义模型已移除，请在 src/config/static/models.py 中配置"

    model_info = config.model_names.get(provider)
    if not model_info:
        raise ValueError(f"Unknown model provider: {provider}")

    env_var = model_info.env

    api_key = os.getenv(env_var) or env_var

    base_url = get_docker_safe_url(model_info.base_url)

    # 获取具体模型配置，检查是否支持思考模式及默认思考强度
    model_config = model_info.models.get(model)
    supports_thinking = model_config.supports_thinking if model_config else False
    thinking_effort = model_config.default_thinking_effort if model_config and model_config.default_thinking_effort else "medium"

    if provider in ["openai", "deepseek"]:
        model_spec = f"{provider}:{model}"
        
        # 如果模型支持思考模式，添加思考相关参数（OpenAI 标准格式）
        if supports_thinking:
            if "extra_body" not in kwargs:
                kwargs["extra_body"] = {}
            kwargs["extra_body"]["enable_thinking"] = True
            kwargs["extra_body"]["reasoning_effort"] = thinking_effort
            logger.debug(f"[thinking] Enabled thinking mode for {model_spec}, effort={thinking_effort}")
        
        logger.debug(f"[official] Loading model {model_spec} with kwargs {kwargs}")
        return init_chat_model(model_spec, **kwargs)

    elif provider in ["dashscope"]:
        from langchain_deepseek import ChatDeepSeek

        # 如果模型支持思考模式，添加思考相关参数
        extra_body = None
        if supports_thinking:
            extra_body = {
                "enable_thinking": True,
                "reasoning_effort": thinking_effort
            }
        
        return ChatDeepSeek(
            model=model,
            api_key=SecretStr(api_key),
            base_url=base_url,
            api_base=base_url,
            stream_usage=True,
            extra_body=extra_body,
        )

    else:
        try:  # 其他模型，默认使用OpenAIBase, like zhipuai, siliconflow
            from langchain_openai import ChatOpenAI

            # 如果模型支持思考模式，添加思考相关参数（OpenAI 标准格式）
            if supports_thinking:
                return ChatOpenAI(
                    model=model,
                    api_key=SecretStr(api_key),
                    base_url=base_url,
                    stream_usage=True,
                    extra_body={
                        "enable_thinking": True,
                        "reasoning_effort": thinking_effort
                    },
                )
            else:
                return ChatOpenAI(
                    model=model,
                    api_key=SecretStr(api_key),
                    base_url=base_url,
                    stream_usage=True,
                )
        except Exception as e:
            raise ValueError(f"Model provider {provider} load failed, {e} \n {traceback.format_exc()}")
