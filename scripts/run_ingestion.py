#!/usr/bin/env python3
"""Main script to run ingestion pipeline.

This script:
1. Syncs locations from HanoiAir
2. Ingests data from all APIs for city + wards
3. Runs data fusion to create canonical tables

Usage:
    python scripts/run_ingestion.py [--city-only] [--skip-fusion]
"""

import argparse
import logging
import os
import sys
from pathlib import Path

import psycopg2
from psycopg2.extras import RealDictCursor

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load .env
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        load_dotenv(env_path, override=True)
except ImportError:
    pass

from concurrent.futures import ThreadPoolExecutor, as_completed

from src.fusion.forecasts_fusion_job import ForecastsFusionJob
from src.fusion.observations_fusion_job import ObservationsFusionJob
from src.ingestion.api_key_manager import ApiKeyManager
from src.ingestion.hanoiair_ingestor import HanoiAirIngestor
from src.ingestion.openmeteo_air_ingestor import OpenMeteoAirIngestor
from src.ingestion.openmeteo_weather_ingestor import OpenMeteoWeatherIngestor
from src.ingestion.openweather_air_ingestor import OpenWeatherAirIngestor
from src.ingestion.openweather_onecall_ingestor import OpenWeatherOneCallIngestor

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)


def get_db_connection():
    """Get database connection from environment variables."""
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        # Parse DATABASE_URL
        if database_url.startswith("postgresql://") or database_url.startswith("postgres://"):
            url = database_url.replace("postgresql://", "").replace("postgres://", "")
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
    
    # Fallback to individual vars
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        database=os.getenv("DB_NAME", "hanoiair_chatbot"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "")
    )


def init_api_sources(db_conn):
    """Initialize api_sources table."""
    logger.info("Initializing API sources...")
    
    sources = [
        {
            "source_id": "openweather_onecall",
            "source_name": "OpenWeatherMap One Call API 3.0",
            "api_version": "3.0",
            "base_url": "https://api.openweathermap.org/data/3.0/onecall",
            "rate_limit_per_day": 1000,
            "rate_limit_per_minute": 60,
            "notes": "Meteorology data: current + hourly + daily"
        },
        {
            "source_id": "openweather_air",
            "source_name": "OpenWeatherMap Air Pollution API",
            "api_version": "2.5",
            "base_url": "http://api.openweathermap.org/data/2.5/air_pollution",
            "rate_limit_per_day": 1000,
            "rate_limit_per_minute": 60,
            "notes": "Air quality: current + forecast (5 days)"
        },
        {
            "source_id": "openmeteo_weather",
            "source_name": "Open-Meteo Weather API",
            "api_version": "v1",
            "base_url": "https://api.open-meteo.com/v1/forecast",
            "rate_limit_per_day": None,
            "rate_limit_per_minute": None,
            "notes": "Meteorology fallback: hourly + daily"
        },
        {
            "source_id": "openmeteo_air",
            "source_name": "Open-Meteo Air Quality API",
            "api_version": "v1",
            "base_url": "https://air-quality-api.open-meteo.com/v1/air-quality",
            "rate_limit_per_day": None,
            "rate_limit_per_minute": None,
            "notes": "Air quality fallback: hourly (5 days)"
        },
        {
            "source_id": "hanoiair",
            "source_name": "HanoiAir API",
            "api_version": None,
            "base_url": "https://geoi.com.vn",
            "rate_limit_per_day": None,
            "rate_limit_per_minute": None,
            "notes": "Ward-level AQI/PM2.5 for 126 wards + Hanoi city"
        }
    ]
    
    with db_conn.cursor() as cur:
        for source in sources:
            cur.execute("""
                INSERT INTO api_sources (
                    source_id, source_name, api_version, base_url,
                    rate_limit_per_day, rate_limit_per_minute, notes
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (source_id) DO UPDATE SET
                    source_name = EXCLUDED.source_name,
                    api_version = EXCLUDED.api_version,
                    base_url = EXCLUDED.base_url,
                    rate_limit_per_day = EXCLUDED.rate_limit_per_day,
                    rate_limit_per_minute = EXCLUDED.rate_limit_per_minute,
                    notes = EXCLUDED.notes
            """, (
                source["source_id"],
                source["source_name"],
                source["api_version"],
                source["base_url"],
                source["rate_limit_per_day"],
                source["rate_limit_per_minute"],
                source["notes"]
            ))
        db_conn.commit()
    
    logger.info("API sources initialized")


