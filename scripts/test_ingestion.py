#!/usr/bin/env python3
"""Test script for ingestion pipeline.

Tests each component step by step to ensure everything works correctly.
"""

import logging
import os
import sys
from pathlib import Path

import psycopg2
from psycopg2.extras import RealDictCursor

# Setup logging first
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load .env file
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        load_dotenv(env_path, override=True)
        logger.info(f"✅ Loaded .env from {env_path}")
        
        # Debug: Check all DB-related environment variables
        all_env = dict(os.environ)
        db_related = {k: ("***" if "PASSWORD" in k or "PASS" in k else v) 
                     for k, v in all_env.items() 
                     if "DB" in k.upper() or "DATABASE" in k.upper()}
        logger.info(f"DB-related env vars: {list(db_related.keys())}")
        
        # Try common variations
        db_vars = {
            "DB_HOST": os.getenv("DB_HOST") or os.getenv("DATABASE_HOST"),
            "DB_PORT": os.getenv("DB_PORT") or os.getenv("DATABASE_PORT"),
            "DB_NAME": os.getenv("DB_NAME") or os.getenv("DATABASE_NAME"),
            "DB_USER": os.getenv("DB_USER") or os.getenv("DATABASE_USER"),
            "DB_PASSWORD": os.getenv("DB_PASSWORD") or os.getenv("DATABASE_PASSWORD")
        }
        logger.info(f"Using DB variables: {list(db_vars.keys())}")
    else:
        logger.warning(f"⚠️  .env file not found at {env_path}")
except ImportError:
    logger.warning("python-dotenv not installed, using environment variables only")
except Exception as e:
    logger.warning(f"Could not load .env: {e}")


def get_db_connection():
    """Get database connection from environment variables."""
    try:
        # Try DATABASE_URL first (common format: postgresql://user:password@host:port/dbname)
        database_url = os.getenv("DATABASE_URL")
        if database_url:
            logger.info("Using DATABASE_URL")
            # Parse DATABASE_URL
            if database_url.startswith("postgresql://") or database_url.startswith("postgres://"):
                # Remove protocol
                url = database_url.replace("postgresql://", "").replace("postgres://", "")
                # Split into parts
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
                else:
                    # No auth
                    db_user = "postgres"
                    db_password = ""
                    if "/" in url:
                        host_port, db_name = url.rsplit("/", 1)
                        if ":" in host_port:
                            db_host, db_port = host_port.split(":", 1)
                        else:
                            db_host = host_port
                            db_port = "5432"
                    else:
                        db_host = url
                        db_port = "5432"
                        db_name = "postgres"
            else:
                # Not a URL, try individual vars
                db_host = (os.getenv("DB_HOST") or os.getenv("DATABASE_HOST") or "localhost")
                db_port = (os.getenv("DB_PORT") or os.getenv("DATABASE_PORT") or "5432")
                db_name = (os.getenv("DB_NAME") or os.getenv("DATABASE_NAME") or "hanoiair_chatbot")
                db_user = (os.getenv("DB_USER") or os.getenv("DATABASE_USER") or "postgres")
                db_password = (os.getenv("DB_PASSWORD") or os.getenv("DATABASE_PASSWORD") or "")
        else:
            # Try individual variables
            db_host = (os.getenv("DB_HOST") or os.getenv("DATABASE_HOST") or "localhost")
            db_port = (os.getenv("DB_PORT") or os.getenv("DATABASE_PORT") or "5432")
            db_name = (os.getenv("DB_NAME") or os.getenv("DATABASE_NAME") or os.getenv("POSTGRES_DB") or "hanoiair_chatbot")
            db_user = (os.getenv("DB_USER") or os.getenv("DATABASE_USER") or "postgres")
            db_password = (os.getenv("DB_PASSWORD") or os.getenv("DATABASE_PASSWORD") or "")
        
        logger.info(f"Connecting to database: {db_user}@{db_host}:{db_port}/{db_name}")
        logger.info(f"Password set: {'Yes' if db_password else 'No'}")
        
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            database=db_name,
            user=db_user,
            password=db_password
        )
        logger.info("✅ Database connection successful")
        return conn
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        raise


