import numpy as np
import pandas as pd
import ta_compat as ta
from strategies.base_strategy import BaseStrategy


class MultiEmaCryptoScalper(BaseStrategy):
    """
    Multi-EMA Crypto Scalper -- LeoDeX Framework (2026-05-03)

    Entry Logic (LONG):
      1. Full EMA stack bullish: price > EMA9 > EMA21 > EMA55 > EMA200
      2. MACD(8,17,9) histogram positive AND rising (momentum confirmation)
      3. RSI(7) > 50 mid-band (overbought gate: RSI < rsi_max_long)
      4. ADX > 25 (trending, not ranging)
      5. Optional killzone filter: London / NY AM / NY PM (SAST times)
      6. CVD proxy positive over last N bars (cumulative directional pressure)
      (SHORT = mirror conditions)

    Exit: ATR-based SL/TP (sl_atr_mult=1.0, tp_atr_mult=3.0 -> 3:1 RR for crypto)

    SAST = UTC+2. Killzone hours:
      London AM  : 09:00 - 11:00
      NY AM      : 17:00 - 19:00
      NY PM      : 21:00 - 23:00
    """

    _KILLZONES_SAST = [
        (9,  11),
        (17, 19),
        (21, 23),
    ]

    def __init__(self, params: dict = None):
        defaults = {
            "ema_fast":       9,
            "ema_mid":       21,
            "ema_slow":      55,
            "ema_200":      200,
            "macd_fast":      8,
            "macd_slow":     17,
            "macd_signal":    9,
            "rsi_period":     7,
            "rsi_long_min":  50,
            "rsi_long_max":  80,
            "rsi_short_max": 50,
            "rsi_short_min": 20,
            "adx_period":    20,
            "adx_min":       25,
            "atr_period":    14,
            "sl_atr_mult":    1.0,
            "tp_atr_mult":    2.0,
            "cvd_lookback":   8,
            "use_killzone": True,
            "cooldown_bars": 10,
            "use_partial_tp": False,
        }
        if params:
            defaults.update(params)
        super().__init__(
            name="Multi_EMA_Crypto_Scalper",
            category="Crypto Scalping",
            params=defaults,
        )

    def validate_params(self) -> bool:
        p = self.params
        return (
            p["ema_fast"] < p["ema_mid"] < p["ema_slow"] < p["ema_200"]
            and p["macd_fast"] < p["macd_slow"]
            and p["adx_min"] > 0
        )

    @staticmethod
    def _in_killzone(hour_series, killzones):
        hours = np.asarray(hour_series)
        mask = np.zeros(len(hours), dtype=bool)
        for start, end in killzones:
            mask |= (hours >= start) & (hours < end)
        return mask  # numpy bool array -- avoids DatetimeIndex/RangeIndex mismatch

    @staticmethod
    def _cvd(df, lookback):
        direction = np.where(df["close"] >= df["open"], 1.0, -1.0)
        delta = df["tick_volume"].astype(float) * direction
        return delta.rolling(lookback).sum()

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        p = self.params
        df = df.copy()
        df["signal"] = 0

        if len(df) < max(p["ema_200"], 50):
            return df

        df["ema9"]   = ta.ema(df["close"], length=p["ema_fast"])
        df["ema21"]  = ta.ema(df["close"], length=p["ema_mid"])
        df["ema55"]  = ta.ema(df["close"], length=p["ema_slow"])
        df["ema200"] = ta.ema(df["close"], length=p["ema_200"])

        macd_df = ta.macd(
            df["close"],
            fast=p["macd_fast"],
            slow=p["macd_slow"],
            signal=p["macd_signal"],
        )
        hist_col = [c for c in macd_df.columns if "hist" in c.lower()]
        df["macd_hist"] = macd_df[hist_col[0]] if hist_col else macd_df.iloc[:, -1]

        df["rsi"] = ta.rsi(df["close"], length=p["rsi_period"])

        adx_df  = ta.adx(df["high"], df["low"], df["close"], length=p["adx_period"])
        adx_col = [c for c in adx_df.columns if c.lower().startswith("adx_")]
        df["adx"] = adx_df[adx_col[0]] if adx_col else adx_df.iloc[:, 0]

        df["atr"]      = ta.atr(df["high"], df["low"], df["close"], length=p["atr_period"])
        df["cvd_roll"] = self._cvd(df, p["cvd_lookback"])

        if p["use_killzone"]:
            kz = self._in_killzone(df.index.hour, self._KILLZONES_SAST)
        else:
            kz = np.ones(len(df), dtype=bool)

        macd_rising  = df["macd_hist"] > df["macd_hist"].shift(1)
        macd_falling = df["macd_hist"] < df["macd_hist"].shift(1)

        bull_stack = (
            (df["close"] > df["ema9"]) &
            (df["ema9"]  > df["ema21"]) &
            (df["ema21"] > df["ema55"]) &
            (df["ema55"] > df["ema200"])
        )
        bear_stack = (
            (df["close"] < df["ema9"]) &
            (df["ema9"]  < df["ema21"]) &
            (df["ema21"] < df["ema55"]) &
            (df["ema55"] < df["ema200"])
        )

        long_cond = (
            bull_stack.values &
            (df["macd_hist"] > 0).values & macd_rising.values &
            (df["rsi"] > p["rsi_long_min"]).values &
            (df["rsi"] < p["rsi_long_max"]).values &
            (df["adx"] > p["adx_min"]).values &
            (df["cvd_roll"] > 0).values &
            kz &
            df["atr"].notna().values
        )
        short_cond = (
            bear_stack.values &
            (df["macd_hist"] < 0).values & macd_falling.values &
            (df["rsi"] < p["rsi_short_max"]).values &
            (df["rsi"] > p["rsi_short_min"]).values &
            (df["adx"] > p["adx_min"]).values &
            (df["cvd_roll"] < 0).values &
            kz &
            df["atr"].notna().values
        )

        cooldown = p["cooldown_bars"]
        last_bar = -cooldown - 1
        signals  = np.zeros(len(df), dtype=int)
        for i in range(len(df)):
            if long_cond[i] and (i - last_bar) > cooldown:
                signals[i] = 1
                last_bar = i
            elif short_cond[i] and (i - last_bar) > cooldown:
                signals[i] = -1
                last_bar = i

        df["signal"]      = signals
        df["sl_distance"] = df["atr"] * p["sl_atr_mult"]
        df["tp_distance"] = df["atr"] * p["tp_atr_mult"]
        return df
