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

    def __init__(self, db_connection=None):
        """
        Initialize the authorization logger.

        Args:
            db_connection: Database connection object (optional, for future use)
        """
        self.db = db_connection

    def log_attempt(self, chat_id: int, status: str, command: str = None,
                   username: str = None, first_name: str = None,
                   last_name: str = None, ip_address: str = None):
        """
        Log an authorization attempt to the database.

        Args:
            chat_id: Telegram Chat ID
            status: 'authorized' or 'unauthorized'
            command: Command attempted
            username: Telegram username
            first_name: User's first name
            last_name: User's last name
            ip_address: IP address (if available)
        """
        try:
            if self.db is None:
                logger.debug(f"AuthLog: {status.upper()} {chat_id} | cmd={command}")
                return

            query = """
                INSERT INTO telegram_auth_log
                (chat_id, username, first_name, last_name, status, command_attempted, ip_address)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            self.db.execute(query, (
                chat_id, username, first_name, last_name,
                status, command, ip_address
            ))
            self.db.commit()

            logger.info(f"AuthLog: {status.upper()} | chat_id={chat_id} | cmd={command}")

        except Exception as e:
            logger.error(f"Failed to log authorization attempt: {e}")

    def get_unauthorized_attempts(self, hours: int = 24, limit: int = 100) -> List[Dict]:
        """
        Get unauthorized access attempts.

        Args:
            hours: Look back this many hours
            limit: Maximum results

        Returns:
            List of unauthorized attempts
        """
        if self.db is None:
            return []

        try:
            query = """
                SELECT
                    chat_id,
                    username,
                    first_name,
                    last_name,
                    command_attempted,
                    timestamp,
                    COUNT(*) as attempt_count
                FROM telegram_auth_log
                WHERE status = 'unauthorized'
                AND timestamp > NOW() - INTERVAL %s HOUR
                GROUP BY chat_id, username, first_name, last_name, command_attempted, timestamp
                ORDER BY timestamp DESC
                LIMIT %s
            """

            self.db.execute(query, (hours, limit))
            results = self.db.fetchall()
            return [dict(row) for row in results]

        except Exception as e:
            logger.error(f"Failed to query unauthorized attempts: {e}")
            return []

    def get_authorized_users(self, limit: int = 50) -> List[Dict]:
        """
        Get authorized users with their access stats.

        Args:
            limit: Maximum results

        Returns:
            List of authorized users
        """
        if self.db is None:
            return []

        try:
            query = """
                SELECT
                    chat_id,
                    username,
                    first_name,
                    last_name,
                    COUNT(*) as command_count,
                    MAX(timestamp) as last_access,
                    MIN(timestamp) as first_access
                FROM telegram_auth_log
                WHERE status = 'authorized'
                GROUP BY chat_id, username, first_name, last_name
                ORDER BY last_access DESC
                LIMIT %s
            """

            self.db.execute(query, (limit,))
            results = self.db.fetchall()
            return [dict(row) for row in results]

        except Exception as e:
            logger.error(f"Failed to query authorized users: {e}")
            return []

    def get_daily_summary(self, days: int = 7) -> List[Dict]:
        """
        Get daily authorization summary.

        Args:
            days: Look back this many days

        Returns:
            List of daily summaries
        """
        if self.db is None:
            return []

        try:
            query = """
                SELECT
                    DATE(timestamp) as date,
                    status,
                    COUNT(*) as attempt_count,
                    COUNT(DISTINCT chat_id) as unique_users
                FROM telegram_auth_log
                WHERE timestamp > NOW() - INTERVAL %s DAY
                GROUP BY DATE(timestamp), status
                ORDER BY date DESC
            """

            self.db.execute(query, (days,))
            results = self.db.fetchall()
            return [dict(row) for row in results]

        except Exception as e:
            logger.error(f"Failed to query daily summary: {e}")
            return []

    def get_suspicious_ips(self, attempt_threshold: int = 5, hours: int = 24) -> List[Dict]:
        """
        Identify suspicious IP addresses with multiple unauthorized attempts.

        Args:
            attempt_threshold: Minimum attempts to flag as suspicious
            hours: Look back this many hours

        Returns:
            List of suspicious IPs with attempt counts
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
                AND timestamp > NOW() - INTERVAL %s HOUR
                GROUP BY ip_address
                HAVING COUNT(*) >= %s
                ORDER BY attempt_count DESC
            """

            self.db.execute(query, (hours, attempt_threshold))
            results = self.db.fetchall()
            return [dict(row) for row in results]

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
