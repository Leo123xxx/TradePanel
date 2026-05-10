"""
webapp/api/router_health.py
============================
Real connectivity health checks for the dashboard sidebar.

Endpoints:
    GET /api/health  — PostgreSQL status, MT5 bridge status, Event Bus status
"""

from fastapi import APIRouter
from datetime import datetime, timedelta
import logging
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from data.db_client import DBClient

router = APIRouter(prefix="/health", tags=["health"])
logger = logging.getLogger(__name__)


@router.get("")
async def get_health():
    """
    Returns real-time connectivity status for all system components.

    - postgresql: whether a live DB query succeeds
    - mt5_bridge:  based on the most recent HEARTBEAT row in bot_health
                   (ONLINE if heartbeat < 5 minutes ago, OFFLINE otherwise)
    - event_bus:   whether the FastAPI EventBus listener is running
                   (checked via the bus singleton's _running flag)
    """
    result = {
        "generated_at": datetime.now().isoformat(),
        "postgresql":   {"status": "OFFLINE", "detail": None},
        "mt5_bridge":   {"status": "OFFLINE", "detail": None},
        "event_bus":    {"status": "OFFLINE", "detail": None},
    }

    # ── 1. PostgreSQL ────────────────────────────────────────────────────────
    try:
        db = DBClient()
        rows = db.execute_query("SELECT 1")
        if rows:
            result["postgresql"]["status"] = "READY"
    except Exception as e:
        result["postgresql"]["detail"] = str(e)
        logger.warning(f"Health: PostgreSQL check failed: {e}")

    # ── 2. MT5 Bridge ────────────────────────────────────────────────────────
    try:
        db = DBClient()
        rows = db.execute_query("""
            SELECT timestamp, status, message
            FROM bot_health
            WHERE event_type = 'HEARTBEAT'
            ORDER BY timestamp DESC
            LIMIT 1
        """)
        if rows:
            last_hb_time = rows[0][0]
            hb_status    = rows[0][1]
            hb_msg       = rows[0][2]
            age_minutes  = (datetime.now() - last_hb_time).total_seconds() / 60

            if age_minutes <= 5:
                result["mt5_bridge"]["status"] = "ONLINE"
            else:
                result["mt5_bridge"]["status"] = "STALE"

            result["mt5_bridge"]["detail"] = (
                f"Last heartbeat {age_minutes:.0f}m ago — {hb_msg or hb_status}"
            )
        else:
            result["mt5_bridge"]["detail"] = "No heartbeat records found"
    except Exception as e:
        result["mt5_bridge"]["detail"] = str(e)
        logger.warning(f"Health: MT5 bridge check failed: {e}")

    # ── 3. Event Bus ─────────────────────────────────────────────────────────
    try:
        from webapp.bus import bus
        if bus._running:
            result["event_bus"]["status"] = "ACTIVE"
            result["event_bus"]["detail"] = f"{len(bus.subscribers)} subscriber(s)"
        else:
            result["event_bus"]["detail"] = "Bus not running"
    except Exception as e:
        result["event_bus"]["detail"] = str(e)
        logger.warning(f"Health: Event Bus check failed: {e}")

    return result


@router.get("/activity")
async def get_activity(limit: int = 10):
    """
    Returns the most recent system activity events from bot_health.
    Filters out HEARTBEAT events to focus on important reports.
    """
    try:
        db = DBClient()
        rows = db.execute_query("""
            SELECT timestamp, event_type, status, message, meta_data
            FROM bot_health
            WHERE event_type != 'HEARTBEAT'
            ORDER BY timestamp DESC
            LIMIT %s
        """, (limit,))
        
        events = []
        for r in rows:
            events.append({
                "timestamp": r[0].isoformat(),
                "type": r[1],
                "status": r[2],
                "message": r[3],
                "meta": r[4]
            })
        return events
    except Exception as e:
        logger.error(f"Activity feed error: {e}")
        return {"error": str(e)}
