# Open-Meteo Weather API Documentation

## Tổng quan

Open-Meteo Weather API là một dịch vụ miễn phí, không yêu cầu API key, cung cấp dữ liệu thời tiết toàn cầu với độ phân giải cao. API này sử dụng các mô hình dự báo thời tiết từ nhiều nguồn như ECMWF, GFS, và các mô hình khác.

**Website:** https://open-meteo.com/en/docs

**Base URL:** `https://api.open-meteo.com/v1/forecast`

**Cost:** Miễn phí, không cần API key

**Coverage:** Toàn cầu

**Resolution:** 11km (có thể cao hơn tùy location)

---

## API Endpoint

### GET `/v1/forecast`

Lấy dữ liệu dự báo thời tiết theo tọa độ địa lý.

#### Parameters

**Required:**
- `latitude` (float, required) - Vĩ độ (-90 đến 90)
- `longitude` (float, required) - Kinh độ (-180 đến 180)

**Optional:**
- `hourly` (array of strings, optional) - Danh sách các biến hourly cần lấy
- `daily` (array of strings, optional) - Danh sách các biến daily cần lấy
- `timezone` (string, optional) - Múi giờ (ví dụ: "Asia/Ho_Chi_Minh", "UTC")
- `forecast_days` (integer, optional) - Số ngày dự báo (mặc định: 7 ngày, tối đa 16 ngày)
- `past_days` (integer, optional) - Số ngày quá khứ (0-92)
- `start_date` (string, optional) - Ngày bắt đầu (YYYY-MM-DD) cho historical data
- `end_date` (string, optional) - Ngày kết thúc (YYYY-MM-DD) cho historical data
- `models` (array of strings, optional) - Chọn weather model cụ thể (auto, ecmwf_ifs04, gfs, gem, jma_seam, meteofrance_arpege, etc.)

#### Example Request

```python
import requests

url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 21.0285,  # Hà Nội
    "longitude": 105.8542,
    "hourly": ["temperature_2m", "relative_humidity_2m", "precipitation", "wind_speed_10m"],
    "timezone": "Asia/Ho_Chi_Minh"
}

response = requests.get(url, params=params)
data = response.json()
```

---

## Variables Available

### Temperature Variables

| Variable Name           | Description                       | Unit | Notes                  |
| ----------------------- | --------------------------------- | ---- | ---------------------- |
| `temperature_2m`        | Temperature at 2m height          | °C   | ✅ Verified for Vietnam |
| `temperature_80m`       | Temperature at 80m height         | °C   | ✅ Verified for Vietnam |
| `temperature_120m`      | Temperature at 120m height        | °C   | ✅ Verified for Vietnam |
| `dewpoint_2m`           | Dewpoint temperature at 2m        | °C   | ✅ Verified for Vietnam |
| `apparent_temperature`  | Apparent temperature (feels like) | °C   | ✅ Verified for Vietnam |
| `soil_temperature_0cm`  | Soil temperature at 0cm depth     | °C   | ✅ Verified for Vietnam |
| `soil_temperature_6cm`  | Soil temperature at 6cm depth     | °C   | ✅ Verified for Vietnam |
| `soil_temperature_18cm` | Soil temperature at 18cm depth    | °C   | ✅ Verified for Vietnam |
| `soil_temperature_54cm` | Soil temperature at 54cm depth    | °C   | ✅ Verified for Vietnam |

### Humidity Variables

| Variable Name             | Description               | Unit | Notes                  |
| ------------------------- | ------------------------- | ---- | ---------------------- |
| `relative_humidity_2m`    | Relative humidity at 2m   | %    | ✅ Verified for Vietnam |
| `relative_humidity_80m`   | Relative humidity at 80m  | %    | ⚠️ Null for Vietnam     |
| `relative_humidity_120m`  | Relative humidity at 120m | %    | ⚠️ Null for Vietnam     |
| `vapour_pressure_deficit` | Vapour pressure deficit   | kPa  | ✅ Verified for Vietnam |

### Precipitation Variables

