import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import ta_compat as ta
from data.db_client import DBClient
from datetime import datetime

class RegimeDetector:
    def __init__(self):
        self.db = DBClient()

    def classify(self, df: pd.DataFrame):
        """
        Classifies the market regime for the last bar in the provided dataframe.
        - ADX > 30 + EMA Alignment: TRENDING (Strong Conviction)
        - ADX > 30: TRENDING_WEAK
        - ADX < 20: RANGING
        - ATR > 1.5x of its average: HIGH_VOL
        - ATR < 0.5x of its average: LOW_VOL
        """
        if len(df) < 50:
            return "INSUFFICIENT_DATA", 0.0, 0.0

        # 1. Calculate ADX (Standard 14 period)
        adx_df = ta.adx(df['high'], df['low'], df['close'], length=14)
        adx = adx_df['ADX_14'].iloc[-1] if not adx_df.empty else 0.0

        # 2. Calculate ATR (Standard 14 period)
        atr_series = ta.atr(df['high'], df['low'], df['close'], length=14)
        atr = atr_series.iloc[-1] if not atr_series.empty else 0.0
        
        # Calculate ATR baseline (20-period moving average of ATR)
        atr_sma = atr_series.rolling(window=20).mean().iloc[-1]
        
        # 3. Calculate EMA Alignment (20, 50, 200)
        ema20 = ta.ema(df['close'], length=20).iloc[-1]
        ema50 = ta.ema(df['close'], length=50).iloc[-1]
        ema200 = ta.ema(df['close'], length=200).iloc[-1] if len(df) >= 200 else 0.0
        
        aligned_bull = (ema20 > ema50 > ema200) if ema200 > 0 else (ema20 > ema50)
        aligned_bear = (ema20 < ema50 < ema200) if ema200 > 0 else (ema20 < ema50)
        is_aligned = aligned_bull or aligned_bear

        # 4. Logic
        regime_base = "RANGING"
        if adx > 30:
            if is_aligned:
                regime_base = "TRENDING"
            else:
                regime_base = "TRENDING_WEAK"
        elif adx >= 20 and adx <= 30:
            regime_base = "NEUTRAL"

        volatility = "NORMAL_VOL"
        if atr_sma > 0:
            if atr > (atr_sma * 1.5):
                volatility = "HIGH_VOL"
            elif atr < (atr_sma * 0.5):
                volatility = "LOW_VOL"
        
        final_regime = f"{regime_base}_{volatility}"
        
        return final_regime, float(adx), float(atr)

    def run_update(self, pair, timeframe="H1"):
        """Fetches latest data, classifies, and logs to DB."""
        print(f"Detecting regime for {pair} {timeframe}...")
        
        # Fetch last 100 bars for calculation
        query = """
            SELECT timestamp, open, high, low, close 
            FROM market_data 
            WHERE pair = %s AND timeframe = %s 
            ORDER BY timestamp DESC LIMIT 100
        """
        rows = self.db.execute_query(query, (pair, timeframe))
        if not rows:
            print("No data found to detect regime.")
            return
            
        # Reverse to chronological order
        df = pd.DataFrame(rows, columns=['timestamp', 'open', 'high', 'low', 'close'])
        df.set_index('timestamp', inplace=True)
        df = df.iloc[::-1] # Reverse
        
        # Ensure floats
        for col in ['open', 'high', 'low', 'close']:
            df[col] = df[col].astype(float)
            
        regime, adx, atr = self.classify(df)
        last_timestamp = df.index[-1]
        
        print(f"Current Regime: {regime} (ADX: {adx:.2f}, ATR: {atr:.2f})")
        
        # Log to regime_log table
        log_query = """
            INSERT INTO regime_log (pair, timestamp, regime, adx_value, atr_value)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (pair, timestamp) DO UPDATE 
            SET regime = EXCLUDED.regime, adx_value = EXCLUDED.adx_value, atr_value = EXCLUDED.atr_value
        """
        # Note: Added UNIQUE(pair, timestamp) to regime_log in a future migration? 
        # Actually setup_db didn't have UNIQUE for regime_log.
        # Let's perform a simple insert for now as per Step 14 requirements.
        
        self.db.execute_query(
            "INSERT INTO regime_log (pair, timestamp, regime, adx_value, atr_value) VALUES (%s, %s, %s, %s, %s)",
            (pair, last_timestamp, regime, adx, atr)
        )
        return regime

if __name__ == "__main__":
    # Test execution
    rd = RegimeDetector()
    rd.run_update("XAUUSD", "H1")
