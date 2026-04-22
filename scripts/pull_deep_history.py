import os
import sys
import time
from datetime import datetime
import MetaTrader5 as mt5

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from mt5_bridge.connector import MT5Connector
from mt5_bridge.data_feed import MT5DataFeed

# Configuration for deep pull
PAIRS = ["XAUUSD", "EURUSD", "GBPUSD", "USDJPY", "XAGUSD", "BTCUSD", "ETHUSD"]

# Recommended deep-pull counts
DEEP_TIMEFRAMES = [
    (mt5.TIMEFRAME_M15, 50000, "M15"),
    (mt5.TIMEFRAME_H1,  50000, "H1"),
    (mt5.TIMEFRAME_H2,  25000, "H2"),
    (mt5.TIMEFRAME_H4,  30000, "H4"),
    (mt5.TIMEFRAME_H6,  15000, "H6"),
    (mt5.TIMEFRAME_H12, 10000, "H12"),
    (mt5.TIMEFRAME_D1,  5000,  "D1")
]

REPORT_FILE = os.path.join(project_root, "data", "ingestion_report.log")

def log_report(message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(REPORT_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")
    print(message)

def run_deep_pull():
    print(f"TradePanel - Deep Historical Data Ingestion")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    log_report("Initializing deep history pull...")

    connector = MT5Connector()
    if not connector.connect():
        log_report("FATAL: Could not connect to MT5 terminal.")
        return

    feed = MT5DataFeed()
    
    summary = []
    summary.append(f"{'Pair':<10} {'TF':<6} {'Target':>10} {'Actual':>10} {'Status':<10}")
    summary.append("-" * 55)

    try:
        for pair in PAIRS:
            log_report(f"\nProcessing {pair}...")
            for tf_const, target_count, tf_label in DEEP_TIMEFRAMES:
                print(f"  Pulling {tf_label} ({target_count} bars)...")
                try:
                    # We use pull_latest_bars with a large count to get as much as the broker allows
                    actual = feed.pull_latest_bars(pair, tf_const, count=target_count)
                    status = "OK" if actual > 0 else "EMPTY"
                    log_report(f"  {pair} {tf_label}: {actual:,} bars pulled.")
                    summary.append(f"{pair:<10} {tf_label:<6} {target_count:>10,} {actual:>10,} {status:<10}")
                except Exception as e:
                    log_report(f"  ERROR {pair} {tf_label}: {e}")
                    summary.append(f"{pair:<10} {tf_label:<6} {target_count:>10,} {'ERROR':>10} {'FAILED':<10}")
                
                time.sleep(0.5) # Anti-rate-limit

        # Final Report
        report_boundary = "=" * 60
        log_report(f"\n{report_boundary}")
        log_report("DEEP INGESTION SUMMARY REPORT")
        log_report(report_boundary)
        for line in summary:
            log_report(line)
        log_report(f"{report_boundary}\n")

    except Exception as e:
        log_report(f"CRITICAL ERROR during deep pull: {e}")
    finally:
        connector.disconnect()
        log_report(f"Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    run_deep_pull()
