#!/usr/bin/env python3
"""Test query service với dữ liệu thực."""

import logging
import os
import sys
from pathlib import Path

import psycopg2

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

# Load .env
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        load_dotenv(env_path, override=True)
except ImportError:
    pass

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.chatbot.query_service import QueryService
from src.chatbot.location_resolver import resolve_location


def get_db_connection():
    """Get database connection với hỗ trợ POSTGRES_* variables."""
    # Thử POSTGRES_URL trước
    postgres_url = os.getenv("POSTGRES_URL")
    if postgres_url:
        logger.info("Using POSTGRES_URL")
        # Parse POSTGRES_URL
        if postgres_url.startswith("postgresql://") or postgres_url.startswith("postgres://"):
            url = postgres_url.replace("postgresql://", "").replace("postgres://", "")
            if "@" in url:
                auth_part, host_part = url.split("@", 1)
                if ":" in auth_part:
                    db_user, db_password = auth_part.split(":", 1)
                else:
                    db_user = auth_part
                    db_password = ""
                
                if "/" in host_part:
                    host_port, db_name = host_part.rsplit("/", 1)
                    if ":" in host_port:
                        db_host, db_port = host_port.split(":", 1)
                    else:
                        db_host = host_port
                        db_port = "5432"
                else:
                    db_host = host_part
                    db_port = "5432"
                    db_name = "postgres"
            
            return psycopg2.connect(
                host=db_host,
                port=db_port,
                database=db_name,
                user=db_user,
                password=db_password
            )
    
    # Fallback to POSTGRES_* individual vars
    db_host = os.getenv("POSTGRES_HOST", "localhost")
    db_port = os.getenv("POSTGRES_PORT", "5432")
    db_name = os.getenv("POSTGRES_DB", "chatbothanoiair")
    db_user = os.getenv("POSTGRES_USER", "postgres")
    db_password = os.getenv("POSTGRES_PASSWORD", "")
    
    logger.info(f"Using POSTGRES_* vars: {db_host}:{db_port}/{db_name} as {db_user}")
    return psycopg2.connect(
        host=db_host,
        port=db_port,
        database=db_name,
        user=db_user,
        password=db_password
    )


def test_location_resolver(conn):
    """Test location resolver."""
    logger.info("\n" + "=" * 60)
    logger.info("Test 1: Location Resolver")
    logger.info("=" * 60)
    
    test_locations = ["Cầu Giấy", "Hồ Tây", "Phường Lĩnh Nam", "Invalid Location"]
    
    for loc_text in test_locations:
        logger.info(f"\n📍 Resolving: '{loc_text}'")
        result = resolve_location(conn, loc_text)
        
        if result["location_id"]:
            logger.info(f"   ✅ Found: {result['name_vi']} (ID: {result['location_id']}, Type: {result['type']})")
            logger.info(f"   Confidence: {result['confidence']:.2f}")
            if result.get("admin_path"):
                logger.info(f"   Admin path: {result['admin_path']}")
        else:
            logger.warning(f"   ❌ Not found (confidence: {result['confidence']:.2f})")
            if result.get("candidates"):
                logger.info(f"   Candidates: {len(result['candidates'])}")
                for cand in result["candidates"][:3]:
                    logger.info(f"      - {cand['name_vi']} (confidence: {cand['confidence']:.2f})")


def test_current_insights(service):
    """Test get_current_air_quality_insights."""
    logger.info("\n" + "=" * 60)
    logger.info("Test 2: Current Air Quality Insights")
    logger.info("=" * 60)
    
    test_cases = [
        ("Cầu Giấy", "aqi"),
        ("Hồ Tây", "pm25"),
    ]
    
    for location, metric in test_cases:
        logger.info(f"\n📊 Getting insights for {location} ({metric})...")
        result = service.get_current_air_quality_insights(location, metric)
        
        if "error" in result:
            logger.warning(f"   ❌ Error: {result['error']}")
            continue
        
        logger.info(f"   ✅ Location: {result['location']['name_vi']} ({result['location']['type']})")
        logger.info(f"   Value: {result.get('value')} {result.get('unit') or ''}")
        if result.get("aqi_level"):
            logger.info(f"   AQI Level: {result['aqi_level']}")
        logger.info(f"   Minutes ago: {result.get('minutes_ago')}")
        logger.info(f"   Delta 1h: {result.get('delta_1h')} ({result.get('delta_1h_pct')}%)")
        logger.info(f"   Trend: {result.get('trend_label')}")
        logger.info(f"   Rank citywide: {result.get('rank_citywide')} (percentile: {result.get('percentile_citywide', 0)*100:.1f}%)")
        if result.get("who_exceedance_flag"):
            logger.info(f"   ⚠️  WHO exceedance: {result.get('exceedance_ratio', 0):.2f}x threshold")


