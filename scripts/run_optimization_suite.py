import sys
import os
import json

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.optimize import optimize

def run_suite():
    all_best = {}
    
    # 1. OPTIMIZE: Institutional Silver Bullet
    # Strong potential, currently 0.99 PF
    sb_grid = {
        "lookback_sweep": [10, 20, 30, 50],
        "risk_reward": [1.5, 2.0, 2.5, 3.0, 4.0],
    }
    all_best["institutional_silver_bullet"] = optimize("institutional_silver_bullet", "XAUUSD", "M15", sb_grid)
    
    # 2. OPTIMIZE: Swing Pullback
    # Failed baseline at 0.98 PF
    sp_grid = {
        "swing_lookback": [3, 5, 8],
        "tp_pips": [100, 150, 200, 300],
        "sl_pips": [30, 50, 70, 100],
    }
    all_best["swing_pullback"] = optimize("swing_pullback", "XAUUSD", "H4", sp_grid)
    
    # 3. OPTIMIZE: Dual EMA Momentum
    # Close at 0.96 PF
    dem_grid = {
        "fast_ema": [13, 20, 34],
        "slow_ema": [50, 89, 144],
        "tp_atr_mult": [2.0, 3.0, 4.0],
    }
    all_best["dual_ema_momentum"] = optimize("dual_ema_momentum", "BTCUSD", "H4", dem_grid)

    # 4. OPTIMIZE: Volatility Contraction
    # PF 0.86
    vc_grid = {
        "range_bars": [5, 10, 15],
        "tp_atr_mult": [2.0, 3.0, 5.0],
        "vol_spike": [1.2, 1.5, 2.0]
    }
    all_best["volatility_contraction"] = optimize("volatility_contraction", "USDJPY", "H4", vc_grid)

    # Save results
    results_path = "results/optimized_params.json"
    os.makedirs("results", exist_ok=True)
    with open(results_path, "w") as f:
        # We only want the serializable part
        serializable = {k: v for k, v in all_best.items() if v}
        json.dump(serializable, f, indent=4)

    print("\n" + "="*60)
    print(f"OPTIMIZATION SUITE COMPLETE. Results saved to: {results_path}")
    print("="*60)

if __name__ == "__main__":
    run_suite()
