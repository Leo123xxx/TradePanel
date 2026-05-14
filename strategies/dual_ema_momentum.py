import pandas as pd
import ta_compat as ta
from strategies.base_strategy import BaseStrategy

class DualEMAMomentum(BaseStrategy):
    """
    Dual EMA Momentum Continuity v3.
    Trend: Full EMA ribbon alignment + ADX rising gate.
    Signal: Engulfing candle in trend direction.
    RR = 2:1 (tp_atr_mult=2.0, sl_atr_mult=1.0).

    v3 upgrades (2026-05-01) — targeting 70%+ WR:
    - Full ribbon alignment: EMA15 > EMA50 > EMA100 > EMA200 for longs
      (all four must agree). Partial alignment (EMA15/100 only) allows counter-trend entries.
    - ADX rising gate: ADX must be higher than previous bar (trend strengthening).
      Catches engulfings at the start of a trend impulse, not at exhaustion.
    """

    def __init__(self, params: dict = None):
        if params is None:
            params = {
                "fast_ema":           15,
                "mid_ema":            50,   # NEW: full ribbon
                "slow_ema":          100,
                "ema200_period":     200,
                "adx_min":            22,   # loosened 25→22
                "adx_rising":        False, # loosened True→False: rising ADX kills too many setups
                "atr_period":         14,
                "tp_atr_mult":         2.0,
                "sl_atr_mult":         1.0,
                "rsi_period":         14,
                "rsi_long_min":       55,
                "rsi_short_max":      45,
                "vol_threshold_mult":  1.2,
            }
        super().__init__(
            name="Dual_EMA_Momentum",
            category="Trend Following",
            params=params,
            regime=["TRENDING"],
            timeframes=["H1", "H4"],
            pairs=["BTCUSD", "ETHUSD", "EURUSD"]
        )

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()

        fast_p        = self.params.get('fast_ema',          15)
        mid_p         = self.params.get('mid_ema',           50)
        slow_p        = self.params.get('slow_ema',         100)
        ema200_p      = self.params.get('ema200_period',    200)
        adx_min       = self.params.get('adx_min',           25)
        adx_rising    = self.params.get('adx_rising',       True)
        rsi_p         = self.params.get('rsi_period',        14)
        rsi_long_min  = self.params.get('rsi_long_min',      55)
        rsi_short_max = self.params.get('rsi_short_max',     45)
        vol_mult      = self.params.get('vol_threshold_mult', 1.2)

        df['ema_fast'] = ta.ema(df['close'], length=fast_p)
        df['ema_mid']  = ta.ema(df['close'], length=mid_p)
        df['ema_slow'] = ta.ema(df['close'], length=slow_p)
        df['ema200']   = ta.ema(df['close'], length=ema200_p)

        adx_df    = ta.adx(df['high'], df['low'], df['close'], length=14)
        df['adx'] = adx_df.iloc[:, 0]

        df['rsi'] = ta.rsi(df['close'], length=rsi_p)

        # Full ribbon alignment
        ribbon_up   = (
            (df['ema_fast'] > df['ema_mid'])
            & (df['ema_mid'] > df['ema_slow'])
            & (df['ema_slow'] > df['ema200'])
        )
        ribbon_down = (
            (df['ema_fast'] < df['ema_mid'])
            & (df['ema_mid'] < df['ema_slow'])
            & (df['ema_slow'] < df['ema200'])
        )

        # ADX gate: above minimum AND rising (trend strengthening)
        adx_above_min = df['adx'] > adx_min
        if adx_rising:
            adx_rising_now = df['adx'] > df['adx'].shift(1)
        else:
            adx_rising_now = True

        adx_ok = adx_above_min & adx_rising_now

        # Volume gate
        if vol_mult > 0 and 'tick_volume' in df.columns:
            df['vol_avg'] = df['tick_volume'].rolling(window=20).mean()
            vol_ok = df['tick_volume'] >= (df['vol_avg'] * vol_mult)
        else:
            vol_ok = True

        # Engulfing detection
        df['is_bull_engulfing'] = (
            (df['close'] > df['open']) &
            (df['open'] <= df['close'].shift(1)) &
            (df['close'] > df['open'].shift(1)) &
            (df['open'].shift(1) > df['close'].shift(1))
        )
        df['is_bear_engulfing'] = (
            (df['close'] < df['open']) &
            (df['open'] >= df['close'].shift(1)) &
            (df['close'] < df['open'].shift(1)) &
            (df['open'].shift(1) < df['close'].shift(1))
        )

        df['atr']     = ta.atr(df['high'], df['low'], df['close'], length=14)
        df['atr_avg'] = df['atr'].rolling(20).mean()

        df['signal'] = 0

        buy_cond = (
            ribbon_up &
            adx_ok &
            (df['rsi'] > rsi_long_min) &
            vol_ok &
            df['is_bull_engulfing']
        )
        sell_cond = (
            ribbon_down &
            adx_ok &
            (df['rsi'] < rsi_short_max) &
            vol_ok &
            df['is_bear_engulfing']
        )

        # Layer 3 — ATR ceiling (ribbon flips on news gaps are unreliable)
        buy_cond, sell_cond = self.apply_atr_ceiling(df, buy_cond, sell_cond)
        # Layer 5 — Previous-bar momentum (confirm the bar before the engulf is directional)
        buy_cond, sell_cond = self.apply_prev_bar_momentum(df, buy_cond, sell_cond)

        df.loc[buy_cond,  'signal'] = 1
        df.loc[sell_cond, 'signal'] = -1

        return df

    def validate_params(self) -> bool:
        return self.params['fast_ema'] < self.params['slow_ema']
