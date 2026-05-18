class CropRepository:

    @staticmethod
    async def patch_crop(session, crop_id: int, data: dict):

        return {
            "id": crop_id,
            "name": data.get("name", "测试农作物"),
            "category": data.get("category", "粮食"),
            "description": data.get("description", ""),
            "planting_season": data.get("planting_season", "春季"),
            "harvest_season": data.get("harvest_season", "秋季"),
            "yield_per_mu": data.get("yield_per_mu", 500)
        }