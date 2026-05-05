import json
import math
import os
from datetime import datetime
from data.db_client import DBClient


def _sanitize(obj):
    """
    Recursively replace float inf / -inf / nan with None so that
    json.dumps produces valid JSON that PostgreSQL can store.
    Python's json module serialises float('inf') as the bare token
    Infinity which is NOT valid JSON and crashes the DB insert.
    """
    if isinstance(obj, float):
        if math.isinf(obj) or math.isnan(obj):
            return None
        return obj
    if isinstance(obj, dict):
        return {k: _sanitize(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_sanitize(v) for v in obj]
    return obj


class EventLogger:
    def __init__(self, archival_path: str = r"D:\Trade_training_data"):
        try:
            self.db = DBClient()
        except Exception:
            # DB not available (e.g. running optimiser in sandbox) - degrades gracefully
            self.db = None
        self.archival_path = archival_path
        if not os.path.exists(self.archival_path):
            try:
                os.makedirs(self.archival_path, exist_ok=True)
            except Exception:
                pass  # Silent - archival path may not exist in sandbox/CI environments

    def log_event(self, event_type: str, status: str, message: str = "", meta_data: dict = None):
        """
        Logs a structured event to the bot_health table.
        event_type: HEARTBEAT | CONNECTION_LOST | ERROR | SYSTEM_START | SYSTEM_STOP
        status: SUCCESS | WARNING | CRITICAL | INFO
        """
        if self.db is None:
            return  # DB not connected - skip silently

        # Sanitize before serialisation — float('inf') / nan are invalid JSON
        # and cause PostgreSQL to reject the insert with "Token Infinity is invalid"
        clean_meta = _sanitize(meta_data) if meta_data else None

        query = """
            INSERT INTO bot_health (timestamp, event_type, status, message, meta_data)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (
            datetime.now(),
            event_type,
            status,
            message,
            json.dumps(clean_meta) if clean_meta is not None else None
        )

        try:
            self.db.execute_query(query, params)

            # Emit NOTIFY for real-time subscribers (FastAPI)
            notify_payload = json.dumps({
                "timestamp": str(datetime.now()),
                "event_type": event_type,
                "status": status,
                "message": message,
                "meta_data": clean_meta
            })
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
