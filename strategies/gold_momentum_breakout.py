import pandas as pd
import ta_compat as ta
from strategies.base_strategy import BaseStrategy

class GoldMomentumBreakoutStrategy(BaseStrategy):
    """
    Gold Momentum Breakout Strategy.
    Identifies a squeeze (consolidation) in Bollinger Bands, and a breakout
    confirmed by the RSI showing momentum in the breakout direction.
    """
    def __init__(self, params: dict = None):
        if params is None:
            params = {
                "bb_length": 20, 
                "bb_std": 2.0, 
                "rsi_length": 14,
                "rsi_buy_min": 50,
                "rsi_sell_max": 50,
                "squeeze_threshold_pct": 0.05
            }
        super().__init__("Gold_Momentum_Breakout", "Breakout", params)

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()
        
        bb_length = self.params.get("bb_length", 20)
        bb_std = self.params.get("bb_std", 2.0)
        rsi_length = self.params.get("rsi_length", 14)
        rsi_buy_min = self.params.get("rsi_buy_min", 50)
        rsi_sell_max = self.params.get("rsi_sell_max", 50)
        squeeze_threshold_pct = self.params.get("squeeze_threshold_pct", 0.05)
        
        # Calculate Bollinger Bands
        bb = ta.bbands(df['close'], length=bb_length, std=bb_std)
        if bb is None or bb.empty:
            df['signal'] = 0
            return df
            
        bb_lower_col = bb.columns[0] # L
        bb_mid_col = bb.columns[1]   # M 
        bb_upper_col = bb.columns[2] # U
        
        df = pd.concat([df, bb], axis=1)

        # 1. Bollinger Band Width (Squeeze calculation) as a % of middle band
        df['bb_width_pct'] = (df[bb_upper_col] - df[bb_lower_col]) / df[bb_mid_col]
        
        # Calculate RSI
        df['rsi'] = ta.rsi(df['close'], length=rsi_length)
        
        df['signal'] = 0
        
        # Condition: Are we breaking out of a squeeze?
        # A simple squeeze check: last bar had width < squeeze threshold
        is_squeeze = df['bb_width_pct'].shift(1) < squeeze_threshold_pct
        
        # Buy: Close > upper band AND we were in a squeeze previously AND RSI > min buy threshold
        buy_cond = (df['close'] > df[bb_upper_col]) & is_squeeze & (df['rsi'] > rsi_buy_min)
        
        # Sell: Close < lower band AND we were in a squeeze previously AND RSI < max sell threshold
        sell_cond = (df['close'] < df[bb_lower_col]) & is_squeeze & (df['rsi'] < rsi_sell_max)
        
        df.loc[buy_cond, 'signal'] = 1
        df.loc[sell_cond, 'signal'] = -1
        
        return df

    def validate_params(self) -> bool:
        return self.params.get("bb_length", 0) > 0 and self.params.get("rsi_length", 0) > 0
