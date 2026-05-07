from sqlalchemy import text

from src.storage.postgres.manager import PostgresManager


class CropRepository:

    @staticmethod
    async def find_users(crop_ids, lat, lng, radius):

        postgres_manager = PostgresManager()

        async with postgres_manager.AsyncSession() as session:

            sql = text("""
                SELECT DISTINCT uc.user_id
                FROM user_crops uc
                WHERE uc.crop_id = ANY(:crop_ids)
                AND (
                    6371 * acos(
                        cos(radians(:lat))
                        * cos(radians(uc.latitude))
                        * cos(radians(uc.longitude) - radians(:lng))
                        + sin(radians(:lat))
                        * sin(radians(uc.latitude))
                    )
                ) <= :radius
            """)

            result = await session.execute(
                sql,
                {
                    "crop_ids": crop_ids,
                    "lat": lat,
                    "lng": lng,
                    "radius": radius
                }
            )

            rows = result.fetchall()

            return [row[0] for row in rows]