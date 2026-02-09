# OpenWeatherMap Air Pollution API Documentation

## Tổng quan

OpenWeatherMap Air Pollution API cung cấp dữ liệu chất lượng không khí hiện tại, dự báo, và lịch sử. API này là nguồn chính cho dữ liệu air quality (PM2.5, PM10, NO2, SO2, O3, CO) trong hệ thống Chatbot Hà Nội Air.

**Website:** https://openweathermap.org/api/air-pollution

**Base URL:** `http://api.openweathermap.org/data/2.5/air_pollution`

**Cost:** 
- **Free tier:** 1,000 calls/day (shared với One Call API)
- **Paid tiers:** Từ $40/tháng với limits cao hơn

**Coverage:** Toàn cầu

**API Key Required:** ✅ Có (đăng ký tại https://openweathermap.org/api)

---

## API Endpoints

OpenWeatherMap Air Pollution API cung cấp 3 endpoints chính:

1. **Current** - Dữ liệu ô nhiễm không khí hiện tại
2. **Forecast** - Dự báo ô nhiễm không khí (tối đa 5 ngày)
3. **History** - Dữ liệu lịch sử về ô nhiễm không khí

---

### 1. GET `/data/2.5/air_pollution` - Current Air Pollution

Lấy dữ liệu ô nhiễm không khí hiện tại cho một location.

#### Parameters

**Required:**
- `lat` (float, required) - Vĩ độ (-90 đến 90)
- `lon` (float, required) - Kinh độ (-180 đến 180)
- `appid` (string, required) - API key từ OpenWeatherMap

#### Example Request

```python
import requests

url = "http://api.openweathermap.org/data/2.5/air_pollution"
params = {
    "lat": 21.0285,  # Hà Nội
    "lon": 105.8542,
    "appid": "YOUR_API_KEY"
}

response = requests.get(url, params=params)
data = response.json()
```

#### Response Structure

```json
{
  "coord": {
    "lon": 105.8544,
    "lat": 21.0294
  },
  "list": [
    {
      "main": {
        "aqi": 5
      },
      "components": {
        "co": 969.95,
        "no": 0.01,
        "no2": 11.4,
        "o3": 33.09,
        "so2": 5,
        "pm2_5": 76.3,
        "pm10": 77.19,
        "nh3": 0.43
      },
      "dt": 1770520478
    }
  ]
}
```

**Note:** Response chỉ chứa 1 item trong `list` array cho current data.

---

### 2. GET `/data/2.5/air_pollution/forecast` - Forecast Air Pollution

Lấy dự báo ô nhiễm không khí theo giờ (tối đa 5 ngày, 120 giờ).

#### Parameters

**Required:**
- `lat` (float, required) - Vĩ độ
- `lon` (float, required) - Kinh độ
- `appid` (string, required) - API key

#### Example Request

```python
import requests

url = "http://api.openweathermap.org/data/2.5/air_pollution/forecast"
params = {
    "lat": 21.0285,
    "lon": 105.8542,
    "appid": "YOUR_API_KEY"
}

response = requests.get(url, params=params)
data = response.json()
```

#### Response Structure

```json
{
  "coord": {
    "lon": 105.8542,
    "lat": 21.0285
  },
  "list": [
    {
      "main": {
        "aqi": 5
      },
      "components": {
        "co": 969.95,
        "no": 0.01,
        "no2": 11.4,
        "o3": 33.09,
        "so2": 5,
        "pm2_5": 76.3,
        "pm10": 77.19,
        "nh3": 0.43
      },
      "dt": 1770519600
    },
    {
      "main": {
        "aqi": 4
      },
      "components": {
        "co": 1028.36,
        "no": 0.03,
        "no2": 12.46,
        "o3": 25.65,
        "so2": 4.04,
        "pm2_5": 67.29,
        "pm10": 68.09,
        "nh3": 0.42
      },
      "dt": 1770523200
    }
    // ... up to 120 items (5 days × 24 hours)
  ]
}
```

**Note:** Response chứa tối đa 120 items (5 ngày × 24 giờ) trong `list` array.

---

### 3. GET `/data/2.5/air_pollution/history` - Historical Air Pollution

Lấy dữ liệu lịch sử về ô nhiễm không khí cho một khoảng thời gian.

#### Parameters

**Required:**
- `lat` (float, required) - Vĩ độ
- `lon` (float, required) - Kinh độ
- `start` (integer, required) - Unix timestamp bắt đầu
- `end` (integer, required) - Unix timestamp kết thúc
- `appid` (string, required) - API key

**Note:** Khoảng thời gian tối đa là 5 ngày (120 giờ).

#### Example Request

```python
import requests
from datetime import datetime, timedelta

# Lấy dữ liệu 7 ngày trước
start_date = datetime.now() - timedelta(days=7)
end_date = start_date + timedelta(days=1)

url = "http://api.openweathermap.org/data/2.5/air_pollution/history"
params = {
    "lat": 21.0285,
    "lon": 105.8542,
    "start": int(start_date.timestamp()),
    "end": int(end_date.timestamp()),
    "appid": "YOUR_API_KEY"
}

response = requests.get(url, params=params)
data = response.json()
```

#### Response Structure

```json
{
  "coord": {
    "lon": 105.8542,
    "lat": 21.0285
  },
  "list": [
    {
      "main": {
        "aqi": 5
      },
      "components": {
        "co": 806.49,
        "no": 0.04,
        "no2": 6.76,
        "o3": 81.65,
        "so2": 7.91,
        "pm2_5": 101.55,
        "pm10": 109.52,
        "nh3": 0.78
      },
      "dt": 1769918400
    }
    // ... hourly data for the time range
  ]
}
```

**Note:** Response chứa hourly data cho khoảng thời gian được chỉ định (tối đa 5 ngày).

---

## Response Fields

### Common Response Structure

Tất cả 3 endpoints đều trả về cùng structure:

```json
{
  "coord": {
    "lon": float,
    "lat": float
  },
  "list": [
    {
      "main": {
        "aqi": integer
      },
      "components": {
        "co": float,
        "no": float,
        "no2": float,
        "o3": float,
        "so2": float,
        "pm2_5": float,
        "pm10": float,
        "nh3": float
      },
      "dt": integer
    }
  ]
}
```

### Field Descriptions

| Field | Type | Unit | Description | Notes |
|-------|------|------|-------------|-------|
| `coord.lon` | float | - | Longitude | ✅ |
| `coord.lat` | float | - | Latitude | ✅ |
| `list[].main.aqi` | integer | - | Air Quality Index | ✅ (1-5 scale) |
| `list[].components.co` | float | µg/m³ | Carbon Monoxide | ✅ |
| `list[].components.no` | float | µg/m³ | Nitrogen Monoxide | ✅ |
| `list[].components.no2` | float | µg/m³ | Nitrogen Dioxide | ✅ |
| `list[].components.o3` | float | µg/m³ | Ozone | ✅ |
| `list[].components.so2` | float | µg/m³ | Sulphur Dioxide | ✅ |
| `list[].components.pm2_5` | float | µg/m³ | Particulate Matter PM2.5 | ✅ |
| `list[].components.pm10` | float | µg/m³ | Particulate Matter PM10 | ✅ |
| `list[].components.nh3` | float | µg/m³ | Ammonia | ✅ |
| `list[].dt` | integer | Unix timestamp | Time of data calculation | ✅ |

### Air Quality Index (AQI) Scale

| AQI Value | Level | Description |
|------------|-------|-------------|
| 1 | Good | Air quality is satisfactory |
| 2 | Fair | Air quality is acceptable |
| 3 | Moderate | Sensitive groups may experience effects |
| 4 | Poor | Everyone may begin to experience effects |
| 5 | Very Poor | Health warnings of emergency conditions |

---

## Code Examples

### Example 1: Current Air Pollution

```python
import requests
from datetime import datetime

API_KEY = "YOUR_API_KEY"

url = "http://api.openweathermap.org/data/2.5/air_pollution"
params = {
    "lat": 21.0285,
    "lon": 105.8542,
    "appid": API_KEY
}

response = requests.get(url, params=params)
data = response.json()

# Process current data
if data.get("list"):
    current = data["list"][0]
    components = current["components"]
    
    print(f"Current Air Quality (AQI: {current['main']['aqi']}):")
    print(f"  PM2.5: {components['pm2_5']} µg/m³")
    print(f"  PM10: {components['pm10']} µg/m³")
    print(f"  NO2: {components['no2']} µg/m³")
    print(f"  SO2: {components['so2']} µg/m³")
    print(f"  O3: {components['o3']} µg/m³")
    print(f"  CO: {components['co']} µg/m³")
    print(f"  Time: {datetime.fromtimestamp(current['dt'])}")
```

### Example 2: Forecast Air Pollution

```python
import requests
import pandas as pd
from datetime import datetime

API_KEY = "YOUR_API_KEY"

url = "http://api.openweathermap.org/data/2.5/air_pollution/forecast"
params = {
    "lat": 21.0285,
    "lon": 105.8542,
    "appid": API_KEY
}

response = requests.get(url, params=params)
data = response.json()

# Process forecast data
forecast_data = []
for item in data.get("list", []):
    forecast_data.append({
        "time": datetime.fromtimestamp(item["dt"]),
        "aqi": item["main"]["aqi"],
        "pm2_5": item["components"]["pm2_5"],
        "pm10": item["components"]["pm10"],
        "no2": item["components"]["no2"],
        "so2": item["components"]["so2"],
        "o3": item["components"]["o3"],
        "co": item["components"]["co"]
    })

df = pd.DataFrame(forecast_data)
print(f"Forecast: {len(df)} hours")
print(f"\nFirst 10 hours:\n{df.head(10)}")
print(f"\nStatistics:\n{df.describe()}")
```

### Example 3: Historical Air Pollution

```python
import requests
import pandas as pd
from datetime import datetime, timedelta

API_KEY = "YOUR_API_KEY"

# Lấy dữ liệu 7 ngày trước (1 ngày)
start_date = datetime.now() - timedelta(days=7)
end_date = start_date + timedelta(days=1)

url = "http://api.openweathermap.org/data/2.5/air_pollution/history"
params = {
    "lat": 21.0285,
    "lon": 105.8542,
    "start": int(start_date.timestamp()),
    "end": int(end_date.timestamp()),
    "appid": API_KEY
}

response = requests.get(url, params=params)
data = response.json()

# Process historical data
historical_data = []
for item in data.get("list", []):
    historical_data.append({
        "time": datetime.fromtimestamp(item["dt"]),
        "aqi": item["main"]["aqi"],
        "pm2_5": item["components"]["pm2_5"],
        "pm10": item["components"]["pm10"],
        "no2": item["components"]["no2"],
        "so2": item["components"]["so2"],
        "o3": item["components"]["o3"],
        "co": item["components"]["co"]
    })

df = pd.DataFrame(historical_data)
print(f"Historical data: {len(df)} hours")
print(f"Date range: {df['time'].min()} to {df['time'].max()}")
print(f"\n{df.head(10)}")
```

### Example 4: Using OpenWeatherAirCollector (from codebase)

```python
from app.services.data.collectors.openweather_air_collector import OpenWeatherAirCollector
import os

# Initialize collector
api_key = os.getenv("OPENWEATHERMAP_API_KEY")
collector = OpenWeatherAirCollector(api_key=api_key)

# Get current air pollution
lat = 21.0285
lon = 105.8542

result = collector.collect_for_coordinates(lat, lon)
print(f"PM2.5: {result['pm25']} µg/m³")
print(f"PM10: {result['pm10']} µg/m³")
print(f"AQI: {result['aqi']}")

# Get forecast
forecast_list = collector.collect_forecast_air_pollution(lat, lon)
print(f"Forecast: {len(forecast_list)} hours")
```

### Example 5: Error Handling with Retry

```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def get_air_pollution(lat, lon, api_key, endpoint="current", max_retries=3):
    """Get air pollution data with retry logic."""
    base_url = "http://api.openweathermap.org/data/2.5/air_pollution"
    
    if endpoint == "current":
        url = base_url
        params = {"lat": lat, "lon": lon, "appid": api_key}
    elif endpoint == "forecast":
        url = f"{base_url}/forecast"
        params = {"lat": lat, "lon": lon, "appid": api_key}
    else:
        raise ValueError("endpoint must be 'current' or 'forecast'")
    
    # Setup session with retry
    session = requests.Session()
    retry_strategy = Retry(
        total=max_retries,
        backoff_factor=1.0,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    
    try:
        response = session.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            raise ValueError("Invalid API key")
        elif e.response.status_code == 429:
            raise ValueError("Rate limit exceeded")
        else:
            raise
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Request failed: {e}")

# Usage
try:
    data = get_air_pollution(21.0285, 105.8542, "YOUR_API_KEY", endpoint="current")
    print("Success!")
except ValueError as e:
    print(f"Error: {e}")
except ConnectionError as e:
    print(f"Connection error: {e}")
```

---

## Tọa độ các thành phố Việt Nam

| Thành phố       | Latitude | Longitude |
| --------------- | -------- | --------- |
| Hà Nội          | 21.0285  | 105.8542  |
| TP. Hồ Chí Minh | 10.7769  | 106.7009  |
| Đà Nẵng         | 16.0544  | 108.2022  |
| Hải Phòng       | 20.8449  | 106.6881  |
| Cần Thơ         | 10.0452  | 105.7469  |

---

## Data Quality & Verification

### Test Results cho Hà Nội (2026-02-08)

**Test Location:** 21.0285°N, 105.8542°E (Hà Nội)

**Test Results:**
- ✅ **Current:** PASSED (200 OK)
  - 1 item trong response
  - AQI: 5 (Very Poor)
  - All components available: PM2.5, PM10, NO2, SO2, O3, CO, NO, NH3
  
- ✅ **Forecast:** PASSED (200 OK)
  - 96 items trong response (4 ngày × 24 giờ)
  - Hourly forecast available
  - All components available
  
- ✅ **Historical:** PASSED (200 OK)
  - 24 items trong response (1 ngày × 24 giờ)
  - Historical data available
  - All components available

**Sample Data Ranges (Hà Nội - Current):**
- PM2.5: 76.3 µg/m³
- PM10: 77.19 µg/m³
- NO2: 11.4 µg/m³
- SO2: 5.0 µg/m³
- O3: 33.09 µg/m³
- CO: 969.95 µg/m³
- AQI: 5 (Very Poor)

---

## Rate Limits & Best Practices

### Rate Limits

**Free Tier:**
- **Daily limit:** 1,000 calls/day (shared với One Call API)
- **Per-minute limit:** 60 calls/minute (shared với One Call API)
- **Monthly limit:** 1,000,000 calls/month

**Paid Tiers:**
- **Startup ($40/month):** 1,000 calls/minute, 1M calls/month
- **Developer ($150/month):** 1,000 calls/minute, 10M calls/month
- **Professional ($400/month):** 1,000 calls/minute, unlimited

### Best Practices

1. **Use Forecast endpoint:** Thay vì gọi current nhiều lần, dùng forecast endpoint để lấy tất cả forecast hours trong 1 call
2. **Cache responses:** Cache với TTL 1 giờ cho current data, 6 giờ cho forecast
3. **Respect rate limits:** Implement rate limiting để tránh exceed daily limit
4. **Error handling:** Xử lý các lỗi:
   - 401: Invalid API key
   - 429: Rate limit exceeded (retry after delay)
   - 500-504: Server errors (retry with exponential backoff)
5. **Request optimization:** 
   - Current: Chỉ gọi khi cần data mới nhất
   - Forecast: Gọi 1 lần để lấy tất cả forecast hours (thay vì gọi current nhiều lần)
   - History: Chỉ gọi khi cần historical data

### Rate Limiting Example

```python
from collections import defaultdict
from datetime import date
import time

class RateLimiter:
    """Simple rate limiter for Air Pollution API."""
    
    DAILY_LIMIT = 1000
    PER_MINUTE_LIMIT = 60
    
    def __init__(self):
        self._daily_calls = defaultdict(int)
        self._minute_calls = []
    
    def check_rate_limit(self):
        """Check and wait if needed."""
        today = date.today().isoformat()
        current_time = time.time()
        
        # Check daily limit
        if self._daily_calls[today] >= self.DAILY_LIMIT:
            raise ValueError(f"Daily limit exceeded: {self.DAILY_LIMIT} calls/day")
        
        # Clean old minute calls
        self._minute_calls = [t for t in self._minute_calls if current_time - t < 60]
        
        # Check per-minute limit
        if len(self._minute_calls) >= self.PER_MINUTE_LIMIT:
            oldest = min(self._minute_calls)
            wait_time = 60 - (current_time - oldest) + 0.1
            if wait_time > 0:
                time.sleep(wait_time)
                self._minute_calls = [t for t in self._minute_calls if current_time - t < 60]
        
        # Record call
        self._minute_calls.append(time.time())
        self._daily_calls[today] += 1

# Usage
rate_limiter = RateLimiter()
rate_limiter.check_rate_limit()  # Call before each API request
```

---

## Limitations

1. **API Key Required:** Cần đăng ký và có API key
2. **Daily Limit:** Free tier chỉ 1,000 calls/day (shared với One Call API)
3. **Point-based:** Data cho một điểm (lat/lon), không phải grid
4. **Forecast Period:** Forecast chỉ tối đa 5 ngày (120 giờ)
5. **Historical Period:** Historical chỉ tối đa 5 ngày mỗi request
6. **Update Frequency:** Dữ liệu được cập nhật hàng giờ, không real-time

---

## Comparison với các nguồn khác

### So sánh với Open-Meteo Air Quality API

| Feature        | OpenWeatherMap Air Pollution API | Open-Meteo Air Quality API |
| -------------- | -------------------------------- | --------------------------- |
| **API Key**    | ✅ Required                      | ❌ Not required             |
| **Cost**       | Free tier: 1K calls/day          | Free, unlimited             |
| **Current**    | ✅ Yes                           | ✅ Yes (forecast)            |
| **Forecast**   | ✅ 5 days (120 hours)            | ✅ 5 days (120 hours)        |
| **Historical** | ✅ Yes (max 5 days per request)  | ✅ Yes (max 92 days)         |
| **Variables**  | 8 components (PM, gases, AQI)    | 17+ variables (PM, gases, UV, AQI, etc.) |
| **AQI**        | ✅ Yes (1-5 scale)               | ✅ Yes (European AQI)        |
| **NH3**        | ✅ Yes                           | ❌ No                        |
| **NO**         | ✅ Yes                           | ❌ No                        |
| **UV Index**   | ❌ No                            | ✅ Yes                       |
| **Methane**    | ❌ No                            | ✅ Yes                       |
| **CO2**        | ❌ No                            | ✅ Yes                       |

### Khi nào sử dụng OpenWeatherMap Air Pollution API?

✅ **Nên dùng khi:**
- Cần current air pollution data
- Cần forecast 5 ngày
- Cần NH3 và NO data (không có trong Open-Meteo)
- Có API key và budget cho paid tier nếu cần
- Cần AQI scale 1-5 (đơn giản hơn European AQI)

❌ **Không nên dùng khi:**
- Không muốn quản lý API key
- Cần nhiều biến hơn (UV Index, Methane, CO2, etc.)
- Cần unlimited free calls
- Cần historical data dài hơn 5 ngày mỗi request
- **Cần nhiều biến pollutants** - Open-Meteo cung cấp 17+ biến miễn phí

---

## Integration với Codebase

### OpenWeatherAirCollector

Codebase đã có `OpenWeatherAirCollector` tại:
- `backend/app/services/data/collectors/openweather_air_collector.py`

**Features:**
- Fetches current air pollution (1 call)
- Fetches forecast air pollution (1 call, thay vì 48 calls)
- Normalizes data to CKG variable format
- Validates data với strict range checks
- Handles errors với retry logic và exponential backoff
- Respects rate limits (60 calls/minute, shared với OneCallCollector)

**Usage:**
```python
from app.services.data.collectors.openweather_air_collector import OpenWeatherAirCollector

collector = OpenWeatherAirCollector(api_key=api_key)
result = collector.collect_for_coordinates(lat, lon)
forecast_list = collector.collect_forecast_air_pollution(lat, lon)
```

**Optimization:**
- Sử dụng forecast endpoint để lấy tất cả forecast hours trong 1 call
- Giảm từ 48 calls/district → 2 calls/district (current + forecast)

---

## Error Codes

| Status Code | Description         | Solution           |
| ----------- | ------------------- | ------------------ |
| 401         | Invalid API key     | Check API key      |
| 429         | Rate limit exceeded | Wait and retry     |
| 500         | Server error        | Retry with backoff |
| 502         | Bad gateway         | Retry with backoff |
| 503         | Service unavailable | Retry with backoff |
| 504         | Gateway timeout     | Retry with backoff |

---

## References

- **Official Documentation:** https://openweathermap.org/api/air-pollution
- **API Key Registration:** https://openweathermap.org/api
- **Pricing:** https://openweathermap.org/price
- **Codebase Collector:** `backend/app/services/data/collectors/openweather_air_collector.py`

---

## Changelog

- **2026-02-08:** Initial documentation
  - Documented all 3 Air Pollution API endpoints
  - Added code examples
  - Documented rate limits và best practices
  - Added comparison với Open-Meteo Air Quality API
  - Tested all endpoints with Hà Nội coordinates

---

**Last Updated:** 2026-02-08  
**API Version:** 2.5  
**Status:** ✅ All 3 endpoints tested and verified  
**Tested Endpoints:** Current, Forecast, History
