"""
scripts/pull_deep_history.py
============================
Full 15-year history backfill for pairs that were added late and only
have a few months of data in the DB (e.g. GBPJPY, AUDUSD, USOIL).

HOW IT WORKS
------------
The normal daily ingestion only pulls *forward* from the last bar in the DB.
Pairs added in Jan 2026 therefore only have data from Jan 2026 onward.
This script forces a full backward fill to DEEP_START_DATE (default 2010-01-01)
using the existing MT5DataFeed.pull_historical_data() which chunks backwards.

Because DB inserts use ON CONFLICT DO NOTHING, re-running is safe — existing
bars are never overwritten.

REALISTIC EXPECTATIONS BY PAIR TYPE
-------------------------------------
  FX crosses (GBPJPY, AUDUSD, USDCAD)  — full 15yr history available on Exness
  Indices    (US500, USTEC)             — typically available from 2015+ on Exness
  Energy     (USOIL)                   — typically available from 2013+ on Exness
  Stock CFDs (NVDA, AMD, MSFT, AAPL)   — Exness typically provides 1-3 years only
                                          Script handles gracefully (pulls what's there)
  XAGUSD                                — full history if enabled on the account

USAGE
-----
    # Pull everything (check first, then confirm)
    venv\\Scripts\\python.exe scripts/pull_deep_history.py --check-only
    venv\\Scripts\\python.exe scripts/pull_deep_history.py

    # Pull specific pairs only
    venv\\Scripts\\python.exe scripts/pull_deep_history.py --pairs GBPJPY AUDUSD USDCAD

    # Override start date (e.g. only 5 years back)
    venv\\Scripts\\python.exe scripts/pull_deep_history.py --start 2019-01-01

    # Skip resample (just pull M1, resample separately)
    venv\\Scripts\\python.exe scripts/pull_deep_history.py --no-resample
"""

import sys
import os
import argparse
import time
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
load_dotenv()

from data.db_client import DBClient

# ── Target pairs ────────────────────────────────────────────────────────────
# Pairs known to have thin DB coverage — the whole point of this script.
# Core FX pairs (EURUSD, GBPUSD, XAUUSD, USDJPY) are already fully covered.
DEEP_PULL_PAIRS = [
    # FX crosses added Jan 2026 — only ~440 H4 bars
    "GBPJPY",
    "AUDUSD",
    "USDCAD",
    # Energy CFD added Jan 2026 — only ~450 H4 bars
    "USOIL",
    # Index CFDs added Jan 2026 — only ~455 H4 bars
    "US500",
    "USTEC",
    # Silver — may be thin depending on account history 
    "XAGUSD",
    "XAUUSD",
    "BTCUSD",
    "ETHUSD",
    "EURUSD",
    "GBPUSD",
    "USDJPY",
    # Stock CFDs — broker caps at 1-3 years; script pulls what's available
    "NVDA",
    "AMD",
    "MSFT",
    "AAPL",
]

# 15 years back. Brokers cap stock CFDs earlier; MT5 returns what it has.
DEEP_START_DATE = datetime(2010, 1, 1)

# Timeframes to resample from M1 after the pull
RESAMPLE_TIMEFRAMES = ["M2","M5", "M15", "M30", "H1", "H2", "H4", "H12", "D1"]


# ── Coverage helpers ─────────────────────────────────────────────────────────

def get_coverage(db: DBClient, pairs: list) -> dict:
    """Returns {pair: {tf: (count, min_ts, max_ts)}} for key timeframes."""
    tfs = ["M1", "M5", "M15", "M30", "H1", "H2","H4", "D1"]
    coverage = {}
    for pair in pairs:
        coverage[pair] = {}
        for tf in tfs:
            rows = db.execute_query(
                "SELECT COUNT(*), MIN(timestamp), MAX(timestamp) "
                "FROM market_data WHERE pair=%s AND timeframe=%s",
                (pair, tf)
            )
            if rows and rows[0][0]:
                count, min_ts, max_ts = rows[0]
                coverage[pair][tf] = (count, min_ts, max_ts)
            else:
                coverage[pair][tf] = (0, None, None)
    return coverage