def main():
    """Main ingestion pipeline."""
    parser = argparse.ArgumentParser(description="Run ingestion pipeline")
    parser.add_argument(
        "--city-only",
        action="store_true",
        help="Only ingest data for Hanoi city (not wards)"
    )
    parser.add_argument(
        "--skip-fusion",
        action="store_true",
        help="Skip data fusion step"
    )
    args = parser.parse_args()
    
    # Get database connection
    db_conn = get_db_connection()
    
    try:
        # Initialize API sources
        init_api_sources(db_conn)
        
        # Step 1: Sync locations from HanoiAir
        logger.info("=" * 60)
        logger.info("Step 1: Syncing locations from HanoiAir")
        logger.info("=" * 60)
        hanoiair = HanoiAirIngestor(db_conn)
        hanoiair.sync_locations()
        
        # Get locations to ingest
        with db_conn.cursor(cursor_factory=RealDictCursor) as cur:
            if args.city_only:
                cur.execute("""
                    SELECT location_id, lat, lon, name_vi, type
                    FROM locations
                    WHERE type = 'city' AND lat IS NOT NULL AND lon IS NOT NULL
                """)
            else:
                cur.execute("""
                    SELECT location_id, lat, lon, name_vi, type
                    FROM locations
                    WHERE lat IS NOT NULL AND lon IS NOT NULL
                    ORDER BY CASE type WHEN 'city' THEN 1 ELSE 2 END, location_id
                """)
            locations = cur.fetchall()
        
        logger.info(f"Found {len(locations)} locations to ingest")
        
        # Step 2: Ingest from OpenWeather APIs (priority sources)
        logger.info("=" * 60)
        logger.info("Step 2: Ingesting from OpenWeather APIs")
        logger.info("=" * 60)
        
        # Load API keys from environment
        openweather_keys = [
            os.getenv("OPENWEATHER_API_KEY_0"),
            os.getenv("OPENWEATHER_API_KEY_1"),
            os.getenv("OPENWEATHER_API_KEY_2"),
            os.getenv("OPENWEATHER_API_KEY_3")
        ]
        openweather_keys = [k for k in openweather_keys if k]  # Filter None values
        
        if not openweather_keys:
            logger.warning("No OpenWeather API keys found, skipping OpenWeather APIs")
        else:
            # Create API key manager (only if we have multiple keys)
            key_manager = None
            if len(openweather_keys) > 1:
                try:
                    key_manager = ApiKeyManager(
                        db_conn=db_conn,
                        source_id="openweather_onecall",  # Shared between OneCall and Air
                        env_key_names=[
                            "OPENWEATHER_API_KEY_0",
                            "OPENWEATHER_API_KEY_1",
                            "OPENWEATHER_API_KEY_2",
                            "OPENWEATHER_API_KEY_3"
                        ],
                        rate_limit_per_minute=60,
                        rate_limit_per_day=1000
                    )
                    logger.info(f"Using {len(openweather_keys)} OpenWeather API keys with round-robin")
                except Exception as e:
                    logger.warning(f"Failed to create key manager, using single key: {e}")
                    key_manager = None
            
            # Create ingestors
            if key_manager:
                # Use key manager for multiple keys
                onecall_ingestor = OpenWeatherOneCallIngestor(
                    db_conn, 
                    api_key=None,
                    api_key_manager=key_manager
                )
                air_ingestor = OpenWeatherAirIngestor(
                    db_conn,
                    api_key=None,
                    api_key_manager=key_manager
                )
            else:
                # Fallback to single key
                onecall_ingestor = OpenWeatherOneCallIngestor(
                    db_conn, 
                    api_key=openweather_keys[0]
                )
                air_ingestor = OpenWeatherAirIngestor(
                    db_conn,
                    api_key=openweather_keys[0]
                )
                logger.info(f"Using single OpenWeather API key")
            
            # Sequential processing (rate limit shared, cannot parallelize)
            for loc in locations:
                logger.info(f"Processing {loc['name_vi']} ({loc['type']})...")
                try:
                    onecall_ingestor.ingest_location(
                        loc["location_id"], loc["lat"], loc["lon"]
                    )
                    air_ingestor.ingest_location(
                        loc["location_id"], loc["lat"], loc["lon"]
                    )
                except Exception as e:
                    logger.error(f"Error ingesting {loc['name_vi']}: {e}")
                    continue
            
            # Log usage stats
            stats = key_manager.get_usage_stats()
            logger.info(f"OpenWeather API usage: {stats['active_keys']}/{stats['total_keys']} keys active")
        
        # Step 3: Ingest from Open-Meteo APIs (fallback) - PARALLEL
        logger.info("=" * 60)
        logger.info("Step 3: Ingesting from Open-Meteo APIs (Parallel)")
        logger.info("=" * 60)
        
        def ingest_meteo_location(loc):
            """Ingest Open-Meteo data for a location (thread-safe)."""
            # Create new connection for this thread
            thread_conn = get_db_connection()
            try:
                meteo_weather = OpenMeteoWeatherIngestor(thread_conn)
                meteo_air = OpenMeteoAirIngestor(thread_conn)
                
                logger.debug(f"Processing {loc['name_vi']} ({loc['type']})...")
                meteo_weather.ingest_location(
                    loc["location_id"], loc["lat"], loc["lon"]
                )
                meteo_air.ingest_location(
                    loc["location_id"], loc["lat"], loc["lon"]
                )
                return True, loc['name_vi']
            except Exception as e:
                logger.error(f"Error ingesting {loc['name_vi']}: {e}")
                return False, loc['name_vi']
            finally:
                thread_conn.close()
        
        # Parallel processing with ThreadPoolExecutor
        max_workers = min(20, len(locations))  # Max 20 workers
        success_count = 0
        error_count = 0
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(ingest_meteo_location, loc): loc 
                for loc in locations
            }
            
            for future in as_completed(futures):
                success, name = future.result()
                if success:
                    success_count += 1
                else:
                    error_count += 1
        
        logger.info(f"Open-Meteo ingestion completed: {success_count} success, {error_count} errors")
        
        # Step 4: Ingest HanoiAir ward forecasts - PARALLEL
        if not args.city_only:
            logger.info("=" * 60)
            logger.info("Step 4: Ingesting HanoiAir ward forecasts (Parallel)")
            logger.info("=" * 60)
            
            # Get all ward locations
            with db_conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT location_id, hanoiair_internal_id, name_vi
                    FROM locations
                    WHERE type = 'ward' AND hanoiair_internal_id IS NOT NULL
                    ORDER BY location_id
                """)
                ward_locations = cur.fetchall()
            
            def ingest_ward_forecast(ward):
                """Ingest forecast for a single ward (thread-safe)."""
                # Create new connection for this thread
                thread_conn = get_db_connection()
                try:
                    thread_hanoiair = HanoiAirIngestor(thread_conn)
                    
                    logger.debug(f"Processing ward {ward['name_vi']}...")
                    # Fetch forecast
                    response_json = thread_hanoiair.fetch_ward_forecast(
                        ward['hanoiair_internal_id'],
                        ward['location_id']
                    )
                    # Parse and insert
                    records = thread_hanoiair.parse_forecast_response(
                        response_json,
                        response_json.get("_response_id"),
                        ward['location_id']
                    )
                    if records:
                        thread_hanoiair._insert_forecasts_raw(records)
                    return True, ward['name_vi']
                except Exception as e:
                    logger.error(f"Error ingesting ward {ward['name_vi']}: {e}")
                    return False, ward['name_vi']
                finally:
                    thread_conn.close()
            
            # Parallel processing
            max_workers = min(15, len(ward_locations))  # Max 15 workers
            success_count = 0
            error_count = 0
            
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = {
                    executor.submit(ingest_ward_forecast, ward): ward
                    for ward in ward_locations
                }
                
                for future in as_completed(futures):
                    success, name = future.result()
                    if success:
                        success_count += 1
                    else:
                        error_count += 1
            
            logger.info(f"HanoiAir ward forecast completed: {success_count} success, {error_count} errors")
        
        # Step 5: Data fusion
        # Với thiết kế mới, forecasts đã được upsert trực tiếp vào forecasts_canonical
        # như snapshot latest, nên chỉ cần chạy fusion cho observations.
        if not args.skip_fusion:
            logger.info("=" * 60)
            logger.info("Step 5: Running data fusion (observations only)")
            logger.info("=" * 60)
            
            obs_fusion = ObservationsFusionJob(db_conn)
            obs_fusion.fuse_observations()
        
        logger.info("=" * 60)
        logger.info("Ingestion pipeline completed successfully!")
        logger.info("=" * 60)
        
    finally:
        db_conn.close()


if __name__ == "__main__":
    main()
