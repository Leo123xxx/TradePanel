import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import argparse
import pandas as pd
from data.db_client import DBClient
from backtesting.walk_forward import WalkForwardOptimizer

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
from strategies.cot_sentiment import COTSentimentStrategy
from strategies.ensemble import EnsembleStrategy

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
    "institutional_silver_bullet":  InstitutionalSilverBullet,
    "ict_judas_swing":              ICTJudasSwing,
    "turtle_soup":                  TurtleSoup,
    "dual_ema_momentum":            DualEMAMomentum,
    "triple_macd_scalping":         TripleMACDScalping,
    "dual_ema_fractal":             DualEMAFractal,
    "rsi_2":                        RSITwoStrategy,
    "vwap_momentum":                VWAPMomentum,
    "hikkake_trap":                 HikkakeTrap,
    "orb":                          ORBStrategy,
    "rvgi_cci_confluence":          RVGICCIConfluence,
    "volatility_contraction":       VolatilityContraction,
    "stat_arb_gold_silver":         StatArbGoldSilver,
    "naked_price_action":           NakedPriceAction,
    "cot_sentiment":                COTSentimentStrategy,
    "ensemble":                     EnsembleStrategy,
}

def run_wf(strategy_name, symbol, timeframe, is_pct, oos_pct, n_windows, limit=0):
    db = DBClient()
    
    print(f"Fetching data for {symbol} {timeframe}...", flush=True)
    query = "SELECT timestamp, open, high, low, close, tick_volume FROM market_data WHERE pair = %s AND timeframe = %s"
    if limit > 0:
        query += f" ORDER BY timestamp DESC LIMIT {limit}"
        rows = db.execute_query(query, (symbol, timeframe))
        rows.reverse() # Restore chronological order
    else:
        query += " ORDER BY timestamp"
        rows = db.execute_query(query, (symbol, timeframe))
    
    if not rows:
        print(f"Error: No data found for {symbol} {timeframe}. Did you run the data feed?")
        return

    df = pd.DataFrame(rows, columns=['timestamp', 'open', 'high', 'low', 'close', 'tick_volume'])
    df.set_index('timestamp', inplace=True)
    
    numeric_cols = ['open', 'high', 'low', 'close', 'tick_volume']
    for col in numeric_cols:
        df[col] = df[col].astype(float)
        
    wf = WalkForwardOptimizer(db)
    
    results = wf.run(
        strategy_key=strategy_name,
        symbol=symbol,
        timeframe=timeframe,
        df=df,
        is_pct=is_pct,
        oos_pct=oos_pct,
        n_windows=n_windows
    )
    
    print("\n" + "="*40)
    print("      WALK-FORWARD PERFORMANCE SUMMARY")
    print("="*40)
    profitable_windows = 0
    total_oos_pnl = 0
    
    for res in results:
        pnl = res.get('oos_profit_factor', 0) # Just checking if it made money basically, Sharpe is better. Wait, we display PF.
        status = "PASS" if res.get('oos_sharpe', 0) >= 1.0 else "FAIL"
        if res.get('oos_sharpe', 0) >= 1.0: profitable_windows += 1
        
        print(f"Window {res['window_index']}: {status}", flush=True)
        print(f"  Sharpe: {res.get('oos_sharpe', 0):6.2f} | PF: {res.get('oos_profit_factor', 0):6.2f}", flush=True)
        print(f"  Best params: {res['best_params']}", flush=True)
        print("-" * 30, flush=True)
    
    pass_rate = (profitable_windows / len(results)) * 100 if results else 0
    print(f"Pass Rate: {pass_rate:.1f}% ({profitable_windows}/{len(results)}) based on Sharpe >= 1.0", flush=True)
    
    if pass_rate >= 70:
        print("\nRESULT: STRATEGY PASSES WALK-FORWARD VALIDATION")
    else:
        print("\nRESULT: STRATEGY FAILS WALK-FORWARD VALIDATION")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run walk-forward optimization.")
    parser.add_argument("--strategy", type=str, required=True, help="Strategy name")
    parser.add_argument("--pair", type=str, default="XAUUSD", help="Trading pair")
    parser.add_argument("--timeframe", type=str, default="H4", help="Timeframe (e.g. H1, H4)")
    parser.add_argument("--is_pct", type=float, default=0.70, help="In-sample fraction")
    parser.add_argument("--oos_pct", type=float, default=0.20, help="Out-of-sample fraction")
    parser.add_argument("--n_windows", type=int, default=5, help="Number of rolling windows")
    parser.add_argument("--limit", type=int, default=0, help="Limit number of rows")
    
    args = parser.parse_args()
    run_wf(args.strategy, args.pair, args.timeframe, args.is_pct, args.oos_pct, args.n_windows, args.limit)
