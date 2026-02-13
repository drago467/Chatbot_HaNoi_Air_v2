"""Location resolver: Phân giải tên địa điểm từ text input.

Hỗ trợ:
- Fuzzy matching tên phường/xã/quận/thành phố.
- Ưu tiên district khi tên mơ hồ (ví dụ "Cầu Giấy" có cả phường và quận).
- Trả về metadata cho virtual district: aggregate_from, member_count.
"""

import logging
import re
import unicodedata
from typing import Dict, List

import psycopg2
from psycopg2.extras import RealDictCursor

logger = logging.getLogger(__name__)


def normalize_text(text: str) -> str:
    """Chuẩn hóa text để so sánh (remove diacritics, lowercase, trim).
    
    Args:
        text: Text input
    
    Returns:
        Text đã chuẩn hóa
    """
    # Remove diacritics
    normalized = unicodedata.normalize("NFD", text)
    ascii_text = "".join(
        c for c in normalized if unicodedata.category(c) != "Mn"
    )
    # Lowercase và trim
    return " ".join(ascii_text.lower().split())


def calculate_similarity(text1: str, text2: str) -> float:
    """Tính độ tương đồng giữa 2 text (simple Jaccard similarity).
    
    Args:
        text1: Text 1
        text2: Text 2
    
    Returns:
        Similarity score (0.0 - 1.0)
    """
    words1 = set(text1.split())
    words2 = set(text2.split())
    
    if not words1 or not words2:
        return 0.0
    
    intersection = len(words1 & words2)
    union = len(words1 | words2)
    
    return intersection / union if union > 0 else 0.0


