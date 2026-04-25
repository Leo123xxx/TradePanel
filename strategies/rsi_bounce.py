import pandas as pd
import ta_compat as ta
from strategies.base_strategy import BaseStrategy

class RSIBounceStrategy(BaseStrategy):
    """
    RSI Mean Reversion Strategy with EMA200 trend filter.
    Mean reversion strategy: use_partial_tp=False, tight TP at 2:1.
    Partial TP + BE hurts mean reversion because price reaches 1:1 naturally
    then snaps back — exit at BE rather than completing the reversal.
    """

    def __init__(self, params: dict = None):
        if params is None:
            params = {
                "rsi_period": 14,
                "oversold": 20,  # tighter from 25 — only trade true extremes
                "overbought": 80,  # tighter from 75 — only trade true extremes
                "ema_trend": 200,
                "tp_atr_mult": 2.0,     # tighter TP for mean reversion (was 3.0)
                "sl_atr_mult": 1.0,
                "atr_period": 14,
                "use_partial_tp": False  # mean reversion — run to full TP
            }
        super().__init__("RSI_Bounce", "Mean Reversion", params)

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()
        rsi_period      = self.params.get("rsi_period", 14)
        overbought      = self.params.get("overbought", 75)
        oversold        = self.params.get("oversold", 25)
        ema_trend_period = self.params.get("ema_trend", 200)

        df['rsi']       = ta.rsi(df['close'], length=rsi_period)
        df['ema_trend'] = ta.ema(df['close'], length=ema_trend_period)
        in_uptrend      = df['close'] > df['ema_trend']
        in_downtrend    = df['close'] < df['ema_trend']

        df['signal'] = 0
        df.loc[in_uptrend   & (df['rsi'] > oversold)   & (df['rsi'].shift(1) <= oversold),   'signal'] =  1
        df.loc[in_downtrend & (df['rsi'] < overbought) & (df['rsi'].shift(1) >= overbought), 'signal'] = -1
        return df

    def validate_params(self) -> bool:
        return (self.params.get("rsi_period", 0) > 0 and
                0 < self.params.get("oversold", 20) < 50 and
                50 < self.params.get("overbought", 75) < 100)
