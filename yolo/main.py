from fastapi import FastAPI, UploadFile, File
from ultralytics import YOLO
from minio import Minio
import shutil
import uuid
import os
import json

app = FastAPI()

# YOLO模型
model = YOLO("yolov8n.pt")

# MinIO配置
MINIO_ENDPOINT = "milvus-minio:9000"
MINIO_ACCESS_KEY = "minioadmin"
MINIO_SECRET_KEY = "minioadmin"
BUCKET_NAME = "yolo-images"

# 初始化 MinIO 客户端
minio_client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False
)

# ✅ 启动时创建 bucket + 设置公开权限
if not minio_client.bucket_exists(BUCKET_NAME):
    minio_client.make_bucket(BUCKET_NAME)

policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {"AWS": ["*"]},
            "Action": ["s3:GetObject"],
            "Resource": [f"arn:aws:s3:::{BUCKET_NAME}/*"]
        }
    ]
}

minio_client.set_bucket_policy(BUCKET_NAME, json.dumps(policy))


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/detect")
async def detect(file: UploadFile = File(...)):
    # 1️⃣ 保存上传文件
    input_path = f"/tmp/{uuid.uuid4()}.jpg"
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 2️⃣ YOLO检测
    results = model(input_path, conf=0.3, iou=0.5)

    # 3️⃣ 保存检测结果图片
    result_filename = f"{uuid.uuid4()}.jpg"
    result_path = f"/tmp/{result_filename}"
    results[0].save(filename=result_path)

    # 4️⃣ 上传到 MinIO
    minio_client.fput_object(
        BUCKET_NAME,
        result_filename,
        result_path
    )

    # 5️⃣ 返回可访问 URL
    image_url = f"http://localhost:9000/{BUCKET_NAME}/{result_filename}"

    # 6️⃣ 解析检测结果
    boxes = results[0].boxes.xyxy.tolist()
    classes = results[0].boxes.cls.tolist()
    scores = results[0].boxes.conf.tolist()

    data = []
    for i in range(len(boxes)):
        data.append({
            "class": model.names[int(classes[i])],
            "confidence": round(float(scores[i]) * 100, 2),
            "bbox": boxes[i]
        })

    return {
        "code": 0,
        "message": "success",
        "image_url": image_url,
        "data": data
    }