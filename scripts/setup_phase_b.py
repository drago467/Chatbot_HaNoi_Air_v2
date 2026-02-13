#!/usr/bin/env python3
"""Setup Phase B: Chạy migrations và tạo views/functions cho chatbot query layer."""

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


def get_db_connection():
    """Get database connection với hỗ trợ POSTGRES_* variables."""
    # Thử POSTGRES_URL trước
    postgres_url = os.getenv("POSTGRES_URL")
    if postgres_url:
        logger.info("Using POSTGRES_URL")
        # Parse POSTGRES_URL (format: postgresql://user:password@host:port/dbname)
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
            else:
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
            
            logger.info(f"Connecting to: {db_host}:{db_port}/{db_name} as {db_user}")
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
    
    # Fix duplicate database name (nếu có)
    if db_name and len(db_name) > 20 and db_name == db_name[:len(db_name)//2] * 2:
        db_name = db_name[:len(db_name)//2]
        logger.warning(f"Fixed duplicate database name, using: {db_name}")
    
    logger.info(f"Using POSTGRES_* vars: {db_host}:{db_port}/{db_name} as {db_user}")
    return psycopg2.connect(
        host=db_host,
        port=db_port,
        database=db_name,
        user=db_user,
        password=db_password
    )


def run_sql_file(conn, sql_file: Path, description: str):
    """Chạy một file SQL.
    
    Args:
        conn: Database connection
        sql_file: Path to SQL file
        description: Mô tả cho logging
    """
    if not sql_file.exists():
        logger.warning(f"⚠️  File not found: {sql_file} - skipping")
        return False
    
    logger.info(f"📄 Running {description}...")
    logger.info(f"   File: {sql_file}")
    
    try:
        with open(sql_file, "r", encoding="utf-8") as f:
            sql_content = f.read()
        
        with conn.cursor() as cur:
            cur.execute(sql_content)
            conn.commit()
        
        logger.info(f"✅ {description} completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error running {description}: {e}")
        conn.rollback()
        return False


def main():
    """Chạy tất cả migrations và views cho Phase B."""
    logger.info("=" * 60)
    logger.info("Setting up Phase B: Chatbot Query Layer")
    logger.info("=" * 60)
    
    # Connect to database
    logger.info("Connecting to database...")
    try:
        conn = get_db_connection()
        logger.info("✅ Connected to database")
    except Exception as e:
        logger.error(f"❌ Failed to connect to database: {e}")
        return 1
    
    success_count = 0
    total_count = 0
    
    try:
        base_path = Path(__file__).parent.parent
        
        # Step 1: Migration - add admin_path
        total_count += 1
        migration_file = base_path / "db" / "migrations" / "add_location_admin_path.sql"
        if run_sql_file(conn, migration_file, "Migration: Add admin_path to locations"):
            success_count += 1
        
        # Step 2: AQI thresholds functions
        total_count += 1
        aqi_file = base_path / "db" / "aqi_thresholds.sql"
        if run_sql_file(conn, aqi_file, "AQI thresholds functions"):
            success_count += 1
        
        # Step 3: Views
        views_dir = base_path / "db" / "views"
        view_files = [
            ("vw_current_air_quality_insights.sql", "View: Current air quality insights"),
            ("vw_hourly_forecast_insights.sql", "View: Hourly forecast insights"),
            ("vw_daily_forecast_insights.sql", "View: Daily forecast insights"),
            ("vw_trend_insights.sql", "Function: Trend insights"),
            ("vw_district_now_insights.sql", "View: District-level current air quality insights"),
        ]
        
        for view_file, description in view_files:
            total_count += 1
            view_path = views_dir / view_file
            if run_sql_file(conn, view_path, description):
                success_count += 1
        
        # Summary
        logger.info("=" * 60)
        logger.info(f"Summary: {success_count}/{total_count} operations completed successfully")
        logger.info("=" * 60)
        
        if success_count == total_count:
            logger.info("✅ Phase B setup completed successfully!")
            return 0
        else:
            logger.warning(f"⚠️  Phase B setup completed with {total_count - success_count} errors")
            return 1
        
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        return 1
    finally:
        conn.close()


if __name__ == "__main__":
    sys.exit(main())
