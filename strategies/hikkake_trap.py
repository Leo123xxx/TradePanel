import pandas as pd
import numpy as np
import ta_compat as ta
from strategies.base_strategy import BaseStrategy

class HikkakeTrap(BaseStrategy):
    """
    Hikkake Inside Bar Trap (Mean Reversion / Price Action)

    Logic:
    1. Detect Inside Bar (Bar 0).
    2. Bar +1 or +2 breaks out of Bar 0 (False breakout).
    3. Price then reverses and breaks the opposite side of Bar 0.
    4. Entry: On opposite breakout.
    RR = 3:1 (tp_atr_mult=3.0, sl_atr_mult=1.0).
    """

    def __init__(self, params: dict = None):
        if params is None:
            params = {
                "lookback_bars": 3,
                "atr_period": 14,
                "tp_atr_mult": 2.0,   # mean reversion TP 2:1 (was 3:1 — too far)
                "sl_atr_mult": 1.0,
                "use_partial_tp": False,  # mean reversion — no partial TP
                "cooldown_bars": 8        # prevent overtrading
            }
        super().__init__(
            name="Hikkake_Trap",
            category="Mean Reversion",
            params=params,
            regime=["CHOPPY", "RANGING"],
            timeframes=["H4", "D1"],
            pairs=["BTCUSD", "ETHUSD"]
        )

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()

        # 1. Inside Bar Detection
        df['is_ib'] = (df['high'] < df['high'].shift(1)) & (df['low'] > df['low'].shift(1))

        # 2. Store IB levels
        df['ib_h'] = df['high'].where(df['is_ib']).ffill()
        df['ib_l'] = df['low'].where(df['is_ib']).ffill()

        # 3. Detect False Breakouts (Simplified Hikkake)
        # Check if we broke low or high of IB recently
        df['broke_l'] = (df['low'] < df['ib_l']) & (~df['is_ib'])
        df['broke_h'] = (df['high'] > df['ib_h']) & (~df['is_ib'])

        # Signal Buy: We broke Low within last 3 bars, now we broke High (reversal)
        df['recent_broke_l'] = df['broke_l'].rolling(window=3).max().shift(1).fillna(0).astype(bool)
        df['recent_broke_h'] = df['broke_h'].rolling(window=3).max().shift(1).fillna(0).astype(bool)

        df['condition_buy'] = df['recent_broke_l'] & (df['close'] > df['ib_h'])
        df['condition_sell'] = df['recent_broke_h'] & (df['close'] < df['ib_l'])

        df['signal'] = 0
        df.loc[df['condition_buy'], 'signal'] = 1
        df.loc[df['condition_sell'], 'signal'] = -1

        # EMA50 trend alignment filter — raises WR by blocking reversals against trend
        ema50 = ta.ema(df['close'], length=50)
        df.loc[(df['signal'] == 1) & (df['close'] < ema50), 'signal'] = 0   # no longs in downtrend
        df.loc[(df['signal'] == -1) & (df['close'] > ema50), 'signal'] = 0  # no shorts in uptrend

        # Cooldown filter — suppress repeated signals within N bars
        cooldown = self.params.get("cooldown_bars", 8)
        signal_arr = df['signal'].values.copy()
        last_signal_bar = -cooldown - 1
        for i in range(len(signal_arr)):
            if signal_arr[i] != 0:
                if i - last_signal_bar <= cooldown:
                    signal_arr[i] = 0
                else:
                    last_signal_bar = i
        df['signal'] = signal_arr

        return df

    def validate_params(self) -> bool:
        return True
