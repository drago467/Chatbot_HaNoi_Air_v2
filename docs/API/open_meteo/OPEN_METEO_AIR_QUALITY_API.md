# Open-Meteo Air Quality API Documentation

## Tổng quan

Open-Meteo Air Quality API là một dịch vụ miễn phí, không yêu cầu API key, cung cấp dữ liệu chất lượng không khí toàn cầu với độ phân giải 11km. API này sử dụng các mô hình dự báo chất lượng không khí từ CAMS (Copernicus Atmosphere Monitoring Service) và các nguồn khác.

**Website:** https://open-meteo.com/en/docs/air-quality-api

**Base URL:** `https://air-quality-api.open-meteo.com/v1/air-quality`

**Cost:** Miễn phí, không cần API key

**Coverage:** Toàn cầu

**Resolution:** 11km

---

## API Endpoint

### GET `/v1/air-quality`

Lấy dữ liệu chất lượng không khí theo tọa độ địa lý.

#### Parameters

**Required:**
- `latitude` (float, required) - Vĩ độ (-90 đến 90)
- `longitude` (float, required) - Kinh độ (-180 đến 180)

**Optional:**
- `hourly` (array of strings, optional) - Danh sách các biến hourly cần lấy
- `daily` (array of strings, optional) - Danh sách các biến daily cần lấy
- `timezone` (string, optional) - Múi giờ (ví dụ: "Asia/Ho_Chi_Minh", "UTC")
- `forecast_days` (integer, optional) - Số ngày dự báo (mặc định: 5 ngày)
- `past_days` (integer, optional) - Số ngày quá khứ (0-92)
- `start_date` (string, optional) - Ngày bắt đầu (YYYY-MM-DD) cho historical data
- `end_date` (string, optional) - Ngày kết thúc (YYYY-MM-DD) cho historical data

#### Example Request

```python
import requests

url = "https://air-quality-api.open-meteo.com/v1/air-quality"
params = {
    "latitude": 21.0285,  # Hà Nội
    "longitude": 105.8542,
    "hourly": ["pm10", "pm2_5", "carbon_monoxide", "nitrogen_dioxide"],
    "timezone": "Asia/Ho_Chi_Minh"
}

response = requests.get(url, params=params)
data = response.json()
```

---

## Variables Available

### Air Quality Pollutants

| Variable Name      | Description              | Unit  | Notes                  |
| ------------------ | ------------------------ | ----- | ---------------------- |
| `pm10`             | Particulate Matter PM10  | µg/m³ | ✅ Verified for Vietnam |
| `pm2_5`            | Particulate Matter PM2.5 | µg/m³ | ✅ Verified for Vietnam |
| `carbon_monoxide`  | Carbon Monoxide CO       | µg/m³ | ✅ Verified for Vietnam |
| `carbon_dioxide`   | Carbon Dioxide CO2       | ppm   | ✅ Verified for Vietnam |
| `nitrogen_dioxide` | Nitrogen Dioxide NO2     | µg/m³ | ✅ Verified for Vietnam |
| `sulphur_dioxide`  | Sulphur Dioxide SO2      | µg/m³ | ✅ Verified for Vietnam |
| `ozone`            | Ozone O3                 | µg/m³ | ✅ Verified for Vietnam |
| `methane`          | Methane CH4              | ppm   | ✅ Verified for Vietnam |

### Optical & UV Variables

| Variable Name           | Description           | Unit  | Notes                  |
| ----------------------- | --------------------- | ----- | ---------------------- |
| `aerosol_optical_depth` | Aerosol Optical Depth | -     | ✅ Verified for Vietnam |
| `dust`                  | Dust concentration    | µg/m³ | ✅ Verified for Vietnam |
| `uv_index`              | UV Index              | -     | ✅ Verified for Vietnam |
| `uv_index_clear_sky`    | UV Index Clear Sky    | -     | ✅ Verified for Vietnam |

### Derived Indices

