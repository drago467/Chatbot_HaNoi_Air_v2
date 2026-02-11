"""HanoiAir API ingestor.

This ingestor handles:
1. Syncing locations (126 wards + Hanoi city) from administrative API
2. Fetching current AQI/PM2.5 for wards
3. Fetching forecast AQI/PM2.5 for wards
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


class HanoiAirIngestor(BaseIngestor):
    """Ingestor for HanoiAir API."""
    
    BASE_URL = "https://geoi.com.vn"
    
    def __init__(self, db_conn: psycopg2.extensions.connection):
        """Initialize HanoiAir ingestor."""
        super().__init__(
            db_conn=db_conn,
            source_id="hanoiair",
            rate_limit_per_minute=None,  # No official limit, but be reasonable
            rate_limit_per_day=None
        )
    
    def sync_locations(self) -> int:
        """Sync locations from HanoiAir administrative API.
        
        Fetches all 126 wards + Hanoi city and populates locations table.
        
        Returns:
            Number of locations synced
        """
        logger.info("Syncing locations from HanoiAir...")
        
        endpoint = f"{self.BASE_URL}/api/administrative/administrative_province_district"
        params = {"province_id": "12", "lang_id": "vi"}
        
        # Log request
        request_id = self.log_request(endpoint, params)
        
        # Fetch data
        start_time = time.time()
        try:
            response = requests.get(endpoint, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            latency_ms = int((time.time() - start_time) * 1000)
            
            # Log response
            response_id = self.log_response(
                request_id=request_id,
                body_json=data,
                http_status=response.status_code,
                latency_ms=latency_ms,
                parse_status="success"
            )
            
            # Parse and insert locations
            locations_to_insert = []
            for item in data:
                if item.get("type") == "province":
                    # Hanoi city
                    locations_to_insert.append({
                        "hanoiair_internal_id": item.get("id"),
                        "name_vi": item.get("name", "Hà Nội"),
                        "name_norm": self._normalize_name(item.get("name", "Hà Nội")),
                        "type": "city",
                        "lat": None,  # Will get from province_extent
                        "lon": None,
                        "bbox": None
                    })
                elif item.get("type") == "district":
                    # Ward
                    locations_to_insert.append({
                        "hanoiair_internal_id": item.get("id"),
                        "name_vi": item.get("name"),
                        "name_norm": self._normalize_name(item.get("name")),
                        "type": "ward",
                        "lat": None,  # Will get from district info API
                        "lon": None,
                        "bbox": None
                    })
            
            # Get province extent for city
            province_extent = self._get_province_extent()
            if province_extent:
                for loc in locations_to_insert:
                    if loc["type"] == "city":
                        loc["lat"] = (province_extent["miny"] + province_extent["maxy"]) / 2
                        loc["lon"] = (province_extent["minx"] + province_extent["maxx"]) / 2
                        loc["bbox"] = {
                            "minx": province_extent["minx"],
                            "miny": province_extent["miny"],
                            "maxx": province_extent["maxx"],
                            "maxy": province_extent["maxy"]
                        }
            
            # Get district extent for each ward
            logger.info("Fetching bounding boxes for wards...")
            for loc in locations_to_insert:
                if loc["type"] == "ward" and loc["hanoiair_internal_id"]:
                    district_extent = self._get_district_extent(loc["hanoiair_internal_id"])
                    if district_extent:
                        loc["lat"] = (district_extent["miny"] + district_extent["maxy"]) / 2
                        loc["lon"] = (district_extent["minx"] + district_extent["maxx"]) / 2
                        loc["bbox"] = {
                            "minx": district_extent["minx"],
                            "miny": district_extent["miny"],
                            "maxx": district_extent["maxx"],
                            "maxy": district_extent["maxy"]
                        }
                    # Small delay to avoid overwhelming API
                    time.sleep(0.1)
            
            # Insert/update locations
            with self.db_conn.cursor() as cur:
                for loc in locations_to_insert:
                    cur.execute("""
                        INSERT INTO locations (
                            hanoiair_internal_id, name_vi, name_norm, type,
                            lat, lon, bbox, updated_at
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
                        ON CONFLICT (hanoiair_internal_id) DO UPDATE SET
                            name_vi = EXCLUDED.name_vi,
                            name_norm = EXCLUDED.name_norm,
                            lat = COALESCE(EXCLUDED.lat, locations.lat),
                            lon = COALESCE(EXCLUDED.lon, locations.lon),
                            bbox = COALESCE(EXCLUDED.bbox, locations.bbox),
                            updated_at = NOW()
                    """, (
                        loc["hanoiair_internal_id"],
                        loc["name_vi"],
                        loc["name_norm"],
                        loc["type"],
                        loc["lat"],
                        loc["lon"],
                        json.dumps(loc["bbox"]) if loc["bbox"] else None
                    ))
                self.db_conn.commit()
            
            logger.info(f"Synced {len(locations_to_insert)} locations")
            return len(locations_to_insert)
            
        except Exception as e:
            latency_ms = int((time.time() - start_time) * 1000)
            self.log_response(
                request_id=request_id,
                body_json={},
                http_status=500,
                latency_ms=latency_ms,
                parse_status="error",
                parse_error_message=str(e)
            )
            raise
    
    def _get_province_extent(self) -> Optional[Dict[str, float]]:
        """Get province bounding box."""
        endpoint = f"{self.BASE_URL}/api/administrative/province_extent"
        params = {"province_id": "12", "lang_id": "vi"}
        
        try:
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.warning(f"Failed to get province extent: {e}")
            return None
    
    def _get_district_extent(self, district_id: str) -> Optional[Dict[str, Any]]:
        """Get district bounding box.
        
        Args:
            district_id: HanoiAir internal_id (e.g., "ID_00364")
        
        Returns:
            Dict with id, name, minx, miny, maxx, maxy
        """
        endpoint = f"{self.BASE_URL}/api/administrative/district_extent"
        params = {"district_id": district_id, "lang_id": "vi"}
        
        try:
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.warning(f"Failed to get district extent for {district_id}: {e}")
            return None
    
    def _normalize_name(self, name: str) -> str:
        """Normalize location name for searching."""
        # Remove diacritics, lowercase, remove extra spaces
        import unicodedata
        normalized = unicodedata.normalize("NFD", name)
        ascii_name = "".join(
            c for c in normalized if unicodedata.category(c) != "Mn"
        )
        return " ".join(ascii_name.lower().split())
    
    def fetch_ward_forecast(
        self,
        district_id: str,
        location_id: int
    ) -> Dict[str, Any]:
        """Fetch forecast data for a ward.
        
        Args:
            district_id: HanoiAir internal_id (e.g., "ID_01889")
            location_id: location_id from database
        
        Returns:
            API response JSON
        """
        endpoint = f"{self.BASE_URL}/api/componentgeotiffdaily/identify_district_id_list_geotiff"
        params = {
            "district_id": district_id,
            "groupcomponent_id": "63",  # PM2.5
            "date_request": datetime.now().strftime("%Y-%m-%d"),
            "predays": 0,  # No historical, just current + forecast
            "nextdays": 9,  # 9 days forecast
            "lang_id": "vi"
        }
        
        request_id = self.log_request(endpoint, params, http_method="POST")
        
        start_time = time.time()
        try:
            response = requests.post(
                endpoint,
                json=params,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
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
            
            # Store response_id in data for parsing
            data["_response_id"] = response_id
            data["_location_id"] = location_id
            
            return data
            
        except Exception as e:
            latency_ms = int((time.time() - start_time) * 1000)
            self.log_response(
                request_id=request_id,
                body_json={},
                http_status=500,
                latency_ms=latency_ms,
                parse_status="error",
                parse_error_message=str(e)
            )
            raise
    
    def parse_forecast_response(
        self,
        response_json: Dict[str, Any],
        response_id: int,
        location_id: int
    ) -> List[Dict[str, Any]]:
        """Parse forecast response into forecasts_raw records.
        
        Returns:
            List of forecasts_raw records
        """
        records = []
        
        if not response_json.get("Data") or not response_json["Data"].get("comps"):
            return records
        
        issue_ts_utc = datetime.now().replace(microsecond=0)
        
        for comp in response_json["Data"]["comps"]:
            requestdate = comp.get("requestdate")
            if not requestdate:
                continue
            
            # Parse date
            try:
                target_ts_utc = datetime.strptime(requestdate, "%Y-%m-%d")
            except:
                continue
            
            val = comp.get("val")  # PM2.5 in µg/m³
            val_aqi = comp.get("val_aqi")  # AQI
            
            if val is not None:
                records.append({
                    "location_id": location_id,
                    "issue_ts_utc": issue_ts_utc,
                    "target_ts_utc": target_ts_utc,
                    "field": "pm25",
                    "value": float(val),
                    "unit": "µg/m³",
                    "source_id": self.source_id,
                    "response_id": response_id,
                    "forecast_horizon_hours": int(
                        (target_ts_utc - issue_ts_utc).total_seconds() / 3600
                    )
                })
            
            if val_aqi is not None:
                records.append({
                    "location_id": location_id,
                    "issue_ts_utc": issue_ts_utc,
                    "target_ts_utc": target_ts_utc,
                    "field": "aqi",
                    "value": float(val_aqi),
                    "unit": None,
                    "source_id": self.source_id,
                    "response_id": response_id,
                    "forecast_horizon_hours": int(
                        (target_ts_utc - issue_ts_utc).total_seconds() / 3600
                    )
                })
        
        return records
    
    def ingest_all_wards_forecast(self):
        """Ingest forecast for all wards.
        
        This is the main ingestion method that:
        1. Gets all ward locations from database
        2. Fetches forecast for each ward
        3. Parses and stores in forecasts_raw
        """
        logger.info("Ingesting forecasts for all wards...")
        
        # Get all ward locations
        with self.db_conn.cursor() as cur:
            cur.execute("""
                SELECT location_id, hanoiair_internal_id, name_vi
                FROM locations
                WHERE type = 'ward' AND hanoiair_internal_id IS NOT NULL
                ORDER BY location_id
            """)
            wards = cur.fetchall()
        
        logger.info(f"Found {len(wards)} wards to ingest")
        
        total_records = 0
        for ward_id, internal_id, name in wards:
            try:
                logger.info(f"Fetching forecast for {name} ({internal_id})...")
                
                # Fetch forecast
                response_json = self.fetch_ward_forecast(internal_id, ward_id)
                
                # Parse response
                records = self.parse_forecast_response(
                    response_json, response_json.get("response_id"), ward_id
                )
                
                # Insert records
                if records:
                    self._insert_forecasts_raw(records)
                    total_records += len(records)
                    logger.info(f"  Inserted {len(records)} forecast records")
                
                # Small delay to avoid overwhelming API
                time.sleep(0.5)
                
            except Exception as e:
                logger.error(f"Error ingesting {name}: {e}")
                continue
        
        logger.info(f"Total forecast records inserted: {total_records}")
    
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
        """Abstract method implementation - not used for HanoiAir."""
        raise NotImplementedError("HanoiAir uses specific methods like sync_locations()")
    
    def parse_response(
        self,
        response_json: Dict[str, Any],
        response_id: int,
        location_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Abstract method implementation - use parse_forecast_response instead."""
        return self.parse_forecast_response(response_json, response_id, location_id)
