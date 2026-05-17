from typing import Optional
from pydantic import BaseModel


# PATCH：部分更新
class CropPatchRequest(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    planting_season: Optional[str] = None
    harvest_season: Optional[str] = None
    yield_per_mu: Optional[float] = None


# PUT：全量更新
class CropPutRequest(BaseModel):
    name: str
    category: str
    description: str
    planting_season: str
    harvest_season: str
    yield_per_mu: float