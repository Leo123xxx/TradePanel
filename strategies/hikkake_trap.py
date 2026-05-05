import pandas as pd
import numpy as np
import ta_compat as ta
from strategies.base_strategy import BaseStrategy

class HikkakeTrap(BaseStrategy):
    """
    Hikkake Inside Bar Trap v2 (Mean Reversion / Price Action)

    Logic:
    1. Detect Inside Bar (Bar 0) with range >= 0.7x ATR14 (meaningful IB only).
    2. Bar +1 or +2 breaks out of Bar 0 (False breakout).
    3. Price then reverses and breaks the opposite side of Bar 0.
    4. Entry: On opposite breakout — close must be in upper 40% of bar range (longs)
       or lower 40% (shorts) for quality confirmation.
    5. ADX tightened to 22 (strictly ranging/choppy market).
    6. Cooldown raised to 12 bars.
    RR = 2:1 (tp_atr_mult=2.0, sl_atr_mult=1.0) — mean reversion.
    """

    def __init__(self, params: dict = None):
        if params is None:
            params = {
                "lookback_bars":        3,
                "atr_period":          14,
                "tp_atr_mult":          2.0,
                "sl_atr_mult":          1.0,
                "use_partial_tp":      False,
                "cooldown_bars":       12,    # raised from 8
                "adx_max":             22,    # tightened from 25
                "ib_atr_min_pct":       0.7,  # IB range must be >= 0.7x ATR14
                "reversal_quality_pct": 0.40, # close must be in top/bottom 40% of bar
                "rsi_period":          14,
                "rsi_long_min":        35,
                "rsi_long_max":        58,
                "rsi_short_min":       42,
                "rsi_short_max":       65,
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

        atr_period       = self.params.get("atr_period", 14)
        adx_max          = self.params.get("adx_max", 22)
        ib_atr_min_pct   = self.params.get("ib_atr_min_pct", 0.7)
        rev_quality_pct  = self.params.get("reversal_quality_pct", 0.40)
        rsi_p            = self.params.get("rsi_period", 14)
        rsi_long_min     = self.params.get("rsi_long_min",  35)
        rsi_long_max     = self.params.get("rsi_long_max",  58)
        rsi_short_min    = self.params.get("rsi_short_min", 42)
        rsi_short_max    = self.params.get("rsi_short_max", 65)
        cooldown         = self.params.get("cooldown_bars", 12)

        # --- ATR for sizing and IB quality filter ---
        df['atr'] = ta.atr(df['high'], df['low'], df['close'], length=atr_period)

        # 1. Inside Bar Detection: bar range must be meaningful (>= 0.7x ATR14)
        df['ib_range'] = df['high'] - df['low']
        df['is_ib'] = (
            (df['high'] < df['high'].shift(1))
            & (df['low'] > df['low'].shift(1))
            & (df['ib_range'] >= ib_atr_min_pct * df['atr'])
        )

        # 2. Store IB levels
        df['ib_h'] = df['high'].where(df['is_ib']).ffill()
        df['ib_l'] = df['low'].where(df['is_ib']).ffill()

        # 3. Detect False Breakouts
        df['broke_l'] = (df['low']  < df['ib_l']) & (~df['is_ib'])
        df['broke_h'] = (df['high'] > df['ib_h']) & (~df['is_ib'])

        # 4. Reversal signal
        df['recent_broke_l'] = df['broke_l'].rolling(window=3).max().shift(1).fillna(0).astype(bool)
        df['recent_broke_h'] = df['broke_h'].rolling(window=3).max().shift(1).fillna(0).astype(bool)

        df['condition_buy']  = df['recent_broke_l'] & (df['close'] > df['ib_h'])
        df['condition_sell'] = df['recent_broke_h'] & (df['close'] < df['ib_l'])

        # 5. Reversal bar quality: close must be in upper 40% (buy) / lower 40% (sell) of bar range
        bar_range = (df['high'] - df['low']).replace(0, np.nan)
        close_position = (df['close'] - df['low']) / bar_range  # 0=bottom, 1=top
        quality_buy  = close_position >= (1.0 - rev_quality_pct)  # close in top 40%
        quality_sell = close_position <= rev_quality_pct           # close in bottom 40%

        # 6. ADX gate
        try:
            adx_df    = ta.adx(df['high'], df['low'], df['close'], length=14)
            df['adx'] = adx_df["ADX_14"]
        except Exception:
            df['adx'] = 15.0
        not_trending = df['adx'] < adx_max

        # 7. RSI zone filter
        df['rsi']  = ta.rsi(df['close'], length=rsi_p)
        rsi_buy_ok  = (df['rsi'] >= rsi_long_min)  & (df['rsi'] <= rsi_long_max)
        rsi_sell_ok = (df['rsi'] >= rsi_short_min) & (df['rsi'] <= rsi_short_max)

        # 8. EMA50 macro alignment
        ema50 = ta.ema(df['close'], length=50)

        df['signal'] = 0
        df.loc[
            df['condition_buy'] & not_trending & rsi_buy_ok & quality_buy & (df['close'] > ema50),
            'signal'
        ] = 1
        df.loc[
            df['condition_sell'] & not_trending & rsi_sell_ok & quality_sell & (df['close'] < ema50),
            'signal'
        ] = -1

        # 9. Cooldown filter
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
