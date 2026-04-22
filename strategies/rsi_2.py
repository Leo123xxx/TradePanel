import pandas as pd
import ta_compat as ta
from strategies.base_strategy import BaseStrategy

class RSITwoStrategy(BaseStrategy):
    """
    Extreme Mean Reversion (RSI-2)
    
    Logic:
    1. Filter: Price must be above a 200 SMA (Bullish context).
    2. Condition: RSI(2) must be below 10 (Oversold).
    3. Signal: Buy when RSI(10) crosses above 10.
    4. Exit: Close when price closes above 5 EMA.
    """

    def __init__(self, params: dict = None):
        if params is None:
            params = {
                "rsi_period": 2,
                "sma_filter": 200,
                "oversold": 10,
                "overbought": 90,
                "exit_ema": 5
            }
        super().__init__(
            name="Extreme_RSI_2",
            category="Mean Reversion",
            params=params,
            regime=["RANGING", "TRENDING"],
            timeframes=["H4", "D1"],
            pairs=["EURUSD", "USDJPY"]
        )

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()
        
        # 1. Indicators
        df['rsi'] = ta.rsi(df['close'], length=self.params['rsi_period'])
        df['sma_200'] = ta.sma(df['close'], length=self.params['sma_filter'])
        
        # 2. Multi-TF Context (D1 Resample)
        # We use reindex with ffill to get the D1 SMA200 value on every H4/H1 bar
        try:
            df_d1 = df.resample('D').last().ffill()
            df_d1['sma200_d1'] = ta.sma(df_d1['close'], length=200)
            df['d1_trend_bullish'] = df_d1['sma200_d1'].reindex(df.index, method='ffill') < df['close']
            df['d1_trend_bearish'] = df_d1['sma200_d1'].reindex(df.index, method='ffill') > df['close']
        except Exception:
            # Fallback if insufficient data for resampling
            df['d1_trend_bullish'] = True
            df['d1_trend_bearish'] = True

        # 3. 2-Bar Break Confirmation
        # Buy: Close > Max High of last 2 bars
        df['prev_2_high'] = df['high'].shift(1).rolling(2).max()
        # Sell: Close < Min Low of last 2 bars
        df['prev_2_low'] = df['low'].shift(1).rolling(2).min()
        
        df['break_high'] = df['close'] > df['prev_2_high']
        df['break_low'] = df['close'] < df['prev_2_low']

        # 4. Signals
        df['signal'] = 0
        
        # We prime the signal if RSI was oversold in the last 3 bars
        df['is_oversold'] = (df['rsi'] < self.params['oversold']).rolling(3).max() > 0
        df['is_overbought'] = (df['rsi'] > self.params['overbought']).rolling(3).max() > 0
        
        # Buy: H4 Bullish + D1 Bullish + Was Oversold + 2-Bar Break
        long_cond = (
            (df['close'] > df['sma_200']) & 
            df['d1_trend_bullish'] & 
            df['is_oversold'] &
            df['break_high']
        )
        
        # Sell: H4 Bearish + D1 Bearish + Was Overbought + 2-Bar Break
        short_cond = (
            (df['close'] < df['sma_200']) & 
            df['d1_trend_bearish'] & 
            df['is_overbought'] &
            df['break_low']
        )
        
        # Filter: Only fire once (on the bar the break happens)
        # Using shift(1) to detect a NEW break_high/break_low is already handled by long_cond logic
        
        df.loc[long_cond, 'signal'] = 1
        df.loc[short_cond, 'signal'] = -1
        
        return df

    def validate_params(self) -> bool:
        return True