| Variable Name               | Description               | Unit | Notes                  |
| --------------------------- | ------------------------- | ---- | ---------------------- |
| `precipitation`             | Total precipitation       | mm   | ✅ Verified for Vietnam |
| `rain`                      | Rain precipitation        | mm   | ✅ Verified for Vietnam |
| `showers`                   | Showers precipitation     | mm   | ✅ Verified for Vietnam |
| `snowfall`                  | Snowfall                  | cm   | ✅ Verified for Vietnam |
| `snow_depth`                | Snow depth                | cm   | ✅ Verified for Vietnam |
| `precipitation_probability` | Precipitation probability | %    | ✅ Verified for Vietnam |

### Wind Variables

| Variable Name         | Description               | Unit      | Notes                  |
| --------------------- | ------------------------- | --------- | ---------------------- |
| `wind_speed_10m`      | Wind speed at 10m height  | m/s       | ✅ Verified for Vietnam |
| `wind_speed_80m`      | Wind speed at 80m height  | m/s       | ✅ Verified for Vietnam |
| `wind_speed_120m`     | Wind speed at 120m height | m/s       | ✅ Verified for Vietnam |
| `wind_direction_10m`  | Wind direction at 10m     | ° (0-360) | ✅ Verified for Vietnam |
| `wind_direction_80m`  | Wind direction at 80m     | ° (0-360) | ✅ Verified for Vietnam |
| `wind_direction_120m` | Wind direction at 120m    | ° (0-360) | ✅ Verified for Vietnam |
| `wind_gusts_10m`      | Wind gusts at 10m         | m/s       | ✅ Verified for Vietnam |

### Pressure Variables

| Variable Name      | Description             | Unit | Notes                  |
| ------------------ | ----------------------- | ---- | ---------------------- |
| `pressure_msl`     | Mean sea level pressure | hPa  | ✅ Verified for Vietnam |
| `surface_pressure` | Surface pressure        | hPa  | ✅ Verified for Vietnam |

### Cloud & Visibility Variables

| Variable Name      | Description       | Unit | Notes                  |
| ------------------ | ----------------- | ---- | ---------------------- |
| `cloud_cover`      | Total cloud cover | %    | ✅ Verified for Vietnam |
| `cloud_cover_low`  | Low cloud cover   | %    | ✅ Verified for Vietnam |
| `cloud_cover_mid`  | Mid cloud cover   | %    | ✅ Verified for Vietnam |
| `cloud_cover_high` | High cloud cover  | %    | ✅ Verified for Vietnam |
| `visibility`       | Visibility        | m    | ✅ Verified for Vietnam |

### Radiation Variables

| Variable Name              | Description               | Unit | Notes                  |
| -------------------------- | ------------------------- | ---- | ---------------------- |
| `shortwave_radiation`      | Shortwave solar radiation | W/m² | ✅ Verified for Vietnam |
| `direct_radiation`         | Direct solar radiation    | W/m² | ✅ Verified for Vietnam |
| `diffuse_radiation`        | Diffuse solar radiation   | W/m² | ✅ Verified for Vietnam |
| `direct_normal_irradiance` | Direct normal irradiance  | W/m² | ✅ Verified for Vietnam |
| `global_tilted_irradiance` | Global tilted irradiance  | W/m² | ✅ Verified for Vietnam |
| `terrestrial_radiation`    | Terrestrial radiation     | W/m² | ✅ Verified for Vietnam |

### Atmospheric Variables

| Variable Name                | Description                           | Unit    | Notes                  |
| ---------------------------- | ------------------------------------- | ------- | ---------------------- |
| `cape`                       | Convective Available Potential Energy | J/kg    | ✅ Verified for Vietnam |
| `lifted_index`               | Lifted Index                          | K       | ✅ Verified for Vietnam |
| `freezing_level_height`      | Freezing level height                 | m       | ✅ Verified for Vietnam |
| `boundary_layer_height`      | Planetary boundary layer height       | m       | ✅ Verified for Vietnam |
| `is_day`                     | Day/Night indicator                   | 0/1     | ✅ Verified for Vietnam |
| `sunshine_duration`          | Sunshine duration                     | seconds | ✅ Verified for Vietnam |
| `et0_fao_evapotranspiration` | ET₀ FAO evapotranspiration            | mm      | ✅ Verified for Vietnam |

### Soil Variables

