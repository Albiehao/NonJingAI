from geopy.distance import distance
from pydantic import BaseModel, Field


class GeoLocation(BaseModel):
    """
    经纬度坐标
    """
    _geo_precision: int = 10000  # 内部精度阈值（米）

    latitude: float = Field(description="纬度")
    longitude: float = Field(description="经度")

    # ========== 工厂方法 ==========

    @classmethod
    def from_dict(cls, geo_context: dict[str, float]) -> "GeoLocation | None":
        """从字典创建（数据库 geo_context 字段）"""
        if geo_context is None:
            return None
        return cls(latitude=geo_context["latitude"], longitude=geo_context["longitude"])

    # ========== 验证方法 ==========

    def is_valid_coordinates(self) -> bool:
        """检查经纬度是否合法"""
        return -90 <= self.latitude <= 90 and -180 <= self.longitude <= 180

    def distance_to(self, other: "GeoLocation") -> float:
        """计算与另一个点的距离（米）"""
        return distance(
            (self.latitude, self.longitude),
            (other.latitude, other.longitude)
        ).meters

    def is_within_precision(self, other: "GeoLocation") -> bool:
        """检查与另一个点的距离是否在精度范围内"""
        return self.distance_to(other) < self._geo_precision


# 兼容旧代码的工厂函数
def get_geo_location(geo_context: dict[str, float] | None) -> GeoLocation | None:
    """从 geo_context 获取经纬度（兼容函数）"""
    return GeoLocation.from_dict(geo_context)
