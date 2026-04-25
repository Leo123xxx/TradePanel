"""
scripts/run_backtest.py — CLI entry point for the backtesting engine.

Usage:
    python scripts/run_backtest.py --strategy ma_crossover --pair XAUUSD --timeframe H1
    python scripts/run_backtest.py --strategy rsi_bounce --pair EURUSD --timeframe H4
    python scripts/run_backtest.py --strategy macd_trend --pair GBPUSD --timeframe D1

Optional flags:
    --lot_size   float  Default 0.1
    --balance    float  Starting balance in USD. Default 10000.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import argparse
import pandas as pd
from data.db_client import DBClient
from backtesting.engine import BacktestEngine
from backtesting.metrics import BacktestMetrics
from backtesting.report import StatsReport
from strategies.ma_crossover import MACrossoverStrategy
from strategies.rsi_bounce import RSIBounceStrategy
from strategies.gold_momentum_breakout import GoldMomentumBreakoutStrategy
from strategies.macd_trend import MACDTrendStrategy
from strategies.range_breakout import RangeBreakoutStrategy
from strategies.rsi_pullback import RSIPullbackStrategy
from strategies.bb_mean_reversion import BBMeanReversionStrategy
from strategies.swing_pullback import SwingPullbackStrategy
from strategies.session_momentum import SessionMomentumStrategy
from strategies.stoch_divergence import StochDivergenceStrategy
from strategies.ema_ribbon_trend import EMARibbonTrendStrategy
from strategies.crypto_rsi_extremes import CryptoRSIExtremesStrategy
from strategies.volatility_squeeze_breakout import VolatilitySqueezeBreakoutStrategy
from strategies.institutional_silver_bullet import InstitutionalSilverBullet
from strategies.ict_judas_swing import ICTJudasSwing
from strategies.turtle_soup import TurtleSoup
from strategies.dual_ema_momentum import DualEMAMomentum
from strategies.triple_macd_scalping import TripleMACDScalping
from strategies.dual_ema_fractal import DualEMAFractal
from strategies.rsi_2 import RSITwoStrategy
from strategies.vwap_momentum import VWAPMomentum
from strategies.hikkake_trap import HikkakeTrap
from strategies.orb import ORBStrategy
from strategies.rvgi_cci_confluence import RVGICCIConfluence
from strategies.volatility_contraction import VolatilityContraction
from strategies.stat_arb_gold_silver import StatArbGoldSilver
from strategies.naked_price_action import NakedPriceAction
from strategies.ensemble import EnsembleStrategy

from strategies.cot_sentiment import COTSentimentStrategy
# NOTE: COT Sentiment RE-ENABLED (2026-04-24)
# CFTC COT data pipeline operational via data/cot_feed.py
# Initial setup: python data/cot_feed.py --history (run once)

STRATEGY_MAP = {
    # Original FX/metals strategies
    "ma_crossover":                 MACrossoverStrategy,
    "rsi_bounce":                   RSIBounceStrategy,
    "gold_momentum_breakout":       GoldMomentumBreakoutStrategy,
    "macd_trend":                   MACDTrendStrategy,
    "range_breakout":               RangeBreakoutStrategy,
    "rsi_pullback":                 RSIPullbackStrategy,
    "bb_mean_reversion":            BBMeanReversionStrategy,
    "swing_pullback":               SwingPullbackStrategy,
    "session_momentum":             SessionMomentumStrategy,
    "stoch_divergence":             StochDivergenceStrategy,
    # New crypto + cross-asset strategies (added 2026-04-18)
    "ema_ribbon_trend":             EMARibbonTrendStrategy,
    "crypto_rsi_extremes":          CryptoRSIExtremesStrategy,
    "volatility_squeeze_breakout":  VolatilitySqueezeBreakoutStrategy,
    # Ensemble strategies (added 2026-04-19 for Path B enhancements)
    "ensemble":                     EnsembleStrategy,
    # Institutional Flow (LeoDeX V2)
    "institutional_silver_bullet":  InstitutionalSilverBullet,
    "ict_judas_swing":              ICTJudasSwing,
    "turtle_soup":                  TurtleSoup,
    # Trend Following (LeoDeX V2)
    "dual_ema_momentum":            DualEMAMomentum,
    "triple_macd_scalping":         TripleMACDScalping,
    "dual_ema_fractal":             DualEMAFractal,
    # Mean Reversion (LeoDeX V2)
    "rsi_2":                        RSITwoStrategy,
    "vwap_momentum":                VWAPMomentum,
    "hikkake_trap":                 HikkakeTrap,
    # Breakout (LeoDeX V2)
    "orb":                          ORBStrategy,
    "rvgi_cci_confluence":          RVGICCIConfluence,
    "volatility_contraction":       VolatilityContraction,
    # Advanced (LeoDeX V2)
    "stat_arb_gold_silver":         StatArbGoldSilver,
    "naked_price_action":           NakedPriceAction,
    "cot_sentiment":            COTSentimentStrategy,
}


def run_backtest(strategy_name: str, symbol: str, timeframe: str,
                 lot_size: float = 0.1, initial_balance: float = 10_000.0):
    db = DBClient()

    # ── 1. Load data from DB ──────────────────────────────────────────────────
    print(f"Loading {symbol} {timeframe} from database...")
    rows = db.execute_query(
        "SELECT timestamp, open, high, low, close, tick_volume FROM market_data "
        "WHERE pair = %s AND timeframe = %s ORDER BY timestamp",
        (symbol, timeframe)
    )
    if not rows:
        print(f"ERROR: No data found for {symbol} {timeframe}")
        return

    data = pd.DataFrame(rows, columns=['timestamp', 'open', 'high', 'low', 'close', 'tick_volume'])
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    data.set_index('timestamp', inplace=True)
    
    # Cast all numeric columns to float (Fix decimal.Decimal vs float issues)
    for col in ['open', 'high', 'low', 'close', 'tick_volume']:
        data[col] = data[col].astype(float)
        
    print(f"  Loaded {len(data)} bars")

    # ── 2. Run backtest ────────────────────────────────────────────────────────
    print(f"\nBacktest Execution: {strategy_name} on {symbol} {timeframe}...")
    
    # Instantiate strategy
    strat_class = STRATEGY_MAP[strategy_name]
    strategy_instance = strat_class()
    
    bt = BacktestEngine(
        initial_balance=initial_balance,
        lot_size=lot_size
    )
    
    # The run() method returns (trades_df, signals_df)
    trades_df, signals_df = bt.run(
        strategy=strategy_instance,
        symbol=symbol,
        timeframe=timeframe,
        data_df=data
    )
    
    # Calculate metrics from trades
    if trades_df is not None and not trades_df.empty:
        metrics_calculator = BacktestMetrics(signals_df, trades_df, initial_balance)
        stats = metrics_calculator.calculate_all()
        print(stats)
    else:
        print("No trades executed during backtest.")
        stats = None

    # ── 3. Print detailed report ───────────────────────────────────────────────
    if stats is not None:
        report = StatsReport()
        report.generate_scorecard(stats)
        
    return stats


def main():
    valid_strategies = " | ".join(sorted(STRATEGY_MAP.keys()))
    parser = argparse.ArgumentParser(description="Backtest a single strategy on a pair/timeframe")
    parser.add_argument("--strategy", type=str, required=True,
                        help=f"Strategy name. Available: {valid_strategies}")
    parser.add_argument("--pair", type=str, default="XAUUSD",
                        help="Trading pair (XAUUSD | EURUSD | GBPUSD | USDJPY | XAGUSD | BTCUSD | ETHUSD)")
    parser.add_argument("--timeframe", type=str, default="H1",
                        help="Timeframe (M1 | M5 | M15 | H1 | H4 | D1)")
    parser.add_argument("--lot_size", type=float, default=0.1,
                        help="Lot size per trade (default 0.1)")
    parser.add_argument("--balance", type=float, default=10_000.0,
                        help="Starting balance in USD (default 10000)")

    args = parser.parse_args()
    run_backtest(args.strategy, args.pair, args.timeframe, args.lot_size, args.balance)


if __name__ == "__main__":
    main()
