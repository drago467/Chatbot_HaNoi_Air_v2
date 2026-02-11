"""Open-Meteo Air Quality API ingestor.

Fetches hourly air quality forecast (fallback for OpenWeather Air).
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


class OpenMeteoAirIngestor(BaseIngestor):
    """Ingestor for Open-Meteo Air Quality API."""
    
    BASE_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"
    
    def __init__(self, db_conn: psycopg2.extensions.connection):
        """Initialize Open-Meteo Air Quality ingestor."""
        super().__init__(
            db_conn=db_conn,
            source_id="openmeteo_air",
            rate_limit_per_minute=None,
            rate_limit_per_day=None
        )
    
    def fetch_data(
        self,
        lat: float,
        lon: float,
        location_id: int
    ) -> Dict[str, Any]:
        """Fetch hourly air quality forecast."""
        hourly_vars = [
            "pm10", "pm2_5", "carbon_monoxide", "nitrogen_dioxide",
            "sulphur_dioxide", "ozone", "european_aqi"
        ]
        
        params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": ",".join(hourly_vars),
            "timezone": "Asia/Ho_Chi_Minh",
            "forecast_days": 5
        }
        
        request_id = self.log_request(self.BASE_URL, params)
        
        start_time = time.time()
        response = None
        try:
            response = requests.get(self.BASE_URL, params=params, timeout=30)
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
            
            data["_response_id"] = response_id
            data["_location_id"] = location_id
            return data
            
        except Exception as e:
            latency_ms = int((time.time() - start_time) * 1000)
            self.log_response(
                request_id=request_id,
                body_json={},
                http_status=getattr(response, "status_code", 500),
                latency_ms=latency_ms,
                parse_status="error",
                parse_error_message=str(e)
            )
            raise
    
    def parse_response(
        self,
        response_json: Dict[str, Any],
        response_id: int,
        location_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Parse response into forecasts_raw."""
        records = []
        
        if "_response_id" in response_json:
            response_id = response_json["_response_id"]
        if "_location_id" in response_json:
            location_id = response_json["_location_id"]
        
        if not location_id or "hourly" not in response_json:
            return records
        
        issue_ts_utc = datetime.now().replace(microsecond=0)
        hourly = response_json["hourly"]
        times = hourly.get("time", [])
        
        field_mapping = {
            "pm2_5": ("pm25", "µg/m³"),
            "pm10": ("pm10", "µg/m³"),
            "carbon_monoxide": ("co", "µg/m³"),
            "nitrogen_dioxide": ("no2", "µg/m³"),
            "sulphur_dioxide": ("so2", "µg/m³"),
            "ozone": ("o3", "µg/m³"),
            "european_aqi": ("aqi_european", None),
        }
        
        for i, time_str in enumerate(times):
            try:
                target_ts_utc = datetime.fromisoformat(time_str.replace("Z", "+00:00"))
            except:
                continue
            
            for api_field, (canonical_field, unit) in field_mapping.items():
                if api_field in hourly:
                    values = hourly[api_field]
                    if i < len(values) and values[i] is not None:
                        records.append({
                            "location_id": location_id,
                            "issue_ts_utc": issue_ts_utc,
                            "target_ts_utc": target_ts_utc,
                            "field": canonical_field,
                            "value": float(values[i]),
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
        """Ingest data for a location."""
        logger.info(f"Ingesting Open-Meteo Air Quality for location {location_id}...")
        
        response_json = self.fetch_data(lat, lon, location_id)
        records = self.parse_response(
            response_json, response_json.get("_response_id"), location_id
        )
        
        if records:
            self._insert_forecasts_raw(records)
        
        logger.info(f"Inserted {len(records)} records")
        return len(records)
    
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
