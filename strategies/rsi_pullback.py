import pandas as pd
import ta_compat as ta
from strategies.base_strategy import BaseStrategy

APPROVED_PAIRS = ["XAUUSD", "EURUSD", "GBPUSD", "USDJPY", "XAGUSD"]
APPROVED_TIMEFRAMES = ["H4", "D1"]

class RSIPullbackStrategy(BaseStrategy):
    """
    RSI Pullback in Trend Strategy.
    """

    def __init__(self, params: dict = None):
        if params is None:
            params = {
                "rsi_period": 14,
                "rsi_pullback_lower": 30,
                "rsi_pullback_upper": 50,
                "fast_ema": 20,
                "slow_ema": 50,
                "atr_period": 14,
                "tp_atr_mult": 2.0,
                "sl_bars_lookback": 5
            }
        super().__init__(
            name="RSI_Pullback",
            category="Trend + Reversion Hybrid",
            params=params,
            regime=["TRENDING"],
            timeframes=APPROVED_TIMEFRAMES,
            pairs=APPROVED_PAIRS
        )

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()

        rsi_period = self.params.get("rsi_period", 14)
        fast_ema = self.params.get("fast_ema", 20)
        slow_ema = self.params.get("slow_ema", 50)
        p_lower = self.params.get("rsi_pullback_lower", 30)
        p_upper = self.params.get("rsi_pullback_upper", 50)

        df['rsi'] = ta.rsi(df['close'], length=rsi_period)
        df['ema_fast'] = ta.ema(df['close'], length=fast_ema)
        df['ema_slow'] = ta.ema(df['close'], length=slow_ema)
        adx_df = ta.adx(df['high'], df['low'], df['close'], length=14)
        df['adx'] = adx_df["ADX_14"]

        df['trend_up'] = (df['ema_fast'] > df['ema_slow']) | ((df['adx'] > 25) & (df['close'] > df['ema_fast']))
        df['trend_down'] = (df['ema_fast'] < df['ema_slow']) | ((df['adx'] > 25) & (df['close'] < df['ema_fast']))

        df['signal'] = 0
        long_cond = df['trend_up'] & df['rsi'].between(p_lower, p_upper) & (df['close'] > df['ema_fast'])
        short_cond = df['trend_down'] & df['rsi'].between(50, 70) & (df['close'] < df['ema_fast'])

        df.loc[long_cond, 'signal'] = 1
        df.loc[short_cond, 'signal'] = -1

        df.loc[(df['signal'] == 1) & (df['signal'].shift(1) == 1), 'signal'] = 0
        df.loc[(df['signal'] == -1) & (df['signal'].shift(1) == -1), 'signal'] = 0

        return df

    def validate_params(self) -> bool:
        return True
