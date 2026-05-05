import sys
import os
import pandas as pd
import numpy as np
import itertools
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.db_client import DBClient
from backtesting.engine import BacktestEngine
from backtesting.metrics import BacktestMetrics
from scripts.run_backtest import STRATEGY_MAP

def get_data(symbol, timeframe):
    db = DBClient()
    rows = db.execute_query(
        "SELECT timestamp, open, high, low, close, tick_volume "
        "FROM market_data WHERE pair = %s AND timeframe = %s ORDER BY timestamp",
        (symbol, timeframe)
    )
    if not rows:
        return None
    df = pd.DataFrame(rows, columns=["timestamp", "open", "high", "low", "close", "tick_volume"])
    df.set_index("timestamp", inplace=True)
    for col in ["open", "high", "low", "close", "tick_volume"]:
        df[col] = df[col].astype(float)
    return df

def optimize(strategy_name, symbol, timeframe, param_grid):
    print(f"\n" + "="*60)
    print(f"OPTIMIZING: {strategy_name} on {symbol} ({timeframe})")
    print("="*60)
    
    df = get_data(symbol, timeframe)
    if df is None:
        print(f"  [!] No data found for {symbol} {timeframe}")
        return
        
    keys = param_grid.keys()
    combinations = list(itertools.product(*param_grid.values()))
    
    results = []
    total = len(combinations)
    
    print(f"  Grid Size: {total} combinations")
    
    for i, values in enumerate(combinations):
        params = dict(zip(keys, values))
        
        # Instantiate strategy with these params
        strat_class = STRATEGY_MAP.get(strategy_name.lower())
        if not strat_class:
            print(f"  [!] Strategy {strategy_name} not found.")
            return
            
        strategy = strat_class(params=params)
        engine = BacktestEngine(initial_balance=10000.0)
        
        try:
            trades_df = engine.run(strategy, symbol, timeframe, df, silent=True)
            metrics = BacktestMetrics(df, trades_df, 10000.0).calculate_all()
            
            if "error" not in metrics and metrics.get("total_trades", 0) > 10:
                pf = metrics.get("profit_factor", 0)
                sharpe = metrics.get("sharpe_ratio", 0)
                trades = metrics.get("total_trades", 0)
                wr = metrics.get("win_rate", 0)
                
                # Composite Score: Reward profit, stability, and enough data points
                score = pf * (np.log10(trades) if trades > 0 else 0) * (sharpe if sharpe > 0 else 0.1)
                
                results.append({
                    "params": params,
                    "PF": pf,
                    "Sharpe": sharpe,
                    "WR": wr,
                    "Trades": trades,
                    "Score": score
                })
        except Exception as e:
            pass # Skip crashes during search
            
        if (i+1) % 10 == 0 or (i+1) == total:
            print(f"  Progress: {i+1}/{total} completed...")

    if not results:
        print("  [!] No valid results generated. Try widening the grid or checking data.")
        return

    # Sort by Score
    best = sorted(results, key=lambda x: x["Score"], reverse=True)[0]
    
    print("\n" + "-"*40)
    print("BEST PARAMETERS FOUND")
    print("-"*40)
    for k, v in best["params"].items():
        print(f"  {k:<20}: {v}")
    print(f"  Profit Factor       : {best['PF']:.2f}")
    print(f"  Sharpe Ratio        : {best['Sharpe']:.2f}")
    print(f"  Win Rate            : {best['WR']:.2f}%")
    print(f"  Total Trades        : {best['Trades']}")
    print("-"*40)
    
    return best

if __name__ == "__main__":
    # Example usage for testing the framework
    # In practice, we will call this from a master runner or CLI
    example_grid = {
        "tp_atr_mult": [1.5, 2.0, 2.5, 3.0],
        "sl_atr_mult": [1.0, 1.5, 2.0]
    }
    # optimize("ma_crossover", "EURUSD", "H1", example_grid)