def test_compare_locations(service):
    """Test compare_locations_now."""
    logger.info("\n" + "=" * 60)
    logger.info("Test 3: Compare Locations")
    logger.info("=" * 60)
    
    logger.info("\n🔀 Comparing Cầu Giấy vs Hồ Tây (AQI)...")
    result = service.compare_locations_now("Cầu Giấy", "Hồ Tây", "aqi")
    
    if "error" in result:
        logger.warning(f"   ❌ Error: {result['error']}")
        return
    
    logger.info(f"   ✅ {result['comparison']}")
    logger.info(f"   Location A: {result['location_a']['value']} (rank: {result['location_a'].get('rank_citywide')})")
    logger.info(f"   Location B: {result['location_b']['value']} (rank: {result['location_b'].get('rank_citywide')})")
    logger.info(f"   Difference: {result['diff_abs']} ({result['diff_pct']:.2f}%)")


def test_forecast_insights(service):
    """Test get_hourly_forecast_insights."""
    logger.info("\n" + "=" * 60)
    logger.info("Test 4: Hourly Forecast Insights")
    logger.info("=" * 60)
    
    logger.info("\n📈 Getting forecast for Cầu Giấy (AQI, next 24h)...")
    result = service.get_hourly_forecast_insights("Cầu Giấy", metric="aqi")
    
    if "error" in result:
        logger.warning(f"   ❌ Error: {result['error']}")
        return
    
    logger.info(f"   ✅ Found {len(result['series'])} forecast points")
    if result["series"]:
        first = result["series"][0]
        logger.info(f"   First: {first.get('target_ts_local')} - Value: {first.get('value')}")
        logger.info(f"   Hour local: {first.get('hour_local')}")
    
    if result.get("summary"):
        summary = result["summary"]
        logger.info(f"   Trend: {summary.get('trend_label')} ({summary.get('trend_change_pct')}%)")
        if summary.get("best_windows"):
            logger.info(f"   Best windows: {len(summary['best_windows'])}")
            for bw in summary["best_windows"][:2]:
                logger.info(f"      - {bw.get('start')} - {bw.get('end')}: {bw.get('avg_value')}")


def test_trend_insights(service):
    """Test get_trend_insights."""
    logger.info("\n" + "=" * 60)
    logger.info("Test 5: Trend Insights")
    logger.info("=" * 60)
    
    logger.info("\n📉 Getting trend for Cầu Giấy (AQI, this_week_vs_last_week)...")
    result = service.get_trend_insights("Cầu Giấy", "aqi", "this_week_vs_last_week", "hour")
    
    if "error" in result:
        logger.warning(f"   ❌ Error: {result['error']}")
        return
    
    logger.info(f"   ✅ Window: {result['window']}")
    logger.info(f"   Current avg: {result.get('current_avg')}")
    logger.info(f"   Previous avg: {result.get('previous_avg')}")
    logger.info(f"   Delta: {result.get('delta_abs')} ({result.get('delta_pct')}%)")
    logger.info(f"   Max value: {result.get('max_value')}")
    logger.info(f"   Best hour: {result.get('best_hour_of_day')}h (avg: {result.get('best_hour_avg')})")
    if result.get("diurnal_pattern"):
        logger.info(f"   Diurnal pattern: {len(result['diurnal_pattern'])} hours")


def test_snapshot_for_causal(service):
    """Test get_snapshot_for_causal."""
    logger.info("\n" + "=" * 60)
    logger.info("Test 6: Snapshot for Causal")
    logger.info("=" * 60)
    
    logger.info("\n🔬 Getting snapshot for Cầu Giấy...")
    result = service.get_snapshot_for_causal("Cầu Giấy")
    
    if "error" in result:
        logger.warning(f"   ❌ Error: {result['error']}")
        return
    
    logger.info(f"   ✅ Location: {result['location_name']}")
    logger.info(f"   Timestamp: {result['ts_utc']}")
    logger.info(f"   Season: {result.get('season')}")
    logger.info(f"   Time of day: {result.get('time_of_day')}h")
    logger.info(f"   Fields available: {len(result.get('fields', {}))}")
    
    # Show some key fields
    key_fields = ["pm25", "aqi", "wind_speed", "rh", "temp"]
    for field in key_fields:
        if field in result.get("fields", {}):
            field_data = result["fields"][field]
            logger.info(f"   {field}: {field_data.get('value')} {field_data.get('unit') or ''}")


def main():
    """Run all tests."""
    logger.info("=" * 60)
    logger.info("Testing Query Service - Phase B")
    logger.info("=" * 60)
    
    # Connect to database
    logger.info("\nConnecting to database...")
    try:
        conn = get_db_connection()
        logger.info("✅ Connected to database")
    except Exception as e:
        logger.error(f"❌ Failed to connect to database: {e}")
        return 1
    
    try:
        # Initialize service
        service = QueryService(conn)
        
        # Run tests
        test_location_resolver(conn)
        test_current_insights(service)
        test_compare_locations(service)
        test_forecast_insights(service)
        test_trend_insights(service)
        test_snapshot_for_causal(service)
        
        logger.info("\n" + "=" * 60)
        logger.info("✅ All tests completed!")
        logger.info("=" * 60)
        return 0
        
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}", exc_info=True)
        return 1
    finally:
        conn.close()


if __name__ == "__main__":
    sys.exit(main())
