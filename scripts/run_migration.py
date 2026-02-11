#!/usr/bin/env python3
"""Run database migration scripts."""

import logging
import os
import sys
from pathlib import Path

import psycopg2

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
    
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        database=os.getenv("DB_NAME", "hanoiair_chatbot"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "")
    )


def run_migration(migration_file: Path):
    """Run a migration file."""
    logger.info(f"Running migration: {migration_file}")
    
    if not migration_file.exists():
        logger.error(f"Migration file not found: {migration_file}")
        return False
    
    conn = None
    try:
        with open(migration_file, 'r', encoding='utf-8') as f:
            migration_sql = f.read()
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(migration_sql)
        conn.commit()
        
        logger.info(f"✅ Migration {migration_file.name} completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error running migration {migration_file.name}: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if conn:
            conn.close()


def main():
    """Run migrations."""
    if len(sys.argv) > 1:
        migration_file = Path(sys.argv[1])
        if not migration_file.is_absolute():
            migration_file = Path(__file__).parent.parent / migration_file
        run_migration(migration_file)
    else:
        # Run default migration
        migration_file = Path(__file__).parent.parent / "db" / "migrations" / "add_api_key_tracking.sql"
        run_migration(migration_file)


if __name__ == "__main__":
    main()