| Variable Name        | Description                | Unit | Notes                  |
| -------------------- | -------------------------- | ---- | ---------------------- |
| `european_aqi`       | European Air Quality Index | -    | ✅ Verified for Vietnam |
| `european_aqi_pm2_5` | European AQI for PM2.5     | -    | ✅ Verified for Vietnam |
| `european_aqi_pm10`  | European AQI for PM10      | -    | ✅ Verified for Vietnam |
| `european_aqi_no2`   | European AQI for NO2       | -    | ✅ Verified for Vietnam |
| `european_aqi_o3`    | European AQI for O3        | -    | ✅ Verified for Vietnam |

**Note:** Tất cả các biến trên đã được test và verify có dữ liệu trả về cho Hà Nội, Việt Nam.

---

## Response Format

### Response Structure

```json
{
  "latitude": 21.0,
  "longitude": 105.899994,
  "generationtime_ms": 12.5,
  "utc_offset_seconds": 25200,
  "timezone": "Asia/Ho_Chi_Minh",
  "timezone_abbreviation": "+07",
  "elevation": 19.0,
  "hourly_units": {
    "time": "iso8601",
    "pm10": "µg/m³",
    "pm2_5": "µg/m³",
    "carbon_monoxide": "µg/m³",
    ...
  },
  "hourly": {
    "time": [
      "2026-02-08T00:00",
      "2026-02-08T01:00",
      ...
    ],
    "pm10": [57.2, 55.8, ...],
    "pm2_5": [55.4, 54.2, ...],
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

- **Forecast:** Mặc định 5 ngày (120 giờ) dự báo
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
url = "https://air-quality-api.open-meteo.com/v1/air-quality"
params = {
    "latitude": 21.0285,
    "longitude": 105.8542,
    "hourly": [
        "pm10",
        "pm2_5",
        "carbon_monoxide",
        "nitrogen_dioxide",
        "sulphur_dioxide",
        "ozone"
    ],
    "timezone": "Asia/Ho_Chi_Minh"
}

responses = openmeteo.weather_api(url, params=params)

# Process first location
response = responses[0]
print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation: {response.Elevation()} m asl")
print(f"Timezone: {response.Timezone()}")

# Process hourly data
hourly = response.Hourly()
hourly_pm10 = hourly.Variables(0).ValuesAsNumpy()
hourly_pm2_5 = hourly.Variables(1).ValuesAsNumpy()
hourly_co = hourly.Variables(2).ValuesAsNumpy()
hourly_no2 = hourly.Variables(3).ValuesAsNumpy()
hourly_so2 = hourly.Variables(4).ValuesAsNumpy()
hourly_o3 = hourly.Variables(5).ValuesAsNumpy()

# Create DataFrame
hourly_data = {
    "date": pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
        end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left"
    )
}

hourly_data["pm10"] = hourly_pm10
hourly_data["pm2_5"] = hourly_pm2_5
hourly_data["carbon_monoxide"] = hourly_co
hourly_data["nitrogen_dioxide"] = hourly_no2
hourly_data["sulphur_dioxide"] = hourly_so2
hourly_data["ozone"] = hourly_o3

hourly_dataframe = pd.DataFrame(data=hourly_data)
print("\nHourly data:\n", hourly_dataframe)
```

### Example 2: Sử dụng `requests` Library (Đơn giản)