| Variable Name           | Description           | Unit  | Notes                  |
| ----------------------- | --------------------- | ----- | ---------------------- |
| `soil_moisture_0_1cm`   | Soil moisture 0-1cm   | m³/m³ | ✅ Verified for Vietnam |
| `soil_moisture_1_3cm`   | Soil moisture 1-3cm   | m³/m³ | ✅ Verified for Vietnam |
| `soil_moisture_3_9cm`   | Soil moisture 3-9cm   | m³/m³ | ✅ Verified for Vietnam |
| `soil_moisture_9_27cm`  | Soil moisture 9-27cm  | m³/m³ | ✅ Verified for Vietnam |
| `soil_moisture_27_81cm` | Soil moisture 27-81cm | m³/m³ | ✅ Verified for Vietnam |

**Note:** Tất cả các biến trên đã được test và verify có dữ liệu trả về cho Hà Nội, Việt Nam (49/51 biến có dữ liệu).

---

## Response Format

### Response Structure

```json
{
  "latitude": 21.0,
  "longitude": 105.899994,
  "generationtime_ms": 8.5,
  "utc_offset_seconds": 25200,
  "timezone": "Asia/Ho_Chi_Minh",
  "timezone_abbreviation": "+07",
  "elevation": 19.0,
  "hourly_units": {
    "time": "iso8601",
    "temperature_2m": "°C",
    "relative_humidity_2m": "%",
    "precipitation": "mm",
    ...
  },
  "hourly": {
    "time": [
      "2026-02-08T00:00",
      "2026-02-08T01:00",
      ...
    ],
    "temperature_2m": [19.2, 18.5, ...],
    "relative_humidity_2m": [85, 87, ...],
    ...
  }
}
```

### Response Fields

- `latitude` (float) - Vĩ độ của location được query
- `longitude` (float) - Kinh độ của location được query
- `elevation` (float) - Độ cao so với mực nước biển (meters)
- `timezone` (string) - Múi giờ được sử dụng
- `utc_offset_seconds` (integer) - Offset UTC tính bằng giây
- `generationtime_ms` (float) - Thời gian xử lý request (milliseconds)
- `hourly_units` (object) - Đơn vị của từng biến trong hourly data
- `hourly` (object) - Dữ liệu theo giờ với các keys:
  - `time` (array of strings) - Timestamps theo ISO 8601 format
  - `{variable_name}` (array of floats) - Giá trị của từng biến theo thời gian

### Data Availability

- **Forecast:** Mặc định 7 ngày (168 giờ) dự báo, tối đa 16 ngày
- **Historical:** Có thể lấy dữ liệu quá khứ (tối đa 92 ngày)
- **Update Frequency:** Dữ liệu được cập nhật hàng giờ

---

## Code Examples

### Example 1: Sử dụng `openmeteo_requests` Library

```python
import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# Tọa độ Hà Nội, Việt Nam
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 21.0285,
    "longitude": 105.8542,
    "hourly": [
        "temperature_2m",
        "relative_humidity_2m",
        "precipitation",
        "wind_speed_10m",
        "wind_direction_10m",
        "pressure_msl",
        "cloud_cover"
    ],
    "timezone": "Asia/Ho_Chi_Minh"
}

responses = openmeteo.weather_api(url, params=params)

# Process first location
response = responses[0]
print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation: {response.Elevation()} m asl")
print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

# Process hourly data. The order of variables needs to be the same as requested.
hourly = response.Hourly()
hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
hourly_precipitation = hourly.Variables(2).ValuesAsNumpy()
hourly_wind_speed_10m = hourly.Variables(3).ValuesAsNumpy()
hourly_wind_direction_10m = hourly.Variables(4).ValuesAsNumpy()
hourly_pressure_msl = hourly.Variables(5).ValuesAsNumpy()
hourly_cloud_cover = hourly.Variables(6).ValuesAsNumpy()

# Create DataFrame
hourly_data = {
    "date": pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
        end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left"
    )
}

hourly_data["temperature_2m"] = hourly_temperature_2m
hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
hourly_data["precipitation"] = hourly_precipitation
hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
hourly_data["wind_direction_10m"] = hourly_wind_direction_10m
hourly_data["pressure_msl"] = hourly_pressure_msl
hourly_data["cloud_cover"] = hourly_cloud_cover

hourly_dataframe = pd.DataFrame(data=hourly_data)
print("\nHourly data:\n", hourly_dataframe)
```

### Example 2: Sử dụng `requests` Library (Đơn giản)

