import numpy as np
import pandas as pd
import ta_compat as ta
from strategies.base_strategy import BaseStrategy


class PowerOf3AMD(BaseStrategy):
    """
    Power of 3 -- Accumulation / Manipulation / Distribution (2026-05-03)

    ICT concept: Smart Money operates in 3 phases within each 24-hour cycle:
      A -- ACCUMULATION  (Asian session):  Range forms, price coils
      M -- MANIPULATION  (London open):    Price sweeps beyond Asian range to
                                           trap retail breakout traders
      D -- DISTRIBUTION  (NY session):     True directional move in the OPPOSITE
                                           direction of the manipulation sweep

    Implementation (all times SAST = UTC+2):
      Asian Range  :  00:00 - 07:00  rolling high/low for today
      London Sweep :  07:00 - 10:00  detect if price pierces Asian H/L
                                     by >= sweep_buffer_atr AND rejects
      NY Entry     :  10:00 - 17:00  first signal bar after confirmed sweep
                                     in OPPOSITE direction of sweep
      EMA200 bias  :  macro filter, same direction as NY distribution move

    Signal:
      - Asian range swept HIGH (bear trap) -> SELL in NY session
      - Asian range swept LOW  (bull trap) -> BUY  in NY session
      - SL: 1.5 ATR  TP: 4.5 ATR  (3:1 RR)

    Best timeframes: M15, H1
    Pairs: BTCUSD, ETHUSD
    """

    ASIAN_START  =  0
    ASIAN_END    =  7
    LONDON_START =  7
    LONDON_END   = 10
    NY_START     = 10
    NY_END       = 17

    def __init__(self, params: dict = None):
        defaults = {
            "ema200_period":      200,
            "atr_period":          14,
            "sl_atr_mult":          1.5,
            "tp_atr_mult":          2.0,
            "sweep_buffer_atr":     0.2,
            "asian_min_range_atr":  0.4,
            "cooldown_bars":        12,
            "require_ema_bias":   False,
            "use_partial_tp": False,
        }
        if params:
            defaults.update(params)
        super().__init__(
            name="Power_of_3_AMD",
            category="Crypto ICT",
            params=defaults,
        )

    def validate_params(self) -> bool:
        p = self.params
        return (
            p["ema200_period"] > 0
            and p["sweep_buffer_atr"] > 0
            and p["tp_atr_mult"] >= 1.5
            and self.ASIAN_END <= self.LONDON_START <= self.NY_START
        )

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        p = self.params
        df = df.copy()
        df["signal"] = 0

        if len(df) < p["ema200_period"] + 48:
            return df

        df["ema200"] = ta.ema(df["close"], length=p["ema200_period"])
        df["atr"]    = ta.atr(df["high"], df["low"], df["close"], length=p["atr_period"])

        high_arr   = df["high"].values
        low_arr    = df["low"].values
        close_arr  = df["close"].values
        atr_arr    = df["atr"].values
        ema200_arr = df["ema200"].values
        hours      = df.index.hour
        dates      = df.index.date

        signals    = np.zeros(len(df), dtype=int)
        cool       = p["cooldown_bars"]
        last_sig   = -cool - 1
        day_state  = {}

        for i in range(p["ema200_period"], len(df)):
            if np.isnan(atr_arr[i]) or np.isnan(ema200_arr[i]):
                continue

            today   = dates[i]
            hour    = int(hours[i])
            atr_val = float(atr_arr[i])

            # Phase A: build Asian range
            if self.ASIAN_START <= hour < self.ASIAN_END:
                if today not in day_state:
                    day_state[today] = {
                        "asian_high": float(high_arr[i]),
                        "asian_low":  float(low_arr[i]),
                        "sweep_dir":  None,
                        "confirmed":  False,
                    }
                else:
                    s = day_state[today]
                    s["asian_high"] = max(s["asian_high"], float(high_arr[i]))
                    s["asian_low"]  = min(s["asian_low"],  float(low_arr[i]))
                continue

            if today not in day_state:
                continue

            state       = day_state[today]
            asian_high  = state["asian_high"]
            asian_low   = state["asian_low"]
            asian_range = asian_high - asian_low

            if asian_range < atr_val * p["asian_min_range_atr"]:
                continue

            sweep_buf = atr_val * p["sweep_buffer_atr"]

            # Phase M: detect manipulation sweep (London session)
            if self.LONDON_START <= hour < self.LONDON_END:
                if state["sweep_dir"] is None:
                    # High swept (bear trap) -> SELL setup
                    if (float(high_arr[i]) > asian_high + sweep_buf
                            and float(close_arr[i]) <= asian_high):
                        state["sweep_dir"] = 1
                        state["confirmed"] = True
                    # Low swept (bull trap) -> BUY setup
                    elif (float(low_arr[i]) < asian_low - sweep_buf
                            and float(close_arr[i]) >= asian_low):
                        state["sweep_dir"] = -1
                        state["confirmed"] = True
                continue

            # Phase D: NY distribution entry
            if self.NY_START <= hour < self.NY_END:
                if not state["confirmed"]:
                    continue
                if (i - last_sig) <= cool:
                    continue

                # Opposite direction to sweep
                trade_dir = -state["sweep_dir"]  # high swept -> SELL; low swept -> BUY

                if p["require_ema_bias"]:
                    bull_bias = bool(close_arr[i] > ema200_arr[i])
                    bear_bias = bool(close_arr[i] < ema200_arr[i])
                    if trade_dir == 1 and not bull_bias:
                        continue
                    if trade_dir == -1 and not bear_bias:
                        continue

                signals[i]        = trade_dir
                last_sig          = i
                state["confirmed"] = False  # one entry per AMD cycle

        df["signal"]      = signals
        df["sl_distance"] = df["atr"] * p["sl_atr_mult"]
        df["tp_distance"] = df["atr"] * p["tp_atr_mult"]
        return df
