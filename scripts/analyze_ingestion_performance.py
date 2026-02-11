#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phân tích hiệu suất ingestion pipeline và tạo báo cáo chi tiết."""

import logging
import os
import sys
from pathlib import Path
from datetime import datetime, timedelta

import psycopg2
from psycopg2.extras import RealDictCursor

# Fix encoding for Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

sys.path.insert(0, str(Path(__file__).parent.parent))

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


def analyze_api_calls(db_conn):
    """Phân tích số lượng API calls đã thực hiện."""
    print("=" * 80)
    print("PHÂN TÍCH API CALLS")
    print("=" * 80)
    
    with db_conn.cursor(cursor_factory=RealDictCursor) as cur:
        # Tổng số requests
        cur.execute("""
            SELECT source_id, COUNT(*) as total_calls,
                   COUNT(CASE WHEN http_status = 200 THEN 1 END) as success_calls,
                   COUNT(CASE WHEN http_status != 200 THEN 1 END) as error_calls,
                   AVG(latency_ms) as avg_latency_ms,
                   MAX(latency_ms) as max_latency_ms,
                   MIN(latency_ms) as min_latency_ms
            FROM api_requests
            WHERE requested_at >= NOW() - INTERVAL '24 hours'
            GROUP BY source_id
            ORDER BY total_calls DESC
        """)
        
        print("\n📊 Thống kê API Calls (24h gần nhất):")
        print("-" * 80)
        total_calls = 0
        total_time = 0
        
        for row in cur.fetchall():
            total_calls += row['total_calls']
            total_time += row['avg_latency_ms'] * row['total_calls'] / 1000  # seconds
            
            print(f"\n{row['source_id']}:")
            print(f"  Tổng calls: {row['total_calls']}")
            print(f"  Thành công: {row['success_calls']} ({row['success_calls']/row['total_calls']*100:.1f}%)")
            print(f"  Lỗi: {row['error_calls']}")
            print(f"  Latency trung bình: {row['avg_latency_ms']:.0f}ms")
            print(f"  Latency min/max: {row['min_latency_ms']:.0f}ms / {row['max_latency_ms']:.0f}ms")
        
        print(f"\n📈 Tổng cộng: {total_calls} calls trong ~{total_time:.1f}s")
    
    return total_calls, total_time


