"""AQI và WHO thresholds configuration cho chatbot Hà Nội Air.

Các ngưỡng này được dùng trong SQL views và Python query service
để tính toán insights (exceedance, levels, rankings).
"""

# AQI Levels (theo thang HanoiAir)
AQI_LEVELS = {
    "Tốt": {"min": 0, "max": 50, "color": "green"},
    "Trung bình": {"min": 51, "max": 100, "color": "yellow"},
    "Kém": {"min": 101, "max": 150, "color": "orange"},
    "Xấu": {"min": 151, "max": 200, "color": "red"},
    "Rất xấu": {"min": 201, "max": 300, "color": "purple"},
    "Nguy hại": {"min": 301, "max": None, "color": "maroon"},
}

# WHO 24h Guidelines (µg/m³)
WHO_THRESHOLDS = {
    "pm25": 15.0,  # µg/m³
    "pm10": 45.0,  # µg/m³
    "o3": 100.0,   # µg/m³ (8h average)
    "no2": 25.0,   # µg/m³ (24h average)
}

# Mapping field names trong DB sang WHO thresholds
FIELD_TO_WHO_THRESHOLD = {
    "pm25": WHO_THRESHOLDS["pm25"],
    "pm10": WHO_THRESHOLDS["pm10"],
    "o3": WHO_THRESHOLDS["o3"],
    "ozone": WHO_THRESHOLDS["o3"],  # alias
    "no2": WHO_THRESHOLDS["no2"],
    "nitrogen_dioxide": WHO_THRESHOLDS["no2"],  # alias
}

# AQI ngưỡng cảnh báo (dùng cho exceedance_risk trong forecast)
AQI_WARNING_THRESHOLD = 150  # AQI > 150 = cảnh báo
AQI_DANGER_THRESHOLD = 200   # AQI > 200 = nguy hiểm


def get_aqi_level(aqi_value: float) -> str:
    """Trả về level AQI từ giá trị số.
    
    Args:
        aqi_value: Giá trị AQI (0-300+)
    
    Returns:
        Tên level: "Tốt", "Trung bình", "Kém", "Xấu", "Rất xấu", "Nguy hại"
    """
    if aqi_value <= 50:
        return "Tốt"
    elif aqi_value <= 100:
        return "Trung bình"
    elif aqi_value <= 150:
        return "Kém"
    elif aqi_value <= 200:
        return "Xấu"
    elif aqi_value <= 300:
        return "Rất xấu"
    else:
        return "Nguy hại"


def get_who_threshold(field: str) -> float:
    """Trả về WHO threshold cho field.
    
    Args:
        field: Tên field (pm25, pm10, o3, no2, ...)
    
    Returns:
        WHO threshold (µg/m³) hoặc None nếu không có
    """
    return FIELD_TO_WHO_THRESHOLD.get(field.lower())


def check_who_exceedance(field: str, value: float) -> tuple[bool, float]:
    """Kiểm tra xem giá trị có vượt ngưỡng WHO không.
    
    Args:
        field: Tên field (pm25, pm10, o3, no2)
        value: Giá trị (µg/m³)
    
    Returns:
        (exceedance_flag, exceedance_ratio)
        - exceedance_flag: True nếu vượt ngưỡng
        - exceedance_ratio: value / threshold (ví dụ 1.8 = cao hơn 1.8 lần)
    """
    threshold = get_who_threshold(field)
    if threshold is None:
        return False, None
    
    exceedance_flag = value > threshold
    exceedance_ratio = value / threshold if threshold > 0 else None
    
    return exceedance_flag, exceedance_ratio


def get_trend_label(delta_1h: float, threshold_pct: float = 5.0) -> str:
    """Xác định trend label từ delta 1h.
    
    Args:
        delta_1h: Chênh lệch so với 1h trước
        threshold_pct: Ngưỡng phần trăm để coi là "tăng"/"giảm" (default: 5%)
    
    Returns:
        "tăng", "giảm", hoặc "ổn định"
    """
    if delta_1h is None:
        return "ổn định"
    
    abs_delta_pct = abs(delta_1h)
    if abs_delta_pct < threshold_pct:
        return "ổn định"
    elif delta_1h > 0:
        return "tăng"
    else:
        return "giảm"
