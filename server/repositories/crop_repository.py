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

    @staticmethod
    async def put_crop(session, crop_id: int, data: dict):

        return {
            "id": crop_id,
            "name": data["name"],
            "category": data["category"],
            "description": data["description"],
            "planting_season": data["planting_season"],
            "harvest_season": data["harvest_season"],
            "yield_per_mu": data["yield_per_mu"]
        }