import sys
import yaml
from pathlib import Path

# Setup root path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.backtest.run_backtest import run_backtest

def run_active_suite():
    config_path = PROJECT_ROOT / "config" / "config.yaml"
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    active_strategies = config.get("strategies", [])
    
    print(f"--- Starting Active Strategy Suite Rerun ---")
    print(f"Found {len(active_strategies)} active strategies.")
    
    results = {}
    
    for strat in active_strategies:
        name = strat.get("name")
        enabled = strat.get("enabled", False)
        if not enabled:
            continue
            
        pairs = strat.get("pairs", [])
        timeframes = strat.get("timeframes", [])
        
        print(f"\n>> Strategy: {name}")
        
        for pair in pairs:
            for tf in timeframes:
                print(f"   - Testing {pair} {tf}...")
                try:
                    stats = run_backtest(name, pair, tf)
                    if stats:
                        results[f"{name}_{pair}_{tf}"] = stats
                except Exception as e:
                    print(f"   [ERROR] {name} on {pair} {tf}: {e}")

    print("\n--- Suite Completion Summary ---")
    for key, stats in results.items():
        print(f"{key}: Sharpe={stats.get('sharpe', 0):.2f}, WinRate={stats.get('win_rate', 0)*100:.1f}%")

if __name__ == "__main__":
    run_active_suite()
