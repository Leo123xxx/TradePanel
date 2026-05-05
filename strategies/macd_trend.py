import pandas as pd
import ta_compat as ta
from strategies.base_strategy import BaseStrategy

class MACDTrendStrategy(BaseStrategy):
    """
    MACD Trend Follower v3.

    v3 upgrades (2026-05-01) — targeting 70%+ WR on EURUSD:
    - MACD histogram slope filter: histogram must be rising for 2 consecutive bars
      before entry. Catches early crossovers in flat histogram zones (EURUSD H1 issue).
    """

    def __init__(self, params: dict = None):
        if params is None:
            params = {
                "macd_fast":         12,
                "macd_slow":         26,
                "macd_signal":        9,
                "adx_length":        14,
                "adx_threshold":     25,   # loosened 28→25: catch more trends
                "tp_atr_mult":        3.0,
                "sl_atr_mult":        1.0,
                "atr_period":        14,
                "rsi_period":        14,
                "rsi_long_min":      55,
                "rsi_short_max":     45,
                "ema200_period":    200,
                "hist_slope_bars":    1,   # loosened 2→1: one rising bar sufficient   # NEW: histogram must rise for N bars pre-entry
            }
        super().__init__("MACD_Trend", "Trend Following", params)

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()

        macd_fast      = self.params.get("macd_fast",       12)
        macd_slow      = self.params.get("macd_slow",       26)
        macd_signal    = self.params.get("macd_signal",      9)
        adx_length     = self.params.get("adx_length",      14)
        adx_threshold  = self.params.get("adx_threshold",   28)
        rsi_p          = self.params.get("rsi_period",      14)
        rsi_long_min   = self.params.get("rsi_long_min",    55)
        rsi_short_max  = self.params.get("rsi_short_max",   45)
        ema200_p       = self.params.get("ema200_period",  200)
        hist_slope_n   = self.params.get("hist_slope_bars",  2)

        # MACD
        macd_res = ta.macd(df['close'], fast=macd_fast, slow=macd_slow, signal=macd_signal)
        if macd_res is None or macd_res.empty:
            df['signal'] = 0
            return df

        macd_line_col   = macd_res.columns[0]
        signal_line_col = macd_res.columns[2]
        hist_col        = macd_res.columns[1]
        df = pd.concat([df, macd_res], axis=1)

        # ADX + DI
        adx_res = ta.adx(df['high'], df['low'], df['close'], length=adx_length)
        if adx_res is None or adx_res.empty:
            df['signal'] = 0
            return df

        adx_col = adx_res.columns[0]
        dmp_col = adx_res.columns[2]   # DI+
        dmn_col = adx_res.columns[3]   # DI-
        df = pd.concat([df, adx_res], axis=1)

        # EMA200 macro gate
        df['ema200'] = ta.ema(df['close'], length=ema200_p)
        macro_up   = df['close'] > df['ema200']
        macro_down = df['close'] < df['ema200']

        # RSI momentum gate
        df['rsi']    = ta.rsi(df['close'], length=rsi_p)
        rsi_ok_long  = df['rsi'] > rsi_long_min
        rsi_ok_short = df['rsi'] < rsi_short_max

        # MACD histogram slope: must rise for hist_slope_n consecutive bars
        # For longs: each bar's histogram > previous bar's histogram for N bars
        # For shorts: each bar's histogram < previous bar's histogram for N bars
        hist_slope_up   = pd.Series(True, index=df.index)
        hist_slope_down = pd.Series(True, index=df.index)
        for k in range(1, hist_slope_n + 1):
            hist_slope_up   = hist_slope_up   & (df[hist_col].shift(k - 1) > df[hist_col].shift(k))
            hist_slope_down = hist_slope_down & (df[hist_col].shift(k - 1) < df[hist_col].shift(k))

        df['signal']   = 0
        strong_trend   = df[adx_col] > adx_threshold

        # MACD crossover detection
        macd_cross_up = (
            (df[macd_line_col] > df[signal_line_col]) &
            (df[macd_line_col].shift(1) <= df[signal_line_col].shift(1))
        )
        macd_cross_down = (
            (df[macd_line_col] < df[signal_line_col]) &
            (df[macd_line_col].shift(1) >= df[signal_line_col].shift(1))
        )

        buy_cond = (
            macd_cross_up
            & hist_slope_up
            & strong_trend
            & (df[dmp_col] > df[dmn_col])
            & macro_up
            & rsi_ok_long
        )

        sell_cond = (
            macd_cross_down
            & hist_slope_down
            & strong_trend
            & (df[dmn_col] > df[dmp_col])
            & macro_down
            & rsi_ok_short
        )

        df.loc[buy_cond,  'signal'] =  1
        df.loc[sell_cond, 'signal'] = -1

        return df

    def validate_params(self) -> bool:
        return (self.params.get("macd_fast", 0) > 0 and
                self.params.get("macd_slow", 0) > self.params.get("macd_fast"))
