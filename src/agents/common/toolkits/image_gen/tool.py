"""Image generation tool using SiliconFlow API."""

import logging
import uuid

import requests
from langchain.tools import tool

from src.storage.minio import aupload_file_to_minio

logger = logging.getLogger(__name__)


@tool
async def text_to_img_demo(text: str) -> str:
    """使用模型生成图片，会返回图片的 URL。

    Args:
        text: 图片描述文本

    Returns:
        上传到 MinIO 后的图片 URL
    """
    url = "https://api.siliconflow.cn/v1/images/generations"

    payload = {
        "model": "Qwen/Qwen-Image",
        "prompt": text,
    }
    headers = {"Authorization": "Bearer {os.getenv('SILICONFLOW_API_KEY')}", "Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers)
        response_json = response.json()
    except Exception as e:
        logger.error(f"Failed to generate image with: {e}")
        raise ValueError(f"Image generation failed: {e}")

    try:
        image_url = response_json["images"][0]["url"]
    except (KeyError, IndexError, TypeError) as e:
        logger.error(f"Failed to parse image URL from response: {e}, {response_json=}")
        raise ValueError(f"Image URL extraction failed: {e}")

    # Upload to MinIO
    response = requests.get(image_url)
    file_data = response.content

    file_name = f"{uuid.uuid4()}.jpg"
    uploaded_url = await aupload_file_to_minio(
        bucket_name="generated-images", file_name=file_name, data=file_data, file_extension="jpg"
    )
    logger.info(f"Image uploaded. URL: {uploaded_url}")
    return uploaded_url
