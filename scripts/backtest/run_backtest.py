import sys
import argparse
import pandas as pd
import yaml
from pathlib import Path

# Setup root path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.lib.logger import setup_logger
from data.db_client import DBClient
from scripts.lib.config_loader import load_strategies
from backtesting.engine import BacktestEngine
from backtesting.metrics import BacktestMetrics
from backtesting.report import StatsReport

from strategies.registry import registry as STRATEGY_REGISTRY

def run_backtest(strategy_name: str, symbol: str, timeframe: str,
                 lot_size: float = 0.1, initial_balance: float = 10_000.0,
                 use_cache: bool = True):
    logger = setup_logger("backtest", "backtest.json.log")
    logger.info(f"V3 Backtest Starting: {strategy_name} on {symbol} {timeframe}", 
                extra={"metrics": {"strategy": strategy_name, "symbol": symbol, "tf": timeframe}})

    # ── 1. Load Data (Performance Tuning: Parquet Cache) ─────────────────────
    data = None
    cache_file = PROJECT_ROOT / "results" / "data" / "cache" / f"{symbol}_{timeframe}.parquet"
    
    if use_cache and cache_file.exists():
        logger.info(f"Loading data from Parquet cache: {cache_file.name}")
        data = pd.read_parquet(cache_file)
        data.set_index('timestamp', inplace=True)
    else:
        logger.info(f"Fetching data from Database for {symbol} {timeframe}...")
        db = DBClient()
        rows = db.execute_query(
            "SELECT timestamp, open, high, low, close, tick_volume FROM market_data "
            "WHERE pair = %s AND timeframe = %s ORDER BY timestamp",
            (symbol, timeframe)
        )
        
        if not rows:
            logger.error(f"No data found for {symbol} {timeframe}")
            return
            
        data = pd.DataFrame(rows, columns=['timestamp', 'open', 'high', 'low', 'close', 'tick_volume'])
        data['timestamp'] = pd.to_datetime(data['timestamp'])
        data.set_index('timestamp', inplace=True)

    # Cast types
    for col in ['open', 'high', 'low', 'close', 'tick_volume']:
        data[col] = data[col].astype(float)
        
    logger.info(f"Loaded {len(data)} bars")

    # ── 2. Run Backtest ──────────────────────────────────────────────────────
    strat_configs = load_strategies()
    params = strat_configs.get(strategy_name, {}).get("parameters", {})
    
    if strategy_name not in STRATEGY_REGISTRY.strategies:
        logger.error(f"Strategy {strategy_name} not found in map.")
        return

    strategy_instance = STRATEGY_REGISTRY.strategies[strategy_name](params=params)
    bt = BacktestEngine(initial_balance=initial_balance, lot_size=lot_size)
    
    trades_df, signals_df = bt.run(
        strategy=strategy_instance,
        symbol=symbol,
        timeframe=timeframe,
        data_df=data
    )
    
    # ── 3. Metrics & Reporting ───────────────────────────────────────────────
    if trades_df is not None and not trades_df.empty:
        metrics_calculator = BacktestMetrics(signals_df, trades_df, initial_balance)
        stats = metrics_calculator.calculate_all()
        
        # Log results for Loki/Grafana
        logger.info("Backtest Complete", extra={"metrics": {
            "win_rate": float(stats.get("win_rate", 0)),
            "sharpe": float(stats.get("sharpe", 0)),
            "trades": int(stats.get("trades", 0)),
            "profit": float(stats.get("net_pnl", 0))
        }})
        
        report = StatsReport()
        report.generate_scorecard(stats)
        return stats
    else:
        logger.warning("No trades executed during backtest.")
        return None

def main():
    parser = argparse.ArgumentParser(description="V3 Modular Backtester")
    parser.add_argument("--strategy", type=str, required=True)
    parser.add_argument("--pair", type=str, default="XAUUSD")
    parser.add_argument("--timeframe", type=str, default="H1")
    parser.add_argument("--lot_size", type=float, default=0.1)
    parser.add_argument("--balance", type=float, default=10000.0)
    parser.add_argument("--no-cache", action="store_false", dest="use_cache")

    args = parser.parse_args()
    run_backtest(args.strategy, args.pair, args.timeframe, args.lot_size, args.balance, args.use_cache)

if __name__ == "__main__":
    main()
