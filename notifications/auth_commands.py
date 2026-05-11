"""
notifications/auth_commands.py
===============================
Telegram commands for authorization logging and monitoring.

Commands:
  /auth_log          — Show recent authorization attempts
  /suspicious        — Show suspicious access patterns
  /auth_users        — Show authorized users and their activity
  /auth_daily        — Show daily authorization summary
  /extract_chat_id   — Extract your Chat ID from logs
"""

import logging
from datetime import datetime
from notifications.auth_logger import AuthorizationLogger

logger = logging.getLogger(__name__)


class AuthorizationCommands:
    """Commands for viewing and analyzing authorization logs."""

    def __init__(self, db_client=None):
        """Initialize with database client."""
        self.auth_logger = AuthorizationLogger(db_client)

    async def auth_log_command(self, update, context):
        """
        Show recent authorization attempts (last 24 hours).
        Usage: /auth_log [hours] [limit]
        """
        try:
            hours = 24
            limit = 20

            if context.args:
                if len(context.args) > 0:
                    hours = int(context.args[0])
                if len(context.args) > 1:
                    limit = int(context.args[1])

            attempts = self.auth_logger.get_unauthorized_attempts(hours=hours, limit=limit)

            if not attempts:
                msg = f"✅ No unauthorized attempts in the last {hours} hours"
                await update.message.reply_html(msg)
                return

            msg = f"🚨 <b>Unauthorized Access Attempts ({hours}h)</b>\n"
            msg += f"━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"

            for attempt in attempts:
                timestamp = attempt.get('timestamp', 'unknown')
                chat_id = attempt.get('chat_id', 'unknown')
                username = attempt.get('username', 'N/A')
                first_name = attempt.get('first_name', '')
                last_name = attempt.get('last_name', '')
                command = attempt.get('command_attempted', 'unknown')
                count = attempt.get('attempt_count', 1)

                user_display = f"@{username}" if username else f"{first_name} {last_name}".strip() or "Unknown"

                msg += f"<b>Chat ID:</b> <code>{chat_id}</code>\n"
                msg += f"<b>User:</b> {user_display}\n"
                msg += f"<b>Command:</b> /{command}\n"
                msg += f"<b>Time:</b> {timestamp}\n"
                msg += f"<b>Attempts:</b> {count}\n"
                msg += "—\n"

            await update.message.reply_html(msg)

        except Exception as e:
            logger.error(f"Error in auth_log_command: {e}")
            await update.message.reply_html(f"❌ Error: {str(e)}")

    async def auth_users_command(self, update, context):
        """
        Show authorized users and their activity stats.
        Usage: /auth_users [limit]
        """
        try:
            limit = 50
            if context.args and len(context.args) > 0:
                limit = int(context.args[0])

            users = self.auth_logger.get_authorized_users(limit=limit)

            if not users:
                await update.message.reply_html("No authorized users found")
                return

            msg = f"<b>✅ Authorized Users</b>\n"
            msg += f"━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"

            for i, user in enumerate(users, 1):
                chat_id = user.get('chat_id', 'unknown')
                username = user.get('username', 'N/A')
                first_name = user.get('first_name', '')
                last_name = user.get('last_name', '')
                command_count = user.get('command_count', 0)
                last_access = user.get('last_access', 'never')
                first_access = user.get('first_access', 'unknown')

                user_display = f"@{username}" if username else f"{first_name} {last_name}".strip() or "Unknown"

                msg += f"{i}. {user_display}\n"
                msg += f"   <b>Chat ID:</b> <code>{chat_id}</code>\n"
                msg += f"   <b>Commands:</b> {command_count}\n"
                msg += f"   <b>Last Access:</b> {last_access}\n"
                msg += f"   <b>First Access:</b> {first_access}\n"
                msg += "   —\n"

            await update.message.reply_html(msg)

        except Exception as e:
            logger.error(f"Error in auth_users_command: {e}")
            await update.message.reply_html(f"❌ Error: {str(e)}")

    async def auth_daily_command(self, update, context):
        """
        Show daily authorization summary.
        Usage: /auth_daily [days]
        """
        try:
            days = 7
            if context.args and len(context.args) > 0:
                days = int(context.args[0])

            summary = self.auth_logger.get_daily_summary(days=days)

            if not summary:
                await update.message.reply_html(f"No data for the last {days} days")
                return

            msg = f"<b>📊 Authorization Summary ({days}d)</b>\n"
            msg += f"━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"

            for entry in summary:
                date = entry.get('date', 'unknown')
                status = entry.get('status', 'unknown')
                attempt_count = entry.get('attempt_count', 0)
                unique_users = entry.get('unique_users', 0)

                status_emoji = "✅" if status == 'authorized' else "❌"
                msg += f"{status_emoji} <b>{date}</b>\n"
                msg += f"   Status: {status.upper()}\n"
                msg += f"   Attempts: {attempt_count}\n"
                msg += f"   Unique Users: {unique_users}\n"
                msg += "   —\n"

            await update.message.reply_html(msg)

        except Exception as e:
            logger.error(f"Error in auth_daily_command: {e}")
            await update.message.reply_html(f"❌ Error: {str(e)}")

    async def suspicious_command(self, update, context):
        """
        Show suspicious access patterns (multiple unauthorized attempts).
        Usage: /suspicious [threshold] [hours]
        """
        try:
            threshold = 5
            hours = 24

            if context.args:
                if len(context.args) > 0:
                    threshold = int(context.args[0])
                if len(context.args) > 1:
                    hours = int(context.args[1])

            suspicious = self.auth_logger.get_suspicious_ips(
                attempt_threshold=threshold,
                hours=hours
            )

            if not suspicious:
                msg = f"✅ No suspicious patterns detected (threshold: {threshold} attempts in {hours}h)"
                await update.message.reply_html(msg)
                return

            msg = f"🚨 <b>Suspicious Access Patterns</b>\n"
            msg += f"━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            msg += f"(Threshold: {threshold}+ attempts in {hours}h)\n\n"

            for pattern in suspicious:
                ip = pattern.get('ip_address', 'unknown')
                attempts = pattern.get('attempt_count', 0)
                unique_ids = pattern.get('unique_chat_ids', 0)
                last_attempt = pattern.get('last_attempt', 'unknown')

                msg += f"<b>IP:</b> <code>{ip}</code>\n"
                msg += f"<b>Attempts:</b> {attempts}\n"
                msg += f"<b>Unique Chat IDs:</b> {unique_ids}\n"
                msg += f"<b>Last Attempt:</b> {last_attempt}\n"
                msg += "—\n"

            await update.message.reply_html(msg)

        except Exception as e:
            logger.error(f"Error in suspicious_command: {e}")
            await update.message.reply_html(f"❌ Error: {str(e)}")

    async def extract_chat_id_command(self, update, context):
        """
        Extract your Chat ID from the authorization logs.
        This shows the Chat ID of the user running the command.
        Usage: /extract_chat_id
        """
        try:
            chat_id = str(update.effective_chat.id)
            username = update.effective_user.username or "N/A"
            first_name = update.effective_user.first_name or ""
            last_name = update.effective_user.last_name or ""

            user_display = f"@{username}" if username != "N/A" else f"{first_name} {last_name}".strip()

            msg = f"<b>🔍 Your Chat ID</b>\n"
            msg += f"━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            msg += f"<b>Chat ID:</b>\n<code>{chat_id}</code>\n\n"
            msg += f"<b>User:</b> {user_display}\n\n"
            msg += f"<b>To whitelist:</b>\n"
            msg += f"Add to <code>.env</code>:\n"
            msg += f"<code>ALLOWED_CHAT_IDS={chat_id}</code>\n"

            await update.message.reply_html(msg)

        except Exception as e:
            logger.error(f"Error in extract_chat_id_command: {e}")
            await update.message.reply_html(f"❌ Error: {str(e)}")
