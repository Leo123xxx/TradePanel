import pandas as pd
import ta_compat as ta
from strategies.base_strategy import BaseStrategy

class GoldMomentumBreakoutStrategy(BaseStrategy):
    """
    Gold Momentum Breakout Strategy.
    Identifies a sustained squeeze (consolidation) in Bollinger Bands, and a breakout
    confirmed by RSI showing momentum in the breakout direction.

    v2 upgrades (2026-04-29) — targeting 70%+ WR from 60.9%:
    - RSI thresholds tightened: 55→60 (buy), 45→40 (sell) — reduces weak-momentum entries
    - EMA200 macro trend filter: only buy above EMA200, only sell below EMA200
    - ADX gate (default 25): confirms we are in a genuine trending/impulsive move
    - Volume gate (vol_threshold_mult): requires above-average tick volume on breakout bar

    squeeze_threshold_pct tightened to 0.03 (was 0.05) and must persist for 3 bars
    to reduce overtrading (was generating 2400+ trades).
    RR = 3:1 (tp_atr_mult=3.0, sl_atr_mult=1.0).
    """

    def __init__(self, params: dict = None):
        if params is None:
            params = {
                "bb_length": 20,
                "bb_std": 2.0,
                "rsi_length": 14,
                "rsi_buy_min": 60,              # tightened: was 55 → fewer but higher-quality entries
                "rsi_sell_max": 40,             # tightened: was 45
                "squeeze_threshold_pct": 0.03,  # tighter squeeze: was 0.05
                "squeeze_lookback": 3,          # squeeze must persist N bars
                "tp_atr_mult": 3.0,             # RR 3:1
                "sl_atr_mult": 1.0,
                "atr_period": 14,
                "cooldown_bars": 12,            # was generating 1693+ trades — throttle
                "adx_min": 25,                  # ADX gate — confirms trending impulse
                "vol_threshold_mult": 1.5,      # Volume gate — breakout bar must have above-avg vol
                "ema200_period": 200,           # Macro trend filter — only trade with EMA200
            }
        super().__init__("Gold_Momentum_Breakout", "Breakout", params)

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()

        bb_length = self.params.get("bb_length", 20)
        bb_std = self.params.get("bb_std", 2.0)
        rsi_length = self.params.get("rsi_length", 14)
        rsi_buy_min = self.params.get("rsi_buy_min", 60)
        rsi_sell_max = self.params.get("rsi_sell_max", 40)
        squeeze_threshold_pct = self.params.get("squeeze_threshold_pct", 0.03)
        squeeze_lookback = self.params.get("squeeze_lookback", 3)
        adx_min = self.params.get("adx_min", 25)
        vol_mult = self.params.get("vol_threshold_mult", 0.0)
        ema200_p = self.params.get("ema200_period", 200)

        # Bollinger Bands
        bb = ta.bbands(df['close'], length=bb_length, std=bb_std)
        if bb is None or bb.empty:
            df['signal'] = 0
            return df

        bb_lower_col = bb.columns[0]  # L
        bb_mid_col = bb.columns[1]    # M
        bb_upper_col = bb.columns[2]  # U

        df = pd.concat([df, bb], axis=1)

        # Bollinger Band Width as % of middle band
        df['bb_width_pct'] = (df[bb_upper_col] - df[bb_lower_col]) / df[bb_mid_col]

        # RSI
        df['rsi'] = ta.rsi(df['close'], length=rsi_length)

        # EMA200 macro trend filter — only trade in direction of dominant trend
        df['ema200'] = ta.ema(df['close'], length=ema200_p)
        macro_up   = df['close'] > df['ema200']
        macro_down = df['close'] < df['ema200']

        # ADX gate — require trending/impulsive market structure
        adx_df    = ta.adx(df['high'], df['low'], df['close'], length=14)
        df['adx'] = adx_df["ADX_14"]
        trend_strength = df['adx'] >= adx_min

        # Volume gate — breakout bar must have above-average tick volume
        if vol_mult > 0 and 'tick_volume' in df.columns:
            df['avg_vol'] = df['tick_volume'].rolling(window=20).mean()
            vol_ok = df['tick_volume'] >= (df['avg_vol'] * vol_mult)
        else:
            vol_ok = True

        # ATR rolling average (for Layer 3)
        df['atr']     = __import__('ta_compat').atr(df['high'], df['low'], df['close'], length=14)
        df['atr_avg'] = df['atr'].rolling(20).mean()

        df['signal'] = 0

        # Sustained squeeze: bb_width must be < threshold for N consecutive bars
        in_squeeze = df['bb_width_pct'] < squeeze_threshold_pct
        sustained_squeeze = in_squeeze.rolling(window=squeeze_lookback).min().shift(1).fillna(0).astype(bool)

        # Buy: breakout above upper band + squeeze + RSI momentum + macro trend + ADX + volume
        buy_cond = (
            (df['close'] > df[bb_upper_col]) &
            sustained_squeeze &
            (df['rsi'] > rsi_buy_min) &
            macro_up &
            trend_strength &
            vol_ok
        )
        sell_cond = (
            (df['close'] < df[bb_lower_col]) &
            sustained_squeeze &
            (df['rsi'] < rsi_sell_max) &
            macro_down &
            trend_strength &
            vol_ok
        )

        # Layer 2 — Candle body ratio (genuine breakout bar, not a wick)
        buy_cond, sell_cond = self.apply_body_ratio_filter(df, buy_cond, sell_cond)
        # Layer 3 — ATR ceiling (skip news explosions that reverse immediately)
        buy_cond, sell_cond = self.apply_atr_ceiling(df, buy_cond, sell_cond)

        df.loc[buy_cond,  'signal'] = 1
        df.loc[sell_cond, 'signal'] = -1

        # Cooldown filter — suppress signals within N bars of last signal
        cooldown = self.params.get("cooldown_bars", 12)
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
        return self.params.get("bb_length", 0) > 0 and self.params.get("rsi_length", 0) > 0