```python
import requests
import pandas as pd
from datetime import datetime

# Tọa độ Hà Nội
url = "https://air-quality-api.open-meteo.com/v1/air-quality"
params = {
    "latitude": 21.0285,
    "longitude": 105.8542,
    "hourly": [
        "pm10",
        "pm2_5",
        "carbon_monoxide",
        "nitrogen_dioxide",
        "sulphur_dioxide",
        "ozone",
        "aerosol_optical_depth",
        "dust",
        "uv_index",
        "uv_index_clear_sky",
        "methane",
        "european_aqi"
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
    "pm10": hourly.get("pm10", []),
    "pm2_5": hourly.get("pm2_5", []),
    "carbon_monoxide": hourly.get("carbon_monoxide", []),
    "nitrogen_dioxide": hourly.get("nitrogen_dioxide", []),
    "sulphur_dioxide": hourly.get("sulphur_dioxide", []),
    "ozone": hourly.get("ozone", []),
    "aerosol_optical_depth": hourly.get("aerosol_optical_depth", []),
    "dust": hourly.get("dust", []),
    "uv_index": hourly.get("uv_index", []),
    "uv_index_clear_sky": hourly.get("uv_index_clear_sky", []),
    "methane": hourly.get("methane", []),
    "european_aqi": hourly.get("european_aqi", [])
})

print(f"\nLocation: {data['latitude']}°N, {data['longitude']}°E")
print(f"Elevation: {data['elevation']} m")
print(f"Timezone: {data['timezone']}")
print(f"\nData shape: {df.shape}")
print(f"\nFirst few rows:\n{df.head()}")
print(f"\nStatistics:\n{df.describe()}")
```

### Example 3: Request tất cả các biến có sẵn

```python
import requests
import pandas as pd

# Tọa độ Hà Nội
url = "https://air-quality-api.open-meteo.com/v1/air-quality"

# Tất cả các biến có sẵn
all_variables = [
    "pm10",
    "pm2_5",
    "carbon_monoxide",
    "carbon_dioxide",
    "nitrogen_dioxide",
    "sulphur_dioxide",
    "ozone",
    "aerosol_optical_depth",
    "dust",
    "uv_index",
    "uv_index_clear_sky",
    "methane",
    "european_aqi",
    "european_aqi_pm2_5",
    "european_aqi_pm10",
    "european_aqi_no2",
    "european_aqi_o3"
]

params = {
    "latitude": 21.0285,
    "longitude": 105.8542,
    "hourly": all_variables,
    "timezone": "Asia/Ho_Chi_Minh",
    "forecast_days": 5
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

url = "https://air-quality-api.open-meteo.com/v1/air-quality"

# Lấy dữ liệu 7 ngày qua
end_date = datetime.now()
start_date = end_date - timedelta(days=7)

params = {
    "latitude": 21.0285,
    "longitude": 105.8542,
    "hourly": ["pm10", "pm2_5", "european_aqi"],
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
    "pm10": hourly["pm10"],
    "pm2_5": hourly["pm2_5"],
    "european_aqi": hourly["european_aqi"]
})

print(f"Historical data from {start_date.date()} to {end_date.date()}")
print(f"\n{df.head(10)}")
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
- ✅ **Data Availability:** 116/120 timestamps có dữ liệu (96.7%)
- ✅ **Forecast Period:** 5 ngày (120 giờ)
- ✅ **All Variables Available:** Tất cả 17 biến đều có dữ liệu

**Sample Data Ranges (Hà Nội):**
- PM10: 9.10 - 167.20 µg/m³ (Avg: 57.22)
- PM2.5: 9.00 - 164.80 µg/m³ (Avg: 55.44)
- Carbon Monoxide: 270.00 - 1752.00 µg/m³ (Avg: 741.82)
- Nitrogen Dioxide: 7.50 - 72.40 µg/m³ (Avg: 28.91)
- Sulphur Dioxide: 8.30 - 67.50 µg/m³ (Avg: 26.28)
- Ozone: 4.00 - 130.00 µg/m³ (Avg: 57.43)
- European AQI: 30.00 - 129.00 (Avg: 81.38)

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
4. **Request Optimization:** Chỉ request các biến cần thiết
5. **Timezone:** Luôn specify timezone để có dữ liệu theo giờ địa phương

### Example với Error Handling

```python
import requests
from time import sleep

def get_air_quality(lat, lon, variables, max_retries=3):
    url = "https://air-quality-api.open-meteo.com/v1/air-quality"
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
data = get_air_quality(21.0285, 105.8542, ["pm10", "pm2_5"])
if data:
    print("Success!")
