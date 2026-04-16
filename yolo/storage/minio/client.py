from minio import Minio
import os

class MinioClient:
    def __init__(self):
        self.client = Minio(
            endpoint=os.getenv("MINIO_URI").replace("http://", ""),
            access_key=os.getenv("MINIO_ACCESS_KEY"),
            secret_key=os.getenv("MINIO_SECRET_KEY"),
            secure=False
        )
        self.bucket = "yolo-images"

        self._ensure_bucket()

    def _ensure_bucket(self):
        if not self.client.bucket_exists(self.bucket):
            self.client.make_bucket(self.bucket)

    def upload_file(self, file_bytes, object_name):
        from io import BytesIO

        self.client.put_object(
            self.bucket,
            object_name,
            BytesIO(file_bytes),
            length=len(file_bytes),
            content_type="image/jpeg"
        )

        return f"{os.getenv('MINIO_URI')}/{self.bucket}/{object_name}"


minio_client = MinioClient()