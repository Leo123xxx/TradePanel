import MetaTrader5 as mt5
from typing import Optional, Dict

class MT5Account:
    def __init__(self):
        pass

    def get_info(self) -> Optional[Dict]:
        """Returns account information as a dictionary."""
        acc_info = mt5.account_info()
        if acc_info is None:
            return None
        return acc_info._asdict()

    def get_balance(self) -> float:
        info = self.get_info()
        return info.get('balance', 0.0) if info else 0.0

    def get_equity(self) -> float:
        info = self.get_info()
        return info.get('equity', 0.0) if info else 0.0

    def get_margin_free(self) -> float:
        info = self.get_info()
        return info.get('margin_free', 0.0) if info else 0.0

if __name__ == "__main__":
    import os
    from mt5_bridge.connector import MT5Connector
    
    connector = MT5Connector()
    if connector.connect():
        acc = MT5Account()
        print(f"Current Balance: {acc.get_balance()}")
        print(f"Current Equity: {acc.get_equity()}")
        connector.disconnect()
