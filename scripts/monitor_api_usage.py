#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Real-time monitoring dashboard for API usage."""

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

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ingestion.usage_logger import UsageLogger

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


def print_usage_summary(usage_logger: UsageLogger, source_id: str):
    """Print usage summary for a source."""
    summary = usage_logger.get_key_usage_summary(source_id, hours=24)
    
    print(f"\n{'=' * 80}")
    print(f"API Usage Summary: {source_id}")
    print(f"{'=' * 80}")
    
    print("\n📊 Key Status:")
    print("-" * 80)
    for key_stat in summary['key_stats']:
        status = "✅ Active" if key_stat['is_active'] else "❌ Disabled"
        print(f"  {key_stat['key_id']}:")
        print(f"    Status: {status}")
        print(f"    Calls today: {key_stat['calls_today']}/1000")
        print(f"    Calls this minute: {key_stat['calls_this_minute']}/60")
        print(f"    Errors: {key_stat['error_count']}")
        if key_stat['last_error_at']:
            print(f"    Last error: {key_stat['last_error_at']}")
    
    print("\n📈 Request Statistics (24h):")
    print("-" * 80)
    for req_stat in summary['request_stats']:
        success_rate = (req_stat['success_calls'] / req_stat['total_calls'] * 100) if req_stat['total_calls'] > 0 else 0
        print(f"  {req_stat['api_key_id']}:")
        print(f"    Total calls: {req_stat['total_calls']}")
        print(f"    Success: {req_stat['success_calls']} ({success_rate:.1f}%)")
        print(f"    Errors: {req_stat['error_calls']}")
        print(f"    Avg latency: {req_stat['avg_latency_ms']:.0f}ms")
        print(f"    Max latency: {req_stat['max_latency_ms']:.0f}ms")


def print_recent_errors(usage_logger: UsageLogger, source_id: str):
    """Print recent errors."""
    errors = usage_logger.get_recent_errors(source_id, limit=10)
    
    if not errors:
        print("\n✅ No recent errors")
        return
    
    print(f"\n{'=' * 80}")
    print(f"Recent Errors: {source_id}")
    print(f"{'=' * 80}")
    
    for error in errors:
        print(f"\n  Request ID: {error['request_id']}")
        print(f"  Key: {error['api_key_id']}")
        print(f"  Endpoint: {error['endpoint']}")
        print(f"  Status: {error['http_status']}")
        print(f"  Time: {error['requested_at']}")
        if error['parse_error_message']:
            print(f"  Error: {error['parse_error_message']}")


def main():
    """Main function."""
    conn = get_db_connection()
    usage_logger = UsageLogger(conn)
    
    try:
        # Monitor OpenWeather APIs
        print_usage_summary(usage_logger, "openweather_onecall")
        print_recent_errors(usage_logger, "openweather_onecall")
        
        # Also check air pollution
        print_usage_summary(usage_logger, "openweather_air")
        print_recent_errors(usage_logger, "openweather_air")
        
    finally:
        conn.close()


if __name__ == "__main__":
    main()