def print_coverage(coverage: dict, label: str = ""):
    if label:
        print(f"\n  {label}")
    print(f"  {'Pair':<10} {'M1 bars':>10}  {'H4 bars':>8}  {'D1 bars':>8}  {'M1 from':>12}  {'M1 to':>12}  {'H2 bars':>8}  {'H12 bars':>8}  {'M2 bars':>10}")
    print("  " + "-" * 72)
    for pair in sorted(coverage):
        m1  = coverage[pair].get("M1",  (0, None, None))
        h4  = coverage[pair].get("H4",  (0, None, None))
        d1  = coverage[pair].get("D1",  (0, None, None))
        h2  = coverage[pair].get("H2",  (0, None, None))
        h12 = coverage[pair].get("H12", (0, None, None))
        m2  = coverage[pair].get("M2",  (0, None, None))
        m1_from = str(m1[1])[:10] if m1[1] else "—"
        m1_to   = str(m1[2])[:10] if m1[2] else "—"
        print(f"  {pair:<10} {m1[0]:>10,}  {h4[0]:>8,}  {d1[0]:>8,}  {m1_from:>12}  {m1_to:>12}")
    print()


# ── Core pull + resample ──────────────────────────────────────────────────────

# Timeframes to pull directly from MT5 — ordered coarsest first so H4/D1
# get populated even if M15 is sparse. MT5 provides H4/D1 going back 10-15yr
# even when M1 only has a few months.
DIRECT_PULL_TIMEFRAMES = [
    ("D1",  "TIMEFRAME_D1"),
    ("H12", "TIMEFRAME_H12"),
    ("H4",  "TIMEFRAME_H4"),
    ("H2",  "TIMEFRAME_H2"),
    ("H1",  "TIMEFRAME_H1"),
    ("M30", "TIMEFRAME_M30"),
    ("M15", "TIMEFRAME_M15"),
    ("M5",  "TIMEFRAME_M5"),
    ("M2",  "TIMEFRAME_M2"),
    ("M1",  "TIMEFRAME_M1"),
]


