"""API Key Manager for managing multiple API keys with round-robin distribution."""

import logging
import os
import time
from datetime import datetime, timedelta
from typing import List, Optional, Tuple

import psycopg2
from psycopg2.extras import RealDictCursor

logger = logging.getLogger(__name__)


class ApiKeyManager:
    """Manages multiple API keys with round-robin distribution and usage tracking.
    
    Features:
    - Round-robin key rotation
    - Per-key usage tracking (calls/min, calls/day)
    - Health check and auto-disable
    - Auto-fallback to next key on errors
    """
    
    def __init__(
        self,
        db_conn: psycopg2.extensions.connection,
        source_id: str,
        env_key_names: List[str],
        rate_limit_per_minute: int = 60,
        rate_limit_per_day: int = 1000,
        max_errors_before_disable: int = 5
    ):
        """Initialize API Key Manager.
        
        Args:
            db_conn: Database connection
            source_id: Source ID (e.g., 'openweather_onecall')
            env_key_names: List of environment variable names for API keys
            rate_limit_per_minute: Rate limit per minute per key
            rate_limit_per_day: Rate limit per day per key
            max_errors_before_disable: Max consecutive errors before disabling key
        """
        self.db_conn = db_conn
        self.source_id = source_id
        self.rate_limit_per_minute = rate_limit_per_minute
        self.rate_limit_per_day = rate_limit_per_day
        self.max_errors_before_disable = max_errors_before_disable
        
        # Load keys from environment
        self.keys: List[str] = []
        self.key_ids: List[str] = []
        for i, env_name in enumerate(env_key_names):
            key = os.getenv(env_name)
            if key:
                self.keys.append(key)
                key_id = f"{source_id}_key_{i}"
                self.key_ids.append(key_id)
            else:
                logger.warning(f"API key {env_name} not found in environment")
        
        if not self.keys:
            raise ValueError(f"No API keys found for {source_id}. Check environment variables: {env_key_names}")
        
        logger.info(f"Initialized ApiKeyManager for {source_id} with {len(self.keys)} keys")
        
        # Initialize keys in database
        self._initialize_keys_in_db()
        
        # Current key index for round-robin
        self._current_index = 0
    
    def _initialize_keys_in_db(self):
        """Initialize or update keys in database."""
        with self.db_conn.cursor() as cur:
            for key_id in self.key_ids:
                cur.execute("""
                    INSERT INTO api_key_usage (
                        key_id, source_id, calls_today, calls_this_minute,
                        last_reset_minute, last_reset_day, is_active
                    ) VALUES (%s, %s, 0, 0, NOW(), CURRENT_DATE, TRUE)
                    ON CONFLICT (key_id) DO UPDATE SET
                        source_id = EXCLUDED.source_id,
                        updated_at = NOW()
                """, (key_id, self.source_id))
            self.db_conn.commit()
    
    def _get_key_usage(self, key_id: str) -> Optional[dict]:
        """Get current usage stats for a key."""
        with self.db_conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT * FROM api_key_usage
                WHERE key_id = %s
            """, (key_id,))
            return cur.fetchone()
    
    def _reset_minute_counter_if_needed(self, key_id: str):
        """Reset minute counter if needed."""
        usage = self._get_key_usage(key_id)
        if usage and usage['last_reset_minute']:
            last_reset = usage['last_reset_minute']
            try:
                if isinstance(last_reset, str):
                    last_reset = datetime.fromisoformat(last_reset.replace('Z', '+00:00'))
                elif not isinstance(last_reset, datetime):
                    return
                
                now = datetime.now(last_reset.tzinfo) if last_reset.tzinfo else datetime.now()
                if now - last_reset >= timedelta(minutes=1):
                    with self.db_conn.cursor() as cur:
                        cur.execute("""
                            UPDATE api_key_usage
                            SET calls_this_minute = 0,
                                last_reset_minute = NOW()
                            WHERE key_id = %s
                        """, (key_id,))
                        self.db_conn.commit()
            except Exception as e:
                logger.warning(f"Error resetting minute counter for {key_id}: {e}")
    
    def _reset_daily_counter_if_needed(self, key_id: str):
        """Reset daily counter if needed."""
        usage = self._get_key_usage(key_id)
        if usage and usage['last_reset_day']:
            last_reset = usage['last_reset_day']
            if isinstance(last_reset, str):
                try:
                    last_reset = datetime.fromisoformat(last_reset).date()
                except:
                    last_reset = datetime.strptime(last_reset, "%Y-%m-%d").date()
            elif hasattr(last_reset, 'date'):
                last_reset = last_reset.date() if hasattr(last_reset, 'date') else last_reset
            
            current_date = datetime.now().date()
            if isinstance(last_reset, type(current_date)) and current_date > last_reset:
                with self.db_conn.cursor() as cur:
                    cur.execute("""
                        UPDATE api_key_usage
                        SET calls_today = 0,
                            last_reset_day = CURRENT_DATE
                        WHERE key_id = %s
                    """, (key_id,))
                    self.db_conn.commit()
    
    def _is_key_available(self, key_id: str) -> bool:
        """Check if a key is available (active and not over limit)."""
        self._reset_minute_counter_if_needed(key_id)
        self._reset_daily_counter_if_needed(key_id)
        
        usage = self._get_key_usage(key_id)
        if not usage or not usage['is_active']:
            return False
        
        # Check daily limit
        if usage['calls_today'] >= self.rate_limit_per_day:
            logger.warning(f"Key {key_id} exceeded daily limit: {usage['calls_today']}/{self.rate_limit_per_day}")
            return False
        
        # Check per-minute limit (conservative: 55 instead of 60)
        conservative_limit = int(self.rate_limit_per_minute * 0.92)  # 92% of limit
        if usage['calls_this_minute'] >= conservative_limit:
            logger.debug(f"Key {key_id} approaching minute limit: {usage['calls_this_minute']}/{conservative_limit}")
            return False
        
        return True
    
    def get_next_key(self) -> Tuple[str, str]:
        """Get next available key using round-robin.
        
        Returns:
            Tuple of (api_key, key_id)
        
        Raises:
            ValueError: If no keys are available
        """
        start_index = self._current_index
        attempts = 0
        
        while attempts < len(self.keys):
            key_id = self.key_ids[self._current_index]
            api_key = self.keys[self._current_index]
            
            # Move to next key for next call
            self._current_index = (self._current_index + 1) % len(self.keys)
            
            if self._is_key_available(key_id):
                return api_key, key_id
            
            attempts += 1
        
        # If we've tried all keys, raise error
        raise ValueError(
            f"No available API keys for {self.source_id}. "
            f"All {len(self.keys)} keys are either disabled or over limit."
        )
    
    def record_call(self, key_id: str, success: bool = True, error_code: Optional[int] = None):
        """Record an API call for a key.
        
        Args:
            key_id: The key ID used
            success: Whether the call was successful
            error_code: HTTP error code if failed (e.g., 429 for rate limit)
        """
        with self.db_conn.cursor() as cur:
            # Update counters
            cur.execute("""
                UPDATE api_key_usage
                SET calls_today = calls_today + 1,
                    calls_this_minute = calls_this_minute + 1,
                    last_reset_minute = COALESCE(last_reset_minute, NOW()),
                    last_reset_day = COALESCE(last_reset_day, CURRENT_DATE),
                    updated_at = NOW()
                WHERE key_id = %s
            """, (key_id,))
            
            # Handle errors
            if not success:
                cur.execute("""
                    UPDATE api_key_usage
                    SET error_count = error_count + 1,
                        last_error_at = NOW(),
                        updated_at = NOW()
                    WHERE key_id = %s
                """, (key_id,))
                
                # Check if we should disable the key
                usage = self._get_key_usage(key_id)
                if usage and usage['error_count'] >= self.max_errors_before_disable:
                    cur.execute("""
                        UPDATE api_key_usage
                        SET is_active = FALSE,
                            updated_at = NOW()
                        WHERE key_id = %s
                    """, (key_id,))
                    logger.warning(f"Disabled key {key_id} after {usage['error_count']} errors")
                
                # If rate limit error (429), temporarily disable
                if error_code == 429:
                    cur.execute("""
                        UPDATE api_key_usage
                        SET is_active = FALSE,
                            updated_at = NOW()
                        WHERE key_id = %s
                    """, (key_id,))
                    logger.warning(f"Temporarily disabled key {key_id} due to rate limit (429)")
            else:
                # Reset error count on success
                cur.execute("""
                    UPDATE api_key_usage
                    SET error_count = 0,
                        updated_at = NOW()
                    WHERE key_id = %s AND error_count > 0
                """, (key_id,))
            
            self.db_conn.commit()
    
    def get_usage_stats(self) -> dict:
        """Get usage statistics for all keys."""
        with self.db_conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT key_id, calls_today, calls_this_minute, is_active, error_count
                FROM api_key_usage
                WHERE source_id = %s
                ORDER BY key_id
            """, (self.source_id,))
            return {
                'keys': cur.fetchall(),
                'total_keys': len(self.keys),
                'active_keys': sum(1 for k in self.keys if self._is_key_available(self.key_ids[self.keys.index(k)]))
            }