def check_schema(db_conn):
    """Check if required tables exist."""
    logger.info("Checking database schema...")
    
    required_tables = [
        "locations", "api_sources", "api_requests", "api_responses",
        "observations_raw", "forecasts_raw",
        "observations_canonical", "forecasts_canonical"
    ]
    
    with db_conn.cursor() as cur:
        cur.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name IN %s
        """, (tuple(required_tables),))
        
        existing = {row[0] for row in cur.fetchall()}
    
    missing = set(required_tables) - existing
    if missing:
        logger.error(f"❌ Missing tables: {missing}")
        logger.error("Please run db/schema_database_logging.sql first")
        return False
    
    logger.info(f"✅ All required tables exist: {existing}")
    return True


def test_hanoiair_sync(db_conn):
    """Test HanoiAir location sync."""
    logger.info("=" * 60)
    logger.info("Testing HanoiAir location sync...")
    logger.info("=" * 60)
    
    try:
        from src.ingestion.hanoiair_ingestor import HanoiAirIngestor
        
        ingestor = HanoiAirIngestor(db_conn)
        count = ingestor.sync_locations()
        
        # Verify locations were inserted
        with db_conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM locations")
            total = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM locations WHERE type = 'city'")
            city_count = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM locations WHERE type = 'ward'")
            ward_count = cur.fetchone()[0]
        
        logger.info(f"✅ Synced {count} locations")
        logger.info(f"   Total in DB: {total} (city: {city_count}, ward: {ward_count})")
        
        # Check if city has lat/lon
        with db_conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT location_id, name_vi, lat, lon
                FROM locations
                WHERE type = 'city'
                LIMIT 1
            """)
            city = cur.fetchone()
            if city:
                logger.info(f"   City: {city['name_vi']} at ({city['lat']}, {city['lon']})")
                if city['lat'] is None or city['lon'] is None:
                    logger.warning("⚠️  City missing lat/lon")
                    return False
        
        return True
        
    except Exception as e:
        logger.error(f"❌ HanoiAir sync failed: {e}", exc_info=True)
        return False


