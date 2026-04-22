import os
import sys
import pandas as pd
from datetime import datetime, timedelta

# Add project root to path
sys.path.insert(0, os.getcwd())

from data.db_client import DBClient
from scripts.run_backtest import STRATEGY_MAP
from backtesting.engine import BacktestEngine
from backtesting.metrics import BacktestMetrics
from backtesting.report import StatsReport

def run_summary():
    print("=" * 60)
    print("   MT5 PLATFORM - STEP 18 STABILIZATION SUMMARY")
    print("=" * 60)
    
    db = DBClient()
    
    # 1. Data Coverage Check
    print("\n1. DATA COVERAGE AUDIT")
    print("-" * 30)
    pairs = ["EURUSD", "XAUUSD", "BTCUSD", "ETHUSD"]
    for p in pairs:
        row = db.execute_query("SELECT COUNT(*), MIN(timestamp), MAX(timestamp) FROM market_data WHERE pair = %s", (p,))
        count, start, end = row[0]
        print(f"  {p:8}: {count:8,} bars | {start.date()} to {end.date()}" if count > 0 else f"  {p:8}: NO DATA")

    # 2. Benchmark Backtests (Last 6 Months)
    print("\n2. STRATEGY BENCHMARKS (Last 6 Months)")
    print("-" * 30)
    
    benchmarks = [
        {"name": "range_breakout",      "pair": "XAUUSD", "tf": "H4"},
        {"name": "rsi_pullback",        "pair": "EURUSD", "tf": "H4"},
        {"name": "ema_ribbon_trend",    "pair": "BTCUSD", "tf": "H4"},
    ]
    
    cutoff = datetime.now() - timedelta(days=180)
    
    for b in benchmarks:
        print(f"  Running {b['name']} on {b['pair']}...")
        rows = db.execute_query(
            "SELECT timestamp, open, high, low, close, tick_volume "
            "FROM market_data WHERE pair = %s AND timeframe = %s AND timestamp > %s ORDER BY timestamp",
            (b['pair'], b['tf'], cutoff)
        )
        if not rows:
            print(f"    [!] Missing data for {b['pair']} {b['tf']}")
            continue
            
        df = pd.DataFrame(rows, columns=["timestamp", "open", "high", "low", "close", "tick_volume"])
        df.set_index("timestamp", inplace=True)
        for col in ["open", "high", "low", "close", "tick_volume"]:
            df[col] = df[col].astype(float)
            
        strategy = STRATEGY_MAP[b['name']]()
        engine = BacktestEngine(lot_size=0.1, initial_balance=10000.0)
        trades_df = engine.run(strategy, b['pair'], b['tf'], df)
        
        if not trades_df.empty:
            metrics = BacktestMetrics(df, trades_df, 10000.0).calculate_all()
            pf = metrics.get('profit_factor', 0)
            sharpe = metrics.get('sharpe_ratio', 0)
            wr = metrics.get('win_rate', 0)
            print(f"    PF: {pf:.2f} | Sharpe: {sharpe:.2f} | WR: {wr:.1%}")
        else:
            print("    [!] No trades generated in 6-month window.")

    # 3. Component Health
    print("\n3. COMPONENT ALIGNMENT CHECK")
    print("-" * 30)
    
    # Check bot_health
    health_row = db.execute_query("SELECT status, timestamp FROM bot_health ORDER BY timestamp DESC LIMIT 1")
    if health_row:
        status, ts = health_row[0]
        ago = (datetime.now() - ts).total_seconds()
        print(f"  System Health: {status} (Last Heartbeat: {ago:.0f}s ago)")
    else:
        print("  System Health: NO HEARTBEAT RECORDED (Never started?)")
    
    # Check trades table presence
    trades_count = db.execute_query("SELECT COUNT(*) FROM trades")[0][0]
    print(f"  Paper Trades : {trades_count} records in 'trades' table")

    print("\n" + "=" * 60)
    print("   STABILIZATION SUMMARY COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    run_summary()
