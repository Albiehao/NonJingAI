from minio import Minio
import os

client = Minio(
    "minio:9000",  # docker服务名
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False
)

BUCKET_NAME = "images"

def upload_file(file_path):
    file_name = os.path.basename(file_path)

    client.fput_object(
        BUCKET_NAME,
        file_name,
        file_path
    )

    return f"http://localhost:9000/{BUCKET_NAME}/{file_name}"