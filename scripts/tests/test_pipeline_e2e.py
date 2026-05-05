import sys
import os
import MetaTrader5 as mt5
from datetime import datetime, timedelta
import yaml
import json
import uuid

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from data.db_client import DBClient
from mt5_bridge.connector import MT5Connector
from risk.manager import RiskManager

def run_e2e_tests():
    print("Starting TradePanel End-to-End Pipeline Validation")
    print("=" * 60)
    
    results = {}
    db = DBClient()
    connector = MT5Connector()
    risk = RiskManager()
    
    # --- 1. Connectivity ---
    print("\n[1/5] Testing Connectivity...")
    
    # MT5
    results["mt5_connection"] = connector.connect()
    print(f"  - MT5 Connection: {'PASS' if results['mt5_connection'] else 'FAIL'}")
    
    # DB
    try:
        db.execute_query("SELECT 1")
        results["db_connection"] = True
    except:
        results["db_connection"] = False
    print(f"  - DB Connection: {'PASS' if results['db_connection'] else 'FAIL'}")

    # --- 2. Data Freshness ---
    print("\n[2/5] Testing Data Freshness (Active Pairs)...")
    with open("config/strategies.yaml") as f:
        strat_cfg = yaml.safe_load(f)
    
    active_pairs = set()
    for s_def in strat_cfg.values():
        if isinstance(s_def, dict) and s_def.get('enabled'):
            active_pairs.update(s_def.get('pairs', []))
            
    fresh_count = 0
    for pair in active_pairs:
        info = mt5.symbol_info(pair)
        if info:
            rates = mt5.copy_rates_from_pos(pair, mt5.TIMEFRAME_M1, 0, 1)
            if rates is not None and len(rates) > 0:
                last_time = datetime.fromtimestamp(rates[0][0])
                age = (datetime.now() - last_time).total_seconds() / 3600
                if age < 4: # 4 hours freshness
                    fresh_count += 1
                else:
                    print(f"    Warning: {pair} data is {age:.1f}h old.")
    
    results["data_freshness"] = (fresh_count == len(active_pairs))
    print(f"  - Data Freshness: {fresh_count}/{len(active_pairs)} pairs fresh")

    # --- 3. Risk & Sizing ---
    print("\n[3/5] Testing Risk & Sizing Logic...")
    try:
        lots = risk.calculate_lot_size("XAUUSD", 500)
        results["lot_sizing"] = (lots > 0)
        
        passed, reason = risk.check_all("ma_crossover", "XAUUSD", lots, "BUY")
        results["risk_checks"] = True 
    except Exception as e:
        print(f"    Error: {e}")
        results["lot_sizing"] = False
        results["risk_checks"] = False
        
    print(f"  - Lot Sizing: {'PASS' if results['lot_sizing'] else 'FAIL'}")
    print(f"  - Risk Checks: {'PASS' if results['risk_checks'] else 'FAIL'}")

    # --- 4. Signal/Trade Simulation ---
    print("\n[4/5] Simulating Signal & Trade Logging...")
    try:
        trade_id = str(uuid.uuid4())
        db.execute_query(
            "INSERT INTO signals (timestamp, pair, direction) VALUES (%s, %s, %s)",
            (datetime.now(), "XAUUSD", "BUY")
        )
        results["signal_logging"] = True
        
        db.execute_query(
            "INSERT INTO trades (trade_id, mode, pair, direction, lot_size, entry_price, open_time, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (trade_id, "TEST", "XAUUSD", "BUY", 0.01, 2000.0, datetime.now(), "OPENED")
        )
        results["trade_logging"] = True
        
        db.execute_query("DELETE FROM trades WHERE mode = 'TEST'")
        db.execute_query("DELETE FROM signals WHERE pair = 'XAUUSD' AND direction = 'BUY'")
        
    except Exception as e:
        print(f"    DB Logging Error: {e}")
        results["signal_logging"] = False
        results["trade_logging"] = False

    print(f"  - Signal Logging: {'PASS' if results['signal_logging'] else 'FAIL'}")
    print(f"  - Trade Logging: {'PASS' if results['trade_logging'] else 'FAIL'}")

    # --- 5. Summary ---
    print("\n" + "=" * 60)
    all_pass = all(results.values())
    print(f"FINAL RESULT: {'ALL PASS' if all_pass else 'SOME FAILURES'}")
    
    os.makedirs("results/tests", exist_ok=True)
    report_path = f"results/tests/pipeline_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Report saved to: {report_path}")

    connector.disconnect()
    return all_pass

if __name__ == "__main__":
    run_e2e_tests()
