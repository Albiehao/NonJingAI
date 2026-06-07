"""Web search tool using Metaso (秘塔) API."""

import logging
import os
from typing import Annotated

import requests
from langchain.tools import tool
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

METASO_API_KEY = os.getenv("METASO_API_KEY")
METASO_API_URL = "https://metaso.cn/api/v1/chat/completions"


class MetasoSearchInput(BaseModel):
    """秘塔搜索输入模型。"""

    query: str = Field(description="搜索关键词")


@tool(name_or_callable="web_search", description="使用秘塔搜索进行网络搜索，适合搜索中文内容和国内信息。")
def metaso_search(
    query: Annotated[str, Field(description="搜索关键词，建议使用中文以获得更好的结果")],
    search_type: Annotated[
        str,
        Field(
            description="搜索类型：'ai' - AI 总结模式，'web' - 传统网页搜索结果",
            default="ai",
        ),
    ] = "ai",
) -> dict:
    """使用秘塔搜索进行网络搜索。

    Args:
        query: 搜索关键词
        search_type: 搜索类型，'ai' 返回 AI 总结的答案，'web' 返回传统搜索结果列表

    Returns:
        包含搜索结果的字典：
        - ai 模式：包含 AI 总结的答案、引用来源
        - web 模式：包含搜索结果列表（标题、链接、摘要）
    """
    if not METASO_API_KEY:
        return {"error": "秘塔搜索 API Key 未配置，请在 .env 文件中设置 METASO_API_KEY"}

    headers = {
        "Authorization": f"Bearer {METASO_API_KEY}",
        "Content-Type": "application/json",
    }

    # 构建搜索提示词
    if search_type == "ai":
        system_prompt = "你是一个智能搜索助手，请根据搜索结果为用户提供准确的中文答案，并注明信息来源。"
        user_prompt = f"请搜索以下信息并提供详细的中文回答：{query}"
    else:
        system_prompt = "你是一个网页搜索助手，请提供相关的网页搜索结果。"
        user_prompt = f"搜索：{query}"

    payload = {
        "model": "metaso",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "stream": False,
    }

    try:
        response = requests.post(METASO_API_URL, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()

        # 解析 OpenAI 兼容格式的响应
        if "choices" not in data or not data["choices"]:
            return {"error": "API 返回格式异常", "raw_response": data}

        answer = data["choices"][0]["message"]["content"]

        result = {
            "query": query,
            "search_type": search_type,
            "answer": answer,
            "references": _extract_references(answer),
        }
        return result

    except requests.exceptions.RequestException as e:
        logger.error(f"秘塔搜索 API 请求失败：{e}")
        return {"error": f"搜索请求失败：{str(e)}"}
    except Exception as e:
        logger.error(f"秘塔搜索出错：{e}")
        return {"error": f"搜索出错：{str(e)}"}


def _extract_references(text: str) -> list:
    """从回答中提取引用来源。"""
    import re
    references = []
    # 提取 [[数字]] 格式的引用
    refs = re.findall(r'\[\[(\d+)\]\]', text)
    if refs:
        for i, ref in enumerate(set(refs), 1):
            references.append({"id": int(ref), "url": f"[{i}]"})
    return references


# 保持与旧代码的兼容性
def get_tavily_search():
    """兼容旧代码，实际返回秘塔搜索工具。"""
    return metaso_search
