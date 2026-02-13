"""Query service: Wrapper cho các SQL views/functions insights.

Lớp này là boundary duy nhất mà lớp chatbot/Intent Router nên dùng để
truy vấn dữ liệu định lượng (current, forecast, trend, district insights).
Không nơi nào khác trong ứng dụng nên gọi SQL trực tiếp.
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import psycopg2
from psycopg2.extras import RealDictCursor

from .aqi_config import get_aqi_level, get_trend_label
from .location_resolver import resolve_location

logger = logging.getLogger(__name__)


class QueryService:
    """Service để truy vấn insights từ database cho chatbot.

    Tất cả các hàm public đều:
    - Nhận input ở dạng text (location/district) + tham số đơn giản.
    - Resolve location qua `location_resolver`.
    - Gọi các view/function SQL tương ứng.
    - Trả về dict JSON-friendly cho LLM/chat layer.
    """

    def __init__(self, db_conn: psycopg2.extensions.connection) -> None:
        """Khởi tạo QueryService.

        Args:
            db_conn: Kết nối PostgreSQL đã mở (psycopg2 connection).
        """
        self.db_conn = db_conn
    
    def get_current_air_quality_insights(
        self,
        location: str,
        metric: str = "aqi",
        scope: Optional[str] = None
    ) -> Dict[str, Any]:
        """Lấy insights cho air quality hiện tại.
        
        Args:
            location: Tên location (text)
            metric: Field name (default: "aqi")
            scope: Scope filter (optional, chưa implement)
        
        Returns:
            Dict với một trong hai dạng:

            - Thành công:
              {
                  "location": {...},
                  "metric": str,
                  "value": float | None,
                  ...
              }

            - Lỗi:
              {
                  "error": str,
                  "location_text": str,
                  "candidates": List[Dict]
              }
        """
        # Resolve location
        location_info = resolve_location(self.db_conn, location)
        
        if not location_info["location_id"]:
            return {
                "error": "Location not found",
                "location_text": location,
                "candidates": location_info.get("candidates", [])
            }
        
        # Query view
        with self.db_conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT *
                FROM vw_current_air_quality_insights
                WHERE location_id = %s AND field = %s
                LIMIT 1
            """, (location_info["location_id"], metric))
            
            row = cur.fetchone()
            
            if not row:
                return {
                    "error": "No data available",
                    "location": location_info,
                    "metric": metric
                }
            
            # Format response
            return {
                "location": {
                    "id": location_info["location_id"],
                    "name_vi": location_info["name_vi"],
                    "type": location_info["type"],
                    "admin_path": location_info.get("admin_path"),
                    "aggregate_from": location_info.get("aggregate_from"),
                    "member_count": location_info.get("member_count"),
                },
                "metric": metric,
                "value": float(row["value"]) if row["value"] else None,
                "unit": row["unit"],
                "aqi_level": row["aqi_level"],
                "minutes_ago": int(row["minutes_ago"]) if row["minutes_ago"] else None,
                "who_exceedance_flag": row["who_exceedance_flag"],
                "exceedance_ratio": float(row["exceedance_ratio"]) if row["exceedance_ratio"] else None,
                "delta_1h": float(row["delta_1h"]) if row["delta_1h"] else None,
                "delta_2h": float(row["delta_2h"]) if row["delta_2h"] else None,
                "delta_3h": float(row["delta_3h"]) if row["delta_3h"] else None,
                "delta_1h_pct": float(row["delta_1h_pct"]) if row["delta_1h_pct"] else None,
                "trend_label": row["trend_label"],
                "rank_citywide": int(row["rank_citywide"]) if row["rank_citywide"] else None,
                "percentile_citywide": float(row["percentile_citywide"]) if row["percentile_citywide"] else None,
                "rank_scope": int(row["rank_scope"]) if row["rank_scope"] else None,
                "percentile_scope": float(row["percentile_scope"]) if row["percentile_scope"] else None
            }

    def get_district_now_insights(
        self,
        district: str,
        metric: str = "aqi",
    ) -> Dict[str, Any]:
        """Lấy insights hiện tại ở cấp quận/huyện (virtual district).

        Args:
            district: Tên quận/huyện/thị xã (text)
            metric: Field name (default: "aqi")

        Returns:
            Dict với district-level insights (aggregate từ wards/communes)
            hoặc dict với khoá "error" nếu có lỗi (location không tìm thấy
            hoặc không phải là district).
        """
        # Resolve location (ưu tiên district trong location_resolver)
        location_info = resolve_location(self.db_conn, district)

        if not location_info["location_id"]:
            return {
                "error": "Location not found",
                "location_text": district,
                "candidates": location_info.get("candidates", []),
            }

        if location_info["type"] != "district":
            return {
                "error": "Resolved location is not a district",
                "location": location_info,
            }

        with self.db_conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT *
                FROM vw_district_now_insights
                WHERE district_location_id = %s
                  AND field = %s
                LIMIT 1
                """,
                (location_info["location_id"], metric),
            )

            row = cur.fetchone()

            if not row:
                return {
                    "error": "No district data available",
                    "location": location_info,
                    "metric": metric,
                }

            coverage_pct = float(row["coverage_pct"]) if row["coverage_pct"] is not None else None

            return {
                "district": {
                    "id": row["district_location_id"],
                    "name_vi": row["district_name_vi"],
                    "admin_path": row.get("admin_path"),
                    "aggregate_from": row.get("aggregated_from"),
                    "member_count": int(row["wards_total"]) if row["wards_total"] is not None else None,
                },
                "metric": metric,
                "stats": {
                    "value_mean": float(row["value_mean"]) if row["value_mean"] is not None else None,
                    "p25": float(row["p25"]) if row["p25"] is not None else None,
                    "p50": float(row["p50"]) if row["p50"] is not None else None,
                    "p75": float(row["p75"]) if row["p75"] is not None else None,
                },
                "coverage": {
                    "wards_total": int(row["wards_total"]) if row["wards_total"] is not None else None,
                    "wards_with_data": int(row["wards_with_data"]) if row["wards_with_data"] is not None else None,
                    "coverage_pct": coverage_pct,
                    "quality": row.get("quality"),
                    "time_window_minutes": int(row["time_window_minutes"]) if row["time_window_minutes"] is not None else 60,
                },
            }
    
    def compare_locations_now(
        self,
        location_a: str,
        location_b: str,
        metric: str = "aqi",
        scope: str = "citywide"
    ) -> Dict[str, Any]:
        """So sánh 2 locations cùng thời điểm.
        
        Args:
            location_a: Tên location A
            location_b: Tên location B
            metric: Field name (default: "aqi")
            scope: Scope filter (default: "citywide")
        
        Returns:
            Dict với comparison insights
        """
        # Resolve cả 2 locations
        loc_a_info = resolve_location(self.db_conn, location_a)
        loc_b_info = resolve_location(self.db_conn, location_b)
        
        if not loc_a_info["location_id"] or not loc_b_info["location_id"]:
            return {
                "error": "One or both locations not found",
                "location_a": loc_a_info,
                "location_b": loc_b_info
            }
        
        # Lấy insights cho cả 2
        insights_a = self.get_current_air_quality_insights(location_a, metric, scope)
        insights_b = self.get_current_air_quality_insights(location_b, metric, scope)
        
        if "error" in insights_a or "error" in insights_b:
            return {
                "error": "Failed to get insights for one or both locations",
                "location_a": insights_a,
                "location_b": insights_b
            }
        
        # Tính diff
        value_a = insights_a.get("value")
        value_b = insights_b.get("value")
        
        if value_a is None or value_b is None:
            return {
                "error": "Missing values for comparison",
                "location_a": insights_a,
                "location_b": insights_b
            }
        
        diff_abs = value_a - value_b
        diff_pct = (diff_abs / value_b * 100.0) if value_b != 0 else None
        
        return {
            "location_a": insights_a,
            "location_b": insights_b,
            "diff_abs": diff_abs,
            "diff_pct": diff_pct,
            "comparison": f"{location_a} {'cao hơn' if diff_abs > 0 else 'thấp hơn'} {location_b} {abs(diff_abs):.1f} điểm {metric} ({abs(diff_pct):.2f}%)" if diff_pct else f"{location_a} {'cao hơn' if diff_abs > 0 else 'thấp hơn'} {location_b} {abs(diff_abs):.1f} điểm {metric}"
        }
    
    def get_hourly_forecast_insights(
        self,
        location: str,
        start_ts: Optional[datetime] = None,
        end_ts: Optional[datetime] = None,
        metric: str = "aqi",
        time_of_day_preference: Optional[str] = None
    ) -> Dict[str, Any]:
        """Lấy insights cho hourly forecast.
        
        Args:
            location: Tên location
            start_ts: Start timestamp (default: NOW())
            end_ts: End timestamp (default: NOW() + 72h)
            metric: Field name (default: "aqi")
            time_of_day_preference: "morning", "afternoon", "evening" (optional)
        
        Returns:
            Dict với forecast insights
        """
        # Resolve location
        location_info = resolve_location(self.db_conn, location)
        
        if not location_info["location_id"]:
            return {
                "error": "Location not found",
                "location_text": location,
                "candidates": location_info.get("candidates", [])
            }
        
        # Default time range
        if not start_ts:
            start_ts = datetime.utcnow()
        if not end_ts:
            end_ts = start_ts + timedelta(hours=72)
        
        # Query view
        with self.db_conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT *
                FROM vw_hourly_forecast_insights
                WHERE location_id = %s 
                  AND field = %s
                  AND target_ts_utc >= %s
                  AND target_ts_utc <= %s
                ORDER BY target_ts_utc ASC
            """, (location_info["location_id"], metric, start_ts, end_ts))
            
            rows = cur.fetchall()
            
            if not rows:
                return {
                    "error": "No forecast data available",
                    "location": location_info,
                    "metric": metric
                }
            
            # Filter theo time_of_day_preference
            if time_of_day_preference:
                hour_ranges = {
                    "morning": (6, 12),
                    "afternoon": (12, 18),
                    "evening": (18, 22)
                }
                if time_of_day_preference in hour_ranges:
                    start_hour, end_hour = hour_ranges[time_of_day_preference]
                    rows = [
                        r for r in rows
                        if start_hour <= r["hour_local"] < end_hour
                    ]
            
            # Format series
            series = [
                {
                    "target_ts_utc": row["target_ts_utc"].isoformat() if row["target_ts_utc"] else None,
                    "target_ts_local": row["target_ts_local"].isoformat() if row["target_ts_local"] else None,
                    "hour_local": row["hour_local"],
                    "value": float(row["value"]) if row["value"] else None,
                    "unit": row["unit"],
                    "uncertainty_p10": float(row["uncertainty_p10"]) if row["uncertainty_p10"] else None,
                    "uncertainty_p50": float(row["uncertainty_p50"]) if row["uncertainty_p50"] else None,
                    "uncertainty_p90": float(row["uncertainty_p90"]) if row["uncertainty_p90"] else None,
                    "trend_slope": float(row["trend_slope"]) if row["trend_slope"] else None,
                    "trend_change_pct": float(row["trend_change_pct"]) if row["trend_change_pct"] else None,
                    "trend_label": row["trend_label"]
                }
                for row in rows
            ]
            
            # Tính best windows (2h windows với min AQI, tránh giờ cao điểm)
            best_windows = self._calculate_best_windows(rows, metric)
            
            # Summary từ row đầu tiên (hoặc aggregate)
            summary = {
                "trend_slope": float(rows[0]["trend_slope"]) if rows and rows[0]["trend_slope"] else None,
                "trend_change_pct": float(rows[0]["trend_change_pct"]) if rows and rows[0]["trend_change_pct"] else None,
                "trend_label": rows[0]["trend_label"] if rows else None,
                "best_windows": best_windows,
                "uncertainty": {
                    "p10": float(rows[0]["uncertainty_p10"]) if rows and rows[0]["uncertainty_p10"] else None,
                    "p50": float(rows[0]["uncertainty_p50"]) if rows and rows[0]["uncertainty_p50"] else None,
                    "p90": float(rows[0]["uncertainty_p90"]) if rows and rows[0]["uncertainty_p90"] else None
                } if rows else None
            }
            
            return {
                "location": {
                    "id": location_info["location_id"],
                    "name_vi": location_info["name_vi"],
                    "type": location_info["type"],
                    "admin_path": location_info.get("admin_path")
                },
                "metric": metric,
                "series": series,
                "summary": summary
            }
    
    def _calculate_best_windows(
        self,
        rows: List[Dict],
        metric: str,
        window_hours: int = 2
    ) -> List[Dict]:
        """Tính best windows (khoảng giờ tốt nhất).
        
        Args:
            rows: List các forecast rows
            metric: Field name
            window_hours: Số giờ trong window (default: 2)
        
        Returns:
            List các best windows
        """
        if not rows:
            return []
        
        # Giờ cao điểm cần tránh: 7-9h, 17-19h
        rush_hours = set(range(7, 9)) | set(range(17, 19))
        
        best_windows = []
        
        # Tìm các 2h windows
        for i in range(len(rows) - window_hours + 1):
            window_rows = rows[i:i + window_hours]
            
            # Check nếu có giờ cao điểm
            has_rush_hour = any(
                row["hour_local"] in rush_hours
                for row in window_rows
            )
            
            if has_rush_hour:
                continue
            
            # Tính avg value trong window
            avg_value = sum(
                float(row["value"]) for row in window_rows if row["value"]
            ) / len([r for r in window_rows if r["value"]])
            
            best_windows.append({
                "start": window_rows[0]["target_ts_local"].strftime("%H:%M") if window_rows[0]["target_ts_local"] else None,
                "end": window_rows[-1]["target_ts_local"].strftime("%H:%M") if window_rows[-1]["target_ts_local"] else None,
                "avg_value": avg_value,
                "reason": "AQI thấp nhất, tránh giờ cao điểm"
            })
        
        # Sort theo avg_value và lấy top 3
        best_windows.sort(key=lambda x: x["avg_value"])
        return best_windows[:3]
    
    def get_trend_insights(
        self,
        location: str,
        metric: str,
        window: str,
        time_granularity: str = "hour"
    ) -> Dict[str, Any]:
        """Lấy trend insights.
        
        Args:
            location: Tên location
            metric: Field name
            window: Window type ("last_24h", "last_7d", "this_week_vs_last_week", "this_month")
            time_granularity: "hour" hoặc "day" (default: "hour")
        
        Returns:
            Dict với trend insights
        """
        # Resolve location
        location_info = resolve_location(self.db_conn, location)
        
        if not location_info["location_id"]:
            return {
                "error": "Location not found",
                "location_text": location,
                "candidates": location_info.get("candidates", [])
            }
        
        # Gọi function
        with self.db_conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT * FROM get_trend_insights(%s, %s, %s, %s)
            """, (location_info["location_id"], metric, window, time_granularity))
            
            row = cur.fetchone()
            
            if not row:
                return {
                    "error": "No trend data available",
                    "location": location_info,
                    "metric": metric,
                    "window": window
                }
            
            # Parse diurnal_pattern từ JSONB
            diurnal_pattern = row["diurnal_pattern"]
            if isinstance(diurnal_pattern, str):
                diurnal_pattern = json.loads(diurnal_pattern)
            
            return {
                "location": {
                    "id": location_info["location_id"],
                    "name_vi": location_info["name_vi"],
                    "type": location_info["type"],
                    "admin_path": location_info.get("admin_path")
                },
                "window": window,
                "current_avg": float(row["current_avg"]) if row["current_avg"] else None,
                "previous_avg": float(row["previous_avg"]) if row["previous_avg"] else None,
                "delta_abs": float(row["delta_abs"]) if row["delta_abs"] else None,
                "delta_pct": float(row["delta_pct"]) if row["delta_pct"] else None,
                "max_value": float(row["max_value"]) if row["max_value"] else None,
                "p95_value": float(row["p95_value"]) if row["p95_value"] else None,
                "exceedance_days": int(row["exceedance_days"]) if row["exceedance_days"] else None,
                "exceedance_hours": int(row["exceedance_hours"]) if row["exceedance_hours"] else None,
                "best_hour_of_day": int(row["best_hour_of_day"]) if row["best_hour_of_day"] else None,
                "best_hour_avg": float(row["best_hour_avg"]) if row["best_hour_avg"] else None,
                "diurnal_pattern": diurnal_pattern
            }
    
    def get_snapshot_for_causal(
        self,
        location: str,
        ts_utc: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Lấy snapshot đầy đủ cho causal analysis.
        
        Args:
            location: Tên location
            ts_utc: Timestamp (default: NOW())
        
        Returns:
            Dict với tất cả fields cần cho CKG
        """
        # Resolve location
        location_info = resolve_location(self.db_conn, location)
        
        if not location_info["location_id"]:
            return {
                "error": "Location not found",
                "location_text": location,
                "candidates": location_info.get("candidates", [])
            }
        
        if not ts_utc:
            ts_utc = datetime.utcnow()
        
        # Lấy tất cả fields từ observations_canonical
        fields_needed = [
            "pm25", "pm10", "aqi", "o3", "no2", "so2", "co",
            "wind_speed", "wind_dir", "rh", "temp", "precip",
            "cloud_cover", "pblh"
        ]
        
        snapshot = {
            "location_id": location_info["location_id"],
            "location_name": location_info["name_vi"],
            "ts_utc": ts_utc.isoformat(),
            "fields": {}
        }
        
        with self.db_conn.cursor(cursor_factory=RealDictCursor) as cur:
            for field in fields_needed:
                cur.execute("""
                    SELECT value, unit, ts_utc
                    FROM observations_canonical
                    WHERE location_id = %s
                      AND field = %s
                      AND ts_utc >= %s - INTERVAL '1 hour'
                      AND ts_utc <= %s
                    ORDER BY ts_utc DESC
                    LIMIT 1
                """, (location_info["location_id"], field, ts_utc, ts_utc))
                
                row = cur.fetchone()
                if row:
                    snapshot["fields"][field] = {
                        "value": float(row["value"]) if row["value"] else None,
                        "unit": row["unit"],
                        "ts_utc": row["ts_utc"].isoformat() if row["ts_utc"] else None
                    }
        
        # Thêm metadata
        snapshot["season"] = self._get_season(ts_utc)
        snapshot["time_of_day"] = ts_utc.hour
        
        return snapshot
    
    def _get_season(self, ts_utc: datetime) -> str:
        """Xác định mùa từ timestamp.
        
        Args:
            ts_utc: Timestamp
        
        Returns:
            "spring", "summer", "autumn", "winter"
        """
        month = ts_utc.month
        if month in [12, 1, 2]:
            return "winter"
        elif month in [3, 4, 5]:
            return "spring"
        elif month in [6, 7, 8]:
            return "summer"
        else:
            return "autumn"
