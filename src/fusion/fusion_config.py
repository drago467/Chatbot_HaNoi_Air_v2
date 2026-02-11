"""Data fusion configuration: priority rules per field category."""

# Priority order: first source has highest priority
FIELD_PRIORITY = {
    "meteorology": {
        "temperature": ["openweather_onecall", "openmeteo_weather"],
        "feels_like_temperature": ["openweather_onecall", "openmeteo_weather"],
        "relative_humidity": ["openweather_onecall", "openmeteo_weather"],
        "pressure": ["openweather_onecall", "openmeteo_weather"],
        "wind_speed": ["openweather_onecall", "openmeteo_weather"],
        "wind_direction": ["openweather_onecall", "openmeteo_weather"],
        "wind_gust": ["openweather_onecall", "openmeteo_weather"],
        "cloud_cover": ["openweather_onecall", "openmeteo_weather"],
        "precipitation": ["openweather_onecall", "openmeteo_weather"],
        "precipitation_probability": ["openweather_onecall", "openmeteo_weather"],
        "dew_point": ["openweather_onecall", "openmeteo_weather"],
        "uv_index": ["openweather_onecall", "openmeteo_weather"],
        "visibility": ["openweather_onecall", "openmeteo_weather"],
        # Open-Meteo specific fields
        "shortwave_radiation": ["openmeteo_weather"],
        "boundary_layer_height": ["openmeteo_weather"],
    },
    "pollutants": {
        "pm25": ["openweather_air", "openmeteo_air"],
        "pm10": ["openweather_air", "openmeteo_air"],
        "no2": ["openweather_air", "openmeteo_air"],
        "so2": ["openweather_air", "openmeteo_air"],
        "o3": ["openweather_air", "openmeteo_air"],
        "co": ["openweather_air", "openmeteo_air"],
        "nh3": ["openweather_air"],  # Only OpenWeather has NH3
        "no": ["openweather_air"],  # Only OpenWeather has NO
        "aqi": ["openweather_air", "openmeteo_air"],
        "aqi_european": ["openmeteo_air"],
    },
    "aqi_ward": {
        "pm25": ["hanoiair"],
        "aqi": ["hanoiair"],
    }
}

# Freshness window in minutes (for observations)
# If step is 1 hour, 30 minutes window is reasonable
FRESHNESS_WINDOW_MINUTES = {
    "meteorology": 30,
    "pollutants": 30,
    "aqi_ward": 30,
}

# Default freshness window
DEFAULT_FRESHNESS_WINDOW_MINUTES = 30


def get_field_category(field: str) -> str:
    """Determine field category for a given field."""
    if field in FIELD_PRIORITY["aqi_ward"]:
        return "aqi_ward"
    elif field in FIELD_PRIORITY["pollutants"]:
        return "pollutants"
    else:
        return "meteorology"


def get_field_priority(field: str) -> list:
    """Get priority list of sources for a field."""
    category = get_field_category(field)
    return FIELD_PRIORITY[category].get(field, [])


def get_freshness_window(field: str) -> int:
    """Get freshness window in minutes for a field."""
    category = get_field_category(field)
    return FRESHNESS_WINDOW_MINUTES.get(
        category, DEFAULT_FRESHNESS_WINDOW_MINUTES
    )