else:
    print("Failed after retries")
```

---

## Limitations

1. **Resolution:** Độ phân giải 11km - không phù hợp cho micro-scale analysis
2. **Model-based:** Dữ liệu từ mô hình dự báo, không phải measurements thực tế
3. **Accuracy:** Có thể có sai số so với measurements thực tế, đặc biệt ở urban areas
4. **Coverage:** Một số vùng có thể thiếu dữ liệu hoặc chất lượng thấp hơn
5. **Update Frequency:** Dữ liệu được cập nhật hàng giờ, không real-time

---

## Comparison với các nguồn khác

### So sánh với HanoiAir API

| Feature        | Open-Meteo Air Quality API    | HanoiAir API            |
| -------------- | ----------------------------- | ----------------------- |
| **Coverage**   | Toàn cầu                      | Chỉ Hà Nội              |
| **Variables**  | 17+ biến (PM, gases, UV, AQI) | Chỉ PM2.5, AQI          |
| **Resolution** | 11km                          | 1km (grid)              |
| **Data Type**  | Model-based forecast          | Measurements + forecast |
| **Cost**       | Miễn phí                      | Miễn phí                |
| **API Key**    | Không cần                     | Không cần               |
| **Historical** | Có (tối đa 92 ngày)           | Có                      |

### Khi nào sử dụng Open-Meteo Air Quality API?

✅ **Nên dùng khi:**
- Cần nhiều biến pollutants (CO, NO2, SO2, O3, etc.)
- Cần dữ liệu cho nhiều locations (không chỉ Hà Nội)
- Cần UV Index, Aerosol Optical Depth
- Cần European AQI
- Cần historical data

❌ **Không nên dùng khi:**
- Cần độ phân giải cao (1km như HanoiAir)
- Cần measurements thực tế thay vì model-based
- Chỉ cần PM2.5 cho Hà Nội (HanoiAir có độ phân giải tốt hơn)

---

## Integration với Codebase

### Gợi ý tạo OpenMeteoAirQualityCollector

Có thể tạo collector tương tự `OpenMeteoCollector` hiện tại:

```python
# backend/app/services/data/collectors/open_meteo_air_quality_collector.py

class OpenMeteoAirQualityCollector:
    """Collector for air quality data from Open-Meteo Air Quality API."""
    
    def __init__(self):
        self.base_url = "https://air-quality-api.open-meteo.com/v1/air-quality"
        self.session = requests.Session()
    
    def fetch_hourly_air_quality(self, lat: float, lon: float) -> List[Dict]:
        """Fetch hourly air quality forecast."""
        params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": [
                "pm10", "pm2_5", "carbon_monoxide", "nitrogen_dioxide",
                "sulphur_dioxide", "ozone", "european_aqi"
            ],
            "timezone": "Asia/Ho_Chi_Minh"
        }
        
        response = self.session.get(self.base_url, params=params, timeout=10)
        response.raise_for_status()
        return self._normalize_hourly(response.json())
    
    def _normalize_hourly(self, raw: Dict) -> List[Dict]:
        """Normalize response to list of records."""
        # Implementation similar to OpenMeteoCollector
        ...
```

---

## References

- **Official Documentation:** https://open-meteo.com/en/docs/air-quality-api
- **API Explorer:** https://open-meteo.com/en/docs/air-quality-api (có thể test trực tiếp)
- **GitHub:** https://github.com/open-meteo/open-meteo

---

## Changelog

- **2026-02-08:** Initial documentation
  - Tested với tọa độ Hà Nội
  - Verified tất cả 17 biến có dữ liệu
  - Added code examples cho Việt Nam

---

**Last Updated:** 2026-02-08  
**Tested Location:** Hà Nội, Việt Nam (21.0285°N, 105.8542°E)  
**Status:** ✅ All variables verified and working
