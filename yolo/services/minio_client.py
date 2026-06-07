from io import BytesIO
from urllib.request import urlopen

import cv2
import numpy as np
from minio import Minio


client = Minio(
    "minio:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False,
)


def get_image_cv2(bucket_name: str, object_name: str):
    """从 MinIO 读取图片并解码为 OpenCV 对象。

    通过 API 代理的 HTTP 接口下载，避免 MinIO 直连的路径问题。
    """
    api_host = "http://api:5050"
    url = f"{api_host}/api/storage/{bucket_name}/{object_name}"
    resp = urlopen(url, timeout=30)
    image_bytes = resp.read()
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    return cv2.imdecode(image_array, cv2.IMREAD_COLOR)


def upload_image_cv2(bucket_name: str, object_name: str, image: np.ndarray):
    """将 OpenCV 图片编码后上传到 MinIO。"""
    success, encoded = cv2.imencode(".jpg", image)
    if not success:
        raise ValueError("图片编码失败")

    image_bytes = encoded.tobytes()
    client.put_object(
        bucket_name,
        object_name,
        BytesIO(image_bytes),
        length=len(image_bytes),
        content_type="image/jpeg",
    )

    return object_name
