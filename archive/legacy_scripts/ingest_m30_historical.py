#!/usr/bin/env python3
"""
scripts/ingest_m30_historical.py
================================
Directly pulls M30 historical data from MT5 for all 7 pairs.
Used to fill the data gap for M30 strategies (2022-2026).
"""

import sys
import os
from datetime import datetime
from pathlib import Path
import MetaTrader5 as mt5

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from mt5_bridge.connector import MT5Connector
from mt5_bridge.data_feed import MT5DataFeed

PAIRS = ["XAUUSD", "EURUSD", "GBPUSD", "USDJPY", "XAGUSD", "BTCUSD", "ETHUSD"]
START_DATE = datetime(2022, 1, 1)
END_DATE = datetime.now()

def run_m30_ingest():
    print(f"Starting M30 historical ingestion from {START_DATE} to {END_DATE}")
    
    connector = MT5Connector()
    if not connector.connect():
        print("Failed to connect to MT5")
        return
        
    feed = MT5DataFeed()
    
    for pair in PAIRS:
        print(f"\nProcessing {pair}...")
        try:
            inserted = feed.pull_historical_data(
                symbol=pair,
                timeframe=mt5.TIMEFRAME_M30,
                start_date=START_DATE,
                end_date=END_DATE
            )
            print(f"  Successfully inserted {inserted:,} bars for {pair}")
        except Exception as e:
            print(f"  Error processing {pair}: {e}")
            
    connector.disconnect()
    print("\nM30 Ingestion Complete.")

if __name__ == "__main__":
    run_m30_ingest()
