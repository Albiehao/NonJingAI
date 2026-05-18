from fastapi import APIRouter, HTTPException

from server.schemas.crop_schema import CropPatchRequest
from server.repositories.crop_repository import CropRepository

crop = APIRouter(
    prefix="/crops",
    tags=["Crops"]
)


@crop.patch("/{crop_id}")
async def patch_crop(crop_id: int, request: CropPatchRequest):

    # 获取用户实际传入字段
    update_data = request.dict(exclude_unset=True)

    # 空请求校验
    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="No fields provided"
        )

    # 调用 repository
    crop_data = await CropRepository.patch_crop(
        None,
        crop_id,
        update_data
    )

    # 未找到数据
    if not crop_data:
        raise HTTPException(
            status_code=404,
            detail="Crop not found"
        )

    # 返回结果
    return {
        "code": 200,
    }