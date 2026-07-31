"""
MinIO URL 数据迁移脚本
将旧格式 http://localhost:9000/... 迁移到 http://47.114.88.3:5050/api/storage/...
"""

import asyncio

from src.storage.postgres.manager import pg_manager
from src.utils import logger

OLD_PREFIX_PATTERNS = [
    "http://localhost:9000/",
    "http://47.114.88.3:9000/",
]
NEW_PREFIX = "http://47.114.88.3:5050/api/storage/"


async def migrate_knowledge_files():
    """迁移 knowledge_files 表中的 minio_url"""
    async with pg_manager.get_async_session_context() as db:
        select_query = """
            SELECT id, minio_url FROM knowledge_files
            WHERE minio_url IS NOT NULL
            AND (minio_url LIKE 'http://localhost:9000/%' OR minio_url LIKE 'http://%:9000/%')
        """
        result = await db.execute(select_query)
        rows = result.fetchall()
        logger.info(f"找到 {len(rows)} 条 knowledge_files 记录需要迁移")

        if not rows:
            return 0

        updated = 0
        for row in rows:
            record_id, old_url = row
            new_url = old_url
            for prefix in OLD_PREFIX_PATTERNS:
                if new_url.startswith(prefix):
                    new_url = NEW_PREFIX + new_url[len(prefix):]
                    break
            if new_url != old_url:
                update_query = "UPDATE knowledge_files SET minio_url = $1 WHERE id = $2"
                await db.execute(update_query, new_url, record_id)
                updated += 1

        logger.info(f"成功迁移 {updated} 条 knowledge_files 记录")
        return updated


async def main():
    """主函数"""
    logger.info("开始 MinIO URL 数据迁移...")
    total = await migrate_knowledge_files()
    logger.info(f"迁移完成，共处理 {total} 条记录")
    return total


if __name__ == "__main__":
    asyncio.run(main())
