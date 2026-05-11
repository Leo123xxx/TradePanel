"""
Paper Trades Router
-------------------
Exposes paper trading data (signals + trades) from the DB for the dashboard.
The paper engine writes to 'trades' (mode='PAPER') and 'signals' tables.

Endpoints:
    GET /api/papertrades/summary  - Aggregate KPIs for the lookback window
    GET /api/papertrades/trades   - Recent paper trades (open + closed)
    GET /api/papertrades/signals  - Recent signals detected by the paper engine
"""

from fastapi import APIRouter, Query
from datetime import datetime, timedelta
import logging
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from data.db_client import DBClient

router = APIRouter(prefix="/papertrades", tags=["papertrades"])
logger = logging.getLogger(__name__)
db = DBClient()


# ---------------------------------------------------------------------------
# Summary KPIs
# ---------------------------------------------------------------------------

@router.get("/summary")
async def get_paper_summary(lookback_days: int = Query(7, ge=1, le=90)):
    """
    Aggregate stats for paper trades in the lookback window.
    Returns: total_trades, wins, losses, win_rate, net_pnl, open_positions,
             signals_today, last_trade_at.
    """
    try:
        since = (datetime.now() - timedelta(days=lookback_days)).isoformat()

        summary_rows = db.execute_query(
            """
            SELECT
                COUNT(*)                                          AS total_trades,
                COUNT(*) FILTER (WHERE net_pnl > 0)              AS wins,
                COUNT(*) FILTER (WHERE net_pnl < 0)              AS losses,
                COALESCE(SUM(net_pnl), 0)                        AS net_pnl,
                COUNT(*) FILTER (WHERE status = 'OPENED')        AS open_positions,
                MAX(COALESCE(close_time, open_time))             AS last_trade_at
            FROM trades
            WHERE mode = 'PAPER'
              AND open_time >= %s::timestamp
            """,
            (since,)
        )

        signals_today_rows = db.execute_query(
            """
            SELECT COUNT(*) FROM signals
            WHERE timestamp >= NOW() - INTERVAL '24 hours'
            """
        )

        row = summary_rows[0] if summary_rows else (0, 0, 0, 0, 0, None)
        total  = int(row[0] or 0)
        wins   = int(row[1] or 0)
        losses = int(row[2] or 0)
        net    = float(row[3] or 0)
        open_p = int(row[4] or 0)
        last_t = row[5].isoformat() if row[5] else None

        sigs_today = int((signals_today_rows[0][0] if signals_today_rows else 0) or 0)

        closed = total - open_p
        win_rate = round((wins / closed * 100) if closed > 0 else 0, 1)

        return {
            "lookback_days": lookback_days,
            "generated_at": datetime.now().isoformat(),
            "total_trades": total,
            "wins": wins,
            "losses": losses,
            "win_rate": win_rate,
            "net_pnl_zar": round(net, 2),
            "open_positions": open_p,
            "signals_today": sigs_today,
            "last_trade_at": last_t,
        }
    except Exception as e:
        logger.error(f"paper summary error: {e}", exc_info=True)
        return {
            "lookback_days": lookback_days,
            "generated_at": datetime.now().isoformat(),
            "total_trades": 0, "wins": 0, "losses": 0,
            "win_rate": 0, "net_pnl_zar": 0,
            "open_positions": 0, "signals_today": 0, "last_trade_at": None,
            "error": str(e),
        }


# ---------------------------------------------------------------------------
# Paper Trades
# ---------------------------------------------------------------------------

