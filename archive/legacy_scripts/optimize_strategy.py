import sys
import os
import itertools
import pandas as pd
import argparse
from datetime import datetime

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.db_client import DBClient
from backtesting.engine import BacktestEngine
from backtesting.metrics import BacktestMetrics
from scripts.run_backtest import STRATEGY_MAP

def optimize_strategy(strategy_name: str, symbol: str, timeframe: str, 
                      lot_size: float = 0.1, initial_balance: float = 10000.0,
                      num_groups: int = 10):
    
    print(f"\nOPTIMIZING Strategy: {strategy_name} on {symbol} {timeframe}")
    db = DBClient()
    
    # 1. Load data
    print(f"Loading {symbol} {timeframe} data...")
    rows = db.execute_query(
        "SELECT timestamp, open, high, low, close, tick_volume "
        "FROM market_data WHERE pair = %s AND timeframe = %s ORDER BY timestamp",
        (symbol, timeframe)
    )
    if not rows:
        print(f"ERROR: No data found for {symbol} {timeframe}")
        return

    df = pd.DataFrame(rows, columns=["timestamp", "open", "high", "low", "close", "tick_volume"])
    df.set_index("timestamp", inplace=True)
    for col in ["open", "high", "low", "close", "tick_volume"]:
        df[col] = df[col].astype(float)

    # 2. Define Parameter Search Space (Hardcoded for common strategy params)
    # In a real scenario, this would be more dynamic.
    param_ranges = {
        "ma_crossover": {
            "fast_period": [7, 9, 12],
            "slow_period": [21, 26, 50],
            "tp_atr_mult": [1.5, 2.0, 3.0],
            "sl_atr_mult": [1.0, 1.5]
        },
        "rsi_pullback": {
            "rsi_period": [7, 14, 21],
            "fast_ema": [10, 20],
            "slow_ema": [50, 100],
            "tp_atr_mult": [1.5, 2.0, 3.0]
        },
        "range_breakout": {
            "consolidation_bars": [15, 20, 25],
            "vol_threshold_mult": [1.2, 1.5, 2.0],
            "tp_range_mult": [2.0, 3.0]
        },
        "swing_pullback": {
            "swing_lookback": [3, 5, 10],
            "tp_pips": [50, 100, 200],
            "sl_pips": [20, 30, 50]
        },
        "ema_ribbon_trend": {
            "fast_ema": [7, 9, 12],
            "mid_ema": [21, 26],
            "slow_ema": [50, 100],
            "tp_atr_mult": [3.0, 4.0]
        },
        "crypto_rsi_extremes": {
            "rsi_period": [14, 21],
            "rsi_oversold": [20, 25, 30],
            "rsi_overbought": [70, 75, 80],
            "tp_atr_mult": [2.0, 3.0]
        },
        "volatility_squeeze_breakout": {
            "squeeze_pct": [0.02, 0.03, 0.04],
            "tp_atr_mult": [2.5, 3.0, 4.0]
        },
        # Generic fallback
        "default": {
            "param1": [1, 2, 3],
            "param2": [10, 20]
        }
    }

    # Get search space or fallback
    space = param_ranges.get(strategy_name.lower(), param_ranges["default"])
    
    # Generate all combinations
    keys = space.keys()
    values = space.values()
    combinations = [dict(zip(keys, v)) for v in itertools.product(*values)]
    
    # Limit to num_groups (user requested 10)
    import random
    if len(combinations) > num_groups:
        combinations = random.sample(combinations, num_groups)

    results = []
    engine = BacktestEngine(lot_size=lot_size, initial_balance=initial_balance)
    
    # 3. Run search
    for i, params in enumerate(combinations):
        print(f"Group {i+1}/{len(combinations)}: Testing {params}...")
        
        # Instantiate strategy with custom params
        strategy_class = STRATEGY_MAP[strategy_name.lower()]
        strategy = strategy_class(params)
        
        trades_df = engine.run(strategy, symbol, timeframe, df)
        if trades_df is not None and not trades_df.empty:
            metrics = BacktestMetrics(df, trades_df, initial_balance).calculate_all()
            results.append({
                "params": params,
                "win_rate": metrics.get("win_rate", 0),
                "profit_factor": metrics.get("profit_factor", 0),
                "sharpe_ratio": metrics.get("sharpe_ratio", 0),
                "total_trades": metrics.get("total_trades", 0),
                "net_profit": metrics.get("net_profit", 0)
            })
        else:
            results.append({
                "params": params,
                "win_rate": 0, "profit_factor": 0, "sharpe_ratio": 0, "total_trades": 0, "net_profit": 0
            })

    # 4. Display Results Summary
    res_df = pd.DataFrame(results)
    res_df = res_df.sort_values(by="profit_factor", ascending=False)
    
    print(f"\n--- OPTIMIZATION SUMMARY for {strategy_name} ---")
    print(res_df.head(10).to_string(index=False))
    
    # Recommend best
    best = res_df.iloc[0] # Best is first after sorting
    print(f"\nRECOMMENDATION: {best['params']}")
    wr = best['win_rate']
    if wr > 1: wr = wr / 100 # Handle 0-100 scale vs 0-1 scale
    print(f"Expected PF: {best['profit_factor']:.2f}, Win Rate: {wr:.2%}")

    return res_df

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--strategy", type=str, required=True)
    parser.add_argument("--pair", type=str, default="XAUUSD")
    parser.add_argument("--timeframe", type=str, default="H4")
    parser.add_argument("--groups", type=int, default=10)
    
    args = parser.parse_args()
    optimize_strategy(args.strategy, args.pair, args.timeframe, num_groups=args.groups)
