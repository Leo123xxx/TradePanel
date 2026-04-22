import sys
import os
import pandas as pd
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.run_backtest import run_backtest

# Phase 1B Test Suite
TEST_SUITE = [
    # Group 1: Institutional Flow
    {"strategy": "institutional_silver_bullet", "pair": "XAUUSD", "tf": "M15"},
    {"strategy": "ict_judas_swing",             "pair": "GBPUSD", "tf": "M15"},
    {"strategy": "turtle_soup",                 "pair": "XAUUSD", "tf": "H1"},
    
    # Group 2: Trend Following
    {"strategy": "dual_ema_momentum",           "pair": "BTCUSD", "tf": "H4"},
    {"strategy": "triple_macd_scalping",        "pair": "XAUUSD", "tf": "M5"},
    {"strategy": "dual_ema_fractal",            "pair": "EURUSD", "tf": "H1"},
    
    # Group 3: Mean Reversion
    {"strategy": "rsi_2",                       "pair": "EURUSD", "tf": "H4"},
    {"strategy": "vwap_momentum",               "pair": "ETHUSD", "tf": "M15"},
    {"strategy": "hikkake_trap",                "pair": "BTCUSD", "tf": "H4"},
    
    # Group 4: Breakout
    {"strategy": "orb",                         "pair": "GBPUSD", "tf": "M15"},
    {"strategy": "rvgi_cci_confluence",         "pair": "USDJPY", "tf": "H1"},
    {"strategy": "volatility_contraction",      "pair": "USDJPY", "tf": "H4"},
    
    # Group 5: Advanced
    {"strategy": "stat_arb_gold_silver",        "pair": "XAUUSD", "tf": "H4"},
    {"strategy": "naked_price_action",          "pair": "EURUSD", "tf": "D1"},
    {"strategy": "cot_sentiment",               "pair": "XAUUSD", "tf": "D1"},
]

def run_phase_1b():
    print("="*60)
    print("STARTING PHASE 1B: LEODEX V2 STRATEGY VALIDATION SUITE")
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
    report_path = "results/phase_1b_validation_report.md"
    os.makedirs("results", exist_ok=True)
    
    with open(report_path, "w") as f:
        f.write("# Phase 1B: LeoDeX V2 Strategy Validation Report\n\n")
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
    print(f"PHASE 1B COMPLETE. Report saved to: {report_path}")
    print("="*60)

if __name__ == "__main__":
    run_phase_1b()
