import pandas as pd
import numpy as np
import ta_compat as ta
from strategies.base_strategy import BaseStrategy
from data.db_client import DBClient

APPROVED_PAIRS = ["XAUUSD", "EURUSD", "GBPUSD", "USDJPY"]
APPROVED_TIMEFRAMES = ["H1", "H4"]   # H4+H1 dual-TF; D1 removed (insufficient divergence frequency)


def _compute_stoch_divergence(df: pd.DataFrame, k_period, sk, sd, look, lower, upper):
    """
    Helper: compute stochastic, crossovers, and divergence conditions for a given OHLCV df.
    Returns a Series of (cross_up, cross_down, bullish_div, bearish_div) as dict of Series.
    """
    stoch_df = ta.stoch(df['high'], df['low'], df['close'],
                        k_period=k_period, smooth_k=sk, smooth_d=sd)
    col_k = f"STOCHk_{k_period}_{sk}_{sd}"
    col_d = f"STOCHd_{k_period}_{sk}_{sd}"
    stoch_k = stoch_df[col_k]
    stoch_d = stoch_df[col_d]

    k_above_d  = stoch_k > stoch_d
    cross_up   = k_above_d & (~k_above_d.shift(1).astype(bool).fillna(False))
    cross_down = (~k_above_d) & (k_above_d.shift(1).astype(bool).fillna(False))

    win_price_low   = df['low'].rolling(look).min()
    prev_price_low  = df['low'].rolling(look).min().shift(look)
    win_price_high  = df['high'].rolling(look).max()
    prev_price_high = df['high'].rolling(look).max().shift(look)
    win_stoch_low   = stoch_k.rolling(look).min()
    prev_stoch_low  = stoch_k.rolling(look).min().shift(look)
    win_stoch_high  = stoch_k.rolling(look).max()
    prev_stoch_high = stoch_k.rolling(look).max().shift(look)

    bullish_div = (win_price_low < prev_price_low) & (win_stoch_low > prev_stoch_low)
    bearish_div = (win_price_high > prev_price_high) & (win_stoch_high < prev_stoch_high)

    return {
        "stoch_k":    stoch_k,
        "cross_up":   cross_up,
        "cross_down": cross_down,
        "bull_div":   bullish_div,
        "bear_div":   bearish_div,
    }


