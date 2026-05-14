"""
scripts/backtest/run_seasonal_waves.py
======================================
Runs seasonal backtests on active Tier-1 strategies across 3-month (Quarterly) 
and 6-month (Bi-annual) waves.

This script helps identify seasonality by testing standard parameter combos 
over specific calendar periods to see if performance varies by time of year.

Outputs:
  - results/seasonal/YYYYMMDD_seasonal_waves.json
  - results/seasonal/YYYYMMDD_seasonal_waves.md
"""

import sys
import os
import argparse
import json
from datetime import datetime, date
from pathlib import Path
from multiprocessing import Pool, cpu_count
import pandas as pd
import yaml

# ── project root on path ─────────────────────────────────────────────────────
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from data.db_client import DBClient
from backtesting.engine import BacktestEngine
from backtesting.metrics import BacktestMetrics

# Strategy map (We import the ones we might test)
from scripts.backtest.run_overnight_backtest import STRATEGY_MAP, load_data

MIN_WIN_RATE = 70.0
MIN_SHARPE = 2.0

def get_waves(start_year=2023, end_year=None):
    """
    Generates 3-month (Quarterly) and 6-month (Bi-annual) date ranges.
    Returns a list of dicts: {"name": str, "type": "3M"|"6M", "start": pd.Timestamp, "end": pd.Timestamp}
    """
    if end_year is None:
        end_year = date.today().year

    waves = []
    for year in range(start_year, end_year + 1):
        # 3-Month Waves (Quarters)
        waves.append({"name": f"{year}-Q1", "type": "3M", "start": pd.Timestamp(f"{year}-01-01"), "end": pd.Timestamp(f"{year}-03-31 23:59:59")})
        waves.append({"name": f"{year}-Q2", "type": "3M", "start": pd.Timestamp(f"{year}-04-01"), "end": pd.Timestamp(f"{year}-06-30 23:59:59")})
        waves.append({"name": f"{year}-Q3", "type": "3M", "start": pd.Timestamp(f"{year}-07-01"), "end": pd.Timestamp(f"{year}-09-30 23:59:59")})
        waves.append({"name": f"{year}-Q4", "type": "3M", "start": pd.Timestamp(f"{year}-10-01"), "end": pd.Timestamp(f"{year}-12-31 23:59:59")})
        
        # 6-Month Waves (Halves)
        waves.append({"name": f"{year}-H1", "type": "6M", "start": pd.Timestamp(f"{year}-01-01"), "end": pd.Timestamp(f"{year}-06-30 23:59:59")})
        waves.append({"name": f"{year}-H2", "type": "6M", "start": pd.Timestamp(f"{year}-07-01"), "end": pd.Timestamp(f"{year}-12-31 23:59:59")})
        
    return waves

def worker(args_tuple):
    strat_name, strat_class, pair, timeframe, df_slice, params, initial_balance, lot_size, wave_info = args_tuple
    
    try:
        if df_slice is None or len(df_slice) < 50:
            return {"strategy": strat_name, "pair": pair, "timeframe": timeframe, "wave_name": wave_info["name"], "wave_type": wave_info["type"], "status": "NO_TRADES"}

        strategy_instance = strat_class(params=params)
        bt = BacktestEngine(initial_balance=initial_balance, lot_size=lot_size)
        os.environ["RUNNING_MODE"] = "BACKTEST"
        
        trades_df, signals_df = bt.run(strategy_instance, pair, timeframe, df_slice, silent=True)

        if trades_df is None or trades_df.empty:
            return {"strategy": strat_name, "pair": pair, "timeframe": timeframe, "wave_name": wave_info["name"], "wave_type": wave_info["type"], "status": "NO_TRADES"}

        metrics = BacktestMetrics(signals_df, trades_df, initial_balance)
        stats = metrics.calculate_all()
        
        return {
            "strategy": strat_name,
            "pair": pair,
            "timeframe": timeframe,
            "wave_name": wave_info["name"],
            "wave_type": wave_info["type"],
            "status": "PASS" if (stats.get("win_rate", 0) >= MIN_WIN_RATE and stats.get("sharpe_ratio", 0) >= MIN_SHARPE) else "REVIEW",
            "win_rate": stats.get("win_rate", 0),
            "sharpe_ratio": stats.get("sharpe_ratio", 0),
            "profit_factor": stats.get("profit_factor", 0),
            "max_drawdown_pct": stats.get("max_drawdown_pct", 0),
            "total_trades": stats.get("total_trades", 0),
            "total_pnl": stats.get("total_pnl", 0)
        }
    except Exception as e:
        return {"strategy": strat_name, "pair": pair, "timeframe": timeframe, "wave_name": wave_info["name"], "wave_type": wave_info["type"], "status": "ERROR", "reason": str(e)}

