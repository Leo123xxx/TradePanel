from abc import ABC, abstractmethod
from typing import List
import pandas as pd
import numpy as np
pd.set_option('future.no_silent_downcasting', True)

# Session hours (UTC) for peak liquidity per pair.
# Signals generated OUTSIDE these windows are suppressed on intraday bars.
SESSION_WINDOWS = {
    # ── Original pairs ──────────────────────────────────────────────────────
    "EURUSD": [(7, 17)],
    "GBPUSD": [(7, 17)],
    "USDJPY": [(0, 3), (12, 17)],
    "XAUUSD": [(7, 20)],
    "XAGUSD": [(7, 20)],
    "BTCUSD": [(0, 24)],
    "ETHUSD": [(0, 24)],
    # ── New pairs added 2026-04-30 ───────────────────────────────────────────
    # NOTE: All hours are applied against SAST timestamps (UTC+2) stored in DB.
    # "UTC 7" here means SAST hour >= 7, which is UTC 05:00 — London open.
    "GBPJPY":  [(0, 3), (7, 17)],   # Tokyo (SAST 0-3) + London/NY (SAST 7-17)
    "AUDUSD":  [(7, 17)],            # London/NY focus — AUD also active in Asia but lower vol
    "USDCAD":  [(12, 20)],           # London PM + full NY (SAST 12 = UTC 10 = NY 06:00)
    "USDZAR":  [(7, 17)],            # London/NY — exotic, avoid thin early/late hours
    "USOIL":   [(7, 20)],            # Full energy session; avoids 21:00 maintenance break
    "US500":   [(13, 21)],           # US equity session: SAST 13 = UTC 11 ~ NY 07:00 pre-market
    "USTEC":   [(13, 21)],           # Nasdaq hours same as US500
    "NVDA":    [(13, 21)],           # Nasdaq-listed stock CFD
    "AMD":     [(13, 21)],           # Nasdaq-listed stock CFD
    "MSFT":    [(13, 21)],           # Nasdaq-listed stock CFD — confirmed Exness 2026-04-30
    "AAPL":    [(13, 21)],           # Nasdaq-listed stock CFD — confirmed Exness 2026-04-30
}
DEFAULT_SESSION = [(0, 24)]


