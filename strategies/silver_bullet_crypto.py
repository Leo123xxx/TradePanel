import numpy as np
import pandas as pd
import ta_compat as ta
from strategies.base_strategy import BaseStrategy


class SilverBulletCrypto(BaseStrategy):
    """
    Silver Bullet Crypto -- ICT Killzone + Liquidity Sweep + FVG (2026-05-03)

    Concept (from LeoDeX PDF -- ICT Silver Bullet):
      1. Wait for a defined KILLZONE window (high-liquidity session)
      2. Confirm EMA200 HTF bias (bull bias = price above EMA200)
      3. Detect a LIQUIDITY SWEEP: price pierces the previous session
         high (for shorts) or low (for longs) by >sweep_buffer ATR,
         then closes back within the range (rejection wick)
      4. Identify a FAIR VALUE GAP (FVG): 3-candle gap where
         high[i-2] < low[i] = bullish FVG, low[i-2] > high[i] = bearish FVG
      5. Enter when price returns to fill the FVG after the sweep

    SAST killzones (UTC+2):
      London AM  : 09:00 - 10:00
      NY AM      : 17:00 - 18:00

    SL: 1.2 x ATR; TP: 3.5 x ATR (3:1 minimum RR for crypto).
    """

    _KILLZONES_SAST = [
        (9,  10),
        (17, 18),
    ]

    def __init__(self, params: dict = None):
        defaults = {
            "ema200_period":     200,
            "atr_period":         14,
            "sl_atr_mult":         1.2,
            "tp_atr_mult":         2.0,
            "sweep_buffer_atr":    0.15,
            "session_lookback":    8,
            "fvg_max_age_bars":   12,
            "cooldown_bars":       8,
            "use_partial_tp": False,
        }
        if params:
            defaults.update(params)
        super().__init__(
            name="Silver_Bullet_Crypto",
            category="Crypto ICT",
            params=defaults,
        )

    def validate_params(self) -> bool:
        p = self.params
        return (
            p["ema200_period"] > 0
            and p["sweep_buffer_atr"] > 0
            and p["tp_atr_mult"] >= 1.5
        )

    @staticmethod
    def _in_killzone(hour_series, killzones) -> pd.Series:
        hours = np.asarray(hour_series)
        mask = np.zeros(len(hours), dtype=bool)
        for start, end in killzones:
            mask |= (hours >= start) & (hours < end)
        return mask  # numpy bool array — avoids DatetimeIndex/RangeIndex mismatch

    @staticmethod
    def _fvg_bullish(high, low, i, lookback):
        """Return True if a bullish FVG (high[j-2] < low[j]) exists in last lookback bars."""
        for j in range(max(2, i - lookback), i + 1):
            if high[j - 2] < low[j]:
                return True
        return False

    @staticmethod
    def _fvg_bearish(high, low, i, lookback):
        """Return True if a bearish FVG (low[j-2] > high[j]) exists in last lookback bars."""
        for j in range(max(2, i - lookback), i + 1):
            if low[j - 2] > high[j]:
                return True
        return False

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        p = self.params
        df = df.copy()
        df["signal"] = 0

        min_bars = p["ema200_period"] + p["session_lookback"] + 5
        if len(df) < min_bars:
            return df

        df["ema200"] = ta.ema(df["close"], length=p["ema200_period"])
        df["atr"]    = ta.atr(df["high"], df["low"], df["close"], length=p["atr_period"])

        kz_mask    = self._in_killzone(df.index.hour, self._KILLZONES_SAST)
        high_arr   = df["high"].values
        low_arr    = df["low"].values
        close_arr  = df["close"].values
        atr_arr    = df["atr"].values
        ema200_arr = df["ema200"].values

        lb     = p["session_lookback"]
        fvg_lb = p["fvg_max_age_bars"]
        buf    = p["sweep_buffer_atr"]
        cool   = p["cooldown_bars"]

        signals  = np.zeros(len(df), dtype=int)
        last_sig = -cool - 1

        for i in range(p["ema200_period"] + lb, len(df)):
            if np.isnan(atr_arr[i]) or np.isnan(ema200_arr[i]):
                continue
            if not kz_mask[i]:
                continue
            if (i - last_sig) <= cool:
                continue

            atr_val   = atr_arr[i]
            sweep_min = buf * atr_val
            sess_high = float(np.max(high_arr[i - lb: i]))
            sess_low  = float(np.min(low_arr[i - lb: i]))
            bull_bias = bool(close_arr[i] > ema200_arr[i])
            bear_bias = bool(close_arr[i] < ema200_arr[i])

            if bull_bias:
                if (low_arr[i] < sess_low
                        and (sess_low - low_arr[i]) >= sweep_min
                        and close_arr[i] > sess_low):
                    if self._fvg_bullish(high_arr, low_arr, i, fvg_lb):
                        signals[i] = 1
                        last_sig = i
            elif bear_bias:
                if (high_arr[i] > sess_high
                        and (high_arr[i] - sess_high) >= sweep_min
                        and close_arr[i] < sess_high):
                    if self._fvg_bearish(high_arr, low_arr, i, fvg_lb):
                        signals[i] = -1
                        last_sig = i

        df["signal"]      = signals
        df["sl_distance"] = df["atr"] * p["sl_atr_mult"]
        df["tp_distance"] = df["atr"] * p["tp_atr_mult"]
        return df