@router.get("/trades")
async def get_paper_trades(
    lookback_days: int = Query(7, ge=1, le=90),
    limit: int = Query(50, ge=1, le=200),
    status: str = Query("", description="OPENED | CLOSED | (empty = all)")
):
    """
    Recent paper trades.  Joins strategies table for strategy_name.
    Returns open trades first, then most recent closed trades.
    """
    try:
        since = (datetime.now() - timedelta(days=lookback_days)).isoformat()
        status_filter = ""
        params = [since]
        if status in ("OPENED", "CLOSED"):
            status_filter = "AND t.status = %s"
            params.append(status)
        params.append(limit)

        rows = db.execute_query(
            f"""
            SELECT
                t.trade_id, s.name AS strategy_name,
                t.pair, t.direction, t.lot_size,
                t.entry_price, t.exit_price,
                t.open_time, t.close_time,
                t.net_pnl AS profit, t.status, t.mt5_ticket
            FROM trades t
            LEFT JOIN strategies s ON t.strategy_id = s.strategy_id
            WHERE t.mode = 'PAPER'
              AND t.open_time >= %s::timestamp
              {status_filter}
            ORDER BY
                CASE WHEN t.status = 'OPENED' THEN 0 ELSE 1 END,
                COALESCE(t.close_time, t.open_time) DESC
            LIMIT %s
            """,
            params
        )

        trades = []
        for r in (rows or []):
            trades.append({
                "trade_id":      r[0],
                "strategy_name": r[1] or "unknown",
                "pair":          r[2],
                "direction":     r[3],
                "lot_size":      float(r[4] or 0),
                "entry_price":   float(r[5] or 0),
                "exit_price":    float(r[6]) if r[6] is not None else None,
                "open_time":     r[7].isoformat() if r[7] else None,
                "close_time":    r[8].isoformat() if r[8] else None,
                "profit":        float(r[9]) if r[9] is not None else None,
                "status":        r[10],
                "mt5_ticket":    r[11],
            })

        return {"lookback_days": lookback_days, "total": len(trades), "trades": trades}

    except Exception as e:
        logger.error(f"paper trades error: {e}", exc_info=True)
        return {"lookback_days": lookback_days, "total": 0, "trades": [], "error": str(e)}


# ---------------------------------------------------------------------------
# Signals
# ---------------------------------------------------------------------------

@router.get("/signals")
async def get_paper_signals(
    lookback_hours: int = Query(24, ge=1, le=168),
    limit: int = Query(100, ge=1, le=500)
):
    """
    Signals recently detected by the paper engine.
    Joins strategies for strategy_name.
    """
    try:
        since = (datetime.now() - timedelta(hours=lookback_hours)).isoformat()

        rows = db.execute_query(
            """
            SELECT
                sig.signal_id, s.name AS strategy_name,
                sig.pair, sig.direction, sig.timeframe,
                sig.timestamp, sig.validity_window, sig.indicator_values,
                (sig.triggered_trade_id IS NOT NULL) AS signal_taken,
                ap.account_id, ap.account_name, ap.account_type,
                t.status AS trade_status,
                COALESCE(t.net_pnl, 0.0) AS trade_pnl
            FROM signals sig
            LEFT JOIN strategies s ON sig.strategy_id = s.strategy_id
            LEFT JOIN trades t ON sig.triggered_trade_id = t.trade_id
            LEFT JOIN account_profiles ap ON t.account_id = ap.account_id
            WHERE sig.timestamp >= %s::timestamp
            ORDER BY sig.timestamp DESC
            LIMIT %s
            """,
            (since, limit)
        )

        signals = []
        for r in (rows or []):
            import json as _json
            ind_vals = r[7]
            if isinstance(ind_vals, str):
                try:
                    ind_vals = _json.loads(ind_vals)
                except Exception:
                    ind_vals = {}
            signals.append({
                "signal_id":       r[0],
                "strategy_name":   r[1] or "unknown",
                "pair":            r[2],
                "direction":       r[3],
                "timeframe":       r[4],
                "timestamp":       r[5].isoformat() if r[5] else None,
                "validity_window": r[6],
                "price":           float(ind_vals.get("price", 0)) if ind_vals else 0,
                "signal_taken":    bool(r[8]),
                "account_id":      r[9],
                "account_name":    r[10] or "—",
                "account_type":    r[11],
                "trade_status":    r[12],
                "trade_pnl":       float(r[13]) if r[13] is not None else 0.0,
            })

        return {
            "lookback_hours": lookback_hours,
            "total": len(signals),
            "signals": signals,
        }

    except Exception as e:
        logger.error(f"paper signals error: {e}", exc_info=True)
        return {"lookback_hours": lookback_hours, "total": 0, "signals": [], "error": str(e)}
