"""YOLO plant disease detection tool using FastAPI service."""

import logging

import requests
from langchain.tools import tool

logger = logging.getLogger(__name__)

def _get_yolo_api_url() -> str:
    """获取 YOLO API URL，支持环境变量配置"""
    import os
    if os.getenv("RUNNING_IN_DOCKER") == "true":
        return os.getenv("YOLO_API_URL", "http://yoloapi:8000/detect")
    else:
        return os.getenv("YOLO_API_URL", "http://127.0.0.1:8001/detect")


@tool()
def yolo(image_url: str) -> str:
    """使用 YOLO 模型识别图片中的农作物病虫害。
    图片url上传到 YOLO 识别服务进行检测，
    返回识别到的病虫害名称、置信度以及标注后的图片 URL。
    Args:
        image_url: 待识别图片的 URL 地址

    Returns:
        JSON 格式的识别结果，包含病虫害列表和标注图片 URL
        格式示例：
            {
              "code": 0,
              "message": "success",
              "data": {
                "source": {
                  "image_url": "http://127.0.0.1:9000/chat-image/r-c.jpg",
                  "bucket_name": "chat-image",
                  "object_name": "r-c.jpg"
                },
                "result_image": {
                  "bucket_name": "yolo-images",
                  "object_name": "r-c_detected.jpg",
                  "image_url": "http://localhost:9000/yolo-images/r-c_detected.jpg"
                },
                "detections": [
                  {
                    "class": "Bacteria_Leaf_Blight",
                    "confidence": 71.42,
                    "bbox": [
                      177.98,
                      8.15,
                      558.51,
                      463.42
                    ]
                  }
                ]
              }
            }
    """
    #获取YOLO API URL
    api_url = _get_yolo_api_url()
    logger.info(f"YOLO API URL: {api_url}")
    response = requests.post(api_url,params={"image_url": image_url})
    return response.json()
