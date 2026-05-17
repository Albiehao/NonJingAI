from typing import Optional
from pydantic import BaseModel


class CropPatchRequest(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    planting_season: Optional[str] = None
    harvest_season: Optional[str] = None
    yield_per_mu: Optional[float] = None