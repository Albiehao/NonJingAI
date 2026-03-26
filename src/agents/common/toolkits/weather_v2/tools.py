import os
import logging
import requests
import json
from langchain_core.tools import tool

logger = logging.getLogger(__name__)


# --- 模块 1：地理位置解析（主备容灾） ---
def _get_location_coords(city: str):
    address = city.strip()
    # 主：高德
    amap_key = os.getenv("AMAP_KEY")
    if amap_key:
        try:
            url = f"https://restapi.amap.com/v3/geocode/geo?address={address}&key={amap_key}"
            res = requests.get(url, timeout=5, proxies={"http": None, "https": None})
            data = res.json()
            logger.info(f"高德 API 响应：address={address}, status={data.get('status')}, info={data.get('info')}")
            if data.get("status") == "1" and data.get("geocodes"):
                lon, lat = data["geocodes"][0]["location"].split(",")
                return lon, lat
            else:
                logger.warning(f"高德地理编码失败：{data.get('info')}")
        except Exception as e:
            logger.warning(f"高德 API 请求异常：{e}")

    # 备：OSM (免Key)
    try:
        url = f"https://nominatim.openstreetmap.org/search?q={address}&format=json&limit=1"
        res = requests.get(url, headers={'User-Agent': 'WeatherAgent'}, timeout=5,
                           proxies={"http": None, "https": None})
        data = res.json()
        if data:
            logger.info(f"OSM API 成功：address={address}")
            return data[0]["lon"], data[0]["lat"]
        else:
            logger.warning(f"OSM 地理编码无结果：{address}")
    except Exception as e:
        logger.warning(f"OSM API 请求异常：{e}")

    logger.error(f"所有地理编码源均失败：{address}")
    return None, None


# --- 模块 2：获取原始 JSON（核心逻辑） ---
def _fetch_raw_weather(lon, lat, dailysteps, hourlysteps):
    caiyun_token = os.getenv("CAIYUN_TOKEN")

    # 【主：彩云 API】
    if caiyun_token:
        try:
            # 严格按照你要求的接口格式
            url = f"https://api.caiyunapp.com/v2.6/{caiyun_token}/{lon},{lat}/weather?alert=true&dailysteps={dailysteps}&hourlysteps={hourlysteps}"
            res = requests.get(url, timeout=10, proxies={"http": None, "https": None})
            # 返回格式化的 JSON 字符串
            json_str = json.dumps(res.json(), ensure_ascii=False, indent=2)
            return json_str
        except Exception as e:
            print(f"[备援触发] 彩云请求失败: {e}")

    # 【备：Open-Meteo (如果彩云挂了或没 Token)】
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,precipitation&daily=weather_code&forecast_days={dailysteps}"
        res = requests.get(url, timeout=10)
        json_str = json.dumps(res.json(), ensure_ascii=False, indent=2)
        return json_str
    except:
        error_json = json.dumps({"error": "所有天气数据源获取失败"}, ensure_ascii=False, indent=2)
        return error_json


# --- 模块 3：工具入口 ---
@tool
def weather_forecast(city: str, dailysteps: int = 1, hourlysteps: int = 24):
    """
    获取指定城市的天气预报原始数据（JSON 格式）。
    包含预警、天级和小时级数据。

    此工具返回纯 JSON 字符串。调用后请将 JSON 数据直接返回给用户，不要添加任何描述、总结或解释。
    用户希望看到原始的 JSON 数据，而不是对天气的解读。
    """
    lon, lat = _get_location_coords(city)
    if not lon:
        return f"无法定位城市: {city}"

    # 直接返回那一大坨原始数据
    return _fetch_raw_weather(lon, lat, dailysteps, hourlysteps)


def get_weather_forecast():
    return weather_forecast