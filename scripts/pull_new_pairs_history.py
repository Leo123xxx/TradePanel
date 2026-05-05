"""
scripts/pull_new_pairs_history.py
==================================
Targeted full-history pull for pairs that may have insufficient data
for backtesting (typically stock CFDs and newer FX crosses).

Checks which pairs have fewer than MIN_BARS bars of H4 data in the DB,
then forces a full historical M1 pull + resample for those pairs only.

Run this before running backtests on: NVDA, AMD, MSFT, AAPL, US500, USTEC,
USOIL, GBPJPY, AUDUSD, USDCAD.

Usage:
    python scripts/pull_new_pairs_history.py
    python scripts/pull_new_pairs_history.py --pairs NVDA AAPL   # specific pairs only
    python scripts/pull_new_pairs_history.py --check-only         # show coverage, no pull
"""

import sys
import os
import argparse
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
load_dotenv()

from data.db_client import DBClient

# Pairs most likely to need a history pull
NEW_PAIRS = [
    "NVDA", "AMD", "MSFT", "AAPL",      # Stock CFDs
    "US500", "USTEC",                    # Index CFDs
    "USOIL",                             # Energy CFD
    "GBPJPY", "AUDUSD", "USDCAD",       # FX crosses
]

MIN_H4_BARS = 200    # minimum H4 bars needed for backtesting


def check_coverage(db: DBClient) -> dict:
    """Return dict of pair -> H4 bar count."""
    coverage = {}
    for pair in NEW_PAIRS:
        rows = db.execute_query(
            "SELECT COUNT(*) FROM market_data WHERE pair = %s AND timeframe = 'H4'",
            (pair,)
        )
        count = rows[0][0] if rows else 0
        coverage[pair] = count
    return coverage


def print_coverage(coverage: dict):
    print("\n  Coverage check (H4 bars):")
    print("  {:12} {:>10}  {}".format("Pair", "H4 Bars", "Status"))
    print("  " + "-" * 40)
    for pair, count in sorted(coverage.items()):
        status = "OK" if count >= MIN_H4_BARS else "NEEDS PULL"
        print("  {:12} {:>10}  {}".format(pair, count, status))
    print()


def pull_pairs(pairs_to_pull: list):
    """Force full history pull for specified pairs by calling MT5 ingestion directly."""
    try:
        import MetaTrader5 as mt5
    except ImportError:
        print("\n  ERROR: MetaTrader5 not installed or not available in this environment.")
        print("  Run this script on the Windows machine with MT5 installed.")
        return

    from data.ingestion import DataIngester, DataResampler

    if not mt5.initialize():
        print("  ERROR: Could not initialize MT5. Is the terminal running and logged in?")
        return

    ingester  = DataIngester()
    resampler = DataResampler()

    print(f"\n  Pulling full M1 history for {len(pairs_to_pull)} pairs...")
    print(f"  Pairs: {', '.join(pairs_to_pull)}\n")

    for pair in pairs_to_pull:
        print(f"  [{pair}] Pulling M1 history...")
        try:
            n = ingester.pull_pair(pair, force_full=True)
            print(f"  [{pair}] Pulled {n} M1 bars")
        except Exception as e:
            print(f"  [{pair}] ERROR during pull: {e}")

    print("\n  Resampling to M5/M15/M30/H1/H4/D1...")
    for pair in pairs_to_pull:
        print(f"  [{pair}] Resampling...")
        try:
            resampler.resample_pair(pair)
            print(f"  [{pair}] Done")
        except Exception as e:
            print(f"  [{pair}] ERROR during resample: {e}")

    mt5.shutdown()


def main():
    parser = argparse.ArgumentParser(description="Pull full history for new pairs")
    parser.add_argument("--pairs", nargs="+", default=None,
                        help="Specific pairs to pull (default: all NEW_PAIRS with insufficient data)")
    parser.add_argument("--check-only", action="store_true",
                        help="Only show coverage, do not pull data")
    parser.add_argument("--force-all", action="store_true",
                        help="Pull all NEW_PAIRS regardless of current coverage")
    args = parser.parse_args()

    print()
    print("=" * 62)
    print("  TradePanel - New Pairs History Pull")
    print(f"  Started : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 62)

    db = DBClient()
    coverage = check_coverage(db)
    print_coverage(coverage)

    if args.check_only:
        print("  [check-only] No data pulled.")
        return

    if args.pairs:
        pairs_to_pull = [p.upper() for p in args.pairs]
    elif args.force_all:
        pairs_to_pull = NEW_PAIRS[:]
    else:
        pairs_to_pull = [p for p, count in coverage.items() if count < MIN_H4_BARS]

    if not pairs_to_pull:
        print("  All pairs have sufficient data (>= {} H4 bars). Nothing to pull.".format(MIN_H4_BARS))
        print("  Use --force-all to re-pull anyway.\n")
        return

    print(f"  Pairs needing data: {', '.join(pairs_to_pull)}")
    pull_pairs(pairs_to_pull)

    # Re-check coverage after pull
    print("\n  Post-pull coverage:")
    coverage_after = check_coverage(db)
    print_coverage(coverage_after)

    print("=" * 62)
    print(f"  Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 62)
    print()


if __name__ == "__main__":
    main()
