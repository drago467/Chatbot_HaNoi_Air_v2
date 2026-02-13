#!/usr/bin/env python3
"""Quick manual test for district-level insights.

Ví dụ chạy:
    python scripts/test_district_insights.py
"""

import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv  # type: ignore

# Thiết lập sys.path để import được package src.*
BASE_PATH = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_PATH))

from setup_phase_b import get_db_connection  # type: ignore
from src.chatbot.query_service import QueryService  # type: ignore



logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def main() -> int:
    env_path = BASE_PATH / ".env"
    if env_path.exists():
        load_dotenv(env_path)  # pragma: no cover

    logger.info("Connecting to database...")
    conn = get_db_connection()

    try:
        service = QueryService(conn)

        test_districts = [
            "Quận Cầu Giấy",
            "Quận Hoàng Mai",
            "Huyện Sóc Sơn",
        ]

        for name in test_districts:
            logger.info("=== District: %s ===", name)
            result = service.get_district_now_insights(name, metric="aqi")
            logger.info("Result: %s", result)

        return 0
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())

