import sys
import os
import MetaTrader5 as mt5

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from risk.manager import RiskManager
from mt5_bridge.connector import MT5Connector

def test_blocked_pairs():
    connector = MT5Connector()
    if not connector.connect():
        print("Failed to connect to MT5")
        return

    risk = RiskManager()
    
    # Test cases: (symbol, should_be_blocked)
    test_cases = [
        ("XAUUSD", False),
        ("EURUSD", False),
        ("USDZAR", True),
        ("USDTRY", True),
    ]

    print("\n--- Testing Blocked Pairs Gating ---")
    print(f"Blocked Pairs: {risk.config['risk_management'].get('blocked_pairs')}")
    print("-" * 50)

    for symbol, should_block in test_cases:
        passed, reason = risk.check_all("ma_crossover", symbol, 0.1, "BUY")
        
        status = "BLOCKED" if not passed else "PASSED"
        result = "CORRECT" if (not passed) == should_block else "WRONG"
        
        print(f"Symbol: {symbol:<10} | Result: {status:<10} | Validation: {result}")
        if not passed:
            print(f"  Reason: {reason}")

    connector.disconnect()

if __name__ == "__main__":
    test_blocked_pairs()
