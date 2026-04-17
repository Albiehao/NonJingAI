import json
import os
import shutil
import uuid

from fastapi import FastAPI, File, UploadFile
from minio import Minio
from ultralytics import YOLO

app = FastAPI()

MODEL_PATH = os.getenv("YOLO_MODEL_PATH", "yolo.pt")

model = YOLO(MODEL_PATH)

MINIO_URI = os.getenv("MINIO_URI", "http://minio:9000")
MINIO_PUBLIC_URI = os.getenv("MINIO_PUBLIC_URI", "http://localhost:9000")
MINIO_ENDPOINT = MINIO_URI.replace("http://", "").replace("https://", "")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin")
BUCKET_NAME = "yolo-images"

minio_client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=MINIO_URI.startswith("https://"),
)

if not minio_client.bucket_exists(BUCKET_NAME):
    minio_client.make_bucket(BUCKET_NAME)

policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {"AWS": ["*"]},
            "Action": ["s3:GetObject"],
            "Resource": [f"arn:aws:s3:::{BUCKET_NAME}/*"],
        }
    ],
}

minio_client.set_bucket_policy(BUCKET_NAME, json.dumps(policy))


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/detect")
async def detect(file: UploadFile = File(...)):
    input_path = f"/tmp/{uuid.uuid4()}.jpg"
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    results = model(input_path, conf=0.3, iou=0.5)

    result_filename = f"{uuid.uuid4()}.jpg"
    result_path = f"/tmp/{result_filename}"
    results[0].save(filename=result_path)

    minio_client.fput_object(BUCKET_NAME, result_filename, result_path)

    image_url = f"{MINIO_PUBLIC_URI}/{BUCKET_NAME}/{result_filename}"

    boxes = results[0].boxes.xyxy.tolist()
    classes = results[0].boxes.cls.tolist()
    scores = results[0].boxes.conf.tolist()

    data = []
    for i in range(len(boxes)):
        data.append(
            {
                "class": model.names[int(classes[i])],
                "confidence": round(float(scores[i]) * 100, 2),
                "bbox": boxes[i],
            }
        )

    return {
        "code": 0,
        "message": "success",
        "image_url": image_url,
        "data": data,
    }
