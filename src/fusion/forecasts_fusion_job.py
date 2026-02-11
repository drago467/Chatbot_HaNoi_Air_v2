"""Fuse forecasts_raw into forecasts_canonical."""

import json
import logging
from datetime import datetime, timedelta
from typing import List, Optional

import psycopg2
from psycopg2.extras import execute_values

from .fusion_config import get_field_priority

logger = logging.getLogger(__name__)


class ForecastsFusionJob:
    """[DEPRECATED] Legacy fusion job for forecasts_raw -> forecasts_canonical.

    Thiết kế mới đã upsert trực tiếp snapshot forecast vào forecasts_canonical
    trong ingestion layer, nên job này không còn được gọi trong pipeline chính.
    Vẫn giữ lại file để tham khảo trong luận văn (so sánh hai kiến trúc)."""
    
    def __init__(self, db_conn: psycopg2.extensions.connection):
        """Initialize fusion job."""
        self.db_conn = db_conn
    
    def fuse_forecasts(
        self,
        location_id: Optional[int] = None,
        issue_ts_start: Optional[datetime] = None,
        issue_ts_end: Optional[datetime] = None
    ) -> int:
        """Fuse forecasts for given location and issue time range.
        
        Args:
            location_id: If None, fuse for all locations
            issue_ts_start: Start issue time (default: now - 6 hours)
            issue_ts_end: End issue time (default: now)
        
        Returns:
            Number of canonical records created/updated
        """
        if issue_ts_end is None:
            issue_ts_end = datetime.now()
        if issue_ts_start is None:
            issue_ts_start = issue_ts_end - timedelta(hours=6)
        
        logger.info(
            f"Fusing forecasts: location_id={location_id}, "
            f"issue_ts_start={issue_ts_start}, issue_ts_end={issue_ts_end}"
        )
        
        # Get all unique (location_id, issue_ts_utc, target_ts_utc, field) combinations
        with self.db_conn.cursor() as cur:
            if location_id:
                cur.execute("""
                    SELECT DISTINCT location_id, issue_ts_utc, target_ts_utc, field
                    FROM forecasts_raw
                    WHERE location_id = %s
                      AND issue_ts_utc >= %s AND issue_ts_utc <= %s
                    ORDER BY location_id, issue_ts_utc, target_ts_utc, field
                """, (location_id, issue_ts_start, issue_ts_end))
            else:
                cur.execute("""
                    SELECT DISTINCT location_id, issue_ts_utc, target_ts_utc, field
                    FROM forecasts_raw
                    WHERE issue_ts_utc >= %s AND issue_ts_utc <= %s
                    ORDER BY location_id, issue_ts_utc, target_ts_utc, field
                """, (issue_ts_start, issue_ts_end))
            
            combinations = cur.fetchall()
        
        logger.info(f"Found {len(combinations)} (location, issue, target, field) combinations")
        
        total_fused = 0
        for loc_id, issue_ts, target_ts, field in combinations:
            try:
                canonical_record = self._fuse_single_forecast(
                    loc_id, issue_ts, target_ts, field
                )
                if canonical_record:
                    self._upsert_canonical(canonical_record)
                    total_fused += 1
            except Exception as e:
                logger.error(
                    f"Error fusing {loc_id}/{issue_ts}/{target_ts}/{field}: {e}"
                )
                continue
        
        logger.info(f"Fused {total_fused} canonical forecasts")
        return total_fused
    
    def _fuse_single_forecast(
        self,
        location_id: int,
        issue_ts_utc: datetime,
        target_ts_utc: datetime,
        field: str
    ) -> Optional[dict]:
        """Fuse a single forecast from multiple sources.
        
        Prefer most recent issue_ts_utc, then highest priority source.
        """
        priority_sources = get_field_priority(field)
        if not priority_sources:
            logger.warning(f"No priority defined for field: {field}")
            return None
        
        # Fetch all raw forecasts, prefer most recent issue_ts
        with self.db_conn.cursor() as cur:
            cur.execute("""
                SELECT forecast_id, source_id, value, unit, response_id
                FROM forecasts_raw
                WHERE location_id = %s
                  AND issue_ts_utc = %s
                  AND target_ts_utc = %s
                  AND field = %s
                ORDER BY
                    CASE source_id
                        WHEN %s THEN 1
                        WHEN %s THEN 2
                        WHEN %s THEN 3
                        WHEN %s THEN 4
                        WHEN %s THEN 5
                        ELSE 999
                    END
                LIMIT 1
            """, (
                location_id, issue_ts_utc, target_ts_utc, field,
                priority_sources[0] if len(priority_sources) > 0 else None,
                priority_sources[1] if len(priority_sources) > 1 else None,
                priority_sources[2] if len(priority_sources) > 2 else None,
                priority_sources[3] if len(priority_sources) > 3 else None,
                priority_sources[4] if len(priority_sources) > 4 else None,
            ))
            
            result = cur.fetchone()
            if not result:
                return None
            
            forecast_id, source_id, value, unit, response_id = result
            
            # Build provenance
            provenance = {
                "selected_source": source_id,
                "raw_forecast_ids": [forecast_id],
                "fusion_method": "priority_based",
                "confidence": 1.0
            }
            
            return {
                "location_id": location_id,
                "issue_ts_utc": issue_ts_utc,
                "target_ts_utc": target_ts_utc,
                "field": field,
                "value": float(value),
                "unit": unit,
                "provenance": json.dumps(provenance)
            }
    
    def _upsert_canonical(self, record: dict):
        """Insert or update canonical forecast (legacy API, unused in new pipeline)."""
        with self.db_conn.cursor() as cur:
            cur.execute("""
                INSERT INTO forecasts_canonical (
                    location_id, issue_ts_utc, target_ts_utc, field, value, unit,
                    provenance, updated_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
                ON CONFLICT (location_id, target_ts_utc, field) DO UPDATE SET
                    value = EXCLUDED.value,
                    unit = EXCLUDED.unit,
                    provenance = EXCLUDED.provenance,
                    updated_at = NOW()
            """, (
                record["location_id"],
                record["issue_ts_utc"],
                record["target_ts_utc"],
                record["field"],
                record["value"],
                record["unit"],
                record["provenance"]
            ))
            self.db_conn.commit()
