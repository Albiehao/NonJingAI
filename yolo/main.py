import json
import os
from pathlib import Path
from urllib.parse import urlparse

from fastapi import FastAPI, HTTPException
from minio import Minio
from ultralytics import YOLO

from services.minio_client import get_image_cv2, upload_image_cv2

app = FastAPI()

MODEL_PATH = os.getenv("YOLO_MODEL_PATH", "yolo.pt")

model = YOLO(MODEL_PATH)

MINIO_URI = os.getenv("MINIO_URI", "http://minio:9000")
MINIO_ENDPOINT = MINIO_URI.replace("http://", "").replace("https://", "")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin")
RESULT_BUCKET_NAME = "yolo-images"


minio_client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=MINIO_URI.startswith("https://"),
)


if not minio_client.bucket_exists(RESULT_BUCKET_NAME):
    minio_client.make_bucket(RESULT_BUCKET_NAME)


policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {"AWS": ["*"]},
            "Action": ["s3:GetObject"],
            "Resource": [f"arn:aws:s3:::{RESULT_BUCKET_NAME}/*"],
        }
    ],
}

minio_client.set_bucket_policy(RESULT_BUCKET_NAME, json.dumps(policy))


@app.get("/health")
def health():
    return {"status": "ok"}


def parse_minio_url(image_url: str):
    parsed = urlparse(image_url)
    path = parsed.path.lstrip("/")
    # 兼容新代理 URL 格式: /api/storage/{bucket}/{object}
    if path.startswith("api/storage/"):
        path = path[len("api/storage/"):]
    parts = path.split("/", 1)
    if len(parts) != 2 or not all(parts):
        raise HTTPException(status_code=400, detail="图片 URL 格式不正确")
    return parts[0], parts[1]


def _get_result_base_url(image_url: str) -> str:
    """从传入的 image_url 提取协议和主机，构造结果图片的基础 URL"""
    parsed = urlparse(image_url)
    return f"{parsed.scheme}://{parsed.netloc}/api/storage"


@app.post("/detect")
async def detect(image_url: str):
    detections = []
    try:
        bucket_name, object_name = parse_minio_url(image_url)
        image = get_image_cv2(bucket_name, object_name)
        if image is None:
            raise HTTPException(status_code=400, detail="无法解码图片，请检查 MinIO 对象是否有效")

        results = model.predict(source=image, conf=0.5, verbose=False)
        result = results[0]

        if result.boxes is not None:
            boxes = result.boxes.xyxy.cpu().numpy().tolist()
            classes = result.boxes.cls.cpu().numpy()
            scores = result.boxes.conf.cpu().numpy()

            for i in range(len(boxes)):
                detections.append(
                    {
                        "class": model.names[int(classes[i])],
                        "confidence": round(float(scores[i]) * 100, 2),
                        "bbox": [round(coord, 2) for coord in boxes[i]],
                    }
                )

        plotted_image = result.plot()
        source_stem = Path(object_name).stem
        result_object_name = f"{source_stem}_detected.jpg"
        upload_image_cv2(RESULT_BUCKET_NAME, result_object_name, plotted_image)
        result_image_url = f"{_get_result_base_url(image_url)}/{RESULT_BUCKET_NAME}/{result_object_name}"

        return {
            "code": 0,
            "message": "success",
            "data": {
                "source": {
                    "image_url": image_url,
                    "bucket_name": bucket_name,
                    "object_name": object_name,
                },
                "result_image": {
                    "bucket_name": RESULT_BUCKET_NAME,
                    "object_name": result_object_name,
                    "image_url": result_image_url,
                },
                "detections": detections,
            },
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"识别过程出错: {str(e)}")
