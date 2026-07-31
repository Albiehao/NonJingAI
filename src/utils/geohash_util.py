"""Geohash encoding utility for proximity queries."""

BASE32 = "0123456789bcdefghjkmnpqrstuvwxyz"

# 各级精度的近似覆盖半径 (km)
PRECISION_RADIUS = {
    1: 2500,
    2: 630,
    3: 78,
    4: 20,
    5: 2.4,
    6: 0.61,
    7: 0.076,
    8: 0.019,
}


def encode(latitude: float, longitude: float, precision: int = 6) -> str:
    """Encode latitude/longitude to a geohash string.

    Args:
        latitude: Latitude in degrees (-90 to 90)
        longitude: Longitude in degrees (-180 to 180)
        precision: Length of the geohash (1-12)

    Returns:
        Geohash string
    """
    lat_interval = [-90.0, 90.0]
    lon_interval = [-180.0, 180.0]
    bits = 0
    hash_chars = []

    while len(hash_chars) < precision:
        for _ in range(5):
            if bits % 2 == 0:
                mid = (lon_interval[0] + lon_interval[1]) / 2
                if longitude > mid:
                    hash_chars.append("1")
                    lon_interval[0] = mid
                else:
                    hash_chars.append("0")
                    lon_interval[1] = mid
            else:
                mid = (lat_interval[0] + lat_interval[1]) / 2
                if latitude > mid:
                    hash_chars.append("1")
                    lat_interval[0] = mid
                else:
                    hash_chars.append("0")
                    lat_interval[1] = mid
            bits += 1

        # Convert 5 bits to base32 char
        char_bits = hash_chars[-5:]
        idx = int("".join(char_bits), 2)
        hash_chars = hash_chars[:-5]
        hash_chars.append(BASE32[idx])

    return "".join(hash_chars)


def encode_precisions(latitude: float, longitude: float) -> tuple[str, str]:
    """Encode lat/lng to geohashes at 10km and 20km precision.

    Returns:
        (geohash_10km, geohash_20km)
    """
    # Precision 4 ≈ ±20km (10km range), Precision 3 ≈ ±78km (20km range)
    return encode(latitude, longitude, 4), encode(latitude, longitude, 3)


def encode_levels(latitude: float, longitude: float, max_precision: int = 8) -> dict[int, str]:
    """Encode lat/lng to all geohash prefix levels from 1 to max_precision.

    一次计算得到所有级别的前缀，用于多级检索:
      level 1: ±2500km, level 2: ±630km, ..., level 8: ±19m

    Returns:
        {precision: geohash_prefix, ...}
    """
    full = encode(latitude, longitude, max_precision)
    return {i: full[:i] for i in range(1, max_precision + 1)}


def precision_for_radius(radius_km: float) -> int:
    """根据搜索半径(km)返回最合适的 geohash 精度级别。"""
    for level in range(1, max(PRECISION_RADIUS) + 1):
        if PRECISION_RADIUS[level] <= radius_km:
            return level
    return max(PRECISION_RADIUS)
