"""OpenWeather One Call API 3.0 ingestor.

Fetches current + hourly (48h) + daily (8 days) weather data.
"""

import json
import logging
import os
import time
from datetime import datetime
from typing import Any, Dict, List, Optional

import psycopg2
import requests
from psycopg2.extras import execute_values

from .base_ingestor import BaseIngestor

logger = logging.getLogger(__name__)


class OpenWeatherOneCallIngestor(BaseIngestor):
    """Ingestor for OpenWeather One Call API 3.0."""
    
    BASE_URL = "https://api.openweathermap.org/data/3.0/onecall"
    
    def __init__(
        self, 
        db_conn: psycopg2.extensions.connection, 
        api_key: Optional[str] = None,
        api_key_manager: Optional[Any] = None
    ):
        """Initialize OpenWeather One Call ingestor.
        
        Args:
            db_conn: Database connection
            api_key: Single API key (for backward compatibility)
            api_key_manager: ApiKeyManager instance (preferred for multiple keys)
        """
        super().__init__(
            db_conn=db_conn,
            source_id="openweather_onecall",
            rate_limit_per_minute=60,  # Shared with Air Pollution API
            rate_limit_per_day=1000,
            api_key_manager=api_key_manager
        )
        self.api_key = api_key  # For backward compatibility
        self.api_key_manager = api_key_manager
    
    def fetch_data(
        self,
        lat: float,
        lon: float,
        location_id: int
    ) -> Dict[str, Any]:
        """Fetch current + hourly + daily forecast.
        
        Args:
            lat: Latitude
            lon: Longitude
            location_id: location_id from database
        
        Returns:
            API response JSON
        """
        endpoint = self.BASE_URL
        
        # Get API key (from manager if available, otherwise use single key)
        # Retry with different key if 401 (unauthorized) or 429 (rate limit)
        max_retries = 3 if self.api_key_manager else 1
        last_error = None
        
        for attempt in range(max_retries):
            api_key = None
            key_id = None
            if self.api_key_manager:
                try:
                    api_key, key_id = self.api_key_manager.get_next_key()
                except ValueError as e:
                    if attempt == 0:
                        logger.error(f"No available API keys: {e}")
                    raise
            else:
                api_key = self.api_key
                if not api_key:
                    raise ValueError("No API key provided and no key manager available")
            
            params = {
                "lat": lat,
                "lon": lon,
                "appid": api_key,
                "units": "metric",
                "exclude": "minutely,alerts",
                "lang": "vi"
            }
            
            request_id = self.log_request(endpoint, params, api_key_id=key_id)
            self.check_rate_limit()
            
            start_time = time.time()
            response = None
            try:
                response = requests.get(endpoint, params=params, timeout=30)
                response.raise_for_status()
                data = response.json()
                latency_ms = int((time.time() - start_time) * 1000)
                
                response_id = self.log_response(
                    request_id=request_id,
                    body_json=data,
                    http_status=response.status_code,
                    latency_ms=latency_ms,
                    parse_status="success"
                )
                
                # Record successful call in key manager
                if self.api_key_manager and key_id:
                    self.api_key_manager.record_call(key_id, success=True)
                
                # Store response_id in data for parsing
                data["_response_id"] = response_id
                data["_location_id"] = location_id
                
                return data
                
            except requests.exceptions.HTTPError as e:
                latency_ms = int((time.time() - start_time) * 1000)
                error_code = e.response.status_code if e.response else None
                last_error = e
                
                # Record failed call in key manager
                if self.api_key_manager and key_id:
                    self.api_key_manager.record_call(key_id, success=False, error_code=error_code)
                
                self.log_response(
                    request_id=request_id,
                    body_json={},
                    http_status=error_code or 500,
                    latency_ms=latency_ms,
                    parse_status="error",
                    parse_error_message=str(e)
                )
                
                # Retry with different key if 401 or 429
                if self.api_key_manager and error_code in (401, 429) and attempt < max_retries - 1:
                    logger.warning(f"Key {key_id} failed with {error_code}, trying next key...")
                    continue
                else:
                    raise
                    
            except Exception as e:
                latency_ms = int((time.time() - start_time) * 1000)
                last_error = e
                
                # Record failed call in key manager
                if self.api_key_manager and key_id:
                    self.api_key_manager.record_call(key_id, success=False)
                
                self.log_response(
                    request_id=request_id,
                    body_json={},
                    http_status=getattr(response, "status_code", 500) if response else 500,
                    latency_ms=latency_ms,
                    parse_status="error",
                    parse_error_message=str(e)
                )
                
                if attempt < max_retries - 1:
                    logger.warning(f"Request failed, retrying with different key...")
                    continue
                else:
                    raise
        
        # If we get here, all retries failed
        if last_error:
            raise last_error
        raise Exception("All retry attempts failed")
    
    def parse_response(
        self,
        response_json: Dict[str, Any],
        response_id: int,
        location_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Parse response into observations_raw and forecasts_raw records."""
        records = []
        
        # Use stored IDs if available
        if "_response_id" in response_json:
            response_id = response_json["_response_id"]
        if "_location_id" in response_json:
            location_id = response_json["_location_id"]
        
        if not location_id:
            raise ValueError("location_id is required")
        
        # Parse current weather (observation)
        if "current" in response_json:
            current = response_json["current"]
            current_ts = datetime.fromtimestamp(current["dt"])
            
            # Map current fields to observations_raw
            field_mapping = {
                "temp": ("temperature", "°C"),
                "feels_like": ("feels_like_temperature", "°C"),
                "pressure": ("pressure", "hPa"),
                "humidity": ("relative_humidity", "%"),
                "dew_point": ("dew_point", "°C"),
                "uvi": ("uv_index", None),
                "clouds": ("cloud_cover", "%"),
                "visibility": ("visibility", "m"),
                "wind_speed": ("wind_speed", "m/s"),
                "wind_deg": ("wind_direction", "°"),
                "wind_gust": ("wind_gust", "m/s"),
            }
            
            for api_field, (canonical_field, unit) in field_mapping.items():
                if api_field in current and current[api_field] is not None:
                    records.append({
                        "location_id": location_id,
                        "ts_utc": current_ts,
                        "field": canonical_field,
                        "value": float(current[api_field]),
                        "unit": unit,
                        "source_id": self.source_id,
                        "response_id": response_id,
                        "quality_flags": json.dumps({"missing": False, "outlier": False})
                    })
            
            # Rain/Snow (optional)
            if "rain" in current and "1h" in current["rain"]:
                records.append({
                    "location_id": location_id,
                    "ts_utc": current_ts,
                    "field": "precipitation",
                    "value": float(current["rain"]["1h"]),
                    "unit": "mm",
                    "source_id": self.source_id,
                    "response_id": response_id,
                    "quality_flags": json.dumps({"missing": False, "outlier": False})
                })
        
        # Parse hourly forecast (forecasts_raw)
        if "hourly" in response_json:
            issue_ts = datetime.now().replace(microsecond=0)
            
            for hour_data in response_json["hourly"]:
                target_ts = datetime.fromtimestamp(hour_data["dt"])
                
                # Same field mapping as current
                for api_field, (canonical_field, unit) in field_mapping.items():
                    if api_field in hour_data and hour_data[api_field] is not None:
                        records.append({
                            "location_id": location_id,
                            "issue_ts_utc": issue_ts,
                            "target_ts_utc": target_ts,
                            "field": canonical_field,
                            "value": float(hour_data[api_field]),
                            "unit": unit,
                            "source_id": self.source_id,
                            "response_id": response_id,
                            "forecast_horizon_hours": int(
                                (target_ts - issue_ts).total_seconds() / 3600
                            )
                        })
                
                # Precipitation probability
                if "pop" in hour_data:
                    records.append({
                        "location_id": location_id,
                        "issue_ts_utc": issue_ts,
                        "target_ts_utc": target_ts,
                        "field": "precipitation_probability",
                        "value": float(hour_data["pop"]) * 100,  # Convert 0-1 to 0-100%
                        "unit": "%",
                        "source_id": self.source_id,
                        "response_id": response_id,
                        "forecast_horizon_hours": int(
                            (target_ts - issue_ts).total_seconds() / 3600
                        )
                    })
        
        # Parse daily forecast (forecasts_raw)
        if "daily" in response_json:
            issue_ts = datetime.now().replace(microsecond=0)
            
            for day_data in response_json["daily"]:
                target_ts = datetime.fromtimestamp(day_data["dt"]).replace(hour=12, minute=0)
                
                # Daily aggregates
                if "temp" in day_data:
                    temp = day_data["temp"]
                    for temp_key in ["min", "max", "day", "night", "eve", "morn"]:
                        if temp_key in temp and temp[temp_key] is not None:
                            records.append({
                                "location_id": location_id,
                                "issue_ts_utc": issue_ts,
                                "target_ts_utc": target_ts,
                                "field": f"temperature_{temp_key}",
                                "value": float(temp[temp_key]),
                                "unit": "°C",
                                "source_id": self.source_id,
                                "response_id": response_id,
                                "forecast_horizon_hours": int(
                                    (target_ts - issue_ts).total_seconds() / 3600
                                )
                            })
                
                # Other daily fields
                daily_fields = {
                    "pressure": ("pressure", "hPa"),
                    "humidity": ("relative_humidity", "%"),
                    "dew_point": ("dew_point", "°C"),
                    "wind_speed": ("wind_speed", "m/s"),
                    "wind_deg": ("wind_direction", "°"),
                    "wind_gust": ("wind_gust", "m/s"),
                    "clouds": ("cloud_cover", "%"),
                    "uvi": ("uv_index", None),
                    "pop": ("precipitation_probability", "%")
                }
                
                for api_field, (canonical_field, unit) in daily_fields.items():
                    if api_field in day_data and day_data[api_field] is not None:
                        value = float(day_data[api_field])
                        if api_field == "pop":
                            value = value * 100  # Convert to percentage
                        
                        records.append({
                            "location_id": location_id,
                            "issue_ts_utc": issue_ts,
                            "target_ts_utc": target_ts,
                            "field": canonical_field,
                            "value": value,
                            "unit": unit,
                            "source_id": self.source_id,
                            "response_id": response_id,
                            "forecast_horizon_hours": int(
                                (target_ts - issue_ts).total_seconds() / 3600
                            )
                        })
        
        return records
    
    def ingest_location(
        self,
        location_id: int,
        lat: float,
        lon: float
    ) -> int:
        """Ingest data for a single location.
        
        Returns:
            Number of records inserted
        """
        logger.info(f"Ingesting OpenWeather One Call for location {location_id}...")
        
        # Fetch data
        response_json = self.fetch_data(lat, lon, location_id)
        
        # Parse response
        records = self.parse_response(response_json, response_json.get("_response_id"), location_id)
        
        # Split into observations and forecasts
        observations = [r for r in records if "issue_ts_utc" not in r]
        forecasts = [r for r in records if "issue_ts_utc" in r]
        
        # Insert observations
        if observations:
            self._insert_observations_raw(observations)
        
        # Insert forecasts
        if forecasts:
            self._insert_forecasts_raw(forecasts)
        
        total = len(observations) + len(forecasts)
        logger.info(f"Inserted {total} records ({len(observations)} obs, {len(forecasts)} forecasts)")
        return total
    
    def _insert_observations_raw(self, records: List[Dict[str, Any]]):
        """Insert observations_raw records."""
        if not records:
            return
        
        with self.db_conn.cursor() as cur:
            execute_values(
                cur,
                """
                INSERT INTO observations_raw (
                    location_id, ts_utc, field, value, unit, source_id,
                    response_id, quality_flags
                ) VALUES %s
                ON CONFLICT (location_id, ts_utc, field, source_id)
                DO UPDATE SET
                    value = EXCLUDED.value,
                    unit = EXCLUDED.unit,
                    response_id = EXCLUDED.response_id,
                    quality_flags = EXCLUDED.quality_flags
                """,
                [(
                    r["location_id"],
                    r["ts_utc"],
                    r["field"],
                    r["value"],
                    r["unit"],
                    self.source_id,
                    r["response_id"],
                    r.get("quality_flags", "{}")
                ) for r in records]
            )
            self.db_conn.commit()
    
    def _insert_forecasts_raw(self, records: List[Dict[str, Any]]):
        """Upsert forecast snapshots into forecasts_canonical.

        Thay vì lưu mọi lần chạy (issue_ts_utc) vào forecasts_raw, ta lưu
        snapshot mới nhất cho mỗi (location_id, target_ts_utc, field) vào
        forecasts_canonical để phục vụ chatbot giải thích.
        """
        if not records:
            return
        
        with self.db_conn.cursor() as cur:
            execute_values(
                cur,
                """
                INSERT INTO forecasts_canonical (
                    location_id, issue_ts_utc, target_ts_utc, field,
                    value, unit, provenance
                ) VALUES %s
                ON CONFLICT (location_id, target_ts_utc, field)
                DO UPDATE SET
                    value = EXCLUDED.value,
                    unit = EXCLUDED.unit,
                    provenance = EXCLUDED.provenance,
                    issue_ts_utc = EXCLUDED.issue_ts_utc,
                    updated_at = NOW()
                """,
                [(
                    r["location_id"],
                    r["issue_ts_utc"],
                    r["target_ts_utc"],
                    r["field"],
                    r["value"],
                    r["unit"],
                    json.dumps(
                        {
                            "selected_source": self.source_id,
                            "response_id": r.get("response_id"),
                            "forecast_horizon_hours": r.get("forecast_horizon_hours"),
                        }
                    ),
                ) for r in records]
            )
            self.db_conn.commit()
