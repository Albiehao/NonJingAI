from server.repositories.crop_repository import CropRepository


class CropService:

    @staticmethod
    async def find_users_by_crop_and_geo(req):

        return await CropRepository.find_users(
            crop_ids=req.crop_ids,
            lat=req.geo_filter.center.lat,
            lng=req.geo_filter.center.lng,
            radius=req.geo_filter.radius_km
        )