def test_openweather_onecall(db_conn):
    """Test OpenWeather One Call API."""
    logger.info("=" * 60)
    logger.info("Testing OpenWeather One Call API...")
    logger.info("=" * 60)
    
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        logger.warning("⚠️  OPENWEATHER_API_KEY not set, skipping")
        return True
    
    try:
        from src.ingestion.openweather_onecall_ingestor import OpenWeatherOneCallIngestor
        
        # Get city location
        with db_conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT location_id, lat, lon, name_vi
                FROM locations
                WHERE type = 'city' AND lat IS NOT NULL AND lon IS NOT NULL
                LIMIT 1
            """)
            city = cur.fetchone()
        
        if not city:
            logger.warning("⚠️  No city location found, skipping")
            return True
        
        logger.info(f"Testing with {city['name_vi']} at ({city['lat']}, {city['lon']})")
        
        ingestor = OpenWeatherOneCallIngestor(db_conn, api_key)
        count = ingestor.ingest_location(
            city["location_id"], city["lat"], city["lon"]
        )
        
        logger.info(f"✅ Ingested {count} records")
        
        # Verify records
        with db_conn.cursor() as cur:
            cur.execute("""
                SELECT COUNT(*) FROM observations_raw
                WHERE location_id = %s AND source_id = 'openweather_onecall'
            """, (city["location_id"],))
            obs_count = cur.fetchone()[0]
            
            cur.execute("""
                SELECT COUNT(*) FROM forecasts_raw
                WHERE location_id = %s AND source_id = 'openweather_onecall'
            """, (city["location_id"],))
            forecast_count = cur.fetchone()[0]
        
        logger.info(f"   Observations: {obs_count}, Forecasts: {forecast_count}")
        return True
        
    except Exception as e:
        logger.error(f"❌ OpenWeather One Call failed: {e}", exc_info=True)
        return False


def test_openweather_air(db_conn):
    """Test OpenWeather Air Pollution API."""
    logger.info("=" * 60)
    logger.info("Testing OpenWeather Air Pollution API...")
    logger.info("=" * 60)
    
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        logger.warning("⚠️  OPENWEATHER_API_KEY not set, skipping")
        return True
    
    try:
        from src.ingestion.openweather_air_ingestor import OpenWeatherAirIngestor
        
        # Get city location
        with db_conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT location_id, lat, lon, name_vi
                FROM locations
                WHERE type = 'city' AND lat IS NOT NULL AND lon IS NOT NULL
                LIMIT 1
            """)
            city = cur.fetchone()
        
        if not city:
            logger.warning("⚠️  No city location found, skipping")
            return True
        
        ingestor = OpenWeatherAirIngestor(db_conn, api_key)
        count = ingestor.ingest_location(
            city["location_id"], city["lat"], city["lon"]
        )
        
        logger.info(f"✅ Ingested {count} records")
        
        # Verify records
        with db_conn.cursor() as cur:
            cur.execute("""
                SELECT COUNT(*) FROM observations_raw
                WHERE location_id = %s AND source_id = 'openweather_air'
            """, (city["location_id"],))
            obs_count = cur.fetchone()[0]
            
            cur.execute("""
                SELECT COUNT(*) FROM forecasts_raw
                WHERE location_id = %s AND source_id = 'openweather_air'
            """, (city["location_id"],))
            forecast_count = cur.fetchone()[0]
        
        logger.info(f"   Observations: {obs_count}, Forecasts: {forecast_count}")
        return True
        
    except Exception as e:
        logger.error(f"❌ OpenWeather Air failed: {e}", exc_info=True)
        return False


def test_openmeteo_weather(db_conn):
    """Test Open-Meteo Weather API."""
    logger.info("=" * 60)
    logger.info("Testing Open-Meteo Weather API...")
    logger.info("=" * 60)
    
    try:
        from src.ingestion.openmeteo_weather_ingestor import OpenMeteoWeatherIngestor
        
        # Get city location
        with db_conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT location_id, lat, lon, name_vi
                FROM locations
                WHERE type = 'city' AND lat IS NOT NULL AND lon IS NOT NULL
                LIMIT 1
            """)
            city = cur.fetchone()
        
        if not city:
            logger.warning("⚠️  No city location found, skipping")
            return True
        
        ingestor = OpenMeteoWeatherIngestor(db_conn)
        count = ingestor.ingest_location(
            city["location_id"], city["lat"], city["lon"]
        )
        
        logger.info(f"✅ Ingested {count} records")
        
        # Verify records
        with db_conn.cursor() as cur:
            cur.execute("""
                SELECT COUNT(*) FROM forecasts_raw
                WHERE location_id = %s AND source_id = 'openmeteo_weather'
            """, (city["location_id"],))
            forecast_count = cur.fetchone()[0]
        
        logger.info(f"   Forecasts: {forecast_count}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Open-Meteo Weather failed: {e}", exc_info=True)
        db_conn.rollback()  # Rollback on error
        return False


def test_openmeteo_air(db_conn):
    """Test Open-Meteo Air Quality API."""
    logger.info("=" * 60)
    logger.info("Testing Open-Meteo Air Quality API...")
    logger.info("=" * 60)
    
    try:
        from src.ingestion.openmeteo_air_ingestor import OpenMeteoAirIngestor
        
        # Get city location
        with db_conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT location_id, lat, lon, name_vi
                FROM locations
                WHERE type = 'city' AND lat IS NOT NULL AND lon IS NOT NULL
                LIMIT 1
            """)
            city = cur.fetchone()
        
        if not city:
            logger.warning("⚠️  No city location found, skipping")
            return True
        
        ingestor = OpenMeteoAirIngestor(db_conn)
        count = ingestor.ingest_location(
            city["location_id"], city["lat"], city["lon"]
        )
        
        logger.info(f"✅ Ingested {count} records")
        
        # Verify records
        with db_conn.cursor() as cur:
            cur.execute("""
                SELECT COUNT(*) FROM forecasts_raw
                WHERE location_id = %s AND source_id = 'openmeteo_air'
            """, (city["location_id"],))
            forecast_count = cur.fetchone()[0]
        
        logger.info(f"   Forecasts: {forecast_count}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Open-Meteo Air Quality failed: {e}", exc_info=True)
        db_conn.rollback()  # Rollback on error
        return False