def analyze_ingestion_flow():
    """Phân tích flow ingestion và tính toán thời gian ước tính."""
    print("\n" + "=" * 80)
    print("PHÂN TÍCH INGESTION FLOW")
    print("=" * 80)
    
    # Số lượng locations
    num_locations = 127  # 1 city + 126 wards
    
    # Rate limits
    rate_limits = {
        "openweather_onecall": {"per_minute": 60, "per_day": 1000},
        "openweather_air": {"per_minute": 60, "per_day": 1000},  # Shared với One Call
        "openmeteo_weather": {"per_minute": None, "per_day": None},
        "openmeteo_air": {"per_minute": None, "per_day": None},
        "hanoiair": {"per_minute": None, "per_day": None}
    }
    
    # Số calls per location
    calls_per_location = {
        "openweather_onecall": 1,  # 1 call cho current + hourly + daily
        "openweather_air": 2,  # 1 call current + 1 call forecast
        "openmeteo_weather": 1,
        "openmeteo_air": 1,
        "hanoiair": 0  # Chỉ gọi 1 lần cho tất cả wards
    }
    
    # Latency ước tính (ms)
    estimated_latency = {
        "openweather_onecall": 800,
        "openweather_air": 900,
        "openmeteo_weather": 1200,
        "openmeteo_air": 1200,
        "hanoiair": 500
    }
    
    print("\n📋 Cấu hình Ingestion:")
    print(f"  Số locations: {num_locations} (1 city + 126 wards)")
    
    print("\n🔢 Số lượng API Calls cần thiết:")
    total_calls = 0
    for source, calls in calls_per_location.items():
        if source == "hanoiair":
            # HanoiAir: 1 call sync locations + 126 calls cho wards
            calls_needed = 1 + 126
        else:
            calls_needed = calls * num_locations
        
        total_calls += calls_needed
        print(f"  {source}: {calls_needed} calls")
    
    print(f"\n  TỔNG CỘNG: {total_calls} API calls")
    
    print("\n⏱️  Thời gian ước tính (không có rate limiting):")
    total_time_seconds = 0
    for source, calls in calls_per_location.items():
        if source == "hanoiair":
            calls_needed = 1 + 126
        else:
            calls_needed = calls * num_locations
        
        time_needed = (calls_needed * estimated_latency[source]) / 1000
        total_time_seconds += time_needed
        print(f"  {source}: {calls_needed} calls × {estimated_latency[source]}ms = {time_needed:.1f}s")
    
    print(f"\n  TỔNG THỜI GIAN (lý thuyết): {total_time_seconds:.1f}s (~{total_time_seconds/60:.1f} phút)")
    
    print("\n🚦 Ảnh hưởng của Rate Limiting:")
    # OpenWeather: 60 calls/min, shared giữa 2 APIs
    openweather_calls = (calls_per_location["openweather_onecall"] + calls_per_location["openweather_air"]) * num_locations
    openweather_time = (openweather_calls / 60) * 60  # seconds (với rate limit 60/min)
    print(f"  OpenWeather APIs: {openweather_calls} calls")
    print(f"    Rate limit: 60 calls/min (shared)")
    print(f"    Thời gian tối thiểu: {openweather_time:.0f}s (~{openweather_time/60:.1f} phút)")
    
    # Open-Meteo: không có limit
    openmeteo_calls = (calls_per_location["openmeteo_weather"] + calls_per_location["openmeteo_air"]) * num_locations
    openmeteo_time = (openmeteo_calls * estimated_latency["openmeteo_weather"]) / 1000
    print(f"  Open-Meteo APIs: {openmeteo_calls} calls")
    print(f"    Không có rate limit")
    print(f"    Thời gian ước tính: {openmeteo_time:.0f}s (~{openmeteo_time/60:.1f} phút)")
    
    # HanoiAir: 126 calls với delay 0.5s
    hanoiair_time = 127 * 0.5 + (127 * estimated_latency["hanoiair"]) / 1000
    print(f"  HanoiAir: 127 calls (1 sync + 126 wards)")
    print(f"    Delay: 0.5s giữa các calls")
    print(f"    Thời gian ước tính: {hanoiair_time:.0f}s (~{hanoiair_time/60:.1f} phút)")
    
    total_with_rate_limit = openweather_time + openmeteo_time + hanoiair_time
    print(f"\n  TỔNG THỜI GIAN (với rate limiting): {total_with_rate_limit:.0f}s (~{total_with_rate_limit/60:.1f} phút)")
    
    return {
        "total_calls": total_calls,
        "total_time_seconds": total_time_seconds,
        "total_with_rate_limit": total_with_rate_limit,
        "openweather_calls": openweather_calls,
        "openmeteo_calls": openmeteo_calls
    }


def analyze_current_performance(db_conn):
    """Phân tích hiệu suất thực tế từ database."""
    print("\n" + "=" * 80)
    print("PHÂN TÍCH HIỆU SUẤT THỰC TẾ")
    print("=" * 80)
    
    with db_conn.cursor(cursor_factory=RealDictCursor) as cur:
        # Thống kê theo location
        cur.execute("""
            SELECT 
                COUNT(DISTINCT location_id) as num_locations,
                COUNT(*) as total_records,
                COUNT(DISTINCT source_id) as num_sources
            FROM observations_raw
            WHERE created_at >= NOW() - INTERVAL '24 hours'
        """)
        obs_stats = cur.fetchone()
        
        cur.execute("""
            SELECT 
                COUNT(DISTINCT location_id) as num_locations,
                COUNT(*) as total_records,
                COUNT(DISTINCT source_id) as num_sources
            FROM forecasts_raw
            WHERE created_at >= NOW() - INTERVAL '24 hours'
        """)
        forecast_stats = cur.fetchone()
        
        print("\n📊 Dữ liệu đã ingest (24h gần nhất):")
        print(f"  Observations: {obs_stats['total_records']} records từ {obs_stats['num_sources']} sources")
        print(f"    Locations: {obs_stats['num_locations']}")
        print(f"  Forecasts: {forecast_stats['total_records']} records từ {forecast_stats['num_sources']} sources")
        print(f"    Locations: {forecast_stats['num_locations']}")
        
        # Thống kê theo source và location
        cur.execute("""
            SELECT source_id, COUNT(DISTINCT location_id) as locations_ingested
            FROM (
                SELECT DISTINCT source_id, location_id FROM observations_raw
                WHERE created_at >= NOW() - INTERVAL '24 hours'
                UNION
                SELECT DISTINCT source_id, location_id FROM forecasts_raw
                WHERE created_at >= NOW() - INTERVAL '24 hours'
            ) AS combined
            GROUP BY source_id
            ORDER BY locations_ingested DESC
        """)
        
        print("\n📍 Số locations đã ingest theo source:")
        for row in cur.fetchall():
            print(f"  {row['source_id']}: {row['locations_ingested']} locations")


