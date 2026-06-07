"""Agrochemicals (农资) query tool for crop management system."""

import asyncio
import logging
import os
from typing import Annotated

import httpx
from langchain.tools import tool
from pydantic import Field

logger = logging.getLogger(__name__)

CROP_BACKEND_URL = os.getenv("QIANXUN_SERVER_URL", "http://qianxun-server:8080")


async def _fetch(endpoint: str, params: dict | None = None) -> dict:
    url = f"{CROP_BACKEND_URL}{endpoint}"
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        logger.error(f"API request failed: {e}")
        return {"error": f"查询失败：{str(e)}"}
    except Exception as e:
        logger.error(f"Query error: {e}")
        return {"error": f"查询出错：{str(e)}"}


@tool(
    name_or_callable="get_agrochemical_by_name",
    description="根据产品名称查询农资（农药、化肥等）的详细信息，包括品牌、价格、剂型、使用方法、注意事项等。输入产品名称即可。",
)
def get_agrochemical_by_name(
    product_name: Annotated[str, Field(description="农资产品名称，如'草甘膦'、'吡虫啉'")],
) -> dict:
    result = asyncio.run(_fetch("/agrochemicals/search", params={"keyword": product_name}))
    data = result.get("data", [])
    if not data:
        return {"error": f"未找到 '{product_name}'"}

    item = data[0]
    price = item.get("price")
    if price is not None:
        price = f"{(int(price) / 100):.2f}"

    return {
        "id": item.get("id"),
        "product_name": item.get("productName"),
        "brand": item.get("brand"),
        "price": price,
        "main_image": item.get("mainImage"),
        "purchase_links": item.get("purchaseLinks"),
        "registration_no": item.get("registrationNo"),
        "formulation": item.get("formulation"),
        "content_spec": item.get("contentSpec"),
        "description": item.get("description"),
        "use_crops": item.get("useCrops"),
        "usage_method": item.get("usageMethod"),
        "precautions": item.get("precautions"),
    }
