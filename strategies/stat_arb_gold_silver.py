import pandas as pd
import numpy as np
from strategies.base_strategy import BaseStrategy
from data.db_client import DBClient

class StatArbGoldSilver(BaseStrategy):
    """
    Statistical Arbitrage (XAUUSD vs XAGUSD)
    
    Logic:
    1. Ratio: Calculate XAUUSD/XAGUSD ratio.
    2. Z-Score: Distance from the 200-period mean in standard deviations.
    3. Signal: 
       - Buy Silver / Sell Gold if Z-Score > 2.0 (Gold expensive)
       - Buy Gold / Sell Silver if Z-Score < -2.0 (Silver expensive)
    
    Implementation: Since the engine processes one symbol, this strategy will
    be applied to XAUUSD and fetch XAGUSD data from the DB to calculate the spread.
    NOTE: Execution only happens on the 'active' symbol (XAUUSD). 
    """

    def __init__(self, params: dict = None):
        if params is None:
            params = {
                "window": 200,
                "z_entry": 2.0,
                "z_exit": 0.0,
                "secondary_symbol": "XAGUSD"
            }
        super().__init__(
            name="Stat_Arb_Gold_Silver",
            category="Advanced",
            params=params,
            regime=["RANGING", "ANY"],
            timeframes=["H4", "D1"],
            pairs=["XAUUSD"]
        )

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()
        db = DBClient()
        
        secondary = self.params.get("secondary_symbol", "XAGUSD")
        
        # 1. Fetch Secondary Data
        # We need the same timeframes and range
        start = df.index.min()
        end = df.index.max()
        
        # Identify Timeframe
        diff = df.index[1] - df.index[0]
        if diff.days > 0: tf = "D1"
        elif diff.seconds >= 43200: tf = "H12"
        elif diff.seconds >= 14400: tf = "H4"
        elif diff.seconds >= 3600: tf = "H1"
        else: tf = "M15"
        
        rows = db.execute_query(
            "SELECT timestamp, close FROM market_data WHERE pair = %s AND timeframe = %s "
            "AND timestamp >= %s AND timestamp <= %s ORDER BY timestamp",
            (secondary, tf, start, end)
        )
        
        if not rows:
            # Fallback check for H1 if current is M15
            print(f"[StatArb] WARNING: No data for {secondary} on {tf}. Trying H4 fallback...")
            rows = db.execute_query(
                "SELECT timestamp, close FROM market_data WHERE pair = %s AND timeframe = %s "
                "AND timestamp >= %s AND timestamp <= %s ORDER BY timestamp",
                (secondary, "H4", start, end)
            )

        if not rows:
            print(f"[StatArb] ERROR: No data for {secondary}")
            df['signal'] = 0
            return df
            
        df_sec = pd.DataFrame(rows, columns=['timestamp', 'close_sec'])
        df_sec['timestamp'] = pd.to_datetime(df_sec['timestamp'])
        df_sec.set_index('timestamp', inplace=True)
        df_sec['close_sec'] = df_sec['close_sec'].astype(float)
        
        # Merge - ensuring indices are compatible
        df.index = pd.to_datetime(df.index)
        df = df.join(df_sec, how='left')
        df['close_sec'] = df['close_sec'].ffill().bfill()
        
        # 2. Ratio & Z-Score
        df['ratio'] = df['close'] / df['close_sec']
        df['mean_ratio'] = df['ratio'].rolling(window=self.params['window']).mean()
        df['std_ratio'] = df['ratio'].rolling(window=self.params['window']).std()
        df['zscore'] = (df['ratio'] - df['mean_ratio']) / df['std_ratio']
        
        # 3. Signals
        df['signal'] = 0
        
        # Z-Score > 2.0: Gold too high -> Sell Gold
        df.loc[df['zscore'] > self.params['z_entry'], 'signal'] = -1
        # Z-Score < -2.0: Gold too low -> Buy Gold
        df.loc[df['zscore'] < -self.params['z_entry'], 'signal'] = 1
        
        # Exit logic is handled by the engine (TP/SL) or we could add reversal logic here.
        
        return df

    def validate_params(self) -> bool:
        return True
