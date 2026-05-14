"""
Backtest Runs Router
--------------------
Stores, retrieves, and restores backtest run history from the backtest_runs table.
Provides snapshot data for report generation and historical comparison.

Endpoints:
    GET  /api/backtests               - List all runs (paginated, filterable)
    POST /api/backtests               - Log a new backtest run
    GET  /api/backtests/{run_id}      - Get full detail for a single run
    GET  /api/backtests/{run_id}/restore  - Return the stored snapshot/metrics blob
    PUT  /api/backtests/{run_id}/notes    - Update notes on a run
    GET  /api/backtests/stats/summary     - Aggregate stats across all runs
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date
import logging
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from data.db_client import DBClient

import subprocess
import asyncio
from fastapi import APIRouter, HTTPException, Query, BackgroundTasks

router = APIRouter(prefix="/backtests", tags=["backtests"])
logger = logging.getLogger(__name__)

# Track active backtest process
active_backtest_process = {"running": False, "pid": None, "start_time": None}


# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------

class BacktestRunCreate(BaseModel):
    run_id: str = Field(..., description="Unique run identifier, e.g. BT-0042")
    strategy_name: str
    period_start: Optional[date] = None
    period_end: Optional[date] = None
    win_rate: Optional[float] = None
    sharpe_ratio: Optional[float] = None
    profit_factor: Optional[float] = None
    net_profit_zar: Optional[float] = None
    max_drawdown_pct: Optional[float] = None
    total_trades: Optional[int] = None
    winning_trades: Optional[int] = None
    losing_trades: Optional[int] = None
    roi_pct: Optional[float] = None
    risk_reward: Optional[float] = None
    recovery_factor: Optional[float] = None
    status: str = "PENDING"
    params_json: Optional[dict] = None
    metrics_json: Optional[dict] = None
    notes: Optional[str] = None
    wfo_fold: Optional[int] = None
    wfo_total_folds: Optional[int] = None


class NotesUpdate(BaseModel):
    notes: str


# ---------------------------------------------------------------------------
# Helper: determine pass/fail/review from go-live criteria
# ---------------------------------------------------------------------------

def _evaluate_status(win_rate, sharpe_ratio, max_drawdown_pct, profit_factor) -> str:
    """
    Go-live criteria (from strategies.yaml):
      PASS   : win_rate >= 0.90, sharpe >= 0.8, max_dd > -0.12, profit_factor >= 1.5
      FAIL   : win_rate < 0.65  OR sharpe < 0.5 OR max_dd <= -0.15
      REVIEW : anything in between
    """
    if win_rate is None or sharpe_ratio is None:
        return "PENDING"

    abs_dd = abs(max_drawdown_pct) if max_drawdown_pct else 0.0
    pf = profit_factor or 0.0

    # Hard fail
    if win_rate < 0.65 or sharpe_ratio < 0.5 or abs_dd >= 0.15 or pf < 1.0:
        return "FAIL"
    # Pass all criteria
    if win_rate >= 0.90 and sharpe_ratio >= 0.8 and abs_dd < 1.2 and pf >= 1.5:
        return "PASS"
    # Everything else
    return "REVIEW"


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@router.get("")
async def list_backtest_runs(
    strategy: Optional[str] = Query(None, description="Filter by strategy name"),
    status: Optional[str] = Query(None, description="Filter by status: PASS, FAIL, REVIEW"),
    win_rate_min: Optional[float] = Query(None, description="Minimum win rate (0.0 to 1.0)"),
    sharpe_min: Optional[float] = Query(None, description="Minimum Sharpe ratio"),
    pf_min: Optional[float] = Query(None, description="Minimum Profit Factor"),
    profit_min: Optional[float] = Query(None, description="Minimum Net Profit (ZAR)"),
    dd_max: Optional[float] = Query(None, description="Maximum Drawdown % (0.0 to 1.0)"),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0)
):
    """List backtest runs, newest first. Supports extensive filtering."""
    try:
        db = DBClient()

        conditions = []
        params = []

        if strategy:
            conditions.append("strategy_name ILIKE %s")
            params.append(f"%{strategy}%")
        if status:
            conditions.append("status = %s")
            params.append(status.upper())
        if win_rate_min is not None:
            conditions.append("win_rate >= %s")
            params.append(win_rate_min)
        if sharpe_min is not None:
            conditions.append("sharpe_ratio >= %s")
            params.append(sharpe_min)
        if pf_min is not None:
            conditions.append("profit_factor >= %s")
            params.append(pf_min)
        if profit_min is not None:
            conditions.append("net_profit_zar >= %s")
            params.append(profit_min)
        if dd_max is not None:
            # max_drawdown_pct is usually negative in some systems, but here we treat it as magnitude if positive
            # Let's assume the user sends a positive % magnitude like 0.12 for 12%
            conditions.append("ABS(max_drawdown_pct) <= %s")
            params.append(dd_max)

        where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
        
        # Build final params for the main query
        query_params = list(params)
        query_params += [limit, offset]

        rows = db.execute_query(
            f"""
            SELECT id, run_id, strategy_name, run_date, period_start, period_end,
                   win_rate, sharpe_ratio, profit_factor, net_profit_zar,
                   max_drawdown_pct, total_trades, winning_trades, losing_trades,
                   roi_pct, risk_reward, recovery_factor, status, notes,
                   wfo_fold, wfo_total_folds, created_at
            FROM backtest_runs
            {where}
            ORDER BY run_date DESC, created_at DESC
            LIMIT %s OFFSET %s
            """,
            tuple(query_params)
        ) or []

        # Count total for pagination
        count_row = db.execute_query(
            f"SELECT COUNT(*) FROM backtest_runs {where}",
            tuple(params) if params else None
        )
        total = count_row[0][0] if count_row else 0

        runs = []
        for r in rows:
            runs.append({
                "id": r[0],
                "run_id": r[1],
                "strategy_name": r[2],
                "run_date": r[3].isoformat() if r[3] else None,
                "period_start": r[4].isoformat() if r[4] else None,
                "period_end": r[5].isoformat() if r[5] else None,
                "win_rate": float(r[6]) if r[6] is not None else None,
                "sharpe_ratio": float(r[7]) if r[7] is not None else None,
                "profit_factor": float(r[8]) if r[8] is not None else None,
                "net_profit_zar": float(r[9]) if r[9] is not None else None,
                "max_drawdown_pct": float(r[10]) if r[10] is not None else None,
                "total_trades": r[11],
                "winning_trades": r[12],
                "losing_trades": r[13],
                "roi_pct": float(r[14]) if r[14] is not None else None,
                "risk_reward": float(r[15]) if r[15] is not None else None,
                "recovery_factor": float(r[16]) if r[16] is not None else None,
                "status": r[17],
                "notes": r[18],
                "wfo_fold": r[19],
                "wfo_total_folds": r[20],
                "created_at": r[21].isoformat() if r[21] else None,
            })

        return {
            "total": total,
            "limit": limit,
            "offset": offset,
            "runs": runs,
            "generated_at": datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"Error listing backtest runs: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("", status_code=201)
async def create_backtest_run(payload: BacktestRunCreate):
    """Log a new backtest run. Auto-evaluates PASS/FAIL/REVIEW if not supplied."""
    try:
        db = DBClient()

        # Auto-evaluate status if not explicitly set
        status = payload.status
        if status == "PENDING":
            status = _evaluate_status(
                payload.win_rate,
                payload.sharpe_ratio,
                payload.max_drawdown_pct,
                payload.profit_factor
            )

        db.execute_query(
            """
            INSERT INTO backtest_runs (
                run_id, strategy_name, period_start, period_end,
                win_rate, sharpe_ratio, profit_factor, net_profit_zar,
                max_drawdown_pct, total_trades, winning_trades, losing_trades,
                roi_pct, risk_reward, recovery_factor, status,
                params_json, metrics_json, notes, wfo_fold, wfo_total_folds
            ) VALUES (
                %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s, %s
            )
            ON CONFLICT (run_id) DO UPDATE SET
                win_rate = EXCLUDED.win_rate,
                sharpe_ratio = EXCLUDED.sharpe_ratio,
                profit_factor = EXCLUDED.profit_factor,
                net_profit_zar = EXCLUDED.net_profit_zar,
                max_drawdown_pct = EXCLUDED.max_drawdown_pct,
                total_trades = EXCLUDED.total_trades,
                status = EXCLUDED.status,
                metrics_json = EXCLUDED.metrics_json,
                updated_at = NOW()
            """,
            (
                payload.run_id, payload.strategy_name,
                payload.period_start, payload.period_end,
                payload.win_rate, payload.sharpe_ratio, payload.profit_factor, payload.net_profit_zar,
                payload.max_drawdown_pct, payload.total_trades, payload.winning_trades, payload.losing_trades,
                payload.roi_pct, payload.risk_reward, payload.recovery_factor, status,
                json.dumps(payload.params_json) if payload.params_json else None,
                json.dumps(payload.metrics_json) if payload.metrics_json else None,
                payload.notes, payload.wfo_fold, payload.wfo_total_folds
            )
        )

        return {"message": "Backtest run saved", "run_id": payload.run_id, "status": status}

    except Exception as e:
        logger.error(f"Error creating backtest run: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats/summary")
async def get_backtest_stats():
    """
    Aggregate stats across all stored backtest runs.
    Useful for the summary section of the Backtests tab.
    """
    try:
        db = DBClient()

        row = db.execute_query(
            """
            SELECT
                COUNT(*)                                        AS total_runs,
                COUNT(*) FILTER (WHERE status = 'PASS')        AS pass_count,
                COUNT(*) FILTER (WHERE status = 'FAIL')        AS fail_count,
                COUNT(*) FILTER (WHERE status = 'REVIEW')      AS review_count,
                AVG(win_rate) FILTER (WHERE status = 'PASS')   AS avg_win_rate_pass,
                AVG(sharpe_ratio) FILTER (WHERE status = 'PASS') AS avg_sharpe_pass,
                MAX(net_profit_zar)                             AS best_net_profit,
                MIN(max_drawdown_pct)                           AS worst_drawdown,
                COUNT(DISTINCT strategy_name)                   AS unique_strategies
            FROM backtest_runs
            """
        )

        if not row:
            return {"total_runs": 0}

        r = row[0]
        return {
            "total_runs": r[0],
            "pass_count": r[1],
            "fail_count": r[2],
            "review_count": r[3],
            "avg_win_rate_pass": float(r[4]) if r[4] else None,
            "avg_sharpe_pass": float(r[5]) if r[5] else None,
            "best_net_profit_zar": float(r[6]) if r[6] else None,
            "worst_drawdown_pct": float(r[7]) if r[7] else None,
            "unique_strategies": r[8],
            "generated_at": datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"Error getting backtest stats: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{run_id}")
async def get_backtest_run(run_id: str):
    """Get full detail for a single run including params_json and metrics_json."""
    try:
        db = DBClient()

        rows = db.execute_query(
            """
            SELECT id, run_id, strategy_name, run_date, period_start, period_end,
                   win_rate, sharpe_ratio, profit_factor, net_profit_zar,
                   max_drawdown_pct, total_trades, winning_trades, losing_trades,
                   roi_pct, risk_reward, recovery_factor, status, notes,
                   params_json, metrics_json, wfo_fold, wfo_total_folds, created_at
            FROM backtest_runs
            WHERE run_id = %s
            """,
            (run_id,)
        )

        if not rows:
            raise HTTPException(status_code=404, detail=f"Run '{run_id}' not found")

        r = rows[0]
        return {
            "id": r[0],
            "run_id": r[1],
            "strategy_name": r[2],
            "run_date": r[3].isoformat() if r[3] else None,
            "period_start": r[4].isoformat() if r[4] else None,
            "period_end": r[5].isoformat() if r[5] else None,
            "win_rate": float(r[6]) if r[6] is not None else None,
            "sharpe_ratio": float(r[7]) if r[7] is not None else None,
            "profit_factor": float(r[8]) if r[8] is not None else None,
            "net_profit_zar": float(r[9]) if r[9] is not None else None,
            "max_drawdown_pct": float(r[10]) if r[10] is not None else None,
            "total_trades": r[11],
            "winning_trades": r[12],
            "losing_trades": r[13],
            "roi_pct": float(r[14]) if r[14] is not None else None,
            "risk_reward": float(r[15]) if r[15] is not None else None,
            "recovery_factor": float(r[16]) if r[16] is not None else None,
            "status": r[17],
            "notes": r[18],
            "params_json": r[19],
            "metrics_json": r[20],
            "wfo_fold": r[21],
            "wfo_total_folds": r[22],
            "created_at": r[23].isoformat() if r[23] else None,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting backtest run {run_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{run_id}/restore")
async def restore_backtest_snapshot(run_id: str):
    """
    Returns the full stored snapshot for a run.
    Includes params_json (strategy parameters) and metrics_json (full metrics blob).
    Used to re-generate reports or restore the exact conditions of a past run.
    """
    try:
        db = DBClient()

        rows = db.execute_query(
            """
            SELECT run_id, strategy_name, run_date, period_start, period_end,
                   params_json, metrics_json, status, notes,
                   win_rate, sharpe_ratio, profit_factor, net_profit_zar,
                   max_drawdown_pct, total_trades
            FROM backtest_runs
            WHERE run_id = %s
            """,
            (run_id,)
        )

        if not rows:
            raise HTTPException(status_code=404, detail=f"Run '{run_id}' not found")

        r = rows[0]
        return {
            "run_id": r[0],
            "strategy_name": r[1],
            "run_date": r[2].isoformat() if r[2] else None,
            "period_start": r[3].isoformat() if r[3] else None,
            "period_end": r[4].isoformat() if r[4] else None,
            "params": r[5] or {},
            "metrics": r[6] or {},
            "summary": {
                "status": r[7],
                "notes": r[8],
                "win_rate": float(r[9]) if r[9] else None,
                "sharpe_ratio": float(r[10]) if r[10] else None,
                "profit_factor": float(r[11]) if r[11] else None,
                "net_profit_zar": float(r[12]) if r[12] else None,
                "max_drawdown_pct": float(r[13]) if r[13] else None,
                "total_trades": r[14],
            },
            "restored_at": datetime.now().isoformat()
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error restoring snapshot for {run_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{run_id}/notes")
async def update_run_notes(run_id: str, payload: NotesUpdate):
    """Update the notes field for a backtest run."""
    try:
        db = DBClient()

        db.execute_query(
            "UPDATE backtest_runs SET notes = %s WHERE run_id = %s",
            (payload.notes, run_id)
        )
        return {"message": "Notes updated", "run_id": run_id}

    except Exception as e:
        logger.error(f"Error updating notes for {run_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------------------------------
# Overnight report (file-based) — auto-sync from results/overnight/
# ---------------------------------------------------------------------------

import glob as _glob

@router.get("/overnight/latest")
async def get_overnight_latest():
    """
    Read the most recent overnight backtest report JSON from results/overnight/.
    Returns full results array plus summary counters.
    Called by the dashboard every 5 min for auto-sync.
    """
    results_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "results", "overnight"
    )
    pattern = os.path.join(results_dir, "*_backtest_report.json")
    files = sorted(_glob.glob(pattern))

    if not files:
        raise HTTPException(status_code=404, detail="No overnight report found. Run the backtest first.")

    latest = files[-1]
    try:
        with open(latest, encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read report: {e}")

    results = data.get("results", [])
    pass_count   = sum(1 for r in results if r.get("status") == "PASS")
    review_count = sum(1 for r in results if r.get("status") == "REVIEW")
    error_count  = len(results) - pass_count - review_count

    filename = os.path.basename(latest)
    report_date_str = filename[:8]  # e.g. "20260505"
    try:
        report_date = f"{report_date_str[:4]}-{report_date_str[4:6]}-{report_date_str[6:8]}"
    except Exception:
        report_date = report_date_str

    return {
        "filename": filename,
        "report_date": report_date,
        "generated": data.get("generated", report_date),
        "pass_count": pass_count,
        "review_count": review_count,
        "error_count": error_count,
        "total": len(results),
        "results": results,
    }