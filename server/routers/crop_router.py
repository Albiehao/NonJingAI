from fastapi import APIRouter, HTTPException

from server.schemas.crop_schema import (
    CropPatchRequest,
    CropPutRequest
)
from server.repositories.crop_repository import CropRepository

crop = APIRouter(
    prefix="/crops",
    tags=["Crops"]
)


# PATCH：部分更新
@crop.patch("/{crop_id}")
async def patch_crop(crop_id: int, request: CropPatchRequest):

    # 只获取用户实际传入字段
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

    return {
        "code": 200,
        "message": "Crop updated successfully",
        "data": {
            "id": crop_data["id"],
            "name": crop_data["name"],
            "category": crop_data["category"],
            "description": crop_data["description"],
            "planting_season": crop_data["planting_season"],
            "harvest_season": crop_data["harvest_season"],
            "yield_per_mu": crop_data["yield_per_mu"]
        }
    }


# PUT：全量更新
@crop.put("/{crop_id}")
async def put_crop(crop_id: int, request: CropPutRequest):

    # PUT 必须传完整字段
    update_data = request.dict()

    # 调用 repository
    crop_data = await CropRepository.put_crop(
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

    return {
        "code": 200,
        "message": "Crop replaced successfully",
        "data": {
            "id": crop_data["id"],
            "name": crop_data["name"],
            "category": crop_data["category"],
            "description": crop_data["description"],
            "planting_season": crop_data["planting_season"],
            "harvest_season": crop_data["harvest_season"],
            "yield_per_mu": crop_data["yield_per_mu"]
        }
    }