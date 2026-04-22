import pandas as pd
import ta_compat as ta
from strategies.base_strategy import BaseStrategy

APPROVED_PAIRS = ["XAUUSD", "EURUSD", "GBPUSD", "USDJPY", "XAGUSD"]
APPROVED_TIMEFRAMES = ["H4", "D1"]

class SwingPullbackStrategy(BaseStrategy):
    """
    Swing Pullback Pattern (ICT-Style).
    """

    def __init__(self, params: dict = None):
        if params is None:
            params = {
                "swing_lookback": 5,
                "swing_buffer_pips": 20,
                "tp_pips": 100,
                "sl_pips": 30,
                "atr_period": 14,
                "min_adx_filter": 15,
                "bars_to_confirm": 1
            }
        super().__init__(
            name="Swing_Pullback",
            category="Price Action / Pattern",
            params=params,
            regime=["ANY"],
            timeframes=APPROVED_TIMEFRAMES,
            pairs=APPROVED_PAIRS
        )

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()
        
        lb = self.params.get("swing_lookback", 5)
        buffer_pips = self.params.get("swing_buffer_pips", 20)
        adx_min = self.params.get("min_adx_filter", 15)

        avg_price = df['close'].mean()
        pip = 0.01 if avg_price > 50 else 0.0001
        buffer_price = buffer_pips * pip

        adx_df = ta.adx(df['high'], df['low'], df['close'], length=14)
        df['adx'] = adx_df["ADX_14"]

        df['swing_high'] = df['high'].rolling(window=lb).max().shift(2)
        df['swing_low'] = df['low'].rolling(window=lb).min().shift(2)

        df['signal'] = 0

        long_cond = (
            (df['low'] <= (df['swing_low'] + buffer_price)) &
            (df['close'] > df['open']) & 
            (df['adx'] > adx_min)
        )

        short_cond = (
            (df['high'] >= (df['swing_high'] - buffer_price)) &
            (df['close'] < df['open']) & 
            (df['adx'] > adx_min)
        )

        df.loc[long_cond, 'signal'] = 1
        df.loc[short_cond, 'signal'] = -1

        df.loc[(df['signal'] == 1) & (df['signal'].shift(1) == 1), 'signal'] = 0
        df.loc[(df['signal'] == -1) & (df['signal'].shift(1) == -1), 'signal'] = 0

        return df

    def validate_params(self) -> bool:
        return True
