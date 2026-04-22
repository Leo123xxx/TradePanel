import asyncio
from logging_.event_logger import EventLogger
from notifications.telegram_bot import TelegramBot
from mt5_bridge.connector import MT5Connector
import MetaTrader5 as mt5

class HealthMonitor:
    def __init__(self):
        self.logger = EventLogger()
        self.notifier = TelegramBot()
        self.mt5_conn = MT5Connector()

    async def check_heartbeat(self):
        """Sends a heartbeat to the DB."""
        print("Sending heartbeat...")
        self.logger.heartbeat()

    def check_mt5_connection(self):
        """Checks if MT5 is still connected and authorized. Returns alert message if failed."""
        from notifications import templates
        from datetime import datetime
        last_hb = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if not mt5.terminal_info():
            self.logger.log_event("CONNECTION_LOST", "CRITICAL", "MT5 Terminal is not running.")
            return templates.HEARTBEAT_LOST.format(last_heartbeat=last_hb)
        
        if not mt5.account_info():
            self.logger.log_event("CONNECTION_LOST", "WARNING", "MT5 terminal open but not logged in.")
            return f"⚠️ <b>WARNING:</b> MT5 is not logged into an account.\n🕒 <b>Time:</b> {last_hb}"
        
        return None