def test_data_fusion(db_conn):
    """Test data fusion."""
    logger.info("=" * 60)
    logger.info("Testing data fusion...")
    logger.info("=" * 60)
    
    try:
        from src.fusion.observations_fusion_job import ObservationsFusionJob
        from src.fusion.forecasts_fusion_job import ForecastsFusionJob
        
        # Fuse observations
        obs_fusion = ObservationsFusionJob(db_conn)
        obs_count = obs_fusion.fuse_observations()
        logger.info(f"✅ Fused {obs_count} observations")
        
        # Fuse forecasts
        forecast_fusion = ForecastsFusionJob(db_conn)
        forecast_count = forecast_fusion.fuse_forecasts()
        logger.info(f"✅ Fused {forecast_count} forecasts")
        
        # Verify canonical tables
        with db_conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM observations_canonical")
            canonical_obs = cur.fetchone()[0]
            
            cur.execute("SELECT COUNT(*) FROM forecasts_canonical")
            canonical_forecasts = cur.fetchone()[0]
        
        logger.info(f"   Canonical observations: {canonical_obs}")
        logger.info(f"   Canonical forecasts: {canonical_forecasts}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Data fusion failed: {e}", exc_info=True)
        db_conn.rollback()  # Rollback on error
        return False


def main():
    """Run all tests."""
    logger.info("=" * 60)
    logger.info("Starting Ingestion Pipeline Tests")
    logger.info("=" * 60)
    
    # Step 1: Database connection
    try:
        db_conn = get_db_connection()
    except Exception as e:
        logger.error("Cannot proceed without database connection")
        return 1
    
    try:
        # Step 2: Check schema
        if not check_schema(db_conn):
            return 1
        
        # Step 3: Initialize API sources
        logger.info("=" * 60)
        logger.info("Initializing API sources...")
        logger.info("=" * 60)
        from scripts.run_ingestion import init_api_sources
        init_api_sources(db_conn)
        
        # Step 4: Test HanoiAir sync
        if not test_hanoiair_sync(db_conn):
            logger.error("HanoiAir sync failed, cannot proceed")
            return 1
        
        # Step 5: Test OpenWeather APIs
        if not test_openweather_onecall(db_conn):
            logger.warning("OpenWeather One Call failed, but continuing...")
        
        if not test_openweather_air(db_conn):
            logger.warning("OpenWeather Air failed, but continuing...")
        
        # Step 6: Test Open-Meteo APIs
        if not test_openmeteo_weather(db_conn):
            logger.warning("Open-Meteo Weather failed, but continuing...")
        
        if not test_openmeteo_air(db_conn):
            logger.warning("Open-Meteo Air Quality failed, but continuing...")
        
        # Step 7: Test data fusion
        if not test_data_fusion(db_conn):
            logger.warning("Data fusion failed, but continuing...")
        
        logger.info("=" * 60)
        logger.info("✅ All tests completed!")
        logger.info("=" * 60)
        
        return 0
        
    finally:
        db_conn.close()


if __name__ == "__main__":
    sys.exit(main())
