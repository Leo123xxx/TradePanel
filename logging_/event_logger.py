import json
import os
from datetime import datetime
from data.db_client import DBClient

class EventLogger:
    def __init__(self, archival_path: str = r"D:\Trade_training_data"):
        self.db = DBClient()
        self.archival_path = archival_path
        if not os.path.exists(self.archival_path):
            try:
                os.makedirs(self.archival_path, exist_ok=True)
            except Exception as e:
                print(f"Warning: Could not create archival path {self.archival_path}: {e}")

    def log_event(self, event_type: str, status: str, message: str = "", meta_data: dict = None):
        """
        Logs a structured event to the bot_health table.
        event_type: HEARTBEAT | CONNECTION_LOST | ERROR | SYSTEM_START | SYSTEM_STOP
        status: SUCCESS | WARNING | CRITICAL | INFO
        """
        query = """
            INSERT INTO bot_health (timestamp, event_type, status, message, meta_data)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (
            datetime.now(),
            event_type,
            status,
            message,
            json.dumps(meta_data, default=str) if meta_data else None
        )
        
        try:
            self.db.execute_query(query, params)
            
            # Emit NOTIFY for real-time subscribers (FastAPI)
            notify_payload = json.dumps({
                "timestamp": str(datetime.now()),
                "event_type": event_type,
                "status": status,
                "message": message,
                "meta_data": meta_data
            }, default=str)
            self.db.execute_query(f"NOTIFY bot_events, '{notify_payload.replace(chr(39), chr(39)+chr(39))}'")
            
            # Archive for research if it's a backtest or strategic event
            if event_type in ["BACKTEST_START", "BACKTEST_END", "TRADE_SIGNAL", "STRATEGY_TWEAK"]:
                self._archive_for_research(event_type, notify_payload)
                
        except Exception as e:
            # Fallback to console if DB is down
            print(f"FAILED to log event to DB: {e}")
            print(f"Event: {event_type} | {status} | {message}")

    def _archive_for_research(self, event_type: str, payload: str):
        """Append strategic events to a local file for long-term research."""
        today = datetime.now().strftime("%Y-%m-%d")
        file_path = os.path.join(self.archival_path, f"research_logs_{today}.jsonl")
        try:
            with open(file_path, "a") as f:
                f.write(payload + "\n")
        except Exception as e:
            print(f"FAILED to archive event: {e}")

    def heartbeat(self, meta_data: dict = None):
        self.log_event("HEARTBEAT", "SUCCESS", "System heartbeat pulse.", meta_data)

if __name__ == "__main__":
    logger = EventLogger()
    logger.log_event("SYSTEM_START", "INFO", "Logger component test initiated.")
    logger.heartbeat({"test": True})
