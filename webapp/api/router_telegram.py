"""
webapp/api/router_telegram.py
==============================
Telegram bot status endpoint for the TradePanel dashboard.

GET /api/telegram/status
  Returns:
    - configured: bool  (token + chat_id both set in .env)
    - token_set: bool
    - chat_id_set: bool
    - last_seen: ISO timestamp of last log entry (or null)
    - last_seen_seconds_ago: int (or null)
    - status: "RUNNING" | "IDLE" | "OFFLINE" | "NOT_CONFIGURED"
    - log_path: str
"""

import os
import re
from datetime import datetime, timezone
from pathlib import Path
from fastapi import APIRouter
from dotenv import load_dotenv

router = APIRouter()

PROJECT_ROOT = Path(__file__).parent.parent.parent
LOG_PATH = PROJECT_ROOT / "logs" / "telegram_bot.log"
ENV_PATH = PROJECT_ROOT / ".env"

# Bot is considered RUNNING if last log entry is within this many seconds
RUNNING_THRESHOLD_SEC = 30
IDLE_THRESHOLD_SEC = 300  # 5 min - polling but maybe quiet


def _parse_last_log_timestamp(log_path: Path):
    """Read the last line of the log and return a datetime (UTC-naive) or None."""
    if not log_path.exists():
        return None
    try:
        # Read last ~4KB to find the last timestamp quickly
        with open(log_path, "r", encoding="utf-8", errors="replace") as f:
            f.seek(0, 2)
            size = f.tell()
            f.seek(max(0, size - 4096))
            tail = f.read()
        # Timestamps look like: 2026-04-24 10:05:21,412
        matches = re.findall(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", tail)
        if not matches:
            return None
        last_ts = matches[-1]
        return datetime.strptime(last_ts, "%Y-%m-%d %H:%M:%S")
    except Exception:
        return None


@router.get("/telegram/status")
def get_telegram_status():
    load_dotenv(ENV_PATH, override=False)
    token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.getenv("TELEGRAM_CHAT_ID", "").strip()

    token_set = bool(token)
    chat_id_set = bool(chat_id)
    configured = token_set and chat_id_set

    last_dt = _parse_last_log_timestamp(LOG_PATH)
    now = datetime.now()

    last_seen_iso = None
    last_seen_seconds_ago = None
    status = "NOT_CONFIGURED"

    if last_dt:
        delta = (now - last_dt).total_seconds()
        last_seen_seconds_ago = int(delta)
        last_seen_iso = last_dt.isoformat()

        if not configured:
            status = "NOT_CONFIGURED"
        elif delta <= RUNNING_THRESHOLD_SEC:
            status = "RUNNING"
        elif delta <= IDLE_THRESHOLD_SEC:
            status = "IDLE"
        else:
            status = "OFFLINE"
    elif configured:
        status = "OFFLINE"

    return {
        "configured": configured,
        "token_set": token_set,
        "chat_id_set": chat_id_set,
        "status": status,
        "last_seen": last_seen_iso,
        "last_seen_seconds_ago": last_seen_seconds_ago,
        "log_path": str(LOG_PATH),
    }
