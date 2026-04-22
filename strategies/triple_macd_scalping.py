import pandas as pd
import ta_compat as ta
from strategies.base_strategy import BaseStrategy

class TripleMACDScalping(BaseStrategy):
    """
    Triple MACD Momentum Scalping
    
    Logic:
    1. Fast MACD (12, 26, 9)
    2. Mid MACD (24, 52, 18)
    3. Slow MACD (48, 104, 36)
    
    Condition: All three MACD lines must be above 0 for BUY, or below 0 for SELL.
    Entry: Fast MACD line crosses its signal line in the direction of the bias.
    """

    def __init__(self, params: dict = None):
        if params is None:
            params = {
                "fast_m": (12, 26, 9),
                "mid_m": (24, 52, 18),
                "slow_m": (48, 104, 36),
                "tp_atr_mult": 1.5,
                "sl_atr_mult": 1.0
            }
        super().__init__(
            name="Triple_MACD_Scalping",
            category="Trend Following",
            params=params,
            regime=["TRENDING", "HIGH_VOL"],
            timeframes=["M5", "M15"],
            pairs=["XAUUSD", "BTCUSD"]
        )

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()
        
        # 1. Calculate 3 MACDs
        macd_f = ta.macd(df['close'], fast=self.params['fast_m'][0], slow=self.params['fast_m'][1], signal=self.params['fast_m'][2])
        macd_m = ta.macd(df['close'], fast=self.params['mid_m'][0], slow=self.params['mid_m'][1], signal=self.params['mid_m'][2])
        macd_s = ta.macd(df['close'], fast=self.params['slow_m'][0], slow=self.params['slow_m'][1], signal=self.params['slow_m'][2])
        
        # Extract lines (matching ta_compat column naming)
        f_line = macd_f.iloc[:, 0]
        f_sig = macd_f.iloc[:, 2]
        m_line = macd_m.iloc[:, 0]
        s_line = macd_s.iloc[:, 0]
        
        # 2. Bias: All lines on same side of 0
        df['bias_bull'] = (f_line > 0) & (m_line > 0) & (s_line > 0)
        df['bias_bear'] = (f_line < 0) & (m_line < 0) & (s_line < 0)
        
        # 3. Entry: Fast MACD cross signal
        df['cross_up'] = (f_line > f_sig) & (f_line.shift(1) <= f_sig.shift(1))
        df['cross_down'] = (f_line < f_sig) & (f_line.shift(1) >= f_sig.shift(1))
        
        # 4. Final signal
        df['signal'] = 0
        df.loc[df['bias_bull'] & df['cross_up'], 'signal'] = 1
        df.loc[df['bias_bear'] & df['cross_down'], 'signal'] = -1
        
        return df

    def validate_params(self) -> bool:
        return True