def save_report(results, out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = date.today().strftime("%Y%m%d")
    
    # Save JSON
    json_path = out_dir / f"{stamp}_seasonal_waves.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({"generated": str(datetime.now()), "results": results}, f, indent=2, default=str)
        
    # Save MD
    md_path = out_dir / f"{stamp}_seasonal_waves.md"
    lines = [
        f"# Seasonal Waves Backtest Report — {date.today().strftime('%d %B %Y')}",
        f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}",
        f"This report compares strategy performance across 3-month and 6-month windows.",
        "\n"
    ]
    
    # Group results by Strategy + Pair + TF
    grouped = {}
    for r in results:
        if r.get("status") in ("ERROR", "SKIP", "NO_TRADES"):
            continue
        key = f"{r['strategy']} | {r['pair']} | {r['timeframe']}"
        if key not in grouped: grouped[key] = []
        grouped[key].append(r)
        
    # Sort groups by best average win_rate
    def get_avg_wr(res_list):
        if not res_list: return 0
        return sum(x.get("win_rate", 0) for x in res_list) / len(res_list)
        
    sorted_groups = sorted(grouped.items(), key=lambda x: -get_avg_wr(x[1]))
    
    for key, res_list in sorted_groups:
        lines.append(f"## {key}")
        lines.append(f"| Wave | Type | Status | WR% | Sharpe | PF | MaxDD% | Trades |")
        lines.append(f"|---|---|---|---|---|---|---|---|")
        
        # Sort chronologically by wave name
        res_list.sort(key=lambda x: x["wave_name"])
        
        for r in res_list:
            status_icon = "✅" if r['status'] == "PASS" else "⚠️"
            lines.append(
                f"| {r['wave_name']} | {r['wave_type']} | {status_icon} "
                f"| {r.get('win_rate',0):.1f} | {r.get('sharpe_ratio',0):.2f} "
                f"| {r.get('profit_factor',0):.2f} | {r.get('max_drawdown_pct',0):.1f} "
                f"| {r.get('total_trades',0)} |"
            )
        lines.append("\n---\n")

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
        
    return json_path, md_path

def load_seasonal_data(db, pair, timeframe, start_year):
    rows = db.execute_query(
        "SELECT timestamp, open, high, low, close, tick_volume FROM market_data "
        "WHERE pair = %s AND timeframe = %s AND timestamp >= %s ORDER BY timestamp",
        (pair, timeframe, f"{start_year}-01-01")
    )
    if not rows:
        return None
    df = pd.DataFrame(rows, columns=["timestamp", "open", "high", "low", "close", "tick_volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df.set_index("timestamp", inplace=True)
    for col in ["open", "high", "low", "close", "tick_volume"]:
        df[col] = df[col].astype(float)
    return df

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/strategies.yaml")
    parser.add_argument("--start_year", type=int, default=2024)
    parser.add_argument("--balance", type=float, default=10000.0)
    parser.add_argument("--lot", type=float, default=0.1)
    args = parser.parse_args()

    db = DBClient()
    
    with open(args.config, 'r') as f:
        full_config = yaml.safe_load(f)
        
    active_strategies = full_config.get("active", [])
    tier1_strats = [s for s in active_strategies if full_config.get(s, {}).get("tier") == "TIER_1"]
    
    waves = get_waves(start_year=args.start_year)
    
    tasks = []
    data_cache = {}
    
    print(f"Preparing seasonal tasks for {len(tier1_strats)} Tier 1 strategies across {len(waves)} waves...")
    
    for strat_name in tier1_strats:
        if strat_name not in STRATEGY_MAP: continue
        strat_class, _ = STRATEGY_MAP[strat_name]
        strat_conf = full_config[strat_name]
        
        pairs = strat_conf.get("pairs", [])
        timeframes = strat_conf.get("timeframes", [])
        if isinstance(timeframes, str): timeframes = [timeframes]
            
        for pair in pairs:
            for tf in timeframes:
                cache_key = (pair, tf)
                if cache_key not in data_cache:
                    df = load_seasonal_data(db, pair, tf, args.start_year)
                    data_cache[cache_key] = df
                    
                df = data_cache[cache_key]
                if df is None or df.empty: continue
                
                params = strat_conf.get("parameters", {}).copy()
                overrides = strat_conf.get("pair_overrides", {})
                if pair in overrides: params.update(overrides[pair])
                if f"{pair}:{tf}" in overrides: params.update(overrides[f"{pair}:{tf}"])
                if not params.get("enabled", True): continue
                    
                for wave in waves:
                    # Slice data for the wave
                    df_slice = df[(df.index >= wave["start"]) & (df.index <= wave["end"])]
                    if len(df_slice) > 50:
                        tasks.append((strat_name, strat_class, pair, tf, df_slice, params, args.balance, args.lot, wave))

    num_cores = min(cpu_count() - 1, 8) if cpu_count() > 1 else 1
    print(f"Launching {len(tasks)} seasonal wave backtests across {num_cores} cores...")
    
    with Pool(processes=num_cores) as pool:
        results = pool.map(worker, tasks)
        
    out_dir = Path(__file__).parent.parent.parent / "results" / "seasonal"
    json_path, md_path = save_report(results, out_dir)
    
    print(f"\nSeasonal Wave Backtest Complete!")
    print(f"JSON: {json_path}")
    print(f"MD: {md_path}")

if __name__ == "__main__":
    main()
