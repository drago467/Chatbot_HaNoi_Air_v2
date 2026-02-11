#!/usr/bin/env python3
"""Setup database schema."""

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
    """Get database connection."""
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


def main():
    """Run schema SQL."""
    schema_file = Path(__file__).parent.parent / "db" / "schema_database_logging.sql"
    
    if not schema_file.exists():
        logger.error(f"Schema file not found: {schema_file}")
        return 1
    
    logger.info(f"Reading schema from {schema_file}")
    with open(schema_file, "r", encoding="utf-8") as f:
        schema_sql = f.read()
    
    logger.info("Connecting to database...")
    conn = get_db_connection()
    
    try:
        with conn.cursor() as cur:
            logger.info("Executing schema SQL...")
            cur.execute(schema_sql)
            conn.commit()
        
        logger.info("✅ Database schema created successfully!")
        return 0
        
    except Exception as e:
        logger.error(f"❌ Error creating schema: {e}")
        conn.rollback()
        return 1
    finally:
        conn.close()


if __name__ == "__main__":
    sys.exit(main())