```python
import requests
import pandas as pd
from datetime import datetime

# Tọa độ Hà Nội
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 21.0285,
    "longitude": 105.8542,
    "hourly": [
        "temperature_2m",
        "relative_humidity_2m",
        "precipitation",
        "wind_speed_10m",
        "wind_direction_10m",
        "pressure_msl",
        "cloud_cover",
        "shortwave_radiation",
        "boundary_layer_height",
        "is_day"
    ],
    "timezone": "Asia/Ho_Chi_Minh"
}

response = requests.get(url, params=params, timeout=30)
response.raise_for_status()
data = response.json()

# Extract hourly data
hourly = data["hourly"]
times = hourly["time"]

# Create DataFrame
df = pd.DataFrame({
    "time": pd.to_datetime(times),
    "temperature_2m": hourly.get("temperature_2m", []),
    "relative_humidity_2m": hourly.get("relative_humidity_2m", []),
    "precipitation": hourly.get("precipitation", []),
    "wind_speed_10m": hourly.get("wind_speed_10m", []),
    "wind_direction_10m": hourly.get("wind_direction_10m", []),
    "pressure_msl": hourly.get("pressure_msl", []),
    "cloud_cover": hourly.get("cloud_cover", []),
    "shortwave_radiation": hourly.get("shortwave_radiation", []),
    "boundary_layer_height": hourly.get("boundary_layer_height", []),
    "is_day": hourly.get("is_day", [])
})

print(f"\nLocation: {data['latitude']}°N, {data['longitude']}°E")
print(f"Elevation: {data['elevation']} m")
print(f"Timezone: {data['timezone']}")
print(f"\nData shape: {df.shape}")
print(f"\nFirst few rows:\n{df.head()}")
```

### Example 3: Request nhiều biến cùng lúc

```python
import requests
import pandas as pd

# Tọa độ Hà Nội
url = "https://api.open-meteo.com/v1/forecast"

# Nhiều biến weather
weather_variables = [
    "temperature_2m",
    "relative_humidity_2m",
    "dewpoint_2m",
    "apparent_temperature",
    "precipitation",
    "rain",
    "showers",
    "snowfall",
    "precipitation_probability",
    "wind_speed_10m",
    "wind_direction_10m",
    "wind_gusts_10m",
    "pressure_msl",
    "surface_pressure",
    "cloud_cover",
    "cloud_cover_low",
    "cloud_cover_mid",
    "cloud_cover_high",
    "visibility",
    "shortwave_radiation",
    "direct_radiation",
    "diffuse_radiation",
    "is_day",
    "sunshine_duration",
    "cape",
    "lifted_index",
    "boundary_layer_height"
]

params = {
    "latitude": 21.0285,
    "longitude": 105.8542,
    "hourly": weather_variables,
    "timezone": "Asia/Ho_Chi_Minh",
    "forecast_days": 7
}

response = requests.get(url, params=params, timeout=30)
response.raise_for_status()
data = response.json()

# Extract và xử lý data
hourly = data["hourly"]
df = pd.DataFrame(hourly)
df["time"] = pd.to_datetime(df["time"])

print(f"Retrieved {len(df)} hourly records")
print(f"Variables: {list(df.columns)}")
print(f"\nData availability:")
for col in df.columns:
    if col != "time":
        non_null = df[col].notna().sum()
        print(f"  {col}: {non_null}/{len(df)} ({non_null/len(df)*100:.1f}%)")
```

### Example 4: Lấy dữ liệu quá khứ (Historical Data)

```python
import requests
import pandas as pd
from datetime import datetime, timedelta

url = "https://api.open-meteo.com/v1/forecast"

# Lấy dữ liệu 7 ngày qua
end_date = datetime.now()
start_date = end_date - timedelta(days=7)

params = {
    "latitude": 21.0285,
    "longitude": 105.8542,
    "hourly": [
        "temperature_2m",
        "relative_humidity_2m",
        "precipitation",
        "wind_speed_10m"
    ],
    "start_date": start_date.strftime("%Y-%m-%d"),
    "end_date": end_date.strftime("%Y-%m-%d"),
    "timezone": "Asia/Ho_Chi_Minh"
}

response = requests.get(url, params=params, timeout=30)
response.raise_for_status()
data = response.json()

hourly = data["hourly"]
df = pd.DataFrame({
    "time": pd.to_datetime(hourly["time"]),
    "temperature_2m": hourly["temperature_2m"],
    "relative_humidity_2m": hourly["relative_humidity_2m"],
    "precipitation": hourly["precipitation"],
    "wind_speed_10m": hourly["wind_speed_10m"]
})

print(f"Historical data from {start_date.date()} to {end_date.date()}")
print(f"\n{df.head(10)}")
```

