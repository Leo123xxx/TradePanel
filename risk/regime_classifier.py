import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.macro_feed import MacroDataFeed
from datetime import datetime

class RegimeClassifier:
    """
    Translates raw macro data into actionable trading biases.
    
    Categories:
    - RISK_OFF: Fear is high, USD strong, Yields up (Safety play -> Long Gold)
    - RISK_ON: Greed is high, USD weak, Yields down (Risk play -> Short Gold / Long Crypto)
    - NEUTRAL: No clear macro direction
    """
    
    def __init__(self):
        self.feed = MacroDataFeed()
        
    def get_market_bias(self):
        """
        Calculates the global macro bias.
        Returns: "RISK_OFF", "RISK_ON", or "NEUTRAL"
        """
        data = self.feed.get_latest_data()
        if not data:
            return "NEUTRAL"
            
        vix = data.get('vix', 0)
        dxy = data.get('dxy', 0)
        dxy_sma = data.get('dxy_50ma', 0)
        yields = data.get('yields', 0)
        yields_prev = data.get('yields_prev', 0)
        
        # 1. RISK_OFF indicators
        #  - VIX > 15 (High fear)
        #  - DXY > 50MA (USD strength)
        #  - Yields rising (Inflation/Rate fears)
        risk_off_score = 0
        if vix > 15: risk_off_score += 1
        if dxy > dxy_sma and dxy_sma > 0: risk_off_score += 1
        if yields > yields_prev: risk_off_score += 1
        
        # 2. RISK_ON indicators
        #  - VIX < 15 (Low fear)
        #  - DXY < 50MA (USD weakness)
        #  - Yields falling
        risk_on_score = 0
        if vix > 0 and vix < 15: risk_on_score += 1
        if dxy > 0 and dxy < dxy_sma: risk_on_score += 1
        if yields > 0 and yields < yields_prev: risk_on_score += 1
        
        if risk_off_score >= 2:
            return "RISK_OFF"
        elif risk_on_score >= 2:
            return "RISK_ON"
        else:
            return "NEUTRAL"

    def get_pair_bias(self, symbol: str):
        """
        Determines the specific bias for a pair based on macro state.
        Returns: 1 (Long focus), -1 (Short focus), 0 (No specific bias)
        """
        bias = self.get_market_bias()
        
        # Gold (XAUUSD) specific logic
        if "XAU" in symbol:
            if bias == "RISK_OFF":
                return 1   # Favor longs in chaos
            elif bias == "RISK_ON":
                return -1  # Favor shorts in stability
                
        # Crypto (BTC/ETH) specific logic
        if any(c in symbol for c in ["BTC", "ETH"]):
            if bias == "RISK_ON":
                return 1   # Favor longs when risk is on
            elif bias == "RISK_OFF":
                return -1  # Favor shorts when fear is high
                
        return 0

if __name__ == "__main__":
    rc = RegimeClassifier()
    print(f"Global Bias: {rc.get_market_bias()}")
    print(f"XAUUSD Bias: {rc.get_pair_bias('XAUUSD')}")
    print(f"BTCUSD Bias: {rc.get_pair_bias('BTCUSD')}")