def pull_pair_direct(feed, pair: str, start_date: datetime) -> dict:
    """
    Pull each required timeframe DIRECTLY from MT5 for a pair.
    This bypasses the M1→resample pipeline which is incremental-only.
    MT5 can serve H4/D1 going back 10-15 years even when M1 only has months.
    Returns {tf_str: bars_inserted}.
    """
    import MetaTrader5 as mt5

    tf_map = {
        "TIMEFRAME_M1":  mt5.TIMEFRAME_M1,
        "TIMEFRAME_M2":  mt5.TIMEFRAME_M2,
        "TIMEFRAME_M5":  mt5.TIMEFRAME_M5,
        "TIMEFRAME_M15": mt5.TIMEFRAME_M15,
        "TIMEFRAME_M30": mt5.TIMEFRAME_M30,
        "TIMEFRAME_H1":  mt5.TIMEFRAME_H1,
        "TIMEFRAME_H2":  mt5.TIMEFRAME_H2,
        "TIMEFRAME_H4":  mt5.TIMEFRAME_H4,
        "TIMEFRAME_H12": mt5.TIMEFRAME_H12,
        "TIMEFRAME_D1":  mt5.TIMEFRAME_D1,
    }

    results = {}
    for tf_str, tf_const_name in DIRECT_PULL_TIMEFRAMES:
        tf_const = tf_map[tf_const_name]
        try:
            n = feed.pull_historical_data(
                symbol=pair,
                timeframe=tf_const,
                start_date=start_date,
                end_date=datetime.now(),
            )
            results[tf_str] = n
        except Exception as e:
            print(f"    ERROR pulling {pair} {tf_str}: {e}")
            results[tf_str] = -1
        time.sleep(0.2)

    return results


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Pull 15-year deep history for thin-coverage pairs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--pairs", nargs="+", default=None,
        metavar="PAIR",
        help="Specific pairs to pull (default: all DEEP_PULL_PAIRS)"
    )
    parser.add_argument(
        "--start", default=None,
        metavar="YYYY-MM-DD",
        help=f"Override start date (default: {DEEP_START_DATE.date()})"
    )
    parser.add_argument(
        "--check-only", action="store_true",
        help="Show current coverage only — do not pull"
    )
    parser.add_argument(
        "--no-resample", action="store_true",
        help="Pull M1 only — skip resample step (useful for debugging)"
    )
    parser.add_argument(
        "--skip-stock-cfds", action="store_true",
        help="Skip NVDA/AMD/MSFT/AAPL (broker history is limited; use to save time)"
    )
    args = parser.parse_args()

    start_date = datetime.strptime(args.start, "%Y-%m-%d") if args.start else DEEP_START_DATE

    pairs = args.pairs if args.pairs else DEEP_PULL_PAIRS[:]
    if args.skip_stock_cfds:
        stock_cfds = {"NVDA", "AMD", "MSFT", "AAPL"}
        pairs = [p for p in pairs if p not in stock_cfds]

    print()
    print("=" * 72)
    print("  TradePanel — Deep History Backfill")
    print(f"  Target start : {start_date.date()}  (up to {(datetime.now() - start_date).days // 365} years back)")
    print(f"  Pairs        : {', '.join(pairs)}")
    print(f"  Started      : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 72)

    db = DBClient()
    coverage_before = get_coverage(db, pairs)
    print_coverage(coverage_before, label="CURRENT COVERAGE (before pull):")

    if args.check_only:
        print("  [--check-only] No data pulled.\n")
        return

    # ── MT5 setup ────────────────────────────────────────────────────────────
    try:
        import MetaTrader5 as mt5
    except ImportError:
        print("  ERROR: MetaTrader5 package not installed.")
        print("  Run: pip install MetaTrader5")
        sys.exit(1)

    if not mt5.initialize():
        print("  ERROR: Could not connect to MT5 terminal.")
        print("  Ensure MetaTrader5 is running and logged into your Exness demo account.")
        sys.exit(1)

    print(f"  MT5 connected: {mt5.terminal_info().name}\n")

    from mt5_bridge.data_feed import MT5DataFeed
    
    feed      = MT5DataFeed()

    # ── Pull loop ────────────────────────────────────────────────────────────
    print("=" * 72)
    print("  STEP 1 — Pulling D1/H4/H2/H1/M30/M15/M5/M2/M1 directly from MT5")
    print("=" * 72)
    print("  (MT5 serves H4/D1 up to 10-15yr; M1 only ~3 months — bypassing M1→resample)")

    pull_results = {}
    stock_cfds = {"NVDA", "AMD", "MSFT", "AAPL"}

    for pair in pairs:
        if pair in stock_cfds:
            print(f"\n  [{pair}] Stock CFD — Exness typically provides 1-3 years.")
            print(f"  [{pair}] Pulling from broker limit (start_date ignored for stock CFDs).")
        else:
            print(f"\n  [{pair}] Pulling M1 from {start_date.date()} to now...")

        try:
            tf_results = pull_pair_direct(feed, pair, start_date)
            pull_results[pair] = tf_results
            h4_bars = tf_results.get("H4", 0)
            d1_bars = tf_results.get("D1", 0)  
            detail = "  ".join(f"{tf}:{n:,}" for tf, n in tf_results.items())
            if h4_bars > 0 or d1_bars > 0:
                print(f"  [{pair}] ✅  {detail}")
            else:
                print(f"  [{pair}] ⚠  0 H4/D1 bars — check symbol or account permissions")
                print(f"          Detail: {detail}")
        except Exception as e:
            print(f"  [{pair}] ❌ ERROR: {e}")
            pull_results[pair] = {}

        time.sleep(0.5)

    # Resample not needed — each TF is pulled directly from MT5.
    # The incremental DataResampler only handles NEW bars going forward;
    # for deep historical backfill we bypass it entirely.
    if args.no_resample:
        print("\n  [--no-resample] flag set (has no effect — direct pull already covers all TFs).")

    mt5.shutdown()

    # ── Post-pull coverage ────────────────────────────────────────────────────
    print()
    print("=" * 72)
    coverage_after = get_coverage(db, pairs)
    print_coverage(coverage_after, label="COVERAGE AFTER PULL:")

    # Summary table
    print("  PULL SUMMARY")
    print(f"  {'Pair':<10} {'H4 added':>10} {'H4 before':>10}  {'H4 after':>10}  {'Status'}")
    print("  " + "-" * 60)
    for pair in pairs:
        before_h4 = coverage_before[pair].get("H4", (0,))[0]
        after_h4  = coverage_after[pair].get("H4", (0,))[0]
        tf_res    = pull_results.get(pair, {})
        h4_added  = tf_res.get("H4", -1) if isinstance(tf_res, dict) else -1
        if isinstance(tf_res, dict) and tf_res:
            status = "✅ Pulled" if h4_added > 0 else "⚠ 0 H4 bars"
        else:
            status = "❌ Error"
        print(f"  {pair:<10} {h4_added:>10,}  {before_h4:>10,}  {after_h4:>10,}  {status}")

    print()
    print("=" * 72)
    print(f"  Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 72)
    print()
    print("  NEXT STEPS:")
    print("  1. Re-run backtests on pairs that gained significant H4 bars:")
    print("     venv\\Scripts\\python.exe scripts/run_overnight_backtest.py --strategy dual_ema_fractal,range_breakout,rvgi_cci_confluence,turtle_soup")
    print("  2. For stock CFDs with only 1-3yr history: accept as monitor_only")
    print("     until broker provides more data.")
    print()


if __name__ == "__main__":
    main()
