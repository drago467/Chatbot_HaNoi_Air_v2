#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Check locations lat/lon in database."""

import logging
import os
import sys
from pathlib import Path

import psycopg2
from psycopg2.extras import RealDictCursor

# Fix encoding for Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

logging.basicConfig(level=logging.INFO)
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
    """Get database connection."""
    database_url = os.getenv("DATABASE_URL")
    if database_url:
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
                        db_host = host_part
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
    
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        database=os.getenv("DB_NAME", "hanoiair_chatbot"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "")
    )


def main():
    """Check locations."""
    conn = get_db_connection()
    
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # Check city
            cur.execute("""
                SELECT name_vi, lat, lon, bbox
                FROM locations
                WHERE type = 'city'
            """)
            city = cur.fetchone()
            if city:
                print(f"City: {city['name_vi']}")
                print(f"  Lat: {city['lat']}, Lon: {city['lon']}")
                print(f"  BBox: {city['bbox']}")
            
            # Check wards
            cur.execute("""
                SELECT COUNT(*) as total,
                       COUNT(lat) as with_lat,
                       COUNT(lon) as with_lon
                FROM locations
                WHERE type = 'ward'
            """)
            stats = cur.fetchone()
            print(f"\nWards: {stats['total']} total, {stats['with_lat']} with lat, {stats['with_lon']} with lon")
            
            # Sample wards with lat/lon
            cur.execute("""
                SELECT name_vi, lat, lon, bbox
                FROM locations
                WHERE type = 'ward' AND lat IS NOT NULL AND lon IS NOT NULL
                ORDER BY location_id
                LIMIT 5
            """)
            print("\nSample wards with lat/lon:")
            for ward in cur.fetchall():
                print(f"  {ward['name_vi']}: ({ward['lat']}, {ward['lon']})")
                if ward['bbox']:
                    bbox = ward['bbox']
                    print(f"    BBox: minx={bbox.get('minx')}, miny={bbox.get('miny')}, maxx={bbox.get('maxx')}, maxy={bbox.get('maxy')}")
            
            # Wards without lat/lon
            cur.execute("""
                SELECT COUNT(*) as missing
                FROM locations
                WHERE type = 'ward' AND (lat IS NULL OR lon IS NULL)
            """)
            missing = cur.fetchone()['missing']
            if missing > 0:
                print(f"\n⚠️  {missing} wards missing lat/lon")
                cur.execute("""
                    SELECT name_vi, hanoiair_internal_id
                    FROM locations
                    WHERE type = 'ward' AND (lat IS NULL OR lon IS NULL)
                    LIMIT 5
                """)
                print("Sample missing:")
                for ward in cur.fetchall():
                    print(f"  {ward['name_vi']} ({ward['hanoiair_internal_id']})")
        
        return 0
        
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        return 1
    finally:
        conn.close()


if __name__ == "__main__":
    sys.exit(main())
