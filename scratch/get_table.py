import os
import sys

# Ensure this path is correct based on where it's executed
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.db_client import DBClient

def get_baseline_results():
    db = DBClient()
    query = """
        SELECT s.name, r.pair, r.timeframe, r.metrics
        FROM backtest_runs r
        JOIN strategies s ON r.strategy_id = s.strategy_id
        ORDER BY r.run_id ASC
    """
    rows = db.execute_query(query)
    
    print("| Strategy | Pair | TF | Trades | Win% | Profit Factor | Sharpe | Max DD% |")
    print("|----------|------|----|--------|------|---------------|--------|---------|")
    
    # We want to format the strategy names correctly like in the document
    name_map = {
        "MA_Crossover": "MA Crossover",
        "Range_Breakout": "Range Breakout",
        "RSI_Pullback": "RSI Pullback",
        "BB_Mean_Reversion": "BB Mean Reversion",
        "Swing_Pullback": "Swing Pullback",
        "Session_Momentum": "Session Momentum",
        "Stoch_Divergence": "Stoch Divergence",
    }
    
    # Just show the latest run for each strategy/pair/tf combo to avoid duplicates
    seen = set()
    # Reverse so we see latest runs first, but we want the original order of the 7 strategies...
    # Let's map dynamically
    for row in reversed(rows):
        strat = row[0]
        pair = row[1]
        tf = row[2]
        
        key = f"{strat}_{pair}_{tf}"
        if key in seen:
            continue
        seen.add(key)
        
        display_name = name_map.get(strat, strat)
        
        trades = row[3].get("total_trades", 0) if isinstance(row[3], dict) else 0
        win_rate = row[3].get("win_rate", 0.0) if isinstance(row[3], dict) else 0.0
        pf = row[3].get("profit_factor", 0.0) if isinstance(row[3], dict) else 0.0
        sharpe = row[3].get("sharpe_ratio", 0.0) if isinstance(row[3], dict) else 0.0
        max_dd = row[3].get("max_drawdown_pct", 0.0) if isinstance(row[3], dict) else 0.0
        
        print(f"| {display_name} | {pair} | {tf} | {trades} | {win_rate:.2f} | {pf:.2f} | {sharpe:.2f} | {max_dd:.2f} |")

if __name__ == "__main__":
    get_baseline_results()
