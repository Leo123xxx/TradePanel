"""
ta_compat.py — Pure pandas/numpy drop-in replacement for pandas-ta.

Replaces pandas-ta (which hard-requires numba, incompatible with Python 3.14).
Implements every function used by the project strategies with matching return
signatures (same column order) so no strategy logic needs to change.

Usage (in strategy files):
    import ta_compat as ta
"""

import pandas as pd
import numpy as np


# ─── Moving Averages ──────────────────────────────────────────────────────────

def ema(series: pd.Series, length: int = 10, **kwargs) -> pd.Series:
    """Exponential Moving Average."""
    return series.ewm(span=length, adjust=False).mean()


def sma(series: pd.Series, length: int = 10, **kwargs) -> pd.Series:
    """Simple Moving Average."""
    return series.rolling(window=length).mean()


# ─── RSI ──────────────────────────────────────────────────────────────────────

def rsi(series: pd.Series, length: int = 14, **kwargs) -> pd.Series:
    """Relative Strength Index."""
    delta = series.diff()
    gain = delta.clip(lower=0).rolling(window=length).mean()
    loss = (-delta.clip(upper=0)).rolling(window=length).mean()
    rs = gain / loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))


# ─── MACD ─────────────────────────────────────────────────────────────────────

def macd(series: pd.Series, fast: int = 12, slow: int = 26,
         signal: int = 9, **kwargs) -> pd.DataFrame:
    """
    MACD — returns DataFrame with 3 columns (matching pandas-ta column order):
        [0] MACD line
        [1] MACD histogram
        [2] MACD signal line
    """
    fast_ema = series.ewm(span=fast, adjust=False).mean()
    slow_ema = series.ewm(span=slow, adjust=False).mean()
    macd_line = fast_ema - slow_ema
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line

    col_macd = f"MACD_{fast}_{slow}_{signal}"
    col_hist = f"MACDh_{fast}_{slow}_{signal}"
    col_sig = f"MACDs_{fast}_{slow}_{signal}"

    return pd.DataFrame(
        {col_macd: macd_line, col_hist: histogram, col_sig: signal_line},
        index=series.index,
    )


# ─── ADX ──────────────────────────────────────────────────────────────────────

def adx(high: pd.Series, low: pd.Series, close: pd.Series,
        length: int = 14, **kwargs) -> pd.DataFrame:
    """
    Average Directional Index — returns DataFrame with 4 columns
    (matching pandas-ta column order used by strategies):
        [0] ADX
        [1] DX  (intermediate — kept to preserve index alignment)
        [2] DI+ (DMP)
        [3] DI- (DMN)
    """
    prev_high = high.shift(1)
    prev_low = low.shift(1)
    prev_close = close.shift(1)

    # True Range
    tr = pd.concat([
        high - low,
        (high - prev_close).abs(),
        (low - prev_close).abs(),
    ], axis=1).max(axis=1)

    # Directional Movement
    up_move = high - prev_high
    down_move = prev_low - low

    plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0.0)
    minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0.0)

    # Smooth with Wilder's method (equivalent to EMA with alpha=1/length)
    atr = pd.Series(plus_dm, index=high.index)  # reuse series for smoothing
    atr = tr.ewm(alpha=1 / length, adjust=False).mean()
    plus_di = 100 * pd.Series(plus_dm, index=high.index).ewm(
        alpha=1 / length, adjust=False).mean() / atr
    minus_di = 100 * pd.Series(minus_dm, index=high.index).ewm(
        alpha=1 / length, adjust=False).mean() / atr

    dx = (100 * (plus_di - minus_di).abs() /
          (plus_di + minus_di).replace(0, np.nan))
    adx_line = dx.ewm(alpha=1 / length, adjust=False).mean()

    col_adx = f"ADX_{length}"
    col_dx = f"DX_{length}"
    col_dmp = f"DMP_{length}"
    col_dmn = f"DMN_{length}"

    return pd.DataFrame(
        {col_adx: adx_line, col_dx: dx, col_dmp: plus_di, col_dmn: minus_di},
        index=high.index,
    )


# ─── Bollinger Bands ──────────────────────────────────────────────────────────

def bbands(series: pd.Series, length: int = 20, std: float = 2.0,
           **kwargs) -> pd.DataFrame:
    """
    Bollinger Bands — returns DataFrame with 3 columns (matching pandas-ta
    column order used by strategies):
        [0] Lower Band
        [1] Middle Band (SMA)
        [2] Upper Band
    """
    mid = series.rolling(window=length).mean()
    std_dev = series.rolling(window=length).std(ddof=0)
    upper = mid + std * std_dev
    lower = mid - std * std_dev

    col_lower = f"BBL_{length}_{std}"
    col_mid = f"BBM_{length}_{std}"
    col_upper = f"BBU_{length}_{std}"

    return pd.DataFrame(
        {col_lower: lower, col_mid: mid, col_upper: upper},
        index=series.index,
    )


# ─── ATR ─────────────────────────────────────────────────────────────────────

def atr(high: pd.Series, low: pd.Series, close: pd.Series,
        length: int = 14, **kwargs) -> pd.Series:
    """Average True Range."""
    prev_close = close.shift(1)
    tr = pd.concat([
        high - low,
        (high - prev_close).abs(),
        (low - prev_close).abs(),
    ], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / length, adjust=False).mean()


# ─── Stochastic Oscillator ───────────────────────────────────────────────────

def stoch(high: pd.Series, low: pd.Series, close: pd.Series,
          k_period: int = 14, smooth_k: int = 3, smooth_d: int = 3,
          **kwargs) -> pd.DataFrame:
    """
    Stochastic Oscillator. Returns DataFrame with columns:
        [0] STOCHk_{k}_{sk}_{sd}
        [1] STOCHd_{k}_{sk}_{sd}
    """
    lowest_low = low.rolling(window=k_period).min()
    highest_high = high.rolling(window=k_period).max()
    
    fast_k = 100 * ((close - lowest_low) / (highest_high - lowest_low).replace(0, np.nan))
    stoch_k = fast_k.rolling(window=smooth_k).mean()
    stoch_d = stoch_k.rolling(window=smooth_d).mean()
    
    col_k = f"STOCHk_{k_period}_{smooth_k}_{smooth_d}"
    col_d = f"STOCHd_{k_period}_{smooth_k}_{smooth_d}"
    
    return pd.DataFrame({col_k: stoch_k, col_d: stoch_d}, index=high.index)