### Example 5: Daily Aggregates

```python
import requests
import pandas as pd

url = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": 21.0285,
    "longitude": 105.8542,
    "daily": [
        "temperature_2m_max",
        "temperature_2m_min",
        "precipitation_sum",
        "wind_speed_10m_max",
        "wind_gusts_10m_max",
        "sunshine_duration"
    ],
    "timezone": "Asia/Ho_Chi_Minh",
    "forecast_days": 7
}

response = requests.get(url, params=params, timeout=30)
response.raise_for_status()
data = response.json()

# Extract daily data
daily = data["daily"]
df = pd.DataFrame({
    "date": pd.to_datetime(daily["time"]),
    "temperature_max": daily["temperature_2m_max"],
    "temperature_min": daily["temperature_2m_min"],
    "precipitation": daily["precipitation_sum"],
    "wind_speed_max": daily["wind_speed_10m_max"],
    "wind_gusts_max": daily["wind_gusts_10m_max"],
    "sunshine_duration": daily["sunshine_duration"]
})

print(f"\nDaily forecast:\n{df}")
```

---

## Tọa độ các thành phố Việt Nam

| Thành phố       | Latitude | Longitude | Timezone         |
| --------------- | -------- | --------- | ---------------- |
| Hà Nội          | 21.0285  | 105.8542  | Asia/Ho_Chi_Minh |
| TP. Hồ Chí Minh | 10.7769  | 106.7009  | Asia/Ho_Chi_Minh |
| Đà Nẵng         | 16.0544  | 108.2022  | Asia/Ho_Chi_Minh |
| Hải Phòng       | 20.8449  | 106.6881  | Asia/Ho_Chi_Minh |
| Cần Thơ         | 10.0452  | 105.7469  | Asia/Ho_Chi_Minh |

---

## Data Quality & Verification

### Test Results cho Hà Nội (2026-02-08)

**Test Location:** 21.0285°N, 105.8542°E (Hà Nội)

**Test Results:**
- ✅ **Status Code:** 200 OK
- ✅ **Data Availability:** 168/168 timestamps có dữ liệu (100%)
- ✅ **Forecast Period:** 7 ngày (168 giờ)
- ✅ **Variables Available:** 49/51 biến có dữ liệu (96.1%)

**Sample Data Ranges (Hà Nội):**
- Temperature 2m: 12.70 - 26.80°C (Avg: 19.21°C)
- Relative Humidity 2m: 61.00 - 98.00% (Avg: 84.05%)
- Precipitation: 0.00 - 1.90 mm (Avg: 0.03 mm)
- Wind Speed 10m: 0.00 - 17.10 m/s (Avg: 7.62 m/s)
- Wind Direction 10m: 11.00 - 360.00° (Avg: 162.21°)
- Pressure MSL: 1012.90 - 1025.20 hPa (Avg: 1018.45 hPa)
- Cloud Cover: 32.00 - 100.00% (Avg: 85.99%)
- Shortwave Radiation: 0.00 - 683.00 W/m² (Avg: 95.86 W/m²)
- Boundary Layer Height: 35.00 - 1660.00 m (Avg: 482.86 m)

**Variables với null values:**
- `relative_humidity_80m`: All null (có thể không available cho location này)
- `relative_humidity_120m`: All null (có thể không available cho location này)

---

## Rate Limits & Best Practices

### Rate Limits

- **No official rate limits** - API miễn phí, không có rate limit chính thức
- **Recommended:** Sử dụng hợp lý, không spam requests
- **Caching:** Nên cache responses để giảm số lượng requests

### Best Practices

1. **Use Caching:** Cache responses với TTL phù hợp (ví dụ: 1 giờ cho forecast data)
2. **Retry Logic:** Implement retry với exponential backoff cho failed requests
3. **Error Handling:** Xử lý các trường hợp:
   - Network errors
   - Timeout errors
   - Invalid coordinates
   - Missing data (null values)
