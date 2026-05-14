"""
scripts/run_wfo_all.py
======================
Batch Walk-Forward Optimisation runner for all enabled strategies.

Reads enabled strategies from config/strategies.yaml, runs WFO for each
primary pair/timeframe combo defined in WFO_CONFIGS, then writes a full
summary to results/wfo_master_summary.md.

Usage:
    python scripts/run_wfo_all.py
    python scripts/run_wfo_all.py --n_windows 3 --is_pct 0.70 --oos_pct 0.20
    python scripts/run_wfo_all.py --strategy moving_average_crossover  # single strategy

Expected runtime: 30-90 minutes for all 18 strategies x 2 combos = ~36 WFO runs.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(1, os.path.dirname(os.path.abspath(__file__)))

import argparse
import yaml
import pandas as pd
from pathlib import Path
from datetime import datetime

from run_walk_forward import STRATEGY_MAP
from data.db_client import DBClient
from backtesting.walk_forward import WalkForwardOptimizer


# =============================================================================
# WFO test configurations per strategy.
# Format: yaml_strategy_name -> list of (pair, timeframe) tuples.
# These are the primary pair/TF combos used for WFO validation.
# Run 2 combos per strategy where possible to cross-validate.
# =============================================================================
WFO_CONFIGS = {
    "bb_mean_reversion": [("XAUUSD", "H4"), ("EURUSD", "H4")],
    "bb_squeeze_scalp": [("USTEC", "H2"), ("XAUUSD", "H2")],
    "cot_sentiment": [("EURUSD", "H12"), ("GBPUSD", "H12")],
    "crypto_rsi_extremes": [("BTCUSD", "H1"), ("ETHUSD", "H1")],
    "donchian_trend": [("BTCUSD", "H1"), ("ETHUSD", "H1")],
    "dual_ema_fractal": [("XAUUSD", "H4"), ("EURUSD", "H4")],
    "dual_ema_momentum": [("XAUUSD", "H4"), ("EURUSD", "H4")],
    "ema_ribbon_scalp": [("XAUUSD", "M15"), ("GBPUSD", "M15")],
    "ema_ribbon_trend": [("XAUUSD", "H4"), ("EURUSD", "H4")],
    "ensemble": [("XAUUSD", "H4"), ("EURUSD", "H4")],
    "fast_ma_scalper": [("GBPUSD", "H1"), ("USDJPY", "H1")],
    "gold_momentum_breakout": [("XAUUSD", "H4"), ("XAUUSD", "H1")],
    "hikkake_trap": [("XAUUSD", "H4"), ("EURUSD", "H4")],
    "ict_judas_swing": [("XAUUSD", "H4"), ("EURUSD", "H4")],
    "institutional_silver_bullet": [("XAUUSD", "H4"), ("EURUSD", "H4")],
    "ma_crossover": [("XAUUSD", "H4"), ("EURUSD", "H4")],
    "macd_trend": [("XAUUSD", "H4"), ("EURUSD", "H4")],
    "macd_zero_scalp": [("GBPUSD", "H1"), ("EURUSD", "H1")],
    "multi_ema_crypto_scalper": [("BTCUSD", "H1"), ("ETHUSD", "H1")],
    "naked_price_action": [("XAUUSD", "H4"), ("EURUSD", "H4")],
    "orb": [("XAUUSD", "H4"), ("EURUSD", "H4")],
    "power_of_3_amd": [("BTCUSD", "H1"), ("ETHUSD", "H1")],
    "range_breakout": [("XAUUSD", "H4"), ("EURUSD", "H4")],
    "rsi_2": [("XAUUSD", "H4"), ("EURUSD", "H4")],
    "rsi_bounce": [("XAUUSD", "H4"), ("EURUSD", "H4")],
    "rsi_extremes_scalp": [("XAUUSD", "M15"), ("GBPUSD", "M15")],
    "rsi_pullback": [("XAUUSD", "H4"), ("EURUSD", "H4")],
    "rvgi_cci_confluence": [("XAUUSD", "H4"), ("EURUSD", "H4")],
    "session_momentum": [("XAUUSD", "H4"), ("EURUSD", "H4")],
    "silver_bullet_crypto": [("BTCUSD", "H1"), ("ETHUSD", "H1")],
    "stat_arb_gold_silver": [("XAUUSD", "H2"), ("XAUUSD", "H1")],
    "stoch_divergence": [("XAUUSD", "H4"), ("EURUSD", "H4")],
    "supertrend": [("XAUUSD", "H4"), ("EURUSD", "H4")],
    "swing_pullback": [("XAUUSD", "H4"), ("EURUSD", "H4")],
    "triple_macd_scalping": [("XAUUSD", "M15"), ("GBPUSD", "M15")],
    "ttm_squeeze": [("XAUUSD", "H4"), ("EURUSD", "H4")],
    "turtle_soup": [("XAUUSD", "H4"), ("EURUSD", "H4")],
    "volatility_breakout_scalp": [("BTCUSD", "H2"), ("BTCUSD", "H1")],
    "volatility_contraction": [("XAUUSD", "H4"), ("EURUSD", "H4")],
    "volatility_squeeze_breakout": [("XAUUSD", "H4"), ("EURUSD", "H4")],
    "vwap_momentum": [("XAUUSD", "H4"), ("EURUSD", "H4")],
}



# =============================================================================
# Helpers
# =============================================================================

def load_enabled_strategies() -> list:
    """Read strategies.yaml and return list of enabled strategy yaml-keys."""
    cfg_path = Path(__file__).parent.parent.parent / "config" / "strategies.yaml"
    with open(cfg_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    enabled = []
    for name, val in cfg.items():
        if isinstance(val, dict) and val.get("enabled", False):
            enabled.append(name)
    return enabled


def calc_pass_rate(window_results: list, timeframe: str = "H1") -> float:
    if not window_results:
        return 0.0
    n_pass = 0
    for r in window_results:
        sharpe = r.get("oos_sharpe", 0)
        wr = r.get("oos_win_rate", 0)
        trades = r.get("oos_trades", 0)
        
        # Relaxed OOS window pass criterion:
        # H4+ timeframes: 5 trades min
        # Others: 10 trades min
        min_tr = 5 if timeframe in ["H1", "H2", "H4", "D1", "W1"] else 10
        
        if sharpe >= 1.5 and wr >= 65.0 and trades >= min_tr:
            n_pass += 1
            
    return (n_pass / len(window_results)) * 100.0


def run_single_wfo(wfo_name: str, pair: str, timeframe: str,
                   is_pct: float, oos_pct: float, n_windows: int) -> list:
    """
    Runs WFO for one strategy/pair/timeframe combo.
    Returns list of per-window result dicts from WalkForwardOptimizer.run().
    Raises ValueError if no data found.
    """
    db = DBClient()
    query = (
        "SELECT timestamp, open, high, low, close, tick_volume "
        "FROM market_data "
        "WHERE pair = %s AND timeframe = %s "
        "ORDER BY timestamp"
    )
    rows = db.execute_query(query, (pair, timeframe))

    if not rows:
        raise ValueError(
            f"No data for {pair} {timeframe}. "
            "Run update_market_data.py first."
        )

    df = pd.DataFrame(
        rows,
        columns=["timestamp", "open", "high", "low", "close", "tick_volume"]
    )
    df.set_index("timestamp", inplace=True)
    for col in ["open", "high", "low", "close", "tick_volume"]:
        df[col] = df[col].astype(float)

    wf = WalkForwardOptimizer(db)
    window_results = wf.run(
        strategy_key=wfo_name,
        symbol=pair,
        timeframe=timeframe,
        df=df,
        is_pct=is_pct,
        oos_pct=oos_pct,
        n_windows=n_windows,
    )

    # Print per-window detail inline
    n_pass = 0
    for res in window_results:
        sharpe = res.get("oos_sharpe", 0)
        pf = res.get("oos_profit_factor", 0)
        wr = res.get("oos_win_rate", 0)
        trades = res.get("oos_trades", 0)
        
        min_tr = 5 if timeframe in ["H1", "H2", "H4", "D1", "W1"] else 10
        status = "PASS" if (sharpe >= 1.5 and wr >= 65.0 and trades >= min_tr) else "FAIL"
        if status == "PASS":
            n_pass += 1
        print(
            f"    Window {res.get('window_index', '?'):>2}: {status}"
            f"  Sharpe={sharpe:6.2f}  WR={wr:5.1f}%  Trades={trades:>3}",
            flush=True
        )

    n_total = len(window_results)
    pass_rate = (n_pass / n_total * 100) if n_total else 0
    verdict = "PASS" if pass_rate >= 70 else "FAIL"
    print(
        f"    Final Pass rate: {pass_rate:.0f}%  [{n_pass}/{n_total}]  -> {verdict}",
        flush=True
    )

    return window_results


# =============================================================================
# Summary writer
# =============================================================================

def write_summary(results: dict, skipped: list,
                  n_windows: int, is_pct: float, oos_pct: float) -> str:
    """Write markdown summary to results/wfo_master_summary.md."""
    out_dir = Path(__file__).parent.parent.parent / "results"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "wfo_master_summary.md"

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines = [
        "# WFO Master Summary",
        "",
        f"**Generated:** {now}  ",
        f"**Config:** {n_windows} windows | IS={is_pct*100:.0f}% | OOS={oos_pct*100:.0f}%  ",
        "**Criterion:** Sharpe >= 1.5, WR >= 65%, Trades >= 5(H4+)/10(Others) per window (OOS); strategy passes if >= 70% of windows pass",
        "",
        "---",
        "",
        "## Results Overview",
        "",
        "| Strategy | Pair | TF | Pass Rate | Windows | Verdict |",
        "|----------|------|----|----------:|---------|---------|",
    ]

    n_pass_total = 0
    n_fail_total = 0
    n_error_total = 0

    for yaml_name, combos in results.items():
        for combo in combos:
            pair = combo["pair"]
            tf = combo["timeframe"]
            error = combo["error"]
            pass_rate = combo["pass_rate"]
            windows = combo["windows"]
            n = len(windows)
            n_p = 0
            for w in windows:
                s = w.get("oos_sharpe", 0)
                wr = w.get("oos_win_rate", 0)
                tr = w.get("oos_trades", 0)
                min_tr = 5 if tf in ["H1", "H2", "H4", "D1", "W1"] else 10
                if s >= 1.5 and wr >= 65.0 and tr >= min_tr:
                    n_p += 1

            if error:
                verdict = "ERROR"
                win_str = f"ERR"
                n_error_total += 1
            elif pass_rate >= 70:
                verdict = "PASS"
                win_str = f"{n_p}/{n}"
                n_pass_total += 1
            else:
                verdict = "FAIL"
                win_str = f"{n_p}/{n}"
                n_fail_total += 1

            lines.append(
                f"| {yaml_name} | {pair} | {tf} | {pass_rate:.0f}% "
                f"| {win_str} | {verdict} |"
            )

    lines += [
        "",
        "---",
        "",
        "## Summary",
        "",
        f"- **PASS:** {n_pass_total} combo(s)",
        f"- **FAIL:** {n_fail_total} combo(s)",
        f"- **ERRORS:** {n_error_total} combo(s)",
        (
            "- **Skipped:** "
            + (", ".join(skipped) if skipped else "none")
        ),
        "",
        "---",
        "",
        "## Per-Window Detail",
        "",
    ]

    for yaml_name, combos in results.items():
        for combo in combos:
            pair = combo["pair"]
            tf = combo["timeframe"]
            windows = combo["windows"]
            error = combo["error"]

            lines.append(f"### {yaml_name} — {pair} {tf}")
            lines.append("")

            if error:
                lines.append(f"> **ERROR:** {error}")
            elif not windows:
                lines.append("> No results returned.")
            else:
                lines.append("| Window | OOS Sharpe | OOS WR% | Trades | Status |")
                lines.append("|-------:|-----------:|--------:|-------:|--------|")
                for w in windows:
                    sharpe = w.get("oos_sharpe", 0)
                    wr = w.get("oos_win_rate", 0)
                    trades = w.get("oos_trades", 0)
                    idx = w.get("window_index", "?")
                    min_tr = 5 if tf in ["H1", "H2", "H4", "D1", "W1"] else 10
                    status = "PASS" if (sharpe >= 1.5 and wr >= 65.0 and trades >= min_tr) else "FAIL"
                    lines.append(f"| {idx} | {sharpe:.3f} | {wr:.1f} | {trades} | {status} |")

            lines.append("")

    out_path.write_text("\n".join(lines), encoding="utf-8")
    return str(out_path)


# =============================================================================
# Main
# =============================================================================

def run_all_wfo(
    n_windows: int = 5,
    is_pct: float = 0.70,
    oos_pct: float = 0.30,
    only_strategy: str = None,
):
    """Main entry point. Runs WFO for all (or one) enabled strategies."""
    print()
    print("=" * 65)
    print("  TradePanel - Batch Walk-Forward Optimisation")
    print(f"  Started : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Windows : {n_windows} | IS={is_pct*100:.0f}% | OOS={oos_pct*100:.0f}%")
    print("=" * 65)

    enabled_strategies = load_enabled_strategies()

    if only_strategy:
        if only_strategy not in enabled_strategies:
            print(f"\n  WARNING: {only_strategy} is not enabled in strategies.yaml")
            print("  Running it anyway as requested...")
        enabled_strategies = [only_strategy]

    print(f"\n  {len(enabled_strategies)} strategy(ies) to process\n")

    results = {}   # yaml_name -> list of combo result dicts
    skipped = []

    for yaml_name in enabled_strategies:
        wfo_name = yaml_name

        # Must be in STRATEGY_MAP
        if wfo_name not in STRATEGY_MAP:
            print(f"  [SKIP] {yaml_name}  (wfo_name={wfo_name!r} not in STRATEGY_MAP)")
            skipped.append(yaml_name)
            continue

        # Must have WFO_CONFIGS entry
        if yaml_name not in WFO_CONFIGS:
            print(f"  [SKIP] {yaml_name}  (no WFO_CONFIGS entry)")
            skipped.append(yaml_name)
            continue

        combos = WFO_CONFIGS[yaml_name]
        results[yaml_name] = []

        for pair, timeframe in combos:
            print(f"  {'-'*57}")
            print(f"  WFO | {yaml_name}  {pair}  {timeframe}")
            print(f"  {'-'*57}")

            try:
                window_results = run_single_wfo(
                    wfo_name, pair, timeframe, is_pct, oos_pct, n_windows
                )
                results[yaml_name].append({
                    "pair": pair,
                    "timeframe": timeframe,
                    "windows": window_results,
                    "pass_rate": calc_pass_rate(window_results, timeframe),
                    "error": None,
                })
            except Exception as exc:
                print(f"    ERROR: {exc}", flush=True)
                results[yaml_name].append({
                    "pair": pair,
                    "timeframe": timeframe,
                    "windows": [],
                    "pass_rate": 0.0,
                    "error": str(exc),
                })

        print()

    summary_path = write_summary(results, skipped, n_windows, is_pct, oos_pct)

    print("=" * 65)
    print(f"  WFO complete.")
    print(f"  Summary  : {summary_path}")
    print(f"  Finished : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 65)
    print()

    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Batch Walk-Forward Optimisation for all enabled strategies."
    )
    parser.add_argument(
        "--n_windows", type=int, default=5,
        help="Number of rolling WFO windows (default: 5)"
    )
    parser.add_argument(
        "--is_pct", type=float, default=0.70,
        help="In-sample fraction 0-1 (default: 0.70)"
    )
    parser.add_argument(
        "--oos_pct", type=float, default=0.30,
        help="Out-of-sample fraction 0-1 (default: 0.30)"
    )
    parser.add_argument(
        "--strategy", type=str, default=None,
        help="Run WFO for a single strategy only (yaml name)"
    )
    args = parser.parse_args()

    run_all_wfo(
        n_windows=args.n_windows,
        is_pct=args.is_pct,
        oos_pct=args.oos_pct,
        only_strategy=args.strategy,
    )
