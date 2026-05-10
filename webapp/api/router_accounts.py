"""
webapp/api/router_accounts.py
Account Profiles router -- trade history, equity curve, KPIs, per-symbol breakdown.
Supports multiple account types (DEMO / LIVE / PAPER) via account_id or account_type.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional
import sys, os, math, logging

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from data.db_client import DBClient

router = APIRouter(prefix="/accounts", tags=["accounts"])
logger = logging.getLogger(__name__)


@router.post("/sync")
async def sync_account():
    """Manually trigger MT5 account history sync."""
    import subprocess
    script = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "scripts", "sync_mt5_account.py")
    try:
        # We run it via subprocess to ensure it uses the host's MT5 connection if needed
        # or we could import it. Since it's a script, subprocess is safer for environment isolation.
        result = subprocess.run([sys.executable, script], capture_output=True, text=True)
        if result.returncode == 0:
            return {"status": "success", "message": "Account sync completed", "output": result.stdout}
        else:
            return {"status": "error", "message": "Account sync failed", "error": result.stderr}
    except Exception as e:
        logger.error(f"sync_account error: {e}")
        return {"status": "error", "message": str(e)}


def _safe(v, fallback=None):
    if v is None:
        return fallback
    if isinstance(v, float) and (math.isinf(v) or math.isnan(v)):
        return fallback
    return v


def _pct(num, den):
    return round(num / den * 100, 2) if den else 0.0


def _sharpe(pnl_list):
    import statistics
    if len(pnl_list) < 2:
        return 0.0
    mu = sum(pnl_list) / len(pnl_list)
    try:
        sd = statistics.stdev(pnl_list)
    except Exception:
        return 0.0
    if sd == 0:
        return 0.0
    return round(min(max((mu / sd) * (252 ** 0.5), -50), 50), 4)


# ---------------------------------------------------------------------------
# List all account profiles
# ---------------------------------------------------------------------------
@router.get("")
async def list_accounts():
    """Return all account profiles with row counts from the trades table."""
    db = DBClient()
    try:
        rows = db.execute_query("""
            SELECT a.account_id, a.account_name, a.account_type,
                   a.broker, a.currency, a.initial_balance,
                   a.is_active, a.notes, a.created_at,
                   COUNT(t.trade_id) AS trade_count
            FROM account_profiles a
            LEFT JOIN trades t ON t.account_id = a.account_id
            GROUP BY a.account_id
            ORDER BY a.account_id
        """) or []

        # Also count trades whose mode matches account_type (legacy rows with NULL account_id)
        mode_counts = db.execute_query("""
            SELECT UPPER(mode), COUNT(*)
            FROM trades
            WHERE account_id IS NULL AND mode IS NOT NULL
            GROUP BY UPPER(mode)
        """) or []
        mode_map = {r[0]: int(r[1]) for r in mode_counts}

        result = []
        for r in rows:
            acct_type = r[2]
            legacy = mode_map.get(acct_type, 0)
            result.append({
                "account_id":      r[0],
                "account_name":    r[1],
                "account_type":    acct_type,
                "broker":          r[3],
                "currency":        r[4],
                "initial_balance": float(r[5]) if r[5] is not None else 10000.0,
                "is_active":       r[6],
                "notes":           r[7],
                "created_at":      r[8].isoformat() if r[8] else None,
                "trade_count":     int(r[9]) + legacy,
            })
        return result
    except Exception as e:
        logger.error(f"list_accounts error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------------------------------
# KPIs for one account
# ---------------------------------------------------------------------------
@router.get("/{account_id}/kpis")
async def account_kpis(
    account_id: int,
    lookback_days: int = Query(90, ge=1, le=1825),
):
    db = DBClient()
    try:
        # Fetch account metadata
        meta = db.execute_query(
            "SELECT account_type, initial_balance, currency FROM account_profiles WHERE account_id = %s",
            (account_id,)
        )
        if not meta:
            raise HTTPException(status_code=404, detail="Account not found")
        acct_type, initial_balance, currency = meta[0]
        ib = float(initial_balance or 10000)

        rows = db.execute_query("""
            SELECT t.trade_id, t.pair, t.entry_price, t.exit_price,
                   t.created_at, t.mode,
                   COALESCE(t.net_pnl, t.exit_price - t.entry_price) AS pnl,
                   t.strategy_id
            FROM trades t
            WHERE (t.account_id = %s OR (t.account_id IS NULL AND UPPER(t.mode) = %s))
              AND t.created_at >= NOW() - INTERVAL %s
              AND t.exit_price IS NOT NULL
            ORDER BY t.created_at
        """, (account_id, acct_type, f"{lookback_days} days")) or []

        if not rows:
            return {"account_id": account_id, "currency": currency, "total_trades": 0}

        pnls = [float(r[6] or 0) for r in rows]
        wins = [p for p in pnls if p > 0]
        losses = [p for p in pnls if p <= 0]
        n = len(pnls)
        total_pnl = sum(pnls)
        equity = ib + total_pnl

        running = ib
        peak = ib
        max_dd = 0.0
        for p in pnls:
            running += p
            if running > peak:
                peak = running
            dd = (peak - running) / peak * 100
            if dd > max_dd:
                max_dd = dd

        gross_p = sum(wins)
        gross_l = abs(sum(losses))
        pf = _safe(gross_p / gross_l, 0.0) if gross_l > 0 else (999.0 if gross_p > 0 else 0.0)

        # ── MANUAL VS BOT BREAKDOWN ──
        manual_pnls = [float(r[6] or 0) for r in rows if r[7] is None]
        bot_pnls    = [float(r[6] or 0) for r in rows if r[7] is not None]

        manual_wins = [p for p in manual_pnls if p > 0]
        bot_wins    = [p for p in bot_pnls if p > 0]

        return {
            "account_id":       account_id,
            "currency":         currency,
            "lookback_days":    lookback_days,
            "total_trades":     n,
            "winning_trades":   len(wins),
            "losing_trades":    len(losses),
            "win_rate":         round(_pct(len(wins), n), 2),
            "total_pnl":        round(total_pnl, 2),
            "gross_profit":     round(gross_p, 2),
            "gross_loss":       round(gross_l, 2),
            "profit_factor":    round(min(pf, 999.0), 4),
            "sharpe_ratio":     _sharpe(pnls),
            "max_drawdown_pct": round(max_dd, 2),
            "final_equity":     round(equity, 2),
            "roi_pct":          round(_pct(total_pnl, ib), 2),
            "avg_win":          round(sum(wins) / len(wins), 4) if wins else 0.0,
            "avg_loss":         round(sum(losses) / len(losses), 4) if losses else 0.0,
            "manual": {
                "count":    len(manual_pnls),
                "pnl":      round(sum(manual_pnls), 2),
                "win_rate": round(_pct(len(manual_wins), len(manual_pnls)), 2)
            },
            "bot": {
                "count":    len(bot_pnls),
                "pnl":      round(sum(bot_pnls), 2),
                "win_rate": round(_pct(len(bot_wins), len(bot_pnls)), 2)
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"account_kpis error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------------------------------
# Equity curve
# ---------------------------------------------------------------------------
@router.get("/{account_id}/equity")
async def account_equity(
    account_id: int,
    lookback_days: int = Query(90, ge=1, le=1825),
):
    db = DBClient()
    try:
        meta = db.execute_query(
            "SELECT account_type, initial_balance FROM account_profiles WHERE account_id = %s",
            (account_id,)
        )
        if not meta:
            raise HTTPException(status_code=404, detail="Account not found")
        acct_type, initial_balance = meta[0]
        ib = float(initial_balance or 10000)

        rows = db.execute_query("""
            SELECT t.created_at,
                   COALESCE(t.net_pnl, t.exit_price - t.entry_price) AS pnl
            FROM trades t
            WHERE (t.account_id = %s OR (t.account_id IS NULL AND UPPER(t.mode) = %s))
              AND t.created_at >= NOW() - INTERVAL %s
              AND t.exit_price IS NOT NULL
            ORDER BY t.created_at
        """, (account_id, acct_type, f"{lookback_days} days")) or []

        running = ib
        points = [{"date": None, "equity": running, "pnl": 0.0}]
        for r in rows:
            pnl = float(r[1] or 0)
            running += pnl
            points.append({
                "date":   r[0].strftime("%Y-%m-%d") if r[0] else None,
                "equity": round(running, 2),
                "pnl":    round(pnl, 4),
            })
        # Remove the synthetic first point if we have real data
        if len(points) > 1:
            points = points[1:]

        return {"account_id": account_id, "initial_balance": ib, "equity_curve": points}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"account_equity error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------------------------------
# Trade history (paginated)
# ---------------------------------------------------------------------------
@router.get("/{account_id}/trades")
async def account_trades(
    account_id: int,
    lookback_days: int = Query(90, ge=1, le=1825),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    symbol: Optional[str] = None,
):
    db = DBClient()
    try:
        meta = db.execute_query(
            "SELECT account_type FROM account_profiles WHERE account_id = %s",
            (account_id,)
        )
        if not meta:
            raise HTTPException(status_code=404, detail="Account not found")
        acct_type = meta[0][0]

        symbol_clause = "AND t.pair = %s" if symbol else ""
        params = [account_id, acct_type, f"{lookback_days} days"]
        if symbol:
            params.append(symbol)

        total_row = db.execute_query(f"""
            SELECT COUNT(*) FROM trades t
            WHERE (t.account_id = %s OR (t.account_id IS NULL AND UPPER(t.mode) = %s))
              AND t.created_at >= NOW() - INTERVAL %s
              AND t.exit_price IS NOT NULL
              {symbol_clause}
        """, params)
        total = int(total_row[0][0]) if total_row else 0

        offset = (page - 1) * page_size
        rows = db.execute_query(f"""
            SELECT t.trade_id, t.pair, t.mode,
                   t.entry_price, t.exit_price,
                   t.created_at,
                   s.name AS strategy_name,
                   t.direction, t.status,
                   COALESCE(t.net_pnl, t.exit_price - t.entry_price) AS pnl
            FROM trades t
            LEFT JOIN strategies s ON t.strategy_id = s.strategy_id
            WHERE (t.account_id = %s OR (t.account_id IS NULL AND UPPER(t.mode) = %s))
              AND t.created_at >= NOW() - INTERVAL %s
              AND t.exit_price IS NOT NULL
              {symbol_clause}
            ORDER BY t.created_at DESC
            LIMIT %s OFFSET %s
        """, params + [page_size, offset]) or []

        trades = []
        for r in rows:
            entry = float(r[3] or 0)
            exit_ = float(r[4] or 0)
            pnl   = float(r[9] or 0)
            trades.append({
                "trade_id":      r[0],
                "pair":          r[1],
                "mode":          r[2],
                "entry_price":   round(entry, 5),
                "exit_price":    round(exit_, 5),
                "pnl":           round(pnl, 4),
                "opened_at":     r[5].isoformat() if r[5] else None,
                "strategy_name": r[6] or "Manual",
                "direction":     r[7],
                "status":        r[8],
            })

        return {
            "account_id":  account_id,
            "total":       total,
            "page":        page,
            "page_size":   page_size,
            "pages":       max(1, math.ceil(total / page_size)),
            "trades":      trades,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"account_trades error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------------------------------
# Per-symbol breakdown
# ---------------------------------------------------------------------------
@router.get("/{account_id}/by-symbol")
async def account_by_symbol(
    account_id: int,
    lookback_days: int = Query(90, ge=1, le=1825),
):
    db = DBClient()
    try:
        meta = db.execute_query(
            "SELECT account_type FROM account_profiles WHERE account_id = %s",
            (account_id,)
        )
        if not meta:
            raise HTTPException(status_code=404, detail="Account not found")
        acct_type = meta[0][0]

        rows = db.execute_query("""
            SELECT t.pair,
                   COUNT(*) AS trades,
                   SUM(COALESCE(t.net_pnl, t.exit_price - t.entry_price)) AS net_pnl,
                   SUM(CASE WHEN COALESCE(t.net_pnl, t.exit_price - t.entry_price) > 0 THEN 1 ELSE 0 END) AS wins
            FROM trades t
            WHERE (t.account_id = %s OR (t.account_id IS NULL AND UPPER(t.mode) = %s))
              AND t.created_at >= NOW() - INTERVAL %s
              AND t.exit_price IS NOT NULL
            GROUP BY t.pair
            ORDER BY net_pnl DESC
        """, (account_id, acct_type, f"{lookback_days} days")) or []

        symbols = []
        for r in rows:
            n = int(r[1])
            pnl = float(r[2] or 0)
            wins = int(r[3] or 0)
            symbols.append({
                "symbol":    r[0],
                "trades":    n,
                "net_pnl":   round(pnl, 4),
                "win_rate":  round(_pct(wins, n), 2),
            })

        return {"account_id": account_id, "by_symbol": symbols}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"account_by_symbol error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
