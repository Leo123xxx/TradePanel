import os
import sys
import subprocess
import time
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def print_banner(text):
    print("\n" + "="*80)
    print(f" {text.center(78)}")
    print("="*80)

def run_script(script_path, args=[]):
    print(f"Running: {script_path} {' '.join(args)}...")
    env = os.environ.copy()
    env["PYTHONPATH"] = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + os.pathsep + env.get("PYTHONPATH", "")
    cmd = [sys.executable, script_path] + args
    # Use capture_output=False to see real-time streaming to stdout
    result = subprocess.run(cmd, capture_output=False, env=env)
    if result.returncode == 0:
        print(f"Success: {script_path}")
        return True, "Success"
    else:
        print(f"Failed: {script_path}")
        return False, "Failed"

def main():
    print_banner("TRADEPANEL END-TO-END SYSTEM TEST")
    start_time = time.time()
    
    # 1. Dependency & Env Check
    # print("Step 1: Environment Check")
    # if not run_script("scripts/check_env.py")[0]:
    #     return

    # 2. Data Ingestion Test (Limited)
    print_banner("STEP 1: DATA INGESTION (XAUUSD H1)")
    # We pull a small amount just to verify connectivity
    success, output = run_script("scripts/pull_all_data.py", ["XAUUSD", "--timeframe", "H1", "--limit", "100"])
    if not success: return

    # 3. Data Resampling Test
    print_banner("STEP 2: DATA RESAMPLING (M1 -> H1/H4)")
    success, output = run_script("data/resampler.py")
    if not success: return

    # 4. Auto-Optimization Test
    print_banner("STEP 3: AUTO-OPTIMIZATION & PARAM SYNC")
    # We'll run a quick optimization for range_breakout as a test
    success, output = run_script("scripts/auto_optimize.py", ["--quick"])
    if not success: return

    # 5. Paper Trading Loop Test
    print_banner("STEP 4: PAPER ENGINE ITERATION")
    # Run once to see if signals generate and risk checks pass
    success, output = run_script("scripts/run_paper.py", ["--once"])
    if not success: return
    print(output)

    # 6. Final Validation Report
    print_banner("STEP 5: GENERATING VALIDATION SUMMARY")
    success, output = run_script("scripts/summary_validation.py")
    if not success: return
    print(output)

    duration = time.time() - start_time
    print_banner(f"E2E TEST COMPLETE - SUCCESS (Total Time: {duration:.1f}s)")

if __name__ == "__main__":
    main()
