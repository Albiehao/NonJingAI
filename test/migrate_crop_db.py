"""
Crop Management System 数据迁移脚本

从 CropManagementSystem.sql 转储文件直接读取数据并导入 PostgreSQL。

用法：
    docker compose exec api uv run python test/migrate_crop_db.py
"""

import asyncio
import re
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.storage.postgres.models_crop import (
    Base,
    CropAgrochemical,
    CropCategory,
    CropCrop,
    CropUser,
    CropUserCrop,
)

POSTGRES_URL = "postgresql+asyncpg://postgres:postgres@postgres:5432/yuxi_know"
SQL_DUMP_PATH = "/app/test/CropManagementSystem.sql"

# MySQL表名 -> (ORM Model, 列名顺序)
TABLE_CONFIG = {
    "users": (
        CropUser,
        ["id", "username", "phone_number", "avatar", "password", "role", "created_at"],
    ),
    "crops": (
        CropCrop,
        ["id", "name", "scientific_name", "created_at", "updated_at", "deleted_at"],
    ),
    "agrochemical_categories": (
        CropCategory,
        ["id", "name", "parent_id", "description", "created_at", "updated_at"],
    ),
    "agrochemicals": (
        CropAgrochemical,
        [
            "id", "product_code", "category_id", "product_name", "brand",
            "monthly_sales", "price", "manufacturer", "registration_no",
            "formulation", "content_spec", "main_image", "description",
            "purchase_links", "use_crops", "usage_method", "precautions",
            "created_at", "updated_at", "deleted_at",
        ],
    ),
    "user_crops": (
        CropUserCrop,
        ["id", "user_id", "crop_id", "created_at", "updated_at", "deleted_at"],
    ),
}


def parse_values_block(block: str) -> list[list[str | None]]:
    rows: list[list[str | None]] = []
    current_row: list[str | None] = []
    current_val = ""
    depth = 0
    in_str = False
    quote_char = ""

    i = 0
    while i < len(block):
        ch = block[i]
        if in_str:
            if ch == "\\" and i + 1 < len(block):
                current_val += ch + block[i + 1]
                i += 2
                continue
            if ch == quote_char:
                in_str = False
            current_val += ch
        elif ch in ("'", '"'):
            in_str = True
            quote_char = ch
            current_val += ch
        elif ch == "(":
            if depth > 0:
                current_val += ch
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                current_row.append(_clean_val(current_val))
                current_val = ""
            else:
                current_val += ch
        elif ch == "," and depth == 1:
            current_row.append(_clean_val(current_val))
            current_val = ""
        elif depth >= 1 and ch not in ("\n", "\r", "\t"):
            current_val += ch
        i += 1

    if current_row:
        rows.append(current_row)
    return rows


def _clean_val(val: str | None) -> str | None:
    if val is None:
        return None
    val = val.strip()
    if val.upper() == "NULL":
        return None
    if (val.startswith("'") and val.endswith("'")) or (val.startswith('"') and val.endswith('"')):
        val = val[1:-1]
        val = val.replace("\\'", "'").replace('\\"', '"').replace("\\\\", "\\")
    return val


def convert_value(val: str | None, col: str) -> object:
    """将 SQL 字符串值转换为 Python 类型"""
    if val is None:
        return None
    # ID 和整数字段
    if col in ("id", "category_id", "parent_id", "user_id", "crop_id", "monthly_sales"):
        return int(val) if val else None
    # 价格：MySQL 为 DECIMAL(10,2) 元，PostgreSQL 存储为分
    if col == "price":
        if val is None or val == "":
            return None
        try:
            return int(round(float(val) * 100))
        except (ValueError, TypeError):
            return None
    # 时间字段
    if col in ("created_at", "updated_at", "deleted_at"):
        if val is None or val == "":
            return None
        return datetime.strptime(val, "%Y-%m-%d %H:%M:%S")
    return val


async def main():
    print("=" * 50)
    print("Crop Management System 数据迁移")
    print("=" * 50)
    print(f"SQL 文件: {SQL_DUMP_PATH}")
    print(f"PostgreSQL: postgresql+asyncpg://postgres:postgres@***")

    try:
        with open(SQL_DUMP_PATH, encoding="utf-8") as f:
            sql_text = f.read()
    except FileNotFoundError:
        print(f"错误: SQL 文件未找到: {SQL_DUMP_PATH}")
        return

    # 解析 INSERT INTO 语句
    pattern = re.compile(
        r"INSERT\s+INTO\s+`(\w+)`\s*(?:\([^)]+\))?\s*VALUES\s+(.+?);",
        re.IGNORECASE | re.DOTALL,
    )

    all_data: dict[str, list[list[str | None]]] = {}
    for match in pattern.finditer(sql_text):
        mysql_table = match.group(1)
        if mysql_table not in TABLE_CONFIG:
            continue
        rows = parse_values_block(match.group(2).strip())
        all_data.setdefault(mysql_table, []).extend(rows)

    if not all_data:
        print("错误: 未解析到任何 INSERT 语句")
        return

    for mysql_table, rows in all_data.items():
        model_class = TABLE_CONFIG[mysql_table][0]
        print(f"  {mysql_table} -> {model_class.__tablename__}: {len(rows)} 条记录")

    # 连接 PostgreSQL
    engine = create_async_engine(POSTGRES_URL)
    session_factory = async_sessionmaker(bind=engine, class_=AsyncSession)
    session = session_factory()

    try:
        table_order = ["users", "crops", "agrochemical_categories", "agrochemicals", "user_crops"]

        for mysql_table in table_order:
            if mysql_table not in all_data:
                print(f"\n  {mysql_table}: 无数据，跳过")
                continue

            model_class, columns = TABLE_CONFIG[mysql_table]
            rows = all_data[mysql_table]
            print(f"\n--- 导入 {model_class.__tablename__} ---")

            count = 0
            for row in rows:
                kwargs = {}
                for i, col in enumerate(columns):
                    val = row[i] if i < len(row) else None
                    kwargs[col] = convert_value(val, col)
                session.add(model_class(**kwargs))
                count += 1
                if count % 50 == 0:
                    await session.flush()

            await session.commit()
            print(f"  写入 {count} 条记录")

        print("\n" + "=" * 50)
        print("迁移完成！")
        print("=" * 50)

    except Exception as e:
        print(f"\n迁移失败: {e}")
        await session.rollback()
        raise
    finally:
        await session.close()
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
