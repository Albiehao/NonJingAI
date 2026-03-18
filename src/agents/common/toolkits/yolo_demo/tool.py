"""YOLO plant disease detection tool using FastAPI service."""

import logging
import io
import os

import requests
from langchain.tools import tool

logger = logging.getLogger(__name__)


def _get_yolo_api_url() -> str:
    """获取 YOLO API URL，支持环境变量配置"""
    return os.getenv("YOLO_API_URL", "http://127.0.0.1:5001/upload/")


@tool
async def yolo_demo(image_url: str) -> str:
    """使用 YOLO 模型识别图片中的农作物病虫害。

    该工具会下载指定 URL 的图片，上传到 YOLO 识别服务进行检测，
    返回识别到的病虫害名称、置信度以及标注后的图片 URL。

    需要把img的url以<img>标签输出

    Args:
        image_url: 待识别图片的 URL 地址

    Returns:
        JSON 格式的识别结果，包含病虫害列表和标注图片 URL
        格式示例：
        {
            "diseases": [
                {"name": "稻瘟病", "confidence": 93.09},
                {"name": "水稻纹枯病", "confidence": 94.67}
            ],
            "image_url": "http://127.0.0.1:9000/my-app-bucket/xxx.jpg"
        }
    """
    # 步骤 1: 从 URL 下载图片
    try:
        logger.info(f"Downloading image from: {image_url}")
        image_response = requests.get(image_url, timeout=30, stream=True)
        image_response.raise_for_status()

        # 获取图片内容
        image_content = image_response.content

        # 尝试从 URL 或 Content-Type 推断文件扩展名
        content_type = image_response.headers.get("Content-Type", "")
        if "jpeg" in content_type or "jpg" in content_type:
            filename = "image.jpg"
        elif "png" in content_type:
            filename = "image.png"
        else:
            filename = "image.jpg"  # 默认使用 jpg

    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to download image: {e}")
        raise ValueError(f"图片下载失败: {e}")

    # 步骤 2: 上传到 YOLO 识别服务
    try:
        yolo_api_url = _get_yolo_api_url()
        logger.info(f"Uploading image to YOLO service: {yolo_api_url}")

        # 准备 multipart/form-data 请求
        files = {"file": (filename, io.BytesIO(image_content), f"image/{filename.split('.')[-1]}")}

        response = requests.post(yolo_api_url, files=files, timeout=60)
        response.raise_for_status()

        result = response.json()

    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to call YOLO API: {e}")
        raise ValueError(f"YOLO 识别服务调用失败: {e}")
    except Exception as e:
        logger.error(f"Unexpected error during YOLO API call: {e}")
        raise ValueError(f"YOLO 识别过程中发生错误: {e}")

    # 步骤 3: 解析并验证响应
    try:
        if result.get("code") != 200:
            error_msg = result.get("message", "未知错误")
            logger.error(f"YOLO API returned error: {error_msg}")
            raise ValueError(f"YOLO 识别失败: {error_msg}")

        data = result.get("data", {})
        diseases = data.get("diseases", [])
        annotated_image_url = data.get("image_url", "")

        if not diseases:
            logger.info("No diseases detected in the image")
            return "未识别到病虫害"

        # 格式化识别结果
        result_lines = ["🌾 病虫害识别结果："]
        for idx, disease in enumerate(diseases, 1):
            name = disease.get("name", "未知")
            confidence = disease.get("confidence", 0)
            result_lines.append(f"{idx}. {name} (置信度: {confidence:.2f}%)")

        if annotated_image_url:
            result_lines.append(f"\n📷 标注图片地址：{annotated_image_url}")

        formatted_result = "\n".join(result_lines)
        logger.info(f"Detection completed: {len(diseases)} diseases found")

        return formatted_result

    except Exception as e:
        logger.error(f"Failed to parse YOLO response: {e}, response={result}")
        raise ValueError(f"解析识别结果失败: {e}")