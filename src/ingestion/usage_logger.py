"""Enhanced logging for API usage tracking."""

import logging
from datetime import datetime
from typing import Dict, List, Optional

import psycopg2
from psycopg2.extras import RealDictCursor

logger = logging.getLogger(__name__)


class UsageLogger:
    """Logs and tracks API usage for monitoring and analysis."""
    
    def __init__(self, db_conn: psycopg2.extensions.connection):
        """Initialize usage logger.
        
        Args:
            db_conn: Database connection
        """
        self.db_conn = db_conn
    
    def log_api_call(
        self,
        source_id: str,
        endpoint: str,
        api_key_id: Optional[str],
        http_status: int,
        latency_ms: int,
        success: bool
    ):
        """Log an API call for monitoring.
        
        This is already handled by api_requests table, but this provides
        a convenient interface for additional logging if needed.
        """
        # Most logging is done in base_ingestor, but we can add additional
        # metrics here if needed
        pass
    
    def get_key_usage_summary(
        self,
        source_id: str,
        hours: int = 24
    ) -> Dict:
        """Get usage summary for API keys.
        
        Args:
            source_id: Source ID to filter
            hours: Number of hours to look back
        
        Returns:
            Dict with usage statistics
        """
        with self.db_conn.cursor(cursor_factory=RealDictCursor) as cur:
            # Get key usage from api_key_usage table
            cur.execute("""
                SELECT 
                    key_id,
                    calls_today,
                    calls_this_minute,
                    is_active,
                    error_count,
                    last_error_at
                FROM api_key_usage
                WHERE source_id = %s
                ORDER BY key_id
            """, (source_id,))
            key_stats = cur.fetchall()
            
            # Get request stats from api_requests
            cur.execute("""
                SELECT 
                    api_key_id,
                    COUNT(*) as total_calls,
                    COUNT(CASE WHEN http_status = 200 THEN 1 END) as success_calls,
                    COUNT(CASE WHEN http_status != 200 THEN 1 END) as error_calls,
                    AVG(latency_ms) as avg_latency_ms,
                    MAX(latency_ms) as max_latency_ms
                FROM api_requests
                WHERE source_id = %s
                  AND requested_at >= NOW() - INTERVAL '%s hours'
                  AND api_key_id IS NOT NULL
                GROUP BY api_key_id
                ORDER BY api_key_id
            """, (source_id, hours))
            request_stats = cur.fetchall()
            
            return {
                'key_stats': key_stats,
                'request_stats': request_stats,
                'hours': hours
            }
    
    def get_recent_errors(
        self,
        source_id: str,
        limit: int = 10
    ) -> List[Dict]:
        """Get recent API errors.
        
        Args:
            source_id: Source ID to filter
            limit: Maximum number of errors to return
        
        Returns:
            List of error records
        """
        with self.db_conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT 
                    ar.request_id,
                    ar.api_key_id,
                    ar.endpoint,
                    ar.requested_at,
                    ar.http_status,
                    ar.latency_ms,
                    arp.parse_error_message
                FROM api_requests ar
                LEFT JOIN api_responses arp ON ar.request_id = arp.request_id
                WHERE ar.source_id = %s
                  AND (ar.http_status != 200 OR arp.parse_status = 'error')
                ORDER BY ar.requested_at DESC
                LIMIT %s
            """, (source_id, limit))
            return cur.fetchall()
