# OpenWeatherMap One Call API 3.0 Documentation

## Tổng quan

OpenWeatherMap One Call API 3.0 là một API mạnh mẽ cung cấp dữ liệu thời tiết hiện tại, dự báo theo giờ (48 giờ), và dự báo theo ngày (8 ngày) trong một lần gọi API duy nhất. API này là nguồn chính cho dữ liệu khí tượng trong hệ thống Chatbot Hà Nội Air.

**Website:** https://openweathermap.org/api/one-call-3

**Base URL:** `https://api.openweathermap.org/data/3.0/onecall`

**Cost:** 
- **Free tier:** 1,000 calls/day
- **Paid tiers:** Từ $40/tháng với limits cao hơn

**Coverage:** Toàn cầu

**API Key Required:** ✅ Có (đăng ký tại https://openweathermap.org/api)

---

## API Endpoints

OpenWeatherMap One Call API 3.0 cung cấp 4 endpoints chính:

1. **Current + Forecast** - Dữ liệu hiện tại và dự báo
2. **Time Machine** - Dữ liệu lịch sử tại một thời điểm
3. **Day Summary** - Tổng hợp dữ liệu theo ngày
4. **Overview** - Tổng quan thời tiết dạng text

---

### 1. GET `/data/3.0/onecall` - Current + Forecast

Lấy dữ liệu thời tiết hiện tại, dự báo theo giờ (48h), và dự báo theo ngày (8 ngày) trong một lần gọi.

#### Parameters

**Required:**
- `lat` (float, required) - Vĩ độ (-90 đến 90)
- `lon` (float, required) - Kinh độ (-180 đến 180)
- `appid` (string, required) - API key từ OpenWeatherMap

**Optional:**
- `exclude` (string, optional) - Loại trừ các phần không cần thiết (comma-separated)
  - `current` - Current weather data
  - `minutely` - Minutely forecast (60 minutes)
  - `hourly` - Hourly forecast (48 hours)
  - `daily` - Daily forecast (8 days)
  - `alerts` - Weather alerts
  - Example: `exclude=minutely,alerts` (loại trừ minutely và alerts)
- `units` (string, optional) - Units format
  - `standard` - Kelvin, m/s (default)
  - `metric` - Celsius, m/s (recommended)
  - `imperial` - Fahrenheit, mph
- `lang` (string, optional) - Language code (e.g., `vi` for Vietnamese)

#### Example Request

```python
import requests

url = "https://api.openweathermap.org/data/3.0/onecall"
params = {
    "lat": 21.0285,  # Hà Nội
    "lon": 105.8542,
    "appid": "YOUR_API_KEY",
    "units": "metric",  # Celsius, m/s
    "exclude": "minutely,alerts",  # Exclude minutely forecast and alerts
    "lang": "vi"  # Vietnamese
}

response = requests.get(url, params=params)
data = response.json()
```

---

### 2. GET `/data/3.0/onecall/timemachine` - Historical Data

Lấy dữ liệu thời tiết lịch sử tại một thời điểm cụ thể (Unix timestamp).

#### Parameters

**Required:**
- `lat` (float, required) - Vĩ độ
- `lon` (float, required) - Kinh độ
- `dt` (integer, required) - Unix timestamp của thời điểm cần lấy dữ liệu
- `appid` (string, required) - API key

**Optional:**
- `units` (string, optional) - Units format (standard, metric, imperial)
- `lang` (string, optional) - Language code

#### Example Request

```python
import requests
from datetime import datetime, timedelta

# Lấy dữ liệu 7 ngày trước
past_date = datetime.now() - timedelta(days=7)
timestamp = int(past_date.timestamp())

url = "https://api.openweathermap.org/data/3.0/onecall/timemachine"
params = {
    "lat": 21.0285,
    "lon": 105.8542,
    "dt": timestamp,
    "appid": "YOUR_API_KEY",
    "units": "metric",
    "lang": "vi"
}

response = requests.get(url, params=params)
data = response.json()
```

#### Response Structure

```json
{
  "lat": 21.0285,
  "lon": 105.8542,
  "timezone": "Asia/Bangkok",
  "timezone_offset": 25200,
  "data": [
    {
      "dt": 1769911811,
      "sunrise": 1769902418,
      "sunset": 1769942787,
      "temp": 18.1,
      "feels_like": 17.82,
      "pressure": 1025,
      "humidity": 71,
      "dew_point": 12.76,
      "clouds": 100,
      "wind_speed": 0.96,
      "wind_deg": 45,
      "wind_gust": 1.71,
      "weather": [
        {
          "id": 804,
          "main": "Clouds",
          "description": "mây đen u ám",
          "icon": "04d"
        }
      ]
    }
  ]
}
```

**Note:** Response chỉ chứa 1 record trong `data` array cho thời điểm được chỉ định.

---

### 3. GET `/data/3.0/onecall/day_summary` - Daily Summary

Lấy dữ liệu tổng hợp theo ngày (min, max, average cho các biến thời tiết).

#### Parameters

**Required:**
- `lat` (float, required) - Vĩ độ
- `lon` (float, required) - Kinh độ
- `date` (string, required) - Ngày theo format YYYY-MM-DD
- `appid` (string, required) - API key

**Optional:**
- `units` (string, optional) - Units format
- `lang` (string, optional) - Language code

#### Example Request

```python
import requests
from datetime import datetime, timedelta

# Lấy summary cho hôm qua
yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

url = "https://api.openweathermap.org/data/3.0/onecall/day_summary"
params = {
    "lat": 21.0285,
    "lon": 105.8542,
    "date": yesterday,
    "appid": "YOUR_API_KEY",
    "units": "metric",
    "lang": "vi"
}

response = requests.get(url, params=params)
data = response.json()
```

#### Response Structure

```json
{
  "lat": 21.0285,
  "lon": 105.8542,
  "tz": "+07:00",
  "date": "2026-02-07",
  "units": "metric",
  "cloud_cover": {
    "afternoon": 55.0
  },
  "humidity": {
    "afternoon": 71.0
  },
  "precipitation": {
    "total": 0.0
  },
  "temperature": {
    "min": 20.96,
    "max": 24.96,
    "afternoon": 22.96,
    "night": 21.96,
    "evening": 23.96,
    "morning": 20.96
  },
  "pressure": {
    "afternoon": 1016.0
  },
  "wind": {
    "max": {
      "speed": 5.83,
      "direction": 187.0
    }
  }
}
```

**Fields:**
- `temperature`: min, max, afternoon, night, evening, morning
- `humidity`: afternoon value
- `cloud_cover`: afternoon value
- `pressure`: afternoon value
- `precipitation`: total for the day
- `wind.max`: maximum wind speed and direction

---

### 4. GET `/data/3.0/onecall/overview` - Weather Overview

Lấy tổng quan thời tiết dạng text (AI-generated summary).

#### Parameters

**Required:**
- `lat` (float, required) - Vĩ độ
- `lon` (float, required) - Kinh độ
- `appid` (string, required) - API key

**Optional:**
- `units` (string, optional) - Units format
- `lang` (string, optional) - Language code

#### Example Request

```python
import requests

url = "https://api.openweathermap.org/data/3.0/onecall/overview"
params = {
    "lat": 21.0285,
    "lon": 105.8542,
    "appid": "YOUR_API_KEY",
    "units": "metric",
    "lang": "vi"
}

response = requests.get(url, params=params)
data = response.json()
```

#### Response Structure

```json
{
  "lat": 21.0285,
  "lon": 105.8542,
  "tz": "+07:00",
  "date": "2026-02-08",
  "units": "metric",
  "weather_overview": "Currently, the weather is overcast with a temperature of 16°C. The wind is blowing at 7 meters per second with gusts up to 11 meters per second. The humidity is at 88% and the visibility is clear at 10,000 meters. The atmospheric pressure is at 1023 hPa. The UV index is low at 0. Overall, it's a cloudy and slightly windy day with moderate temperature. Make sure to dress accordingly and be cautious of the wind if you're heading outdoors."
}
```

**Fields:**
- `weather_overview` (string) - Text summary về thời tiết hiện tại
- `date` (string) - Ngày của overview
- `tz` (string) - Timezone

---

## Response Structure (Current + Forecast)

### Full Response Structure

```json
{
  "lat": 21.0285,
  "lon": 105.8542,
  "timezone": "Asia/Bangkok",
  "timezone_offset": 25200,
  "current": {
    "dt": 1769571220,
    "sunrise": 1769556885,
    "sunset": 1769597034,
    "temp": 20.98,
    "feels_like": 20.73,
    "pressure": 1021,
    "humidity": 61,
    "dew_point": 13.18,
    "uvi": 4.16,
    "clouds": 100,
    "visibility": 10000,
    "wind_speed": 3.22,
    "wind_deg": 154,
    "wind_gust": 4.61,
    "weather": [
      {
        "id": 804,
        "main": "Clouds",
        "description": "overcast clouds",
        "icon": "04d"
      }
    ],
    "rain": { "1h": 0.5 },  // Optional
    "snow": { "1h": 0.0 },  // Optional
    "solar_radiation": 450.5  // Optional, requires subscription
  },
  "hourly": [
    {
      "dt": 1769569200,
      "temp": 20.96,
      "feels_like": 20.73,
      "pressure": 1021,
      "humidity": 62,
      "dew_point": 13.41,
      "uvi": 2.75,
      "clouds": 100,
      "visibility": 10000,
      "wind_speed": 2.94,
      "wind_deg": 154,
      "wind_gust": 4.55,
      "weather": [...],
      "pop": 0,  // Probability of precipitation
      "rain": { "1h": 0.12 }  // Optional
    }
    // ... 48 hourly forecasts
  ],
  "daily": [
    {
      "dt": 1769576400,
      "sunrise": 1769556885,
      "sunset": 1769597034,
      "moonrise": 1769579580,
      "moonset": 1769539800,
      "moon_phase": 0.32,
      "summary": "Expect a day of partly cloudy with clear spells",
      "temp": {
        "day": 21.5,
        "min": 17.18,
        "max": 25.25,
        "night": 18.48,
        "eve": 22.6,
        "morn": 17.18
      },
      "feels_like": {
        "day": 21.25,
        "night": 18.37,
        "eve": 22.25,
        "morn": 17.25
      },
      "pressure": 1021,
      "humidity": 59,
      "dew_point": 13.16,
      "wind_speed": 5.72,
      "wind_deg": 136,
      "wind_gust": 9.08,
      "weather": [...],
      "clouds": 99,
      "pop": 0,
      "rain": 0.46,  // Optional
      "snow": 0.0,   // Optional
      "uvi": 6.15
    }
    // ... 8 daily forecasts
  ]
}
```

---

## Data Fields Available

### Current Weather Fields

| Field             | Type    | Unit           | Description              | Notes                                                                                                                                     |
| ----------------- | ------- | -------------- | ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `dt`              | integer | Unix timestamp | Time of data calculation | ✅                                                                                                                                         |
| `sunrise`         | integer | Unix timestamp | Sunrise time             | ✅                                                                                                                                         |
| `sunset`          | integer | Unix timestamp | Sunset time              | ✅                                                                                                                                         |
| `temp`            | float   | °C (metric)    | Current temperature      | ✅                                                                                                                                         |
| `feels_like`      | float   | °C (metric)    | Feels like temperature   | ✅                                                                                                                                         |
| `pressure`        | integer | hPa            | Atmospheric pressure     | ✅                                                                                                                                         |
| `humidity`        | integer | %              | Relative humidity        | ✅                                                                                                                                         |
| `dew_point`       | float   | °C             | Dew point temperature    | ✅                                                                                                                                         |
| `uvi`             | float   | -              | UV Index                 | ✅                                                                                                                                         |
| `clouds`          | integer | %              | Cloud cover              | ✅                                                                                                                                         |
| `visibility`      | integer | m              | Visibility               | ✅                                                                                                                                         |
| `wind_speed`      | float   | m/s (metric)   | Wind speed               | ✅                                                                                                                                         |
| `wind_deg`        | integer | ° (0-360)      | Wind direction           | ✅                                                                                                                                         |
| `wind_gust`       | float   | m/s            | Wind gust                | ✅                                                                                                                                         |
| `weather[]`       | array   | -              | Weather conditions       | ✅                                                                                                                                         |
| `rain.1h`         | float   | mm             | Rain volume (last hour)  | Optional                                                                                                                                  |
| `snow.1h`         | float   | mm             | Snow volume (last hour)  | Optional                                                                                                                                  |
| `solar_radiation` | float   | W/m²           | Solar radiation          | ⚠️ Requires subscription<br>💡 **Alternative:** Open-Meteo cung cấp `shortwave_radiation`, `direct_radiation`, `diffuse_radiation` miễn phí |

### Hourly Forecast Fields (48 hours)

| Field        | Type    | Unit           | Description                  | Notes    |
| ------------ | ------- | -------------- | ---------------------------- | -------- |
| `dt`         | integer | Unix timestamp | Time of forecast             | ✅        |
| `temp`       | float   | °C             | Temperature                  | ✅        |
| `feels_like` | float   | °C             | Feels like temperature       | ✅        |
| `pressure`   | integer | hPa            | Atmospheric pressure         | ✅        |
| `humidity`   | integer | %              | Relative humidity            | ✅        |
| `dew_point`  | float   | °C             | Dew point                    | ✅        |
| `uvi`        | float   | -              | UV Index                     | ✅        |
| `clouds`     | integer | %              | Cloud cover                  | ✅        |
| `visibility` | integer | m              | Visibility                   | ✅        |
| `wind_speed` | float   | m/s            | Wind speed                   | ✅        |
| `wind_deg`   | integer | °              | Wind direction               | ✅        |
| `wind_gust`  | float   | m/s            | Wind gust                    | ✅        |
| `weather[]`  | array   | -              | Weather conditions           | ✅        |
| `pop`        | float   | 0-1            | Probability of precipitation | ✅        |
| `rain.1h`    | float   | mm             | Rain volume                  | Optional |
| `snow.1h`    | float   | mm             | Snow volume                  | Optional |

### Daily Forecast Fields (8 days)

| Field              | Type    | Unit           | Description                  | Notes    |
| ------------------ | ------- | -------------- | ---------------------------- | -------- |
| `dt`               | integer | Unix timestamp | Date                         | ✅        |
| `sunrise`          | integer | Unix timestamp | Sunrise time                 | ✅        |
| `sunset`           | integer | Unix timestamp | Sunset time                  | ✅        |
| `moonrise`         | integer | Unix timestamp | Moonrise time                | ✅        |
| `moonset`          | integer | Unix timestamp | Moonset time                 | ✅        |
| `moon_phase`       | float   | 0-1            | Moon phase                   | ✅        |
| `summary`          | string  | -              | Daily summary                | ✅        |
| `temp.day`         | float   | °C             | Day temperature              | ✅        |
| `temp.min`         | float   | °C             | Minimum temperature          | ✅        |
| `temp.max`         | float   | °C             | Maximum temperature          | ✅        |
| `temp.night`       | float   | °C             | Night temperature            | ✅        |
| `temp.eve`         | float   | °C             | Evening temperature          | ✅        |
| `temp.morn`        | float   | °C             | Morning temperature          | ✅        |
| `feels_like.day`   | float   | °C             | Feels like (day)             | ✅        |
| `feels_like.night` | float   | °C             | Feels like (night)           | ✅        |
| `feels_like.eve`   | float   | °C             | Feels like (evening)         | ✅        |
| `feels_like.morn`  | float   | °C             | Feels like (morning)         | ✅        |
| `pressure`         | integer | hPa            | Atmospheric pressure         | ✅        |
| `humidity`         | integer | %              | Relative humidity            | ✅        |
| `dew_point`        | float   | °C             | Dew point                    | ✅        |
| `wind_speed`       | float   | m/s            | Wind speed                   | ✅        |
| `wind_deg`         | integer | °              | Wind direction               | ✅        |
| `wind_gust`        | float   | m/s            | Wind gust                    | ✅        |
| `weather[]`        | array   | -              | Weather conditions           | ✅        |
| `clouds`           | integer | %              | Cloud cover                  | ✅        |
| `pop`              | float   | 0-1            | Probability of precipitation | ✅        |
| `rain`             | float   | mm             | Rain volume                  | Optional |
| `snow`             | float   | mm             | Snow volume                  | Optional |
| `uvi`              | float   | -              | UV Index                     | ✅        |

### Weather Condition Object

Mỗi `weather` array chứa objects với:
- `id` (integer) - Weather condition ID
- `main` (string) - Main condition (e.g., "Clear", "Clouds", "Rain")
- `description` (string) - Detailed description (e.g., "clear sky", "overcast clouds")
- `icon` (string) - Icon code (e.g., "01d", "04n")

---

## Code Examples

### Example 1: Basic Request

```python
import requests
import os
from datetime import datetime

# Get API key from environment variable
API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")

url = "https://api.openweathermap.org/data/3.0/onecall"
params = {
    "lat": 21.0285,  # Hà Nội
    "lon": 105.8542,
    "appid": API_KEY,
    "units": "metric",
    "exclude": "minutely,alerts",
    "lang": "vi"
}

response = requests.get(url, params=params, timeout=10)
response.raise_for_status()
data = response.json()

# Current weather
current = data["current"]
print(f"Current Temperature: {current['temp']}°C")
print(f"Feels Like: {current['feels_like']}°C")
print(f"Humidity: {current['humidity']}%")
print(f"Wind Speed: {current['wind_speed']} m/s")
print(f"Description: {current['weather'][0]['description']}")

# Hourly forecast (first 5 hours)
print("\nHourly Forecast (next 5 hours):")
for hour in data["hourly"][:5]:
    dt = datetime.fromtimestamp(hour["dt"])
    print(f"{dt.strftime('%H:%M')}: {hour['temp']}°C, {hour['weather'][0]['description']}")

# Daily forecast
print("\nDaily Forecast:")
for day in data["daily"][:3]:
    dt = datetime.fromtimestamp(day["dt"])
    print(f"{dt.strftime('%Y-%m-%d')}: {day['temp']['min']}°C - {day['temp']['max']}°C, {day['summary']}")
```

### Example 2: Using OneCallCollector (from codebase)

```python
from app.services.data.collectors.onecall_collector import OneCallCollector
import os

# Initialize collector
api_key = os.getenv("OPENWEATHERMAP_API_KEY")
collector = OneCallCollector(api_key=api_key)

# Collect data for a district
district_id = "001"
lat = 21.0285
lon = 105.8542

# Get current + hourly forecast
result = collector.collect_for_district(district_id, lat, lon)
print(f"Data source: {result['data_source']}")
print(f"Temperature: {result['temperature']}°C")
print(f"Humidity: {result['relative_humidity']}%")

# Get hourly forecast only
hourly_forecast = collector.collect_hourly_forecast(district_id, lat, lon)
print(f"Hourly forecast: {len(hourly_forecast)} hours")
```

### Example 3: Process Full Response

```python
import requests
import pandas as pd
from datetime import datetime

API_KEY = "YOUR_API_KEY"

url = "https://api.openweathermap.org/data/3.0/onecall"
params = {
    "lat": 21.0285,
    "lon": 105.8542,
    "appid": API_KEY,
    "units": "metric",
    "exclude": "minutely,alerts"
}

response = requests.get(url, params=params)
data = response.json()

# Process current weather
current = data["current"]
current_df = pd.DataFrame([{
    "time": datetime.fromtimestamp(current["dt"]),
    "temp": current["temp"],
    "feels_like": current["feels_like"],
    "humidity": current["humidity"],
    "pressure": current["pressure"],
    "wind_speed": current["wind_speed"],
    "wind_deg": current["wind_deg"],
    "clouds": current["clouds"],
    "uvi": current["uvi"],
    "description": current["weather"][0]["description"]
}])

print("Current Weather:")
print(current_df)

# Process hourly forecast
hourly_data = []
for hour in data["hourly"]:
    hourly_data.append({
        "time": datetime.fromtimestamp(hour["dt"]),
        "temp": hour["temp"],
        "humidity": hour["humidity"],
        "wind_speed": hour["wind_speed"],
        "pop": hour["pop"],
        "description": hour["weather"][0]["description"]
    })

hourly_df = pd.DataFrame(hourly_data)
print(f"\nHourly Forecast ({len(hourly_df)} hours):")
print(hourly_df.head(10))

# Process daily forecast
daily_data = []
for day in data["daily"]:
    daily_data.append({
        "date": datetime.fromtimestamp(day["dt"]).date(),
        "temp_min": day["temp"]["min"],
        "temp_max": day["temp"]["max"],
        "humidity": day["humidity"],
        "wind_speed": day["wind_speed"],
        "pop": day["pop"],
        "summary": day["summary"]
    })

daily_df = pd.DataFrame(daily_data)
print(f"\nDaily Forecast ({len(daily_df)} days):")
print(daily_df)
```

### Example 4: Time Machine (Historical Data)

```python
import requests
from datetime import datetime, timedelta

API_KEY = "YOUR_API_KEY"

# Lấy dữ liệu 7 ngày trước
past_date = datetime.now() - timedelta(days=7)
timestamp = int(past_date.timestamp())

url = "https://api.openweathermap.org/data/3.0/onecall/timemachine"
params = {
    "lat": 21.0285,
    "lon": 105.8542,
    "dt": timestamp,
    "appid": API_KEY,
    "units": "metric",
    "lang": "vi"
}

response = requests.get(url, params=params)
data = response.json()

# Process historical data
if data.get("data"):
    historical = data["data"][0]
    print(f"Historical Weather at {datetime.fromtimestamp(historical['dt'])}:")
    print(f"  Temperature: {historical['temp']}°C")
    print(f"  Humidity: {historical['humidity']}%")
    print(f"  Wind Speed: {historical['wind_speed']} m/s")
    print(f"  Description: {historical['weather'][0]['description']}")
```

### Example 5: Day Summary

```python
import requests
from datetime import datetime, timedelta

API_KEY = "YOUR_API_KEY"

# Lấy summary cho hôm qua
yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

url = "https://api.openweathermap.org/data/3.0/onecall/day_summary"
params = {
    "lat": 21.0285,
    "lon": 105.8542,
    "date": yesterday,
    "appid": API_KEY,
    "units": "metric",
    "lang": "vi"
}

response = requests.get(url, params=params)
data = response.json()

print(f"Daily Summary for {data['date']}:")
print(f"  Temperature: {data['temperature']['min']}°C - {data['temperature']['max']}°C")
print(f"  Humidity: {data['humidity']['afternoon']}%")
print(f"  Precipitation: {data['precipitation']['total']} mm")
print(f"  Max Wind Speed: {data['wind']['max']['speed']} m/s")
```

### Example 6: Overview

```python
import requests

API_KEY = "YOUR_API_KEY"

url = "https://api.openweathermap.org/data/3.0/onecall/overview"
params = {
    "lat": 21.0285,
    "lon": 105.8542,
    "appid": API_KEY,
    "units": "metric",
    "lang": "vi"
}

response = requests.get(url, params=params)
data = response.json()

print(f"Weather Overview for {data['date']}:")
print(data['weather_overview'])
```

### Example 7: Error Handling with Retry

```python
import requests
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def get_onecall_data(lat, lon, api_key, max_retries=3):
    """Get One Call API data with retry logic."""
    url = "https://api.openweathermap.org/data/3.0/onecall"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key,
        "units": "metric",
        "exclude": "minutely,alerts"
    }
    
    # Setup session with retry
    session = requests.Session()
    retry_strategy = Retry(
        total=max_retries,
        backoff_factor=1.0,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    
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
    data = get_onecall_data(21.0285, 105.8542, "YOUR_API_KEY")
    print("Success!")
except ValueError as e:
    print(f"Error: {e}")
except ConnectionError as e:
    print(f"Connection error: {e}")
```

---

## Rate Limits & Best Practices

### Rate Limits

**Free Tier:**
- **Daily limit:** 1,000 calls/day
- **Per-minute limit:** 60 calls/minute (shared với Air Pollution API)
- **Monthly limit:** 1,000,000 calls/month

**Paid Tiers:**
- **Startup ($40/month):** 1,000 calls/minute, 1M calls/month
- **Developer ($150/month):** 1,000 calls/minute, 10M calls/month
- **Professional ($400/month):** 1,000 calls/minute, unlimited

### Best Practices

1. **Use `units=metric`:** Để có Celsius và m/s (phù hợp với Việt Nam)
2. **Exclude unnecessary data:** Sử dụng `exclude=minutely,alerts` để giảm response size
3. **Cache responses:** Cache với TTL 1 giờ cho forecast data
4. **Respect rate limits:** Implement rate limiting để tránh exceed daily limit
5. **Error handling:** Xử lý các lỗi:
   - 401: Invalid API key
   - 429: Rate limit exceeded (retry after delay)
   - 500-504: Server errors (retry with exponential backoff)
6. **Request optimization:** Chỉ request khi cần thiết, không spam requests

### Rate Limiting Example

```python
from collections import defaultdict
from datetime import date
import time

class RateLimiter:
    """Simple rate limiter for One Call API."""
    
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
        
        # Clean old minute calls (older than 1 minute)
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

## Tọa độ các thành phố Việt Nam

| Thành phố       | Latitude | Longitude |
| --------------- | -------- | --------- |
| Hà Nội          | 21.0285  | 105.8542  |
| TP. Hồ Chí Minh | 10.7769  | 106.7009  |
| Đà Nẵng         | 16.0544  | 108.2022  |
| Hải Phòng       | 20.8449  | 106.6881  |
| Cần Thơ         | 10.0452  | 105.7469  |

---

## Integration với Codebase

### OneCallCollector

Codebase đã có `OneCallCollector` tại:
- `backend/app/services/data/collectors/onecall_collector.py`

**Features:**
- Fetches current + hourly (48h) + daily (8 days) trong 1 call
- Normalizes data to CKG variable format
- Validates data với strict range checks
- Handles errors với retry logic và exponential backoff
- Respects rate limits (1000 calls/day)

**Usage:**
```python
from app.services.data.collectors.onecall_collector import OneCallCollector

collector = OneCallCollector(api_key=api_key)
result = collector.collect_for_district(district_id, lat, lon)
```

---

## Limitations

1. **API Key Required:** Cần đăng ký và có API key
2. **Daily Limit:** Free tier chỉ 1,000 calls/day
3. **Point-based:** Data cho một điểm (lat/lon), không phải grid
4. **Forecast Period:** Hourly chỉ 48 giờ, daily chỉ 8 ngày
5. **Solar Radiation:** Cần subscription để có solar_radiation data
6. **Update Frequency:** Dữ liệu được cập nhật hàng giờ, không real-time

---

## Comparison với các nguồn khác

### So sánh với Open-Meteo Weather API

| Feature       | OpenWeatherMap One Call 3.0                        | Open-Meteo Weather API                                                                                                                                              |
| ------------- | -------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **API Key**   | ✅ Required                                         | ❌ Not required                                                                                                                                                      |
| **Cost**      | Free tier: 1K calls/day                            | Free, unlimited                                                                                                                                                     |
| **Current**   | ✅ Yes                                              | ❌ No                                                                                                                                                                |
| **Hourly**    | ✅ 48 hours                                         | ✅ 7-16 days                                                                                                                                                         |
| **Daily**     | ✅ 8 days                                           | ✅ 7-16 days                                                                                                                                                         |
| **Solar Rad** | ⚠️ Requires subscription<br>(chỉ `solar_radiation`) | ✅ Free<br>(6 biến: `shortwave_radiation`, `direct_radiation`, `diffuse_radiation`, `direct_normal_irradiance`, `global_tilted_irradiance`, `terrestrial_radiation`) |
| **Variables** | ~20 main variables                                 | 49+ variables                                                                                                                                                       |
| **Accuracy**  | High (model + stations)                            | High (model-based)                                                                                                                                                  |

### Khi nào sử dụng One Call API 3.0?

✅ **Nên dùng khi:**
- Cần current weather data
- Cần hourly forecast 48h và daily forecast 8 days trong 1 call
- Có API key và budget cho paid tier nếu cần
- Cần data từ weather stations (không chỉ model)

❌ **Không nên dùng khi:**
- Cần forecast dài hơn 48 giờ (hourly) hoặc 8 ngày (daily)
- Không muốn quản lý API key
- Cần nhiều biến weather chi tiết (soil, radiation, etc.)
- Cần unlimited free calls
- **Cần solar radiation data** - Open-Meteo cung cấp 6 biến radiation miễn phí (`shortwave_radiation`, `direct_radiation`, `diffuse_radiation`, `direct_normal_irradiance`, `global_tilted_irradiance`, `terrestrial_radiation`) trong khi One Call API chỉ có `solar_radiation` và cần subscription

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

- **Official Documentation:** https://openweathermap.org/api/one-call-3
- **API Key Registration:** https://openweathermap.org/api
- **Pricing:** https://openweathermap.org/price
- **Codebase Collector:** `backend/app/services/data/collectors/onecall_collector.py`

---

## Test Results

### Test Date: 2026-02-08
### Test Location: Hà Nội (21.0285°N, 105.8542°E)
### API Key: Verified and working

**Test Results:**
- ✅ **Current + Forecast:** PASSED (200 OK)
  - Current weather: Available
  - Hourly forecast: 48 hours
  - Daily forecast: 8 days
  
- ✅ **Time Machine:** PASSED (200 OK)
  - Historical data: Available for past dates
  - Response contains 1 record for specified timestamp
  
- ✅ **Day Summary:** PASSED (200 OK)
  - Daily aggregated data: Available
  - Includes min/max temperatures, precipitation, wind max
  
- ✅ **Overview:** PASSED (200 OK)
  - Weather overview text: Available
  - AI-generated summary in requested language

---

## Changelog

- **2026-02-08:** Initial documentation
  - Documented One Call API 3.0 main endpoint
  - Added code examples
  - Documented rate limits và best practices
  - Added comparison với Open-Meteo

- **2026-02-08 (Updated):** Added all endpoints
  - Added Time Machine endpoint (historical data)
  - Added Day Summary endpoint (daily aggregated)
  - Added Overview endpoint (text summary)
  - Tested all 4 endpoints with Hà Nội coordinates
  - Verified API key and all endpoints working

---

**Last Updated:** 2026-02-08  
**API Version:** 3.0  
**Status:** ✅ All 4 endpoints tested and verified  
**Tested Endpoints:** Current+Forecast, Time Machine, Day Summary, Overview
