import os
import subprocess
import time
import pandas as pd
from datetime import datetime

# Focused Configuration - Priority Pairs: BTCUSD, ETHUSD, XAUUSD, USDJPY, EURUSD
# Only Tier 1/2 passing strategies + Tier 3 upgrade targets
STRATEGIES = [
    # Tier 1 (High Priority WR Push)
    ("stat_arb_gold_silver", "XAUUSD", "H4"),
    ("range_breakout", "XAUUSD", "H4"),
    ("ema_ribbon_trend", "BTCUSD", "H4"),
    ("bb_mean_reversion", "XAUUSD", "H1"),
    
    # Tier 2 (Stability Push)
    ("stoch_divergence", "EURUSD", "H4"),
    ("rsi_pullback", "XAUUSD", "H4"),
    ("session_momentum", "XAUUSD", "H1"),
    ("hikkake_trap", "XAUUSD", "H4"),
    
    # Tier 3 Upgrade Targets (Logic Enhanced version)
    ("ict_judas_swing", "XAUUSD", "H1"),
    ("ict_judas_swing", "EURUSD", "H1"),
    ("ict_judas_swing", "USDJPY", "H1"),
    
    ("rsi_2", "BTCUSD", "M15"),
    ("rsi_2", "ETHUSD", "M15"),
    ("rsi_2", "USDJPY", "M15"),
    ("rsi_2", "EURUSD", "M15"),
    
    ("ema_ribbon_trend", "ETHUSD", "H4"), # New pair for BTC-heavy strategy
]

N_WINDOWS = 8
IS_PCT = 0.70
OOS_PCT = 0.20

def run_strategy_wfo(name, pair, tf):
    print(f"\n{'='*60}")
    print(f"RUNNING REFINED WFO: {name} on {pair} ({tf})")
    print(f"{'='*60}")
    
    cmd = [
        "python", "scripts/run_walk_forward.py",
        "--strategy", name,
        "--pair", pair,
        "--timeframe", tf,
        "--n_windows", str(N_WINDOWS),
        "--is_pct", str(IS_PCT),
        "--oos_pct", str(OOS_PCT)
    ]
    
    try:
        # 45 min timeout to keep suite moving
        subprocess.run(cmd, check=True, timeout=2700)
    except subprocess.TimeoutExpired:
        print(f"  [!] WFO TIMEOUT for {name} on {pair}")
    except Exception as e:
        print(f"  [!] Error running WFO for {name} on {pair}: {e}")

def main():
    print(f"PHASE 2 (REFINED): FOCUSED WALK-FORWARD OPTIMIZATION")
    print(f"Start Time: {datetime.now()}")
    print(f"Targeting WR >= 60% across BTC, ETH, XAU, JPY, EUR")
    print(f"Total Sequences: {len(STRATEGIES)}")
    
    start_time = time.time()
    
    for i, (name, pair, tf) in enumerate(STRATEGIES):
        progress = (i / len(STRATEGIES)) * 100
        print(f"\nProgress: {progress:.1f}% ({i}/{len(STRATEGIES)})")
        run_strategy_wfo(name, pair, tf)
        
    end_time = time.time()
    duration = (end_time - start_time) / 3600
    print(f"\n{'='*60}")
    print(f"PHASE 2 REFINED WFO COMPLETE")
    print(f"Total Duration: {duration:.2f} hours")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
