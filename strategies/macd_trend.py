import pandas as pd
import ta_compat as ta
from strategies.base_strategy import BaseStrategy

class MACDTrendStrategy(BaseStrategy):
    """
    MACD Trend Follower.
    Waits for a MACD crossover in the direction of a strong trend confirmed by ADX.
    """
    def __init__(self, params: dict = None):
        if params is None:
            params = {
                "macd_fast": 12,
                "macd_slow": 26,
                "macd_signal": 9,
                "adx_length": 14,
                "adx_threshold": 25,
                "tp_atr_mult": 3.0,    # trend following — wider target
                "sl_atr_mult": 1.0,
                "atr_period": 14
            }
        super().__init__("MACD_Trend", "Trend Following", params)

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()
        
        macd_fast = self.params.get("macd_fast", 12)
        macd_slow = self.params.get("macd_slow", 26)
        macd_signal = self.params.get("macd_signal", 9)
        adx_length = self.params.get("adx_length", 14)
        adx_threshold = self.params.get("adx_threshold", 25)
        
        # Calculate MACD
        macd_res = ta.macd(df['close'], fast=macd_fast, slow=macd_slow, signal=macd_signal)
        if macd_res is None or macd_res.empty:
            df['signal'] = 0
            return df
            
        macd_line_col = macd_res.columns[0]
        signal_line_col = macd_res.columns[2]
        
        df = pd.concat([df, macd_res], axis=1)
        
        # Calculate ADX
        adx_res = ta.adx(df['high'], df['low'], df['close'], length=adx_length)
        if adx_res is None or adx_res.empty:
            df['signal'] = 0
            return df
            
        adx_col = adx_res.columns[0]
        dmp_col = adx_res.columns[2] # DI+
        dmn_col = adx_res.columns[3] # DI-
        
        df = pd.concat([df, adx_res], axis=1)
        
        df['signal'] = 0
        
        # Condition: Are we in a strong trend?
        strong_trend = df[adx_col] > adx_threshold
        
        # Buy: MACD crosses above Signal Line AND ADX indicates strong uptrend (DI+ > DI-)
        macd_cross_up = (df[macd_line_col] > df[signal_line_col]) & (df[macd_line_col].shift(1) <= df[signal_line_col].shift(1))
        buy_cond = macd_cross_up & strong_trend & (df[dmp_col] > df[dmn_col])
        
        # Sell: MACD crosses below Signal Line AND ADX indicates strong downtrend (DI- > DI+)
        macd_cross_down = (df[macd_line_col] < df[signal_line_col]) & (df[macd_line_col].shift(1) >= df[signal_line_col].shift(1))
        sell_cond = macd_cross_down & strong_trend & (df[dmn_col] > df[dmp_col])
        
        df.loc[buy_cond, 'signal'] = 1
        df.loc[sell_cond, 'signal'] = -1
        
        return df

    def validate_params(self) -> bool:
        return self.params.get("macd_fast", 0) > 0 and self.params.get("macd_slow", 0) > self.params.get("macd_fast")
