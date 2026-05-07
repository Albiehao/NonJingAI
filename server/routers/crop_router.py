from fastapi import APIRouter
from pydantic import BaseModel, Field, field_validator
from typing import List

from server.services.crop_service import CropService

router = APIRouter(prefix="/crops", tags=["crops"])


class Center(BaseModel):
    lat: float = Field(..., ge=-90, le=90)
    lng: float = Field(..., ge=-180, le=180)


class GeoFilter(BaseModel):
    type: str
    center: Center
    radius_km: float = Field(..., gt=0, le=1000)

    @field_validator("type")
    @classmethod
    def check_type(cls, v):
        if v != "radius":
            raise ValueError("geo_filter.type 目前只支持 radius")
        return v


class CropQueryRequest(BaseModel):
    crop_ids: List[int]
    geo_filter: GeoFilter

    @field_validator("crop_ids")
    @classmethod
    def check_crop_ids(cls, v):
        if not v:
            raise ValueError("crop_ids不能为空")

        if any(i <= 0 for i in v):
            raise ValueError("crop_ids必须为正整数")

        return v


@router.post("/find")
async def find_users(req: CropQueryRequest):

    user_ids = await CropService.find_users_by_crop_and_geo(req)

    return {
        "code": 200,
        "message": "success",
        "data": user_ids
    }