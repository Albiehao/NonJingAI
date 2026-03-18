import requests
import json
import urllib3
from langchain_core.tools import tool

# 1. 禁用 HTTPS 安全警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# --- 内部函数：高德地图解析经纬度 ---
def _get_location_coords(city: str):
    # 【⚠️ 必须填入】高德 Web服务 Key
    amap_key = "35254691247fc50970da73d25156931b"

    # 对城市名进行简单的清洗，防止空格导致请求失败
    address = city.strip()
    url = f"https://restapi.amap.com/v3/geocode/geo?address={address}&key={amap_key}"

    try:
        # 强制不走代理，确保直连
        res = requests.get(url, timeout=10, verify=False, proxies={"http": None, "https": None})
        data = res.json()

        if data.get("status") == "1" and data.get("geocodes"):
            # 高德返回格式: "118.7968,32.0602" (经度,纬度)
            location = data["geocodes"][0]["location"]
            print(f"[DEBUG] 高德解析成功: {city} -> {location}")
            return location
        else:
            print(f"[DEBUG] 高德解析失败，返回数据: {data}")
            return None
    except Exception as e:
        print(f"[ERROR] 高德接口请求崩溃: {str(e)}")
        return None


# --- 内部函数：调用彩云天气 API ---
def _get_caiyun_data(location: str):
    # 【⚠️ 必须填入】彩云天气 API Token
    # 注意：请确保是在彩云开发者后台复制的 Token，不是 Secret Key
    caiyun_token = "MnKHbJOuJvAkgXR5"

    # 彩云 V2.6 标准接口：token/经度,纬度/weather.json
    url = f"https://api.caiyunapp.com/v2.6/{caiyun_token}/{location}/weather.json"

    try:
        print(f"[DEBUG] 正在请求彩云 API: {url}")
        res = requests.get(url, timeout=15, verify=False, proxies={"http": None, "https": None})
        data = res.json()

        # 如果失败，彩云通常会返回 {"status": "failed", "error": "..."}
        if data.get("status") == "ok":
            result = data.get("result", {})
            realtime = result.get("realtime", {})

            # 提取核心数据
            temp = realtime.get("temperature", "未知")
            skycon = realtime.get("skycon", "未知")
            # 降水预报描述
            minutely_desc = result.get("minutely", {}).get("description", "暂无分钟级预报")

            # 将彩云的天气代码转成中文（简单映射）
            sky_map = {
                "CLEAR_DAY": "晴", "CLEAR_NIGHT": "晴", "PARTLY_CLOUDY_DAY": "多云",
                "PARTLY_CLOUDY_NIGHT": "多云", "CLOUDY": "阴", "LIGHT_HAZE": "轻度雾霾",
                "MODERATE_HAZE": "中度雾霾", "HEAVY_HAZE": "重度雾霾", "LIGHT_RAIN": "小雨",
                "MODERATE_RAIN": "中雨", "HEAVY_RAIN": "大雨", "STORM_RAIN": "暴雨",
                "FOG": "雾", "LIGHT_SNOW": "小雪", "MODERATE_SNOW": "中雪",
                "HEAVY_SNOW": "大雪", "STORM_SNOW": "暴雪", "DUST": "浮尘", "SAND": "沙尘"
            }
            weather_zh = sky_map.get(skycon, skycon)

            return f"实时温度 {temp}℃，天气情况：{weather_zh}。预报详情：{minutely_desc}"
        else:
            # 这里的打印非常重要，它会告诉你为什么 failed
            error_info = data.get("error", "未知错误原因")
            print(f"[ERROR] 彩云返回失败: {data}")
            return f"彩云接口返回失败，状态：{data.get('status')}，原因：{error_info}"

    except Exception as e:
        print(f"[ERROR] 彩云接口请求崩溃: {str(e)}")
        return f"连接彩云天气服务时发生错误: {str(e)}"


# --- 🌟 系统核心工具入口 🌟 ---
@tool
def weather_forecast(city: str):
    """
    查询指定城市的天气预报。
    参数 city: 城市名称，如 '南京'、'北京市'。
    """
    print(f"\n>>> 收到天气查询指令，城市: {city}")

    # 1. 地址转经纬度
    location = _get_location_coords(city)
    if not location:
        return f"无法定位城市【{city}】，请确认名称是否正确。"

    # 2. 经纬度转天气
    weather_result = _get_caiyun_data(location)

    return f"【{city} 天气实时播报】\n{weather_result}"


# --- 解决系统的启动导入问题 ---
def get_weather_forecast():
    """初始化函数，供注册表调用"""
    return weather_forecast