def suggest_optimizations(stats):
    """Đề xuất tối ưu hóa."""
    print("\n" + "=" * 80)
    print("ĐỀ XUẤT TỐI ƯU HÓA")
    print("=" * 80)
    
    print("\n💡 Các phương án tối ưu:")
    
    print("\n1. **Parallel Processing (Đa luồng)**")
    print("   - Chạy ingestion cho nhiều locations song song")
    print("   - Sử dụng ThreadPoolExecutor hoặc asyncio")
    print("   - Giảm thời gian từ ~20 phút xuống ~5-7 phút")
    print("   - ⚠️  Cần cẩn thận với rate limits")
    
    print("\n2. **Batch Processing cho Open-Meteo**")
    print("   - Open-Meteo không có rate limit")
    print("   - Có thể chạy song song nhiều requests")
    print("   - Giảm thời gian Open-Meteo từ ~4 phút xuống ~30 giây")
    
    print("\n3. **Tối ưu Rate Limiting**")
    print("   - OpenWeather: 60 calls/min (shared)")
    print("   - Với 127 locations × 2 APIs = 254 calls")
    print("   - Cần ~4.2 phút tối thiểu (không thể giảm)")
    print("   - ✅ Đã tối ưu: rate limiter tự động wait")
    
    print("\n4. **Skip Redundant Calls**")
    print("   - Kiểm tra dữ liệu đã có trong DB trước khi gọi API")
    print("   - Chỉ update khi dữ liệu cũ hơn freshness window")
    print("   - Giảm số lượng calls không cần thiết")
    
    print("\n5. **HanoiAir Ward Forecasts**")
    print("   - Hiện tại: 126 calls tuần tự với delay 0.5s")
    print("   - Có thể chạy song song (không có rate limit)")
    print("   - Giảm từ ~2 phút xuống ~10-15 giây")
    
    print("\n📊 Ước tính thời gian sau tối ưu:")
    print("   - OpenWeather: ~4.2 phút (không thể giảm do rate limit)")
    print("   - Open-Meteo: ~30 giây (parallel)")
    print("   - HanoiAir: ~15 giây (parallel)")
    print("   - Data Fusion: ~30 giây")
    print("   - TỔNG: ~6 phút (thay vì ~20 phút)")


def main():
    """Main function."""
    print("=" * 80)
    print("BÁO CÁO PHÂN TÍCH HIỆU SUẤT INGESTION PIPELINE")
    print("=" * 80)
    print(f"Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Phân tích flow
    stats = analyze_ingestion_flow()
    
    # Phân tích hiệu suất thực tế
    try:
        db_conn = get_db_connection()
        analyze_current_performance(db_conn)
        analyze_api_calls(db_conn)
        db_conn.close()
    except Exception as e:
        logger.warning(f"Không thể kết nối database: {e}")
    
    # Đề xuất tối ưu
    suggest_optimizations(stats)
    
    print("\n" + "=" * 80)
    print("KẾT LUẬN")
    print("=" * 80)
    print(f"""
Với 127 locations, ingestion pipeline hiện tại cần:
- Tổng số API calls: {stats['total_calls']}
- Thời gian ước tính: ~{stats['total_with_rate_limit']/60:.1f} phút

Nguyên nhân chậm:
1. Rate limiting của OpenWeather (60 calls/min) → ~4.2 phút bắt buộc
2. Chạy tuần tự (sequential) → không tận dụng được parallel processing
3. Delay 0.5s giữa các HanoiAir calls → ~1 phút không cần thiết

Giải pháp:
- Implement parallel processing cho Open-Meteo và HanoiAir
- Giữ nguyên rate limiting cho OpenWeather (đã tối ưu)
- Có thể giảm thời gian từ ~20 phút xuống ~6 phút
    """)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
