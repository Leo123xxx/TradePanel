import os
import sys
import json
import argparse
from datetime import datetime
import pandas as pd
from ruamel.yaml import YAML

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.db_client import DBClient
from backtesting.walk_forward import WalkForwardOptimizer

def auto_optimize(quick_mode=False):
    db = DBClient()
    yaml_handler = YAML()
    yaml_handler.preserve_quotes = True
    yaml_handler.indent(mapping=2, sequence=4, offset=2)
    
    config_path = "config/strategies.yaml"
    with open(config_path, "r") as f:
        strat_data = yaml_handler.load(f)
    
    # Initialize Optimizer
    optimizer = WalkForwardOptimizer(db)
    
    summary_logs = []
    processed_count = 0
    
    for strat_key, strat_info in strat_data.items():
        if not isinstance(strat_info, dict) or strat_info.get("status") != "implemented":
            continue
            
        if quick_mode and processed_count >= 1:
            break
            
        name = strat_info.get("name", strat_key)
        print(f"\n--- Optimizing {name} ({strat_key}) ---")
        
        pairs = strat_info.get("pairs", ["XAUUSD"])
        timeframes = strat_info.get("timeframes", ["H4"])
        
        # We'll optimize for the first pair/timeframe as a representative
        # In a more advanced version, we'd optimize for all and update overrides
        symbol = pairs[0]
        tf = timeframes[0]
        
        # Load data
        query = "SELECT timestamp, open, high, low, close, tick_volume FROM market_data WHERE pair = %s AND timeframe = %s ORDER BY timestamp"
        rows = db.execute_query(query, (symbol, tf))
        
        if not rows:
            print(f"  No data for {symbol} {tf}. Skipping.")
            continue
            
        df = pd.DataFrame(rows, columns=['timestamp', 'open', 'high', 'low', 'close', 'tick_volume'])
        df.set_index('timestamp', inplace=True)
        for col in ['open', 'high', 'low', 'close', 'tick_volume']:
            df[col] = df[col].astype(float)
            
        # Run WFO
        try:
            results = optimizer.run(
                strategy_key=strat_key,
                symbol=symbol,
                timeframe=tf,
                df=df,
                is_pct=0.7,
                oos_pct=0.2,
                n_windows=2 if quick_mode else 5
            )
            
            processed_count += 1
            
            if not results:
                continue
                
            # Evaluation
            profitable_windows = sum(1 for res in results if res.get('oos_sharpe', 0) > 0)
            pass_rate = (profitable_windows / len(results)) * 100
            
            print(f"  Pass Rate: {pass_rate:.1f}%")
            
            if pass_rate >= 70:
                # Take best params from the MOST RECENT window
                latest_best_params = results[-1]['best_params']
                print(f"  Passed! Updating parameters to: {latest_best_params}")
                
                # Update strat_data
                if "parameters" in strat_info:
                    for k, v in latest_best_params.items():
                        if k in strat_info["parameters"]:
                             strat_info["parameters"][k] = v
                
                summary_logs.append(f"[SUCCESS] {name}: Optimized. Pass Rate {pass_rate:.1f}%. Params updated.")
            else:
                summary_logs.append(f"[FAILED] {name}: Failed validation ({pass_rate:.1f}%). Params kept at baseline.")
                
        except Exception as e:
            print(f"  Error optimizing {strat_key}: {e}")
            summary_logs.append(f"[WARN] {name}: Error during optimization.")

    # Save back to YAML
    with open(config_path, "w") as f:
        yaml_handler.dump(strat_data, f)
        
    print("\n" + "="*40)
    print(" AUTO-OPTIMIZATION COMPLETE")
    print("="*40)
    for log in summary_logs:
        print(log)
        
    # Append to automation summary file if it exists
    summary_file = "DAILY_AUTOMATION_SUMMARY.md"
    with open(summary_file, "a") as f:
        f.write(f"\n### AUTO-OPTIMIZATION SYNC ({datetime.now().strftime('%Y-%m-%d %H:%M')})\n")
        for log in summary_logs:
            f.write(f"- {log}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick", action="store_true", help="Run quick optimization (1 strat, 2 windows)")
    args = parser.parse_args()
    
    auto_optimize(quick_mode=args.quick)
