"""OpenWeather Air Pollution API ingestor.

Fetches current + forecast (5 days, 120 hours) air pollution data.
"""

import json
import logging
import time
from datetime import datetime
from typing import Any, Dict, List, Optional

import psycopg2
import requests
from psycopg2.extras import execute_values

from .base_ingestor import BaseIngestor

logger = logging.getLogger(__name__)


class OpenWeatherAirIngestor(BaseIngestor):
    """Ingestor for OpenWeather Air Pollution API."""
    
    BASE_URL = "http://api.openweathermap.org/data/2.5/air_pollution"
    
    def __init__(
        self, 
        db_conn: psycopg2.extensions.connection, 
        api_key: Optional[str] = None,
        api_key_manager: Optional[Any] = None
    ):
        """Initialize OpenWeather Air ingestor.
        
        Args:
            db_conn: Database connection
            api_key: Single API key (for backward compatibility)
            api_key_manager: ApiKeyManager instance (preferred for multiple keys)
        """
        super().__init__(
            db_conn=db_conn,
            source_id="openweather_air",
            rate_limit_per_minute=60,  # Shared with One Call API
            rate_limit_per_day=1000,
            api_key_manager=api_key_manager
        )
        self.api_key = api_key  # For backward compatibility
        self.api_key_manager = api_key_manager
    
    def fetch_current(
        self,
        lat: float,
        lon: float,
        location_id: int
    ) -> Dict[str, Any]:
        """Fetch current air pollution."""
        endpoint = self.BASE_URL
        
        # Get API key with retry logic
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
                "appid": api_key
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
        
        if last_error:
            raise last_error
        raise Exception("All retry attempts failed")
    
    def fetch_forecast(
        self,
        lat: float,
        lon: float,
        location_id: int
    ) -> Dict[str, Any]:
        """Fetch forecast air pollution (5 days, 120 hours)."""
        endpoint = f"{self.BASE_URL}/forecast"
        
        # Get API key with retry logic
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
                "appid": api_key
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
        
        if last_error:
            raise last_error
        raise Exception("All retry attempts failed")
    
    def parse_current_response(
        self,
        response_json: Dict[str, Any],
        response_id: int,
        location_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Parse current response into observations_raw."""
        records = []
        
        if "_response_id" in response_json:
            response_id = response_json["_response_id"]
        if "_location_id" in response_json:
            location_id = response_json["_location_id"]
        
        if not location_id or "list" not in response_json or not response_json["list"]:
            return records
        
        current = response_json["list"][0]
        ts_utc = datetime.fromtimestamp(current["dt"])
        
        # AQI
        if "main" in current and "aqi" in current["main"]:
            records.append({
                "location_id": location_id,
                "ts_utc": ts_utc,
                "field": "aqi",
                "value": float(current["main"]["aqi"]),
                "unit": None,
                "source_id": self.source_id,
                "response_id": response_id,
                "quality_flags": json.dumps({"missing": False, "outlier": False})
            })
        
        # Pollutants
        if "components" in current:
            components = current["components"]
            field_mapping = {
                "pm2_5": ("pm25", "µg/m³"),
                "pm10": ("pm10", "µg/m³"),
                "no2": ("no2", "µg/m³"),
                "so2": ("so2", "µg/m³"),
                "o3": ("o3", "µg/m³"),
                "co": ("co", "µg/m³"),
                "nh3": ("nh3", "µg/m³"),
                "no": ("no", "µg/m³")
            }
            
            for api_field, (canonical_field, unit) in field_mapping.items():
                if api_field in components and components[api_field] is not None:
                    records.append({
                        "location_id": location_id,
                        "ts_utc": ts_utc,
                        "field": canonical_field,
                        "value": float(components[api_field]),
                        "unit": unit,
                        "source_id": self.source_id,
                        "response_id": response_id,
                        "quality_flags": json.dumps({"missing": False, "outlier": False})
                    })
        
        return records
    
    def parse_forecast_response(
        self,
        response_json: Dict[str, Any],
        response_id: int,
        location_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Parse forecast response into forecasts_raw."""
        records = []
        
        if "_response_id" in response_json:
            response_id = response_json["_response_id"]
        if "_location_id" in response_json:
            location_id = response_json["_location_id"]
        
        if not location_id or "list" not in response_json:
            return records
        
        issue_ts_utc = datetime.now().replace(microsecond=0)
        
        for item in response_json["list"]:
            target_ts_utc = datetime.fromtimestamp(item["dt"])
            
            # AQI
            if "main" in item and "aqi" in item["main"]:
                records.append({
                    "location_id": location_id,
                    "issue_ts_utc": issue_ts_utc,
                    "target_ts_utc": target_ts_utc,
                    "field": "aqi",
                    "value": float(item["main"]["aqi"]),
                    "unit": None,
                    "source_id": self.source_id,
                    "response_id": response_id,
                    "forecast_horizon_hours": int(
                        (target_ts_utc - issue_ts_utc).total_seconds() / 3600
                    )
                })
            
            # Pollutants
            if "components" in item:
                components = item["components"]
                field_mapping = {
                    "pm2_5": ("pm25", "µg/m³"),
                    "pm10": ("pm10", "µg/m³"),
                    "no2": ("no2", "µg/m³"),
                    "so2": ("so2", "µg/m³"),
                    "o3": ("o3", "µg/m³"),
                    "co": ("co", "µg/m³"),
                    "nh3": ("nh3", "µg/m³"),
                    "no": ("no", "µg/m³")
                }
                
                for api_field, (canonical_field, unit) in field_mapping.items():
                    if api_field in components and components[api_field] is not None:
                        records.append({
                            "location_id": location_id,
                            "issue_ts_utc": issue_ts_utc,
                            "target_ts_utc": target_ts_utc,
                            "field": canonical_field,
                            "value": float(components[api_field]),
                            "unit": unit,
                            "source_id": self.source_id,
                            "response_id": response_id,
                            "forecast_horizon_hours": int(
                                (target_ts_utc - issue_ts_utc).total_seconds() / 3600
                            )
                        })
        
        return records
    
    def ingest_location(
        self,
        location_id: int,
        lat: float,
        lon: float
    ) -> int:
        """Ingest current + forecast for a location."""
        logger.info(f"Ingesting OpenWeather Air for location {location_id}...")
        
        total_records = 0
        
        # Fetch current
        try:
            current_response = self.fetch_current(lat, lon, location_id)
            current_records = self.parse_current_response(
                current_response, current_response.get("_response_id"), location_id
            )
            if current_records:
                self._insert_observations_raw(current_records)
                total_records += len(current_records)
        except Exception as e:
            logger.error(f"Error fetching current air pollution: {e}")
        
        # Fetch forecast
        try:
            forecast_response = self.fetch_forecast(lat, lon, location_id)
            forecast_records = self.parse_forecast_response(
                forecast_response, forecast_response.get("_response_id"), location_id
            )
            if forecast_records:
                self._insert_forecasts_raw(forecast_records)
                total_records += len(forecast_records)
        except Exception as e:
            logger.error(f"Error fetching forecast air pollution: {e}")
        
        logger.info(f"Inserted {total_records} records")
        return total_records
    
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
        """Upsert forecast snapshots into forecasts_canonical."""
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
    
    def fetch_data(self, *args, **kwargs) -> Dict[str, Any]:
        """Abstract method implementation - use fetch_current or fetch_forecast instead."""
        raise NotImplementedError("Use fetch_current() or fetch_forecast() instead")
    
    def parse_response(
        self,
        response_json: Dict[str, Any],
        response_id: int,
        location_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Abstract method implementation - use parse_current_response or parse_forecast_response instead."""
        # Try to determine if it's current or forecast
        if "list" in response_json and len(response_json.get("list", [])) == 1:
            return self.parse_current_response(response_json, response_id, location_id)
        else:
            return self.parse_forecast_response(response_json, response_id, location_id)