def resolve_location(
    db_conn: psycopg2.extensions.connection,
    location_text: str,
    min_confidence: float = 0.8,
) -> Dict:
    """Phân giải location từ text input.
    
    Args:
        db_conn: Database connection
        location_text: Text input (ví dụ "Hồ Tây", "Cầu Giấy", "Phường Lĩnh Nam")
        min_confidence: Ngưỡng confidence tối thiểu (default: 0.8)
    
    Returns:
        Dict với format:
        - Khi resolve thành công (location_id != None):
          {
              "location_id": int,
              "name_vi": str,
              "type": str,
              "admin_path": str | None,
              "confidence": float,
              "candidates": List[Dict],  # các ứng viên khác (nếu có)
              "aggregate_from": str | None,  # "wards_communes" nếu là district ảo
              "member_count": int | None,    # số ward/xã thuộc district (nếu có)
          }

        - Khi không đủ chắc chắn (hoặc không tìm thấy):
          {
              "location_id": None,
              "name_vi": None,
              "type": None,
              "admin_path": None,
              "confidence": float,
              "candidates": List[Dict],  # top-N gợi ý để chatbot hỏi lại
              "aggregate_from": None,
              "member_count": None,
          }
    """
    if not location_text or not location_text.strip():
        return {
            "location_id": None,
            "name_vi": None,
            "type": None,
            "admin_path": None,
            "confidence": 0.0,
            "candidates": [],
            "aggregate_from": None,
            "member_count": None,
        }
    
    # Chuẩn hóa input
    normalized_input = normalize_text(location_text)
    
    # Tìm kiếm trong database
    with db_conn.cursor(cursor_factory=RealDictCursor) as cur:
        # Tìm exact match trên name_norm
        cur.execute("""
            SELECT location_id, name_vi, type, admin_path, name_norm
            FROM locations
            WHERE name_norm = %s
            LIMIT 1
        """, (normalized_input,))
        
        exact_match = cur.fetchone()
        
        if exact_match:
            aggregate_from = None
            member_count = None

            if exact_match["type"] == "district":
                # Lấy số members cho district (wards/communes)
                try:
                    cur.execute(
                        """
                        SELECT COUNT(*) AS member_count
                        FROM location_district_membership
                        WHERE district_location_id = %s
                        """,
                        (exact_match["location_id"],),
                    )
                    count_row = cur.fetchone()
                    member_count = count_row["member_count"] if count_row else None
                except Exception:
                    member_count = None

                aggregate_from = "wards_communes" if member_count else None

            return {
                "location_id": exact_match["location_id"],
                "name_vi": exact_match["name_vi"],
                "type": exact_match["type"],
                "admin_path": exact_match.get("admin_path"),
                "confidence": 1.0,
                "candidates": [],
                "aggregate_from": aggregate_from,
                "member_count": member_count,
            }
        
        # Fuzzy match: tìm các locations có name_norm chứa input hoặc ngược lại
        # Escape special characters để tránh SQL injection
        normalized_input_escaped = normalized_input.replace("%", "\\%").replace("_", "\\_")
        pattern_start = f"{normalized_input_escaped}%"
        pattern_contains = f"%{normalized_input_escaped}%"
        
        cur.execute("""
            SELECT location_id, name_vi, type, admin_path, name_norm
            FROM locations
            WHERE name_norm LIKE %s
               OR name_norm LIKE %s
               OR name_norm = %s
            ORDER BY 
                CASE 
                    WHEN name_norm = %s THEN 1
                    WHEN name_norm LIKE %s THEN 2
                    WHEN name_norm LIKE %s THEN 3
                    ELSE 4
                END,
                LENGTH(name_norm)
            LIMIT 10
        """, (
            pattern_start,
            pattern_contains,
            normalized_input,
            normalized_input,
            pattern_start,
            pattern_contains
        ))
        
        candidates = cur.fetchall()
        
        if not candidates:
            return {
                "location_id": None,
                "name_vi": None,
                "type": None,
                "admin_path": None,
                "confidence": 0.0,
                "candidates": []
            }
        
        # Tính similarity cho mỗi candidate
        scored_candidates = []
        for cand in candidates:
            similarity = calculate_similarity(
                normalized_input,
                cand["name_norm"]
            )
            scored_candidates.append({
                "location_id": cand["location_id"],
                "name_vi": cand["name_vi"],
                "type": cand["type"],
                "admin_path": cand.get("admin_path"),
                "confidence": similarity
            })
        
        # Sắp xếp theo confidence
        scored_candidates.sort(key=lambda x: x["confidence"], reverse=True)

        best_match = scored_candidates[0]

        # Ưu tiên district nếu có candidate district với confidence gần bằng best_match
        district_candidates = [
            c for c in scored_candidates if c["type"] == "district"
        ]
        if district_candidates:
            best_district = max(district_candidates, key=lambda x: x["confidence"])
            if best_district["confidence"] >= best_match["confidence"] - 0.05:
                best_match = best_district
        
        # Nếu confidence >= 0.6, tự động chọn best match (ngay cả khi < min_confidence)
        # Điều này giúp xử lý trường hợp "Cầu Giấy" -> "Phường Cầu Giấy"
        if best_match["confidence"] >= 0.6:
            aggregate_from = None
            member_count = None

            if best_match["type"] == "district":
                try:
                    cur.execute(
                        """
                        SELECT COUNT(*) AS member_count
                        FROM location_district_membership
                        WHERE district_location_id = %s
                        """,
                        (best_match["location_id"],),
                    )
                    count_row = cur.fetchone()
                    member_count = count_row["member_count"] if count_row else None
                except Exception:
                    member_count = None

                aggregate_from = "wards_communes" if member_count else None

            return {
                "location_id": best_match["location_id"],
                "name_vi": best_match["name_vi"],
                "type": best_match["type"],
                "admin_path": best_match.get("admin_path"),
                "confidence": best_match["confidence"],
                "candidates": scored_candidates[1:3] if len(scored_candidates) > 1 else [],
                "aggregate_from": aggregate_from,
                "member_count": member_count,
            }
        
        # Nếu confidence < 0.6, trả top-3 candidates
        if best_match["confidence"] < min_confidence:
            return {
                "location_id": None,
                "name_vi": None,
                "type": None,
                "admin_path": None,
                "confidence": best_match["confidence"],
                "candidates": scored_candidates[:3],
                "aggregate_from": None,
                "member_count": None,
            }
        
        # Trả về best match (confidence >= min_confidence)
        aggregate_from = None
        member_count = None

        if best_match["type"] == "district":
            try:
                cur.execute(
                    """
                    SELECT COUNT(*) AS member_count
                    FROM location_district_membership
                    WHERE district_location_id = %s
                    """,
                    (best_match["location_id"],),
                )
                count_row = cur.fetchone()
                member_count = count_row["member_count"] if count_row else None
            except Exception:
                member_count = None

            aggregate_from = "wards_communes" if member_count else None

        return {
            "location_id": best_match["location_id"],
            "name_vi": best_match["name_vi"],
            "type": best_match["type"],
            "admin_path": best_match.get("admin_path"),
            "confidence": best_match["confidence"],
            "candidates": [],
            "aggregate_from": aggregate_from,
            "member_count": member_count,
        }


def resolve_multiple_locations(
    db_conn: psycopg2.extensions.connection,
    location_texts: List[str],
    min_confidence: float = 0.8
) -> List[Dict]:
    """Phân giải nhiều locations cùng lúc.
    
    Args:
        db_conn: Database connection
        location_texts: List các text input
        min_confidence: Ngưỡng confidence tối thiểu
    
    Returns:
        List các kết quả resolve_location
    """
    return [
        resolve_location(db_conn, text, min_confidence)
        for text in location_texts
    ]
