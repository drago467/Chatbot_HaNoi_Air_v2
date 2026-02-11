"""Fuse observations_raw into observations_canonical."""

import json
import logging
from datetime import datetime, timedelta
from typing import List, Optional

import psycopg2
from psycopg2.extras import execute_values

from .fusion_config import (
    get_freshness_window,
    get_field_priority,
)

logger = logging.getLogger(__name__)


class ObservationsFusionJob:
    """Fuse observations from multiple sources into canonical table."""
    
    def __init__(self, db_conn: psycopg2.extensions.connection):
        """Initialize fusion job."""
        self.db_conn = db_conn
    
    def fuse_observations(
        self,
        location_id: Optional[int] = None,
        ts_start: Optional[datetime] = None,
        ts_end: Optional[datetime] = None
    ) -> int:
        """Fuse observations for given location and time range.
        
        Args:
            location_id: If None, fuse for all locations
            ts_start: Start time (default: now - 1 hour)
            ts_end: End time (default: now)
        
        Returns:
            Number of canonical records created/updated
        """
        if ts_end is None:
            ts_end = datetime.now()
        if ts_start is None:
            ts_start = ts_end - timedelta(hours=1)
        
        logger.info(
            f"Fusing observations: location_id={location_id}, "
            f"ts_start={ts_start}, ts_end={ts_end}"
        )
        
        # Get all unique (location_id, ts_utc, field) combinations
        with self.db_conn.cursor() as cur:
            if location_id:
                cur.execute("""
                    SELECT DISTINCT location_id, ts_utc, field
                    FROM observations_raw
                    WHERE location_id = %s
                      AND ts_utc >= %s AND ts_utc <= %s
                    ORDER BY location_id, ts_utc, field
                """, (location_id, ts_start, ts_end))
            else:
                cur.execute("""
                    SELECT DISTINCT location_id, ts_utc, field
                    FROM observations_raw
                    WHERE ts_utc >= %s AND ts_utc <= %s
                    ORDER BY location_id, ts_utc, field
                """, (ts_start, ts_end))
            
            combinations = cur.fetchall()
        
        logger.info(f"Found {len(combinations)} (location, time, field) combinations")
        
        total_fused = 0
        for loc_id, ts_utc, field in combinations:
            try:
                canonical_record = self._fuse_single_observation(
                    loc_id, ts_utc, field
                )
                if canonical_record:
                    self._upsert_canonical(canonical_record)
                    total_fused += 1
            except Exception as e:
                logger.error(
                    f"Error fusing {loc_id}/{ts_utc}/{field}: {e}"
                )
                continue
        
        logger.info(f"Fused {total_fused} canonical observations")
        return total_fused
    
    def _fuse_single_observation(
        self,
        location_id: int,
        ts_utc: datetime,
        field: str
    ) -> Optional[dict]:
        """Fuse a single observation from multiple sources.
        
        Returns:
            Canonical record dict or None if no valid data
        """
        # Get priority list for this field
        priority_sources = get_field_priority(field)
        if not priority_sources:
            logger.warning(f"No priority defined for field: {field}")
            return None
        
        # Get freshness window
        freshness_minutes = get_freshness_window(field)
        ts_window_start = ts_utc - timedelta(minutes=freshness_minutes)
        ts_window_end = ts_utc + timedelta(minutes=freshness_minutes)
        
        # Fetch all raw observations in freshness window
        with self.db_conn.cursor() as cur:
            cur.execute("""
                SELECT obs_id, source_id, value, unit, response_id, quality_flags
                FROM observations_raw
                WHERE location_id = %s
                  AND field = %s
                  AND ts_utc >= %s AND ts_utc <= %s
                  AND (quality_flags->>'outlier')::boolean IS NOT TRUE
                ORDER BY
                    CASE source_id
                        WHEN %s THEN 1
                        WHEN %s THEN 2
                        WHEN %s THEN 3
                        WHEN %s THEN 4
                        WHEN %s THEN 5
                        ELSE 999
                    END,
                    ABS(EXTRACT(EPOCH FROM (ts_utc - %s)))
                LIMIT 1
            """, (
                location_id, field, ts_window_start, ts_window_end,
                priority_sources[0] if len(priority_sources) > 0 else None,
                priority_sources[1] if len(priority_sources) > 1 else None,
                priority_sources[2] if len(priority_sources) > 2 else None,
                priority_sources[3] if len(priority_sources) > 3 else None,
                priority_sources[4] if len(priority_sources) > 4 else None,
                ts_utc
            ))
            
            result = cur.fetchone()
            if not result:
                return None
            
            obs_id, source_id, value, unit, response_id, quality_flags = result
            
            # Build provenance
            provenance = {
                "selected_source": source_id,
                "raw_obs_ids": [obs_id],
                "fusion_method": "priority_based",
                "confidence": 1.0,
                "freshness_window_minutes": freshness_minutes
            }
            
            return {
                "location_id": location_id,
                "ts_utc": ts_utc,
                "field": field,
                "value": float(value),
                "unit": unit,
                "provenance": json.dumps(provenance)
            }
    
    def _upsert_canonical(self, record: dict):
        """Insert or update canonical observation."""
        with self.db_conn.cursor() as cur:
            cur.execute("""
                INSERT INTO observations_canonical (
                    location_id, ts_utc, field, value, unit, provenance,
                    updated_at
                ) VALUES (%s, %s, %s, %s, %s, %s, NOW())
                ON CONFLICT (location_id, ts_utc, field) DO UPDATE SET
                    value = EXCLUDED.value,
                    unit = EXCLUDED.unit,
                    provenance = EXCLUDED.provenance,
                    updated_at = NOW()
            """, (
                record["location_id"],
                record["ts_utc"],
                record["field"],
                record["value"],
                record["unit"],
                record["provenance"]
            ))
            self.db_conn.commit()
