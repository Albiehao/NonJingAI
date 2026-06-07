"""图片拦截与YOLO识别中间件 - 拦截图片并调用YOLO识别病虫害。"""

import os
from collections.abc import Callable

import aiohttp
from langchain.agents.middleware import AgentMiddleware, ModelRequest, ModelResponse

from src.utils import logger


def _get_yolo_api_url() -> str:
    return os.getenv("YOLO_API_URL", "http://127.0.0.1:8001/detect")


def _build_yolo_result_text(detections: list[dict]) -> str:
    """将YOLO检测结果组装为文本描述。"""
    if not detections:
        return "【YOLO识别：未检测到目标】"

    lines = ["【YOLO农作物病虫害识别结果】"]
    for i, det in enumerate(detections, 1):
        cls_name = det.get("class", "未知")
        confidence = det.get("confidence", 0)
        lines.append(f"  {i}. 检测到: {cls_name} (置信度: {confidence:.1f}%)")

    lines.append("")
    lines.append("请根据以上YOLO识别结果进行分析和诊断。")
    return "\n".join(lines)


def _build_image_notice(original_content: list) -> str:
    """回退方案：提取用户文本并追加不支持图片的提示。"""
    text_parts = []
    for block in original_content:
        if isinstance(block, dict) and block.get("type") == "text":
            text_parts.append(block.get("text", ""))
    user_text = " ".join(filter(None, text_parts))
    notice = "【用户上传了一张图片，当前模型不支持图片识别，请根据文字描述进行分析。】"
    if user_text:
        return f"{user_text}\n\n{notice}"
    return notice


def _is_http_url(url: str) -> bool:
    return url.startswith("http://") or url.startswith("https://")


async def _call_yolo_api(image_url: str) -> str | None:
    """异步调用 YOLO API，返回检测结果文本，失败返回 None。"""
    api_url = _get_yolo_api_url()
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                api_url, params={"image_url": image_url}, timeout=aiohttp.ClientTimeout(total=15)
            ) as resp:
                if resp.status != 200:
                    logger.warning(f"YOLO API returned status {resp.status}")
                    return None
                data = await resp.json()
    except Exception as e:
        logger.warning(f"YOLO API call failed: {e}")
        return None

    if data.get("code") != 0:
        logger.warning(f"YOLO API error: {data.get('message')}")
        return None

    detections = data.get("data", {}).get("detections", [])
    return _build_yolo_result_text(detections)


class ImageInterceptorMiddleware(AgentMiddleware):
    """拦截并处理消息中的 image_url 内容。

    1. 对 HTTP 图片 URL 调用 YOLO API 进行病虫害识别
    2. 将识别结果替换为文本供模型分析
    3. 若非 HTTP URL，则替换为通用提示文本
    """

    async def awrap_model_call(
        self, request: ModelRequest, handler: Callable[[ModelRequest], ModelResponse]
    ) -> ModelResponse:
        messages = list(request.messages)
        modified = False

        for i, msg in enumerate(messages):
            content = None
            if isinstance(msg, dict):
                content = msg.get("content")
            else:
                content = getattr(msg, "content", None)

            if not content or not isinstance(content, list):
                continue

            image_blocks = [
                block
                for block in content
                if isinstance(block, dict) and block.get("type") == "image_url"
            ]

            if not image_blocks:
                continue

            yolo_results = []
            for block in image_blocks:
                image_url_info = block.get("image_url", {})
                if isinstance(image_url_info, dict):
                    url = image_url_info.get("url", "")
                else:
                    url = str(image_url_info)

                logger.info(f"ImageInterceptorMiddleware: processing image_url (len={len(url)})")

                if _is_http_url(url):
                    result = await _call_yolo_api(url)
                    if result:
                        yolo_results.append(result)
                    else:
                        yolo_results.append("【YOLO识别失败，请根据文字描述进行分析】")
                else:
                    yolo_results.append("【用户上传了一张图片，当前模型不支持图片识别，请根据文字描述进行分析。】")

            result_text = "\n\n".join(yolo_results)

            # 提取原始用户文本
            text_parts = []
            for block in content:
                if isinstance(block, dict) and block.get("type") == "text":
                    text_parts.append(block.get("text", ""))
            user_text = " ".join(filter(None, text_parts))

            new_content = f"{user_text}\n\n{result_text}" if user_text else result_text

            if isinstance(msg, dict):
                msg["content"] = new_content
                messages[i] = msg
            else:
                messages[i] = {"role": "user", "content": new_content}

            modified = True
            logger.info(f"ImageInterceptorMiddleware: replaced image_url in message {i} with YOLO results")

        if modified:
            request = request.override(messages=messages)

        return await handler(request)


# Singleton instance for easy import
image_interceptor = ImageInterceptorMiddleware()
