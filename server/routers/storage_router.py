import asyncio

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from src.storage.minio.client import StorageError, get_minio_client
from src.utils import logger

storage_router = APIRouter(prefix="/storage", tags=["storage"])

MEDIA_TYPES = {
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "png": "image/png",
    "gif": "image/gif",
    "webp": "image/webp",
    "svg": "image/svg+xml",
    "ico": "image/x-icon",
    "bmp": "image/bmp",
    "pdf": "application/pdf",
    "txt": "text/plain",
    "json": "application/json",
    "html": "text/html",
    "css": "text/css",
    "js": "application/javascript",
    "mp4": "video/mp4",
    "webm": "video/webm",
    "mp3": "audio/mpeg",
    "wav": "audio/wav",
    "ogg": "audio/ogg",
}


@storage_router.get("/{bucket}/{object_name:path}")
async def proxy_storage_file(bucket: str, object_name: str):
    """代理 MinIO 文件访问，通过 API 服务器流式传输文件"""
    minio_client = get_minio_client()
    try:
        minio_response = await minio_client.adownload_response(bucket, object_name)
    except StorageError as e:
        logger.warning(f"Storage proxy 404: bucket={bucket}, object={object_name}, error={e}")
        raise HTTPException(status_code=404, detail=str(e))

    ext = object_name.rsplit(".", 1)[-1].lower() if "." in object_name else ""
    media_type = MEDIA_TYPES.get(ext, "application/octet-stream")

    async def minio_stream():
        try:
            while True:
                chunk = await asyncio.to_thread(minio_response.read, 8192)
                if not chunk:
                    break
                yield chunk
        finally:
            minio_response.close()
            minio_response.release_conn()

    return StreamingResponse(minio_stream(), media_type=media_type)