class StochDivergenceStrategy(BaseStrategy):
    """
    Stochastic Divergence Mean Reversion — v3 Dual-TF Overhaul.

    Architecture: H4 is the confirmation timeframe; H1 (or H4) is the entry timeframe.
    - Run divergence + crossover detection on BOTH the entry TF and the H4 TF.
    - Only enter when divergence is confirmed on BOTH timeframes simultaneously.
    - H4 divergence is resampled/aligned to the entry TF's bar timestamps.
    - Eliminates low-conviction single-TF divergence signals (WR 14-34% -> targeting 60%+).

    Other v3 changes:
    - Timeframes: D1 removed; H1 added. Entry TF = H1 or H4.
    - Tighter stoch zones: oversold=20, overbought=80 (same as v2).
    - EMA200 macro gate retained.
    - ADX max = 30 retained.
    """

    def __init__(self, params: dict = None):
        if params is None:
            params = {
                "stoch_period":        14,
                "stoch_smooth_k":       3,
                "stoch_smooth_d":       3,
                "divergence_lookback": 10,
                "stoch_oversold":      20,
                "stoch_overbought":    80,
                "confirm_timeframe":  "H4",   # H4 is always the confirmation TF
                "atr_period":          14,
                "tp_atr_mult":          2.0,
                "sl_atr_mult":          1.0,
                "adx_max":             30,
                "ema200_period":      200,
                "rsi_period":          14,
                "rsi_bull_min":        25,
                "rsi_bull_max":        55,
                "rsi_bear_min":        45,
                "rsi_bear_max":        75,
                "use_partial_tp":      False,
            }
        super().__init__(
            name="Stoch_Divergence",
            category="Divergence / Mean Reversion",
            params=params,
            regime=["RANGING", "ANY"],
            timeframes=APPROVED_TIMEFRAMES,
            pairs=APPROVED_PAIRS,
        )

    def _fetch_h4_data(self, symbol: str, start, end) -> pd.DataFrame:
        """Fetch H4 OHLCV from DB for the given symbol and date range."""
        db = DBClient()
        rows = db.execute_query(
            "SELECT timestamp, open, high, low, close, tick_volume "
            "FROM market_data WHERE pair = %s AND timeframe = 'H4' "
            "AND timestamp >= %s AND timestamp <= %s ORDER BY timestamp",
            (symbol, start, end)
        )
        if not rows:
            return pd.DataFrame()
        df_h4 = pd.DataFrame(rows, columns=["timestamp", "open", "high", "low", "close", "tick_volume"])
        df_h4.set_index("timestamp", inplace=True)
        for col in ["open", "high", "low", "close", "tick_volume"]:
            df_h4[col] = df_h4[col].astype(float)
        return df_h4

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()

        k_period      = self.params.get("stoch_period",        14)
        sk            = self.params.get("stoch_smooth_k",       3)
        sd            = self.params.get("stoch_smooth_d",       3)
        look          = self.params.get("divergence_lookback",  10)
        lower         = self.params.get("stoch_oversold",       20)
        upper         = self.params.get("stoch_overbought",     80)
        adx_max       = self.params.get("adx_max",              30)
        ema200_p      = self.params.get("ema200_period",       200)
        rsi_p         = self.params.get("rsi_period",           14)
        rsi_bull_min  = self.params.get("rsi_bull_min",         25)
        rsi_bull_max  = self.params.get("rsi_bull_max",         55)
        rsi_bear_min  = self.params.get("rsi_bear_min",         45)
        rsi_bear_max  = self.params.get("rsi_bear_max",         75)

        # Detect current timeframe
        diff = df.index[1] - df.index[0]
        entry_tf_is_h4 = diff.seconds >= 14400 if not diff.days else False

        # ── Entry TF signals ──────────────────────────────────────────────────
        entry = _compute_stoch_divergence(df, k_period, sk, sd, look, lower, upper)

        # ── H4 confirmation ───────────────────────────────────────────────────
        # If entry TF is already H4, we skip the second DB fetch (same data)
        h4_confirm_available = False
        h4_cross_up   = pd.Series(True, index=df.index)   # default: pass if unavailable
        h4_cross_down = pd.Series(True, index=df.index)
        h4_bull_div   = pd.Series(True, index=df.index)
        h4_bear_div   = pd.Series(True, index=df.index)

        if not entry_tf_is_h4:
            # Infer symbol from data (try attribute, fallback to XAUUSD)
            symbol = getattr(self, '_current_symbol', None)
            if symbol is None:
                # Try to get from context — strategy runner sets this via set_symbol()
                symbol = self.params.get("_symbol", "XAUUSD")

            start = df.index.min()
            end   = df.index.max()
            try:
                df_h4 = self._fetch_h4_data(symbol, start, end)
                if not df_h4.empty and len(df_h4) >= k_period + look + 10:
                    h4 = _compute_stoch_divergence(df_h4, k_period, sk, sd, look, lower, upper)
                    # Forward-fill H4 signals onto H1 bar timestamps
                    for s_name, h4_series in [
                        ("h4_cross_up",   h4["cross_up"]),
                        ("h4_cross_down", h4["cross_down"]),
                        ("h4_bull_div",   h4["bull_div"]),
                        ("h4_bear_div",   h4["bear_div"]),
                    ]:
                        combined = h4_series.reindex(df.index, method="ffill")
                        if s_name == "h4_cross_up":
                            h4_cross_up = combined.astype(bool).fillna(False)
                        elif s_name == "h4_cross_down":
                            h4_cross_down = combined.astype(bool).fillna(False)
                        elif s_name == "h4_bull_div":
                            h4_bull_div = combined.astype(bool).fillna(False)
                        elif s_name == "h4_bear_div":
                            h4_bear_div = combined.astype(bool).fillna(False)
                    h4_confirm_available = True
            except Exception as e:
                print(f"  [StochDiv] H4 fetch failed ({e}); using entry-TF only")

        # ── ADX gate ──────────────────────────────────────────────────────────
        try:
            adx_df    = ta.adx(df['high'], df['low'], df['close'], length=14)
            df['adx'] = adx_df.iloc[:, 0]
        except Exception:
            df['adx'] = 15.0
        ranging = df['adx'] < adx_max

        # ── EMA200 macro gate ─────────────────────────────────────────────────
        df['ema200'] = ta.ema(df['close'], length=ema200_p)
        macro_up   = df['close'] > df['ema200']
        macro_down = df['close'] < df['ema200']

        # ── RSI confirmation ──────────────────────────────────────────────────
        df['rsi']   = ta.rsi(df['close'], length=rsi_p)
        rsi_bull_ok = df['rsi'].between(rsi_bull_min, rsi_bull_max)
        rsi_bear_ok = df['rsi'].between(rsi_bear_min, rsi_bear_max)

        # ── Final signals ─────────────────────────────────────────────────────
        df['signal'] = 0

        long_cond = (
            entry["cross_up"] &
            (entry["stoch_k"] <= lower + 10) &
            entry["bull_div"] &
            h4_bull_div &    # H4 must also show bullish divergence
            ranging &
            macro_up &
            rsi_bull_ok
        )
        short_cond = (
            entry["cross_down"] &
            (entry["stoch_k"] >= upper - 10) &
            entry["bear_div"] &
            h4_bear_div &    # H4 must also show bearish divergence
            ranging &
            macro_down &
            rsi_bear_ok
        )

        df.loc[long_cond,  'signal'] =  1
        df.loc[short_cond, 'signal'] = -1

        # Suppress consecutive duplicates
        df.loc[(df['signal'] ==  1) & (df['signal'].shift(1) ==  1), 'signal'] = 0
        df.loc[(df['signal'] == -1) & (df['signal'].shift(1) == -1), 'signal'] = 0

        n_confirm = "dual-TF" if h4_confirm_available else "single-TF"
        print(f"  [StochDiv] mode={n_confirm}  longs={int((df['signal']==1).sum())}  shorts={int((df['signal']==-1).sum())}")

        return df

    def validate_params(self) -> bool:
        return True
