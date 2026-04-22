import sys
import os
import pandas as pd
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.run_backtest import run_backtest

from scripts.run_backtest import run_backtest, STRATEGY_MAP

# Define default symbol/TF mappings for strategies
# This ensures we test each strategy on its intended market
STRAT_DEFAULTS = {
    # Metals
    "gold_momentum_breakout": ("XAUUSD", "H1"),
    "stat_arb_gold_silver": ("XAUUSD", "H4"),
    "range_breakout": ("XAUUSD", "H4"),
    "rsi_pullback": ("XAUUSD", "H4"),
    "swing_pullback": ("XAUUSD", "H4"),
    "rsi_bounce": ("XAUUSD", "H1"),
    "session_momentum": ("XAUUSD", "H1"),
    "triple_macd_scalping": ("XAUUSD", "M15"),
    
    # Forex
    "ma_crossover": ("EURUSD", "H1"),
    "macd_trend": ("GBPUSD", "H1"),
    "stoch_divergence": ("EURUSD", "H4"),
    "dual_ema_momentum": ("EURUSD", "H1"),
    "dual_ema_fractal": ("EURUSD", "H1"),
    "naked_price_action": ("GBPUSD", "H4"),
    
    # Crypto
    "ema_ribbon_trend": ("BTCUSD", "H4"),
    "crypto_rsi_extremes": ("BTCUSD", "H4"),
    "volatility_squeeze_breakout": ("BTCUSD", "H1"),
    "rsi_2": ("BTCUSD", "M15"),
    "vwap_momentum": ("ETHUSD", "M15"),
    
    # Institutional / SMC
    "institutional_silver_bullet": ("XAUUSD", "M15"),
    "ict_judas_swing": ("XAUUSD", "H1"),
    "turtle_soup": ("XAUUSD", "H1"),
    "orb": ("XAUUSD", "M15"),
    "hikkake_trap": ("XAUUSD", "H4"),
}

# Dynamically build the TEST_SUITE for all 28 strategies
TEST_SUITE = []
for strat_name in STRATEGY_MAP.keys():
    pair, tf = STRAT_DEFAULTS.get(strat_name, ("XAUUSD", "H1")) # Defaults to XAU H1
    TEST_SUITE.append({"strategy": strat_name, "pair": pair, "tf": tf})

def run_phase_1a():
    print("="*60)
    print("STARTING PHASE 1A: STRATEGY VALIDATION SUITE")
    print("="*60)
    
    results = []
    
    for test in TEST_SUITE:
        strat = test["strategy"]
        pair = test["pair"]
        tf = test["tf"]
        
        print(f"\n[RUNNING] {strat} on {pair} ({tf})...")
        try:
            metrics = run_backtest(strat, pair, tf)
            
            if metrics and "error" not in metrics:
                results.append({
                    "Strategy": strat,
                    "Pair": pair,
                    "TF": tf,
                    "Trades": metrics.get("total_trades", 0),
                    "Win Rate": f"{metrics.get('win_rate', 0):.2f}%",
                    "PF": f"{metrics.get('profit_factor', 0):.2f}",
                    "Sharpe": f"{metrics.get('sharpe_ratio', 0):.2f}",
                    "Status": "PASS" if metrics.get('profit_factor', 0) > 1.0 else "FAIL"
                })
            else:
                results.append({
                    "Strategy": strat, "Pair": pair, "TF": tf,
                    "Trades": 0, "Win Rate": "N/A", "PF": "N/A", "Sharpe": "N/A", "Status": "ERROR"
                })
        except Exception as e:
            print(f"  [!] Exception: {e}")
            results.append({
                "Strategy": strat, "Pair": pair, "TF": tf,
                "Trades": 0, "Win Rate": "N/A", "PF": "N/A", "Sharpe": "N/A", "Status": "CRASH"
            })

    # Generate Report
    report_path = "results/tier_assignment_existing_10.md"
    os.makedirs("results", exist_ok=True)
    
    with open(report_path, "w") as f:
        f.write("# Phase 1A: Existing Strategy Validation Report\n\n")
        f.write(f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Manual Table
        headers = ["Strategy", "Pair", "TF", "Trades", "Win Rate", "PF", "Sharpe", "Status"]
        f.write("| " + " | ".join(headers) + " |\n")
        f.write("| " + " | ".join(["---"] * len(headers)) + " |\n")
        for res in results:
            row = [str(res.get(h, "")) for h in headers]
            f.write("| " + " | ".join(row) + " |\n")
        
        f.write("\n\n---\n*Note: Status PASS indicates PF > 1.0. Final Tier Assignment will be based on WR and Sharpe.*")

    print("\n" + "="*60)
    print(f"PHASE 1A COMPLETE. Report saved to: {report_path}")
    print("="*60)

if __name__ == "__main__":
    run_phase_1a()
