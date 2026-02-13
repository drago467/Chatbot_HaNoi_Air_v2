#!/usr/bin/env python3
"""Import ward/commune → district mapping into database.

Nguồn dữ liệu: data/location_completed.csv

- Tạo (nếu chưa có) các bản ghi `locations` type='district' cho 30 quận/huyện/thị xã.
- Tạo mapping vào bảng `location_district_membership`.
- Cập nhật `admin_path` cho các district ở dạng: "Hà Nội > <district_name_vi>".
"""

import csv
import logging
import os
import sys
from pathlib import Path
from typing import Dict, Tuple

import psycopg2

# Reuse DB connection helper from setup_database
from setup_database import get_db_connection  # type: ignore

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def load_mapping_csv(csv_path: Path) -> Tuple[int, int]:
    """Import mapping từ CSV vào database.

    Args:
        csv_path: Path tới file CSV hoàn chỉnh

    Returns:
        Tuple (wards_processed, mappings_created)
    """
    if not csv_path.exists():
        logger.error("CSV file not found: %s", csv_path)
        return 0, 0

    # Connect DB
    conn = get_db_connection()
    wards_processed = 0
    mappings_created = 0

    try:
        with conn, conn.cursor() as cur, open(
            csv_path, "r", encoding="utf-8-sig"
        ) as f:
            reader = csv.DictReader(f)

            for row in reader:
                # Handle possible BOM in header names
                ward_name_vi = row.get("ward_name_vi") or row.get("\ufeffward_name_vi")
                ward_name_norm = row.get("ward_name_norm")
                district_name_vi = row.get("district_name_vi")
                district_name_norm = row.get("district_name_norm")

                if not ward_name_vi or not ward_name_norm:
                    continue

                wards_processed += 1

                # Tìm ward location
                cur.execute(
                    """
                    SELECT location_id
                    FROM locations
                    WHERE (name_vi = %s OR name_norm = %s)
                      AND type = 'ward'
                    LIMIT 1
                    """,
                    (ward_name_vi, ward_name_norm),
                )
                ward_row = cur.fetchone()
                if not ward_row:
                    logger.warning(
                        "Ward not found in locations table: %s (%s)",
                        ward_name_vi,
                        ward_name_norm,
                    )
                    continue

                ward_location_id = ward_row[0]

                # Nếu không có district (ví dụ: Phường Hồng Hà trực thuộc thành phố),
                # bỏ qua mapping nhưng vẫn coi là processed.
                if not district_name_vi or not district_name_norm:
                    continue

                # Tìm hoặc tạo district location
                cur.execute(
                    """
                    SELECT location_id
                    FROM locations
                    WHERE name_vi = %s
                      AND type = 'district'
                    LIMIT 1
                    """,
                    (district_name_vi,),
                )
                district_row = cur.fetchone()

                if district_row:
                    district_location_id = district_row[0]
                else:
                    # Tạo mới district location
                    cur.execute(
                        """
                        INSERT INTO locations (
                            hanoiair_internal_id,
                            hanoiair_admin_id,
                            name_vi,
                            name_norm,
                            type,
                            lat,
                            lon,
                            bbox
                        )
                        VALUES (NULL, %s, %s, %s, 'district', NULL, NULL, NULL)
                        RETURNING location_id
                        """,
                        (district_name_norm, district_name_vi, district_name_norm),
                    )
                    district_location_id = cur.fetchone()[0]

                    # Cập nhật admin_path nếu cột này tồn tại
                    try:
                        cur.execute(
                            """
                            UPDATE locations
                            SET admin_path = %s
                            WHERE location_id = %s
                            """,
                            (f"Hà Nội > {district_name_vi}", district_location_id),
                        )
                    except psycopg2.errors.UndefinedColumn:
                        # admin_path có thể chưa tồn tại nếu migration chưa chạy;
                        # bỏ qua phần này.
                        conn.rollback()
                        conn.autocommit = False

                # Tạo mapping vào location_district_membership
                cur.execute(
                    """
                    INSERT INTO location_district_membership (
                        district_location_id,
                        ward_location_id
                    )
                    VALUES (%s, %s)
                    ON CONFLICT (district_location_id, ward_location_id) DO NOTHING
                    """,
                    (district_location_id, ward_location_id),
                )
                if cur.rowcount > 0:
                    mappings_created += 1

        logger.info(
            "Imported mapping for %d wards, created %d membership rows",
            wards_processed,
            mappings_created,
        )
        return wards_processed, mappings_created

    except Exception as exc:  # pragma: no cover - defensive logging
        logger.error("Error importing location mapping: %s", exc)
        conn.rollback()
        return wards_processed, mappings_created
    finally:
        conn.close()


def main() -> int:
    base_path = Path(__file__).parent.parent
    csv_path = base_path / "data" / "location_completed.csv"

    logger.info("Importing location mapping from %s", csv_path)
    wards_processed, mappings_created = load_mapping_csv(csv_path)

    logger.info(
        "Done. Wards processed: %d, mappings created: %d",
        wards_processed,
        mappings_created,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

