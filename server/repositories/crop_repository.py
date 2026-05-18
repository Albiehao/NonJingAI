from sqlalchemy import text
from src.storage.postgres.manager import PostgresManager

# 模块级单例
postgres_manager = PostgresManager()


class CropRepository:

    @staticmethod
    async def find_users(crop_ids, lat, lng, radius):

        async with postgres_manager.AsyncSession() as session:

            sql = text("""
                SELECT DISTINCT uc.user_id
                FROM user_crops uc
                JOIN users u ON u.id = uc.user_id
                WHERE uc.crop_id = ANY(:crop_ids)
                  AND u.is_deleted = 0
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