"""Base ingestor class with common functionality for all API ingestors."""

import hashlib
import json
import logging
import time
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional

import psycopg2
from psycopg2.extras import execute_values

logger = logging.getLogger(__name__)


class BaseIngestor(ABC):
    """Base class for all API ingestors.
    
    Provides common functionality:
    - Database connection management
    - Request/response logging
    - Rate limiting
    - Error handling
    """
    
    def __init__(
        self,
        db_conn: psycopg2.extensions.connection,
        source_id: str,
        rate_limit_per_minute: Optional[int] = None,
        rate_limit_per_day: Optional[int] = None,
        api_key_manager: Optional[Any] = None
    ):
        """Initialize base ingestor.
        
        Args:
            db_conn: PostgreSQL database connection
            source_id: Source ID from api_sources table
            rate_limit_per_minute: Optional rate limit per minute
            rate_limit_per_day: Optional rate limit per day
            api_key_manager: Optional ApiKeyManager instance for multiple keys
        """
        self.db_conn = db_conn
        self.source_id = source_id
        self.rate_limit_per_minute = rate_limit_per_minute
        self.rate_limit_per_day = rate_limit_per_day
        self.api_key_manager = api_key_manager
        
        # Rate limiting state (for backward compatibility when no key manager)
        self._minute_calls = []
        self._daily_calls = {}
    
    def log_request(
        self,
        endpoint: str,
        params: Dict[str, Any],
        http_method: str = "GET",
        api_key_id: Optional[str] = None
    ) -> int:
        """Log API request to database.
        
        Args:
            endpoint: API endpoint
            params: Request parameters
            http_method: HTTP method (default: GET)
            api_key_id: Optional API key ID used for this request
        
        Returns:
            request_id: The ID of the logged request
        """
        with self.db_conn.cursor() as cur:
            cur.execute("""
                INSERT INTO api_requests (
                    source_id, endpoint, http_method, params, requested_at, api_key_id
                ) VALUES (%s, %s, %s, %s, NOW(), %s)
                RETURNING request_id
            """, (self.source_id, endpoint, http_method, json.dumps(params), api_key_id))
            request_id = cur.fetchone()[0]
            self.db_conn.commit()
            return request_id
    
    def log_response(
        self,
        request_id: int,
        body_json: Dict[str, Any],
        http_status: int,
        latency_ms: int,
        parse_status: str = "pending",
        parse_error_message: Optional[str] = None
    ) -> int:
        """Log API response to database.
        
        Returns:
            response_id: The ID of the logged response
        """
        # Calculate body hash
        body_str = json.dumps(body_json, sort_keys=True)
        body_hash = hashlib.sha256(body_str.encode()).hexdigest()
        
        with self.db_conn.cursor() as cur:
            # Update request with status and latency
            cur.execute("""
                UPDATE api_requests
                SET http_status = %s, latency_ms = %s, response_size_bytes = %s
                WHERE request_id = %s
            """, (http_status, latency_ms, len(body_str), request_id))
            
            # Insert response
            cur.execute("""
                INSERT INTO api_responses (
                    request_id, received_at, body_json, body_hash,
                    parse_status, parse_error_message
                ) VALUES (%s, NOW(), %s, %s, %s, %s)
                RETURNING response_id
            """, (
                request_id, json.dumps(body_json), body_hash,
                parse_status, parse_error_message
            ))
            response_id = cur.fetchone()[0]
            self.db_conn.commit()
            return response_id
    
    def check_rate_limit(self):
        """Check and enforce rate limits.
        
        If api_key_manager is set, rate limiting is handled by the manager.
        Otherwise, falls back to instance-based rate limiting.
        """
        # If using key manager, rate limiting is handled per-key
        if self.api_key_manager:
            # Key manager handles rate limiting internally
            return
        
        # Fallback to instance-based rate limiting (for backward compatibility)
        current_time = time.time()
        today = datetime.now().date().isoformat()
        
        # Check daily limit
        if self.rate_limit_per_day:
            if today not in self._daily_calls:
                self._daily_calls[today] = 0
            
            if self._daily_calls[today] >= self.rate_limit_per_day:
                raise ValueError(
                    f"Daily rate limit exceeded: {self.rate_limit_per_day} calls/day"
                )
        
        # Check per-minute limit
        if self.rate_limit_per_minute:
            # Clean old calls (older than 1 minute)
            self._minute_calls = [
                t for t in self._minute_calls
                if current_time - t < 60
            ]
            
            if len(self._minute_calls) >= self.rate_limit_per_minute:
                # Wait until oldest call is 1 minute old
                oldest = min(self._minute_calls)
                wait_time = 60 - (current_time - oldest) + 0.1
                if wait_time > 0:
                    logger.info(f"Rate limit: waiting {wait_time:.1f}s")
                    time.sleep(wait_time)
                    # Re-clean after waiting
                    current_time = time.time()
                    self._minute_calls = [
                        t for t in self._minute_calls
                        if current_time - t < 60
                    ]
        
        # Record this call
        self._minute_calls.append(time.time())
        if self.rate_limit_per_day:
            self._daily_calls[today] = self._daily_calls.get(today, 0) + 1
    
    @abstractmethod
    def fetch_data(self, *args, **kwargs) -> Dict[str, Any]:
        """Fetch data from API. Must be implemented by subclasses."""
        pass
    
    @abstractmethod
    def parse_response(
        self,
        response_json: Dict[str, Any],
        response_id: int,
        location_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Parse API response into observations_raw or forecasts_raw records.
        
        Returns:
            List of dicts with keys matching observations_raw or forecasts_raw columns
        """
        pass