4. **Request Optimization:** Chỉ request các biến cần thiết để giảm response size
5. **Timezone:** Luôn specify timezone để có dữ liệu theo giờ địa phương
6. **Forecast Days:** Chỉ request số ngày cần thiết (mặc định 7 ngày, tối đa 16 ngày)

### Example với Error Handling

```python
import requests
from time import sleep

def get_weather_forecast(lat, lon, variables, max_retries=3):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": variables,
        "timezone": "Asia/Ho_Chi_Minh"
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            print(f"Timeout on attempt {attempt + 1}")
            if attempt < max_retries - 1:
                sleep(2 ** attempt)  # Exponential backoff
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            if attempt < max_retries - 1:
                sleep(2 ** attempt)
    
    return None

# Usage
data = get_weather_forecast(21.0285, 105.8542, ["temperature_2m", "precipitation"])
if data:
    print("Success!")
else:
    print("Failed after retries")
```

---

## Limitations

1. **Resolution:** Độ phân giải 11km - có thể không capture micro-scale weather patterns
2. **Model-based:** Dữ liệu từ mô hình dự báo, không phải measurements thực tế
3. **Accuracy:** Có thể có sai số so với measurements thực tế, đặc biệt ở complex terrain
4. **Coverage:** Một số biến có thể không available cho một số locations
5. **Update Frequency:** Dữ liệu được cập nhật hàng giờ, không real-time
6. **Forecast Accuracy:** Accuracy giảm dần theo thời gian (ngày 1-3 tốt hơn ngày 7-16)

---

## Comparison với các nguồn khác

### So sánh với OpenWeatherMap API

| Feature        | Open-Meteo Weather API | OpenWeatherMap API |
| -------------- | ---------------------- | ------------------ |
| **Coverage**   | Toàn cầu               | Toàn cầu           |
| **Variables**  | 49+ biến weather       | ~20 biến chính     |
| **Resolution** | 11km                   | Point-based        |
| **Data Type**  | Model-based forecast   | Model + stations   |
| **Cost**       | Miễn phí               | Free tier limited  |
| **API Key**    | Không cần              | Cần API key        |
| **Historical** | Có (tối đa 92 ngày)    | Limited            |
| **Soil Data**  | Có                     | Không có           |
| **Radiation**  | Chi tiết (6 biến)      | Limited            |

### Khi nào sử dụng Open-Meteo Weather API?

✅ **Nên dùng khi:**
- Cần nhiều biến weather chi tiết (soil, radiation, atmospheric)
- Cần dữ liệu miễn phí không giới hạn
- Cần historical data
- Cần soil temperature/moisture data
- Cần detailed radiation data
- Không muốn quản lý API key

❌ **Không nên dùng khi:**
- Cần measurements thực tế từ weather stations
- Cần real-time data (không phải forecast)
- Cần độ chính xác cao cho specific location
- Cần data từ weather stations cụ thể

---

## Integration với Codebase

### Hiện tại đã có OpenMeteoCollector

Codebase đã có `OpenMeteoCollector` tại:
- `backend/app/services/data/collectors/open_meteo_collector.py`

Collector này hiện tại focus vào:
- Radiation variables (shortwave_radiation, direct_normal_irradiance, diffuse_radiation)
- Boundary layer height (PBLH)
- Temperature 2m
- is_day, sunshine_duration

Có thể mở rộng collector này để thêm các biến weather khác nếu cần.

---

## References

- **Official Documentation:** https://open-meteo.com/en/docs
- **API Explorer:** https://open-meteo.com/en/docs (có thể test trực tiếp)
- **GitHub:** https://github.com/open-meteo/open-meteo
- **Weather Models:** https://open-meteo.com/en/docs/weather-api#weather_models

---

## Changelog

- **2026-02-08:** Initial documentation
  - Tested với tọa độ Hà Nội
  - Verified 49/51 biến có dữ liệu
  - Added code examples cho Việt Nam
  - Documented tất cả weather variables available

---

**Last Updated:** 2026-02-08  
**Tested Location:** Hà Nội, Việt Nam (21.0285°N, 105.8542°E)  
**Status:** ✅ 49/51 variables verified and working
