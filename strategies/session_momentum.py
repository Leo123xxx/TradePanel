import pandas as pd
import ta_compat as ta
from strategies.base_strategy import BaseStrategy

APPROVED_PAIRS = ["EURUSD", "GBPUSD", "XAUUSD"]
APPROVED_TIMEFRAMES = ["H1"]

class SessionMomentumStrategy(BaseStrategy):
    """
    Session-Based Momentum (London Open + NY Open) v3.

    v3 upgrades (2026-05-01) — targeting 70%+ WR:
    - Volume threshold raised 1.2x -> 1.5x: only enter on strong volume spikes
    - ADX minimum raised 25 -> 28: tighter trending regime requirement
    - RSI gate tightened 52/48 -> 57/43: stronger momentum confirmation
    - Breakout distance filter added: close must be >= 0.3x ATR above/below range
      to avoid entering on micro-breakouts that reverse immediately
    """

    def __init__(self, params: dict = None):
        if params is None:
            params = {
                "london_start_utc":      7,
                "london_end_utc":       10,
                "ny_start_utc":         13,
                "ny_end_utc":           16,
                "pre_session_bars":     12,
                "atr_period":           14,
                "tp_atr_mult":           2.0,
                "sl_atr_mult":           0.8,
                "min_adx_filter":       25,    # loosened 28→25
                "vol_threshold_mult":    1.2,   # loosened 1.5→1.2
                "fast_ema":             20,
                "slow_ema":             50,
                "ema200_period":       200,
                "rsi_period":           14,
                "rsi_long_min":         54,    # loosened 57→54
                "rsi_short_max":        46,    # loosened 43→46
                "breakout_atr_min":      0.15, # loosened 0.3→0.15
                "use_partial_tp":        False,
            }
        super().__init__(
            name="Session_Momentum",
            category="Session-Based / Momentum",
            params=params,
            regime=["TRENDING"],
            timeframes=APPROVED_TIMEFRAMES,
            pairs=APPROVED_PAIRS
        )

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()

        lon_start       = self.params.get("london_start_utc",   7)
        lon_end         = self.params.get("london_end_utc",    10)
        ny_start        = self.params.get("ny_start_utc",      13)
        ny_end          = self.params.get("ny_end_utc",        16)
        pre_bars        = self.params.get("pre_session_bars",  12)
        fast_ema_p      = self.params.get("fast_ema",          20)
        slow_ema_p      = self.params.get("slow_ema",          50)
        adx_min         = self.params.get("min_adx_filter",    28)
        vol_mult        = self.params.get("vol_threshold_mult",  1.5)
        ema200_p        = self.params.get("ema200_period",     200)
        rsi_p           = self.params.get("rsi_period",         14)
        rsi_long_min    = self.params.get("rsi_long_min",       57)
        rsi_short_max   = self.params.get("rsi_short_max",      43)
        bo_atr_min      = self.params.get("breakout_atr_min",    0.3)

        # ── Indicators ────────────────────────────────────────────────────────
        df['ema_fast'] = ta.ema(df['close'], length=fast_ema_p)
        df['ema_slow'] = ta.ema(df['close'], length=slow_ema_p)
        df['ema200']   = ta.ema(df['close'], length=ema200_p)
        df['rsi']      = ta.rsi(df['close'], length=rsi_p)
        df['atr']      = ta.atr(df['high'], df['low'], df['close'], length=14)

        adx_df    = ta.adx(df['high'], df['low'], df['close'], length=14)
        df['adx'] = adx_df["ADX_14"]

        # ── Volume confirmation ───────────────────────────────────────────────
        df['avg_vol'] = df['tick_volume'].rolling(window=20).mean().shift(1)
        df['vol_ok']  = df['tick_volume'] >= (df['avg_vol'] * vol_mult)

        # ── EMA trend + macro gates ───────────────────────────────────────────
        trend_up   = df['ema_fast'] > df['ema_slow']
        trend_down = df['ema_fast'] < df['ema_slow']
        macro_up   = df['close'] > df['ema200']
        macro_down = df['close'] < df['ema200']

        # ── RSI momentum gate ─────────────────────────────────────────────────
        rsi_bull_ok = df['rsi'] > rsi_long_min
        rsi_bear_ok = df['rsi'] < rsi_short_max

        # ── Pre-session range ─────────────────────────────────────────────────
        df['pre_range_high'] = df['high'].rolling(window=pre_bars).max().shift(1)
        df['pre_range_low']  = df['low'].rolling(window=pre_bars).min().shift(1)

        # ── Breakout distance gate: close must be >= bo_atr_min * ATR beyond range ──
        df['bo_dist_long']  = df['close'] - df['pre_range_high']
        df['bo_dist_short'] = df['pre_range_low'] - df['close']
        bo_dist_ok_long  = df['bo_dist_long']  >= bo_atr_min * df['atr']
        bo_dist_ok_short = df['bo_dist_short'] >= bo_atr_min * df['atr']

        # ── Session mask ──────────────────────────────────────────────────────
        try:
            hour = df.index.hour
            in_session = (
                ((hour >= lon_start) & (hour < lon_end)) |
                ((hour >= ny_start)  & (hour < ny_end))
            )
        except Exception:
            in_session = True

        # ── Signals ───────────────────────────────────────────────────────────
        df['signal'] = 0

        long_cond = (
            in_session
            & (df['close'] > df['pre_range_high'])
            & bo_dist_ok_long
            & (df['adx'] >= adx_min)
            & trend_up
            & macro_up
            & df['vol_ok']
            & rsi_bull_ok
        )

        short_cond = (
            in_session
            & (df['close'] < df['pre_range_low'])
            & bo_dist_ok_short
            & (df['adx'] >= adx_min)
            & trend_down
            & macro_down
            & df['vol_ok']
            & rsi_bear_ok
        )

        df.loc[long_cond,  'signal'] =  1
        df.loc[short_cond, 'signal'] = -1

        # Suppress consecutive duplicates
        df.loc[(df['signal'] ==  1) & (df['signal'].shift(1) ==  1), 'signal'] = 0
        df.loc[(df['signal'] == -1) & (df['signal'].shift(1) == -1), 'signal'] = 0

        return df

    def validate_params(self) -> bool:
        return True
