"""Weather forecast tool using Caiyun API."""

import logging
import os
from typing import Annotated

import requests
from langchain.tools import tool
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

CAIYUN_API_KEY = os.getenv("CAIYUN_API_KEY", "TAkhjf8d1nlSlspN")
CAIYUN_API_URL = "https://api.caiyunapp.com/v2.6"


class WeatherInput(BaseModel):
    """Weather query input model."""

    location: str = Field(
        description="地理位置，可以是城市名称或经纬度坐标（格式：'经度，纬度'，如 '116.3176,39.9760'）"
    )


def geocode_location(location: str) -> tuple[str, str] | None:
    """将城市名称转换为经纬度坐标。

    Args:
        location: 城市名称或坐标字符串

    Returns:
        (longitude, latitude) 元组，如果失败返回 None
    """
    # 如果已经是坐标格式，直接返回
    try:
        parts = location.split(",")
        if len(parts) == 2:
            lon = float(parts[0].strip())
            lat = float(parts[1].strip())
            return str(lon), str(lat)
    except (ValueError, AttributeError):
        pass

    # 使用高德地图 API 进行地理编码（需要配置 API Key）
    # 这里使用一个简单的映射表作为示例
    city_coords = {
        "北京": ("116.4074", "39.9042"),
        "上海": ("121.4737", "31.2304"),
        "广州": ("113.2644", "23.1291"),
        "深圳": ("114.0579", "22.5431"),
        "杭州": ("120.1551", "30.2741"),
        "成都": ("104.0668", "30.5728"),
        "重庆": ("106.5517", "29.5628"),
        "武汉": ("114.3054", "30.5931"),
        "西安": ("108.9398", "34.3416"),
        "南京": ("118.7969", "32.0603"),
    }

    # 尝试匹配城市名称
    for city, coords in city_coords.items():
        if city in location:
            return coords

    logger.warning(f"无法解析地理位置：{location}，请提供经纬度坐标")
    return None


@tool(name_or_callable="weather_forecast", description="查询指定地区的天气预报，包括实时天气、分钟级降水、小时级预报和天级预报。")
def weather_forecast(
    location: Annotated[str, Field(description="地理位置，城市名称或经纬度（格式：'经度，纬度'）")],
    include_alert: Annotated[bool, Field(description="是否包含天气预警信息", default=True)] = True,
) -> dict:
    """查询指定地区的天气预报。

    Args:
        location: 地理位置，可以是城市名称或经纬度坐标
        include_alert: 是否包含天气预警信息

    Returns:
        包含天气预报信息的字典，包括：
        - realtime: 实时天气数据
        - minutely: 分钟级降水数据（未来 2 小时）
        - hourly: 小时级预报（未来 24 小时）
        - daily: 天级预报（未来 15 天）
        - alert: 天气预警信息
        - forecast_keypoint: 天气预报关键点
    """
    # 解析地理位置
    coords = geocode_location(location)
    if not coords:
        return {
            "error": f"无法解析地理位置：{location}，请使用标准城市名称或提供经纬度坐标（格式：'经度，纬度'）",
            "examples": ["北京", "上海", "116.3176,39.9760"],
        }

    longitude, latitude = coords

    try:
        # 构建 API 请求
        url = f"{CAIYUN_API_URL}/{CAIYUN_API_KEY}/{longitude},{latitude}/weather"
        params = {
            "alert": str(include_alert).lower(),
            "dailysteps": 3,  # 未来 3 天
            "hourlysteps": 24,  # 未来 24 小时
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("status") != "ok":
            return {"error": f"API 返回错误：{data.get('status', 'unknown')}"}

        result = data.get("result", {})

        # 提取关键信息
        weather_info = {
            "location": {
                "coordinates": [float(longitude), float(latitude)],
                "timezone": data.get("timezone", "Asia/Shanghai"),
            },
            "forecast_keypoint": result.get("forecast_keypoint", "暂无天气预报关键点"),
            "realtime": _parse_realtime(result.get("realtime", {})),
            "minutely": _parse_minutely(result.get("minutely", {})),
            "hourly": _parse_hourly(result.get("hourly", {})),
            "daily": _parse_daily(result.get("daily", {})),
        }

        if include_alert and result.get("alert"):
            weather_info["alert"] = _parse_alert(result["alert"])

        logger.info(f"Successfully fetched weather for {location}")
        return weather_info

    except requests.exceptions.RequestException as e:
        logger.error(f"Weather API request failed: {e}")
        return {"error": f"天气查询失败：{str(e)}"}
    except Exception as e:
        logger.error(f"Weather forecast error: {e}")
        return {"error": f"天气查询出错：{str(e)}"}


def _parse_realtime(realtime: dict) -> dict:
    """解析实时天气数据。"""
    return {
        "status": realtime.get("status", ""),  # 天气状况
        "temperature": realtime.get("temperature", 0),  # 温度
        "apparent_temperature": realtime.get("apparent_temperature", 0),  # 体感温度
        "humidity": realtime.get("humidity", 0),  # 湿度
        "wind": {
            "speed": realtime.get("wind", {}).get("speed", 0),  # 风速
            "direction": realtime.get("wind", {}).get("direction", 0),  # 风向
        },
        "pressure": realtime.get("pressure", 0),  # 气压
        "visibility": realtime.get("visibility", 0),  # 能见度
        "cloudrate": realtime.get("cloudrate", 0),  # 云量
        "aqi": realtime.get("aqi", {}).get("aqi", 0) if realtime.get("aqi") else 0,  # 空气质量指数
    }


def _parse_minutely(minutely: dict) -> dict:
    """解析分钟级降水数据。"""
    return {
        "description": minutely.get("desc", ""),  # 分钟级描述
        "probability": minutely.get("probability", []),  # 降水概率
    }


def _parse_hourly(hourly: dict) -> dict:
    """解析小时级预报数据。"""
    return {
        "description": hourly.get("description", ""),  # 小时级描述
        "temperature": hourly.get("temperature", []),  # 温度列表
    }


def _parse_daily(daily: dict) -> list:
    """解析天级预报数据。"""
    daily_forecast = []
    for i, day in enumerate(daily.get("temperature", [])):
        daily_forecast.append({
            "date": i,  # 第几天
            "max_temp": day.get("max", 0),  # 最高温度
            "min_temp": day.get("min", 0),  # 最低温度
        })
    return daily_forecast


def _parse_alert(alert: dict) -> list:
    """解析天气预警信息。"""
    alerts = []
    for status in alert.get("status", []):
        alerts.append({
            "type": status.get("type", ""),  # 预警类型
            "description": status.get("desc", ""),  # 预警描述
            "level": status.get("level", ""),  # 预警等级
        })
    return alerts
