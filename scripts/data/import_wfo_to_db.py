"""
import_wfo_to_db.py
-------------------
Reads the walk_forward_results table (populated by the WFO engine) and upserts
each strategy+pair+timeframe combo into backtest_runs so the web UI Backtests
tab shows real data instead of seed rows.

Also removes the placeholder seed rows (BT-0001 to BT-0004) if they exist.

Usage:
    python scripts/import_wfo_to_db.py
    python scripts/import_wfo_to_db.py --dry-run   # print rows without writing
"""

import os
import sys
import json
import argparse
from datetime import datetime, date

from pathlib import Path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from dotenv import load_dotenv
load_dotenv()

import math

def _sanitize(obj):
    """Replace float inf/nan with None so json.dumps produces valid JSON."""
    if isinstance(obj, float):
        return None if (math.isinf(obj) or math.isnan(obj)) else obj
    if isinstance(obj, dict):
        return {k: _sanitize(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_sanitize(v) for v in obj]
    return obj



from data.db_client import DBClient


def _safe_num(v, clamp=9999.0):
    """Clamp a float to [-clamp, clamp], converting inf/nan to None."""
    if v is None:
        return None
    if isinstance(v, float) and (math.isinf(v) or math.isnan(v)):
        return None
    return max(-clamp, min(clamp, float(v)))

# ── Go-live criteria (mirrors strategies.yaml) ──────────────────────────────
MIN_PASS_WINDOWS_PCT = 1.0   # 100% windows must pass for PASS verdict
SHARPE_PASS          = 0.8
SHARPE_FAIL          = 0.0   # Sharpe <= 0 is a hard fail
PF_PASS              = 1.2
DD_LIMIT             = 0.12  # 12% max drawdown limit


def evaluate_status(pass_rate: float, avg_sharpe: float, avg_pf: float) -> str:
    if pass_rate >= MIN_PASS_WINDOWS_PCT and avg_sharpe >= SHARPE_PASS and avg_pf >= PF_PASS:
        return "PASS"
    if pass_rate == 0.0 or avg_sharpe <= SHARPE_FAIL:
        return "FAIL"
    return "REVIEW"


def main(dry_run: bool = False):
    db = DBClient()

    # ── 1. Fetch all WFO window results ─────────────────────────────────────
    print("\nFetching walk_forward_results from DB...")
    rows = db.execute_query(
        """
        SELECT
            wfr.strategy_id,
            s.name          AS strategy_name,
            wfr.symbol,
            wfr.timeframe,
            wfr.window_index,
            wfr.is_start,
            wfr.is_end,
            wfr.oos_start,
            wfr.oos_end,
            wfr.best_params,
            wfr.is_sharpe,
            wfr.oos_sharpe,
            wfr.oos_profit_factor,
            wfr.oos_trades
        FROM walk_forward_results wfr
        JOIN strategies s ON s.strategy_id = wfr.strategy_id
        ORDER BY s.name, wfr.symbol, wfr.timeframe, wfr.window_index
        """
    )

    if not rows:
        print("  No rows in walk_forward_results. Run a WFO first.")
        return

    print(f"  Found {len(rows)} window rows.\n")

    # ── 2. Group by strategy + symbol + timeframe ────────────────────────────
    combos: dict = {}
    for r in rows:
        (strategy_id, strategy_name, symbol, timeframe,
         window_index, is_start, is_end, oos_start, oos_end,
         best_params, is_sharpe, oos_sharpe, oos_pf, oos_trades) = r

        key = (strategy_name, symbol, timeframe)
        if key not in combos:
            combos[key] = {
                "strategy_id":   strategy_id,
                "strategy_name": strategy_name,
                "symbol":        symbol,
                "timeframe":     timeframe,
                "windows":       [],
                "period_start":  oos_start,
                "period_end":    oos_end,
            }
        combos[key]["windows"].append({
            "window_index":     window_index,
            "is_start":         is_start,
            "is_end":           is_end,
            "oos_start":        oos_start,
            "oos_end":          oos_end,
            "best_params":      best_params,
            "is_sharpe":        float(is_sharpe) if is_sharpe is not None else 0.0,
            "oos_sharpe":       float(oos_sharpe) if oos_sharpe is not None else 0.0,
            "oos_pf":           float(oos_pf) if oos_pf is not None else 0.0,
            "oos_trades":       int(oos_trades) if oos_trades else 0,
        })
        # Track widest date range
        if oos_end and (combos[key]["period_end"] is None or oos_end > combos[key]["period_end"]):
            combos[key]["period_end"] = oos_end
        if oos_start and (combos[key]["period_start"] is None or oos_start < combos[key]["period_start"]):
            combos[key]["period_start"] = oos_start

    # ── 3. Compute aggregate metrics per combo ───────────────────────────────
    records = []
    run_counter = 1

    for (strategy_name, symbol, timeframe), c in sorted(combos.items()):
        windows = c["windows"]
        n = len(windows)

        sharpes = [w["oos_sharpe"] for w in windows]
        pfs     = [w["oos_pf"]     for w in windows]

        avg_sharpe = sum(sharpes) / n
        avg_pf     = sum(pfs) / n
        pass_count = sum(1 for s in sharpes if s > 0)
        pass_rate  = pass_count / n

        status = evaluate_status(pass_rate, avg_sharpe, avg_pf)

        run_id = f"WFO-{run_counter:04d}"
        run_counter += 1

        # Params from last window's best IS params (most recent)
        last_params = windows[-1].get("best_params") or {}
        if isinstance(last_params, str):
            try:
                last_params = json.loads(last_params)
            except Exception:
                last_params = {}

        metrics_blob = {
            "windows": [
                {
                    "window": w["window_index"],
                    "oos_sharpe": w["oos_sharpe"],
                    "oos_pf":     w["oos_pf"],
                    "oos_trades": w["oos_trades"],
                    "pass":       w["oos_sharpe"] > 0,
                }
                for w in windows
            ],
            "pass_rate":   round(pass_rate, 4),
            "avg_sharpe":  _safe_num(round(avg_sharpe, 4)),
            "avg_pf":      _safe_num(round(avg_pf, 4)),
        }

        period_start = c["period_start"]
        period_end   = c["period_end"]
        if isinstance(period_start, datetime):
            period_start = period_start.date()
        if isinstance(period_end, datetime):
            period_end = period_end.date()

        notes = (
            f"WFO {n} windows | {pass_count}/{n} passed | "
            f"Avg OOS Sharpe {avg_sharpe:.2f} | Avg PF {avg_pf:.2f} | "
            f"Run: {datetime.now().strftime('%Y-%m-%d')}"
        )

        records.append({
            "run_id":         run_id,
            "strategy_name":  f"{strategy_name} ({symbol} {timeframe})",
            "period_start":   period_start,
            "period_end":     period_end,
            "win_rate":       None,           # WFO doesn't compute win_rate per window
            "sharpe_ratio":   _safe_num(round(avg_sharpe, 4)),
            "profit_factor":  _safe_num(round(avg_pf, 4)),
            "net_profit_zar": None,           # No ZAR P&L from WFO
            "max_drawdown_pct": None,
            "total_trades":   sum(w["oos_trades"] for w in windows),
            "status":         status,
            "params_json":    last_params,
            "metrics_json":   metrics_blob,
            "notes":          notes,
            "wfo_fold":       n,
            "wfo_total_folds":n,
        })

        verdict_icon = "✅" if status == "PASS" else ("⚠️" if status == "REVIEW" else "❌")
        print(f"  {verdict_icon}  {run_id}  {strategy_name:<30} {symbol} {timeframe:<4}  "
              f"Pass {pass_count}/{n}  AvgSharpe {avg_sharpe:+.2f}  -> {status}")

    # ── 4. Remove placeholder seed rows ─────────────────────────────────────
    if not dry_run:
        seed_ids = ["BT-0001", "BT-0002", "BT-0003", "BT-0004"]
        db.execute_query(
            "DELETE FROM backtest_runs WHERE run_id = ANY(%s)",
            (seed_ids,)
        )
        print(f"\n  Removed placeholder seed rows: {seed_ids}")

    # ── 5. Upsert records into backtest_runs ─────────────────────────────────
    inserted = 0
    for rec in records:
        if dry_run:
            print(f"\n  [DRY RUN] Would upsert: {rec['run_id']} — {rec['strategy_name']} ({rec['status']})")
            continue

        db.execute_query(
            """
            INSERT INTO backtest_runs (
                run_id, strategy_name, period_start, period_end,
                win_rate, sharpe_ratio, profit_factor, net_profit_zar,
                max_drawdown_pct, total_trades, status,
                params_json, metrics_json, notes, wfo_fold, wfo_total_folds
            ) VALUES (
                %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s,
                %s, %s, %s, %s, %s
            )
            ON CONFLICT (run_id) DO UPDATE SET
                sharpe_ratio    = EXCLUDED.sharpe_ratio,
                profit_factor   = EXCLUDED.profit_factor,
                total_trades    = EXCLUDED.total_trades,
                status          = EXCLUDED.status,
                metrics_json    = EXCLUDED.metrics_json,
                notes           = EXCLUDED.notes,
                updated_at      = NOW()
            """,
            (
                rec["run_id"], rec["strategy_name"],
                rec["period_start"], rec["period_end"],
                rec["win_rate"], rec["sharpe_ratio"], rec["profit_factor"],
                rec["net_profit_zar"], rec["max_drawdown_pct"], rec["total_trades"],
                rec["status"],
                json.dumps(_sanitize(rec["params_json"])),
                json.dumps(_sanitize(rec["metrics_json"])),
                rec["notes"],
                rec["wfo_fold"], rec["wfo_total_folds"],
            )
        )
        inserted += 1

    if not dry_run:
        print(f"\n  ✓ Upserted {inserted} WFO runs into backtest_runs.")
        # Verify counts
        counts = db.execute_query(
            "SELECT status, COUNT(*) FROM backtest_runs GROUP BY status ORDER BY status"
        )
        print("\n  backtest_runs status breakdown:")
        for row in (counts or []):
            print(f"    {row[0]:<8} {row[1]}")
    else:
        print(f"\n  [DRY RUN] Would upsert {len(records)} rows.")

    print("\nDone.\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Import WFO results into backtest_runs")
    parser.add_argument("--dry-run", action="store_true", help="Print what would be inserted without writing")
    args = parser.parse_args()
    main(dry_run=args.dry_run)
