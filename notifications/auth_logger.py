"""
notifications/auth_logger.py
=============================
Authorization logging for Telegram bot.

Tracks all authorization attempts (successful and failed) in the database.
Provides methods to query and analyze access patterns.
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class AuthorizationLogger:
    """Logs and analyzes Telegram bot authorization attempts."""

    def __init__(self, db_client=None):
        """
        Initialize the authorization logger.

        Args:
            db_client: DBClient instance (optional)
        """
        self.db = db_client

    def log_attempt(self, chat_id: int, status: str, command: str = None,
                   username: str = None, first_name: str = None,
                   last_name: str = None, ip_address: str = None):
        """
        Log an authorization attempt to the database.
        """
        try:
            if self.db is None:
                logger.info(f"AuthLog: {status.upper()} {chat_id} | cmd={command}")
                return

            query = """
                INSERT INTO telegram_auth_log 
                (chat_id, username, first_name, last_name, status, command_attempted, ip_address)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            self.db.execute_query(query, (
                chat_id, username, first_name, last_name,
                status, command, ip_address
            ))

            logger.info(f"AuthLog: {status.upper()} | chat_id={chat_id} | cmd={command}")

        except Exception as e:
            logger.error(f"Failed to log authorization attempt: {e}")

    def get_unauthorized_attempts(self, hours: int = 24, limit: int = 100) -> List[Dict]:
        """
        Get unauthorized access attempts using the database view for analysis.
        """
        if self.db is None:
            return []

        try:
            query = """
                SELECT * FROM telegram_unauthorized_attempts
                WHERE last_attempt > NOW() - INTERVAL '%s hours'
                LIMIT %s
            """
            # DBClient.execute_query returns list of tuples. 
            # We need to map them to dicts or handle them correctly.
            # However, the view has columns: chat_id, username, first_name, last_name, command_attempted, attempt_count, last_attempt, first_attempt
            rows = self.db.execute_query(query, (hours, limit))
            if not rows:
                return []
                
            results = []
            for row in rows:
                results.append({
                    'chat_id': row[0],
                    'username': row[1],
                    'first_name': row[2],
                    'last_name': row[3],
                    'command_attempted': row[4],
                    'attempt_count': row[5],
                    'timestamp': row[6], # last_attempt
                    'first_attempt': row[7]
                })
            return results

        except Exception as e:
            logger.error(f"Failed to query unauthorized attempts: {e}")
            return []

    def get_authorized_users(self, limit: int = 50) -> List[Dict]:
        """
        Get authorized users with their access stats from the view.
        """
        if self.db is None:
            return []

        try:
            query = "SELECT * FROM telegram_authorized_users LIMIT %s"
            rows = self.db.execute_query(query, (limit,))
            if not rows:
                return []
                
            results = []
            for row in rows:
                results.append({
                    'chat_id': row[0],
                    'username': row[1],
                    'first_name': row[2],
                    'last_name': row[3],
                    'command_count': row[4],
                    'last_access': row[5],
                    'first_access': row[6]
                })
            return results

        except Exception as e:
            logger.error(f"Failed to query authorized users: {e}")
            return []

    def get_daily_summary(self, days: int = 7) -> List[Dict]:
        """
        Get daily authorization summary from the view.
        """
        if self.db is None:
            return []

        try:
            query = "SELECT * FROM telegram_auth_daily_summary WHERE date > NOW() - INTERVAL '%s days' LIMIT %s"
            rows = self.db.execute_query(query, (days, days * 2))
            if not rows:
                return []
                
            results = []
            for row in rows:
                results.append({
                    'date': row[0],
                    'status': row[1],
                    'attempt_count': row[2],
                    'unique_users': row[3]
                })
            return results

        except Exception as e:
            logger.error(f"Failed to query daily summary: {e}")
            return []

    def get_suspicious_ips(self, attempt_threshold: int = 5, hours: int = 24) -> List[Dict]:
        """
        Identify suspicious IP addresses.
        """
        if self.db is None:
            return []

        try:
            query = """
                SELECT 
                    ip_address, 
                    COUNT(*) as attempt_count,
                    COUNT(DISTINCT chat_id) as unique_chat_ids,
                    MAX(timestamp) as last_attempt
                FROM telegram_auth_log
                WHERE status = 'unauthorized'
                AND ip_address IS NOT NULL
                AND timestamp > NOW() - INTERVAL '%s hours'
                GROUP BY ip_address
                HAVING COUNT(*) >= %s
                ORDER BY attempt_count DESC
            """
            rows = self.db.execute_query(query, (hours, attempt_threshold))
            if not rows:
                return []
                
            results = []
            for row in rows:
                results.append({
                    'ip_address': row[0],
                    'attempt_count': row[1],
                    'unique_chat_ids': row[2],
                    'last_attempt': row[3]
                })
            return results

        except Exception as e:
            logger.error(f"Failed to query suspicious IPs: {e}")
            return []


    def is_chat_id_whitelisted(self, chat_id: int) -> bool:
        """
        Check if a Chat ID has ever been authorized.

        Args:
            chat_id: Telegram Chat ID

        Returns:
            True if authorized at least once
        """
        if self.db is None:
            return False

        try:
            query = """
                SELECT COUNT(*) as count
                FROM telegram_auth_log
                WHERE chat_id = %s AND status = 'authorized'
                LIMIT 1
            """

            self.db.execute(query, (chat_id,))
            result = self.db.fetchone()
            return result['count'] > 0 if result else False

        except Exception as e:
            logger.error(f"Failed to check whitelist status: {e}")
            return False
