"""
data/ingestion.py
=================
Full historical data pipeline for all 5 approved trading pairs.

What this script does:
  1. Connects to the MT5 terminal
  2. Pulls M1 OHLCV history from DEFAULT_START_DATE to now for all 5 pairs
  3. Stores raw M1 bars in the market_data table
  4. Resamples M1 → M5, M15, H1, H4, D1 for each pair
  5. Runs a gap check on each pair/timeframe
  6. Prints a data coverage summary

Run this ONCE before starting the backtesting engine (Step 11).
After the initial ingest, the scheduler's daily data ingest job
(jobs.py — midnight) will keep data topped up using pull_latest_bars().

Usage:
  python -m data.ingestion
  OR
  python data/ingestion.py

Expected duration: 5–20 minutes depending on broker data depth.
"""

import time
from datetime import datetime

import MetaTrader5 as mt5

from mt5_bridge.connector import MT5Connector
from mt5_bridge.data_feed import MT5DataFeed, DEFAULT_START_DATE
from data.resampler import DataResampler
from data.cleaner import DataCleaner

# ---------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------

# All approved pairs — must match config.yaml pairs section
# Crypto pairs (BTCUSD, ETHUSD) are included: Exness provides crypto CFD history from MT5.
# If your broker uses different symbol names (e.g. 'BTC/USD'), update these strings to match.
PAIRS = ["XAUUSD", "EURUSD", "GBPUSD", "USDJPY", "XAGUSD", "BTCUSD", "ETHUSD"]

# Pairs that trade 24/7 — weekend data will be present, no gaps expected Sat/Sun
CRYPTO_PAIRS = ["BTCUSD", "ETHUSD"]

# Source timeframe — all higher TFs are derived from this
SOURCE_TIMEFRAME = mt5.TIMEFRAME_M1

# Derived timeframes to resample into after M1 pull
RESAMPLE_TIMEFRAMES = ["M5", "M15", "H1", "H4", "D1"]

# Pull from this date to now
START_DATE = DEFAULT_START_DATE  # 2020-01-01 by default


def pull_m1_history(feed: MT5DataFeed) -> dict:
    """
    Step 1: Pull M1 history for all pairs.
    Now optimized: checks the DB for existing data and only pulls the bridge.
    Returns a summary dict {pair: bars_inserted}.
    """
    print("\n" + "=" * 60)
    print("STEP 1 - Pulling M1 history (Incremental Update)")
    print("=" * 60)

    results = {}
    for pair in PAIRS:
        print(f"\n[{pair}]")
        
        # Check DB for existing data
        info = feed.get_data_range(pair, "M1")
        last_in_db = info.get("latest")
        
        if last_in_db:
            # We have data, so start from the last bar + 1 min to avoid overlap
            from datetime import timedelta
            pull_start = last_in_db + timedelta(minutes=1)
            print(f"  Existing data found. Syncing from {pull_start}...")
        else:
            # Fresh start
            pull_start = START_DATE
            print(f"  No existing data in DB. Performing full backfill from {pull_start.date()}...")

        try:
            bars = feed.pull_historical_data(
                symbol=pair,
                timeframe=SOURCE_TIMEFRAME,
                start_date=pull_start,
                end_date=datetime.now()
            )
            results[pair] = bars
        except Exception as e:
            print(f"  ERROR pulling {pair}: {e}")
            results[pair] = 0

        time.sleep(0.5)  # Brief pause between pairs to avoid rate limits

    # Warn about any crypto pairs that returned 0 bars (symbol name may differ per broker)
    for pair in CRYPTO_PAIRS:
        if results.get(pair, 0) == 0:
            print(f"\n  [WARN] {pair} returned 0 bars.")
            print(f"     Check symbol name: python -c \"import MetaTrader5 as mt5; mt5.initialize(); print([s.name for s in mt5.symbols_get() if 'BTC' in s.name])\"")

    return results


def resample_all_pairs(resampler: DataResampler) -> None:
    """
    Step 2: Derive M5, M15, H1, H4, D1 from M1 for all pairs.
    """
    print("\n" + "=" * 60)
    print("STEP 2 - Resampling M1 -> M5, M15, H1, H4, D1")
    print("=" * 60)

    for pair in PAIRS:
        print(f"\n[{pair}]")
        for tf in RESAMPLE_TIMEFRAMES:
            try:
                resampler.resample_and_store(pair, tf)
            except Exception as e:
                print(f"  ERROR resampling {pair} {tf}: {e}")


def run_gap_checks(cleaner: DataCleaner) -> None:
    """
    Step 3: Check data quality — flag gaps in each pair/timeframe.
    """
    print("\n" + "=" * 60)
    print("STEP 3 - Running gap checks on all pairs/timeframes")
    print("=" * 60)

    check_timeframes = ["M1", "H1", "D1"]  # Representative sample

    for pair in PAIRS:
        for tf in check_timeframes:
            try:
                gaps = cleaner.find_gaps(pair, tf)
                if gaps:
                    print(f"  WARN: {pair} {tf} — {len(gaps)} gap(s) found")
                else:
                    print(f"  OK:   {pair} {tf} — clean")
            except Exception as e:
                print(f"  ERROR checking {pair} {tf}: {e}")


def print_coverage_summary(feed: MT5DataFeed) -> None:
    """
    Step 4: Print a coverage table so you can confirm what data is available.
    """
    print("\n" + "=" * 60)
    print("DATA COVERAGE SUMMARY")
    print("=" * 60)
    print(f"{'Pair':<10} {'TF':<6} {'Bars':>10}  {'From':<12} {'To':<12}")
    print("-" * 56)

    check_timeframes = ["M1", "H1", "D1"]
    for pair in PAIRS:
        for tf in check_timeframes:
            info = feed.get_data_range(pair, tf)
            bars = info.get("total_bars", 0)
            if bars > 0:
                frm = str(info["earliest"].date())
                to  = str(info["latest"].date())
            else:
                frm, to = "-", "-"
            print(f"{pair:<10} {tf:<6} {bars:>10,}  {frm:<12} {to:<12}")

    print()
    print("Next step: Run the backtesting engine (Step 11).")
    print("  python scripts/run_backtest.py --strategy ma_crossover --pair XAUUSD --timeframe H1")


def run_full_ingestion():
    """
    Main entry point. Runs all 4 ingestion steps end-to-end.
    """
    print("\nTradePanel - Full Historical Data Ingestion")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Connect to MT5
    connector = MT5Connector()
    if not connector.connect():
        print("FATAL: Could not connect to MT5 terminal. Is it running and logged in?")
        return

    feed = MT5DataFeed()
    resampler = DataResampler()
    cleaner = DataCleaner()

    try:
        # Step 1: Pull M1 history
        m1_results = pull_m1_history(feed)

        # Only proceed if at least one pair has data
        if all(v == 0 for v in m1_results.values()):
            print("\nFATAL: No M1 data pulled. Check MT5 symbol names and broker data depth.")
            return

        # Step 2: Resample to higher timeframes
        resample_all_pairs(resampler)

        # Step 3: Gap checks
        run_gap_checks(cleaner)

        # Step 4: Coverage summary
        print_coverage_summary(feed)

    except Exception as e:
        print(f"\nERROR during ingestion: {e}")
        raise

    finally:
        connector.disconnect()
        print(f"\nFinished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


# Alias used by scheduler/jobs.py
run_ingestion = run_full_ingestion


if __name__ == "__main__":
    run_full_ingestion()