class BaseStrategy(ABC):
    """
    Abstract base class all strategies must inherit.

    Session filter (filter_by_session):
      Called by the engine after generate_signals(). Zeroes out signals fired
      outside peak liquidity hours for intraday bars.
      Daily+ data (median bar gap ≥ 20 h) is always passed through unfiltered —
      this handles brokers that store D1 bars at 21:00 or 22:00 UTC rather than midnight.
    """

    def __init__(
        self,
        name: str,
        category: str,
        params: dict,
        regime: List[str] = None,
        timeframes: List[str] = None,
        pairs: List[str] = None
    ):
        self.name = name
        self.category = category
        self.params = params
        self.regime = regime or ["ANY"]
        self.timeframes = timeframes or []
        self.pairs = pairs or []
        self.confirm_tf = params.get("confirm_timeframe")
        self.use_regime_filter = params.get("use_regime_filter", False)
        self.use_session_filter = params.get("use_session_filter", True)
        self.allow_long = params.get("allow_long", True)
        self.allow_short = params.get("allow_short", True)


    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        pass

    def filter_by_direction(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Zeroes out signals based on 'allow_long' and 'allow_short' parameters.
        """
        df = df.copy()
        if not self.allow_long:
            df.loc[df['signal'] == 1, 'signal'] = 0
        if not self.allow_short:
            df.loc[df['signal'] == -1, 'signal'] = 0
        return df

    def filter_by_session(self, df: pd.DataFrame, pair: str) -> pd.DataFrame:
        """
        Zeroes out signals outside peak liquidity hours for intraday data.
        Daily+ timeframes (median bar gap ≥ 20 h) are always passed through
        regardless of the bar's clock time — this is robust to brokers that
        anchor D1 bars at 21:00/22:00 UTC instead of midnight.
        """
        if not self.use_session_filter:
            return df
        if not hasattr(df.index, 'hour'):
            return df

        # Detect daily+ data by median bar spacing — broker-agnostic
        if len(df) > 1:
            try:
                median_gap_hours = (
                    df.index.to_series().diff().median().total_seconds() / 3600
                )
                if median_gap_hours >= 20:
                    return df  # D1 / W1 / MN — skip session filter
            except Exception:
                pass

        windows = SESSION_WINDOWS.get(pair, DEFAULT_SESSION)
        if windows == [(0, 24)]:
            return df

        hour = df.index.hour
        in_session = pd.Series(False, index=df.index)
        for start_h, end_h in windows:
            if start_h < end_h:
                in_session |= (hour >= start_h) & (hour < end_h)
            else:
                in_session |= (hour >= start_h) | (hour < end_h)

        df = df.copy()
        df.loc[~in_session, 'signal'] = 0
        return df

    def get_parameters(self) -> dict:
        return self.params

    def get_metadata(self) -> dict:
        return {
            "name": self.name,
            "category": self.category,
            "params": self.params,
            "regime": self.regime,
            "timeframes": self.timeframes,
            "pairs": self.pairs,
            "confirm_tf": self.confirm_tf,
            "use_regime_filter": self.use_regime_filter,
            "use_session_filter": self.use_session_filter,
        }

    @abstractmethod
    def validate_params(self) -> bool:
        pass

    def apply_meta_labeling(self, df: pd.DataFrame, rsi_long=None, rsi_short=None, vol_mult=None) -> pd.DataFrame:
        """
        Prunes signals that lack momentum or conviction.
        Priority:
        1. Passed arguments
        2. self.params (rsi_long_min, rsi_short_max, vol_threshold_mult)
        3. Hardcoded defaults (55, 45, 1.2)
        """
        import ta_compat as ta
        df = df.copy()

        # Resolve thresholds
        r_long = rsi_long or self.params.get("rsi_long_min", 55)
        r_short = rsi_short or self.params.get("rsi_short_max", 45)
        v_mult = vol_mult or self.params.get("vol_threshold_mult", 1.2)
        
        # RSI Momentum Gate
        rsi = ta.rsi(df['close'], length=14)
        
        # Volume Conviction Gate
        if 'tick_volume' in df.columns:
            vol_avg = df['tick_volume'].rolling(window=20).mean()
            vol_ok = df['tick_volume'] >= (vol_avg * v_mult)
        else:
            vol_ok = True

        # Prune Longs
        df.loc[(df['signal'] == 1) & ((rsi <= r_long) | (~vol_ok)), 'signal'] = 0
        
        # Prune Shorts
        df.loc[(df['signal'] == -1) & ((rsi >= r_short) | (~vol_ok)), 'signal'] = 0
        
        return df

    # ── Confluence Helpers (Layers 1-5) ──────────────────────────────────────

    def apply_vwap_gate(self, df: pd.DataFrame, buy_cond, sell_cond):
        """
        Layer 1 — VWAP Gate.
        Only allow longs when price is above session VWAP;
        only allow shorts when price is below session VWAP.
        Skipped silently if tick_volume column is absent.
        """
        if 'tick_volume' not in df.columns:
            return buy_cond, sell_cond
        cum_tp_vol = (df['close'] * df['tick_volume']).cumsum()
        cum_vol    = df['tick_volume'].cumsum().replace(0, float('nan'))
        df['_vwap'] = cum_tp_vol / cum_vol
        above_vwap  = df['close'] > df['_vwap']
        below_vwap  = df['close'] < df['_vwap']
        return buy_cond & above_vwap, sell_cond & below_vwap

    def apply_body_ratio_filter(self, df: pd.DataFrame, buy_cond, sell_cond, min_ratio: float = None):
        """
        Layer 2 — Candle Body Ratio Filter.
        Rejects entries driven by wicks rather than a genuine directional close.
        body / (high - low) must be >= min_ratio (default from params or 0.50).
        """
        ratio = min_ratio or self.params.get('body_ratio_min', 0.50)
        body      = (df['close'] - df['open']).abs()
        bar_range = (df['high'] - df['low']).replace(0, float('nan'))
        strong    = (body / bar_range) >= ratio
        return buy_cond & strong, sell_cond & strong

    def apply_atr_ceiling(self, df: pd.DataFrame, buy_cond, sell_cond,
                          atr_col: str = 'atr', avg_col: str = 'atr_avg'):
        """
        Layer 3 — ATR Ceiling Gate.
        Suppresses entries when current ATR is above atr_ceil_mult × rolling average
        (typically a news spike or gap open). Also enforces a floor so the market
        has enough volatility to justify an entry.
        Requires df to already contain the atr and atr_avg columns.
        """
        ceil_mult  = self.params.get('atr_ceil_mult',  2.5)
        floor_mult = self.params.get('atr_floor_mult', 0.8)
        if atr_col not in df.columns or avg_col not in df.columns:
            return buy_cond, sell_cond
        atr_ok = (
            (df[atr_col] < df[avg_col] * ceil_mult) &
            (df[atr_col] > df[avg_col] * floor_mult)
        )
        return buy_cond & atr_ok, sell_cond & atr_ok

    def apply_cooldown(self, df: pd.DataFrame, cooldown_bars: int = None) -> pd.DataFrame:
        """
        Layer 4 — Cooldown Bar Suppression.
        Optimized for performance using numpy array processing.
        """
        bars = cooldown_bars or self.params.get('cooldown_bars', 0)
        if bars <= 0 or 'signal' not in df.columns:
            return df
        
        # Working with raw numpy arrays is much faster than pandas Series
        signals = df['signal'].values
        if not np.any(signals):
            return df
            
        arr = signals.copy()
        last_idx = -bars - 1
        
        # Finding indices of non-zero signals to avoid iterating over every bar
        nonzero_indices = np.nonzero(arr)[0]
        
        for i in nonzero_indices:
            if i - last_idx <= bars:
                arr[i] = 0
            else:
                last_idx = i
                
        df = df.copy()
        df['signal'] = arr
        return df

    def apply_prev_bar_momentum(self, df: pd.DataFrame, buy_cond, sell_cond):
        """
        Layer 5 — Previous-Bar Momentum Confirmation.
        The bar immediately before the signal must close in the trade direction
        (bullish close for longs, bearish close for shorts).
        Eliminates Doji/inside-bar crossovers that frequently fail.
        """
        prev_bull = df['close'].shift(1) > df['open'].shift(1)
        prev_bear = df['close'].shift(1) < df['open'].shift(1)
        return buy_cond & prev_bull, sell_cond & prev_bear
