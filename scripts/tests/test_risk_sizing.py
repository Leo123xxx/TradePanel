import sys
import os
import MetaTrader5 as mt5

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from risk.manager import RiskManager
from mt5_bridge.connector import MT5Connector

def test_lot_sizing():
    connector = MT5Connector()
    if not connector.connect():
        print("Failed to connect to MT5")
        return

    risk = RiskManager()
    
    # Test cases: (symbol, sl_points)
    test_cases = [
        ("XAUUSD", 1000),  # 1000 points SL
        ("XAUUSD", 500),   # 500 points SL
        ("EURUSD", 100),   # 10 pips
        ("EURUSD", 200),   # 20 pips
        ("GBPUSD", 500),   # 50 pips
        ("USDZAR", 10000), # 100 pips on ZAR (Exotic)
    ]

    print("\n--- Testing 1% Risk Lot Sizing ---")
    balance = risk.account.get_balance()
    risk_pct = risk.config['risk_management'].get('risk_per_trade_pct', 1.0)
    risk_amount = balance * (risk_pct / 100.0)
    
    print(f"Account Balance: R{balance:.2f}")
    print(f"Risk Per Trade ({risk_pct}%): R{risk_amount:.2f}")
    print("-" * 50)
    print(f"{'Symbol':<10} | {'SL Pts':<10} | {'Lots':<10} | {'Tick Val':<10}")
    print("-" * 50)

    for symbol, sl_pts in test_cases:
        # Mock calculation to see internals
        symbol_info = mt5.symbol_info(symbol)
        if not symbol_info:
            print(f"{symbol:<10} | Symbol not found")
            continue
            
        lots = risk.calculate_lot_size(symbol, sl_pts)
        tick_val = symbol_info.trade_tick_value
        
        print(f"{symbol:<10} | {sl_pts:<10} | {lots:<10.2f} | {tick_val:<10.2f}")

    connector.disconnect()

if __name__ == "__main__":
    test_lot_sizing()
