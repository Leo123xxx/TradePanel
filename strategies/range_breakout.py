import pandas as pd
import ta_compat as ta
from strategies.base_strategy import BaseStrategy

APPROVED_PAIRS = ["XAUUSD", "EURUSD", "GBPUSD", "USDJPY", "XAGUSD"]
APPROVED_TIMEFRAMES = ["H4", "D1"]

class RangeBreakoutStrategy(BaseStrategy):
    """
    Range Breakout — Breakout Strategy.
    """

    def __init__(self, params: dict = None):
        if params is None:
            params = {
                "consolidation_bars": 20,
                "vol_threshold_mult": 1.3,
                "tp_range_mult": 2.5,
                "sl_buffer_pips": 15,
                "adx_min_filter": 20,
                "ema_period": 20
            }
        super().__init__(
            name="Range_Breakout",
            category="Breakout",
            params=params,
            regime=["RANGING", "BREAKOUT", "ANY"],
            timeframes=APPROVED_TIMEFRAMES,
            pairs=APPROVED_PAIRS
        )

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()

        consolidation_bars = self.params.get("consolidation_bars", 20)
        vol_threshold_mult = self.params.get("vol_threshold_mult", 1.3)
        adx_min = self.params.get("adx_min_filter", 20)
        ema_period = self.params.get("ema_period", 20)

        # Resistance and Support of N bars before current bar
        df['highest_high'] = df['high'].rolling(window=consolidation_bars).max().shift(1)
        df['lowest_low'] = df['low'].rolling(window=consolidation_bars).min().shift(1)

        df['ema'] = ta.ema(df['close'], length=ema_period)

        # Volume spike
        df['avg_vol'] = df['tick_volume'].rolling(window=consolidation_bars).mean().shift(1)
        df['vol_spike'] = df['tick_volume'] >= (df['avg_vol'] * vol_threshold_mult)

        # ADX
        adx_df = ta.adx(df['high'], df['low'], df['close'], length=14)
        df['adx'] = adx_df["ADX_14"]

        # Signal
        df['signal'] = 0

        long_cond = (
            (df['close'] > df['highest_high']) &
            (df['close'] > df['ema']) &
            (df['vol_spike'] | (df['adx'] > adx_min))
        )

        short_cond = (
            (df['close'] < df['lowest_low']) &
            (df['close'] < df['ema']) &
            (df['vol_spike'] | (df['adx'] > adx_min))
        )

        df.loc[long_cond, 'signal'] = 1
        df.loc[short_cond, 'signal'] = -1

        # Crossover only
        df.loc[(df['signal'] == 1) & (df['signal'].shift(1) == 1), 'signal'] = 0
        df.loc[(df['signal'] == -1) & (df['signal'].shift(1) == -1), 'signal'] = 0

        return df

    def validate_params(self) -> bool:
        return True
