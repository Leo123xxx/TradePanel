import sys
import os
from pathlib import Path
from datetime import datetime

# Set repo root explicitly
REPO_ROOT = r"f:\REPOS\leo123xxx\TradePanel"
sys.path.insert(0, REPO_ROOT)

from data.db_client import DBClient
from data.resampler import DataResampler

def main():
    db = DBClient()
    resampler = DataResampler(db)
    
    pairs = ["XAUUSD", "EURUSD", "GBPUSD", "USDJPY", "XAGUSD", "BTCUSD", "ETHUSD"]
    
    print(f"Starting full M30 backfill for all pairs...")
    
    for pair in pairs:
        try:
            # Resample M30 only, with 1500 days lookback
            resampler.resample_m1_to_higher(pair, target_tfs=['M30'], lookback_days=1500)
        except Exception as e:
            print(f"Error backfilling {pair}: {e}")
            
    print("Full M30 backfill complete.")

if __name__ == "__main__":
    main()
