import time
import os
import sys
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Setup root path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from data.db_client import DBClient
from strategies.bb_mean_reversion import BBMeanReversionStrategy
try:
    import MetaTrader5 as mt5
except ImportError:
    mt5 = None

def benchmark_db():
    print("\n[DB Benchmark]")
    db = DBClient()
    
    start = time.time()
    # Test simple query
    db.execute_query("SELECT 1")
    simple_time = (time.time() - start) * 1000
    print(f"  Simple query: {simple_time:.2f}ms")
    
    start = time.time()
    # Test larger query
    db.execute_query("SELECT * FROM market_data LIMIT 1000")
    large_time = (time.time() - start) * 1000
    print(f"  Fetch 1000 bars: {large_time:.2f}ms")

def benchmark_mt5():
    if not mt5:
        print("\n[MT5 Benchmark] Skipping (MetaTrader5 not installed)")
        return
        
    print("\n[MT5 Benchmark]")
    if not mt5.initialize():
        print("  Failed to initialize MT5")
        return
        
    symbol = "XAUUSD"
    start = time.time()
    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_H1, 0, 100)
    fetch_time = (time.time() - start) * 1000
    print(f"  Fetch 100 bars ({symbol} H1): {fetch_time:.2f}ms")
    
    start = time.time()
    mt5.account_info()
    acc_time = (time.time() - start) * 1000
    print(f"  Account info fetch: {acc_time:.2f}ms")
    
    mt5.shutdown()

def benchmark_strategy():
    print("\n[Strategy Benchmark]")
    # Generate dummy data
    data = pd.DataFrame({
        'open': np.random.randn(5000),
        'high': np.random.randn(5000),
        'low': np.random.randn(5000),
        'close': np.random.randn(5000),
        'tick_volume': np.random.randint(100, 1000, 5000)
    }, index=pd.date_range(start='2020-01-01', periods=5000, freq='h'))
    
    strategy = BBMeanReversionStrategy()
    
    start = time.time()
    strategy.generate_signals(data)
    gen_time = (time.time() - start) * 1000
    print(f"  BB Mean Reversion (5000 bars): {gen_time:.2f}ms")
    
    # Test Cooldown optimization
    data['signal'] = np.random.choice([0, 1, -1], 5000, p=[0.9, 0.05, 0.05])
    start = time.time()
    strategy.apply_cooldown(data, cooldown_bars=10)
    cool_time = (time.time() - start) * 1000
    print(f"  Apply Cooldown (5000 bars): {cool_time:.2f}ms")

def main():
    print("=" * 60)
    print("  TradePanel Performance Benchmark")
    print(f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    benchmark_db()
    benchmark_mt5()
    benchmark_strategy()
    
    print("\n" + "=" * 60)
    print("  Benchmark Complete")
    print("=" * 60)

if __name__ == "__main__":
    main()
