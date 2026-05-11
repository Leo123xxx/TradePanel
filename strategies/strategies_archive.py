"""
strategies/strategies_archive.py
=================================
Archive of disabled / experimental strategies — retained for data analysis.
These strategies are NOT loaded by the registry or executed by the scheduler.

To re-enable a strategy:
  1. Copy its class back to strategies/<name>.py
  2. Set enabled: true in config/strategies.yaml
  3. Add it to the `active:` list in strategies.yaml
  4. Run a full overnight backtest to validate

Archived on: 2026-05-10
Reason codes:
  DISABLED   — strategy present in YAML with enabled: false (TIER_3)
  ORPHAN     — strategy file exists on disk but has no YAML entry

Archive contents (13 strategies):
  cot_sentiment            DISABLED | Advanced        | COT data dependency, data freshness risk
  crypto_rsi_extremes      DISABLED | Mean Reversion  | Crypto — low WR without D1 regime filter
  ema_ribbon_scalp         DISABLED | Scalping        | Low statistical significance on M15
  ema_ribbon_trend         DISABLED | Trend Following | Superseded by dual_ema_fractal + supertrend
  ict_judas_swing          DISABLED | SMC             | ICT concept needs liquidity sweep data
  institutional_silver_bullet DISABLED | SMC          | ICT liquidity sweep = continuation not reversal
  ma_crossover             DISABLED | Trend Following | WR < 70% across most pairs
  multi_ema_crypto_scalper DISABLED | Crypto Scalping | WR 35-44%; symmetric net RR due to BTC pip cost
  power_of_3_amd           DISABLED | Crypto ICT     | AMD reversal fails in trending crypto regime
  rsi_bounce               DISABLED | Mean Reversion  | ADX max 18 too restrictive; needs re-tuning
  silver_bullet_crypto     DISABLED | Crypto ICT     | WR 41-42%; ICT reversal fails in BTC trends
  vwap_momentum            DISABLED | Intraday        | Session filter + VWAP issues on crypto pairs
  volatility_contraction   ORPHAN   | Unknown         | No YAML entry; removed from active tracking
"""



# ═══════════════════════════════════════════════════════════════════════════
# ARCHIVED STRATEGY: cot_sentiment
# ═══════════════════════════════════════════════════════════════════════════
"""
strategies/cot_sentiment.py - COT Sentiment Swing Strategy
===========================================================
Uses CFTC Commitments of Traders (COT) data to detect extreme
commercial positioning as a contrarian swing signal.

Logic:
  1. COT Index >= buy_threshold (default 85) -> BUY signal
  2. COT Index <= sell_threshold (default 20) -> SELL signal
  3. COT Delta filter (v3 NEW): the 4-week rate of change of COT Index must be
     moving TOWARD the extreme (delta < 0 for buy signals = positioning building,
     delta > 0 for sell signals = shorting pressure building).
  4. EMA50 filter: only trade in the direction of the 50-period EMA trend
  5. RSI momentum confirmation gate (v2)
  6. Pair-dependent trend gate: EMA200 for commodities, EMA50 for FX

Data dependency:
  Requires `cot_data` table populated by data/cot_feed.py.
  Initial setup:  python data/cot_feed.py --history
  Weekly update:  runs automatically every Friday at 21:00 UTC via APScheduler.

Timeframes: D1, W1
Pairs:      XAUUSD, EURUSD, GBPUSD, USDJPY
"""

import pandas as pd
import numpy as np
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from strategies.base_strategy import BaseStrategy


class COTSentimentStrategy(BaseStrategy):
    """
    v3 upgrades (2026-05-01):
    - COT delta filter: 4-week rate of change of COT Index must be moving
      in the direction of the extreme (positioning must be BUILDING, not reversing).
      Eliminates entries on exhausted extremes where the COT is already turning.
    """

    _COMMODITY_PAIRS = {"XAUUSD", "XAGUSD"}

    def __init__(self, params=None):
        default_params = {
            "sentiment_threshold":  75,    # loosened 85→75: catch more extremes
            "sell_threshold":       25,    # loosened 20→25
            "ema_filter":           50,
            "atr_period":           14,
            "tp_atr_mult":           3.0,
            "sl_atr_mult":           1.5,
            "rsi_period":           14,
            "rsi_buy_min":          52,
            "rsi_sell_max":         48,
            "cot_delta_weeks":       4,   # NEW: rolling window for COT rate of change
        }
        if params:
            default_params.update(params)

        super().__init__(
            name="COT_Sentiment_Swing",
            category="Advanced",
            params=default_params,
            regime=["TRENDING"],
            timeframes=["D1", "W1"],
            pairs=["XAUUSD", "EURUSD", "GBPUSD", "USDJPY"]
        )
        self._cot_cache = {}
        self._active_pair = None

    def _load_cot_data(self, pair):
        try:
            from data.db_client import DBClient
            db = DBClient()
            rows = db.execute_query(
                """SELECT report_date, cot_index
                   FROM cot_data
                   WHERE pair = %s AND cot_index IS NOT NULL
                   ORDER BY report_date ASC""",
                (pair,)
            )
            if not rows or len(rows) < 8:
                return None
            dates  = pd.to_datetime([r[0] for r in rows])
            values = pd.Series(
                [float(r[1]) for r in rows],
                index=dates,
                name="cot_index"
            )
            return values
        except Exception as e:
            print("[COT_Sentiment] Could not load COT data for {}: {}".format(pair, e))
            return None

    def _align_cot_to_bars(self, price_df, cot_series):
        cot_reindexed = cot_series.reindex(
            price_df.index.union(cot_series.index)
        ).sort_index().ffill()
        return cot_reindexed.reindex(price_df.index)

    def generate_signals(self, data):
        df = data.copy()
        df["signal"] = 0

        pair = self._active_pair
        if pair is None or pair not in (self.pairs or []):
            print("[COT_Sentiment] Pair '{}' not in strategy list - no signals.".format(pair))
            return df

        if pair not in self._cot_cache:
            self._cot_cache[pair] = self._load_cot_data(pair)
        cot = self._cot_cache[pair]

        if cot is None or cot.empty:
            print("[COT_Sentiment] No COT data for {}. Run: python data/cot_feed.py --history".format(pair))
            return df

        df.index = pd.to_datetime(df.index)
        df["cot_index"] = self._align_cot_to_bars(df, cot).values

        # COT delta: 4-week rate of change
        # Positive delta = COT index rising (bulls building for buy threshold, bears reversing)
        # For BUY signals we want: COT >= 85 AND delta < 0 (still moving lower = more extreme)
        # Wait -- reconsider: if COT >= 85 (already extreme) and delta < 0 means still heading to extremes
        # COT Index for commercials: high index = heavy net long = bullish reversal signal
        # Delta < 0 near the top = still building toward extreme (positioning not yet reversing)
        delta_weeks  = self.params.get("cot_delta_weeks", 4)
        df["cot_delta"] = df["cot_index"].diff(delta_weeks)

        # Delta filter:
        # BUY: COT at extreme high, delta <= 0 (still moving toward extreme or plateauing)
        # SELL: COT at extreme low, delta >= 0 (still moving toward extreme or plateauing)
        # This removes entries where the extreme was 4 weeks ago and COT is already reversing
        cot_delta_ok_buy  = df["cot_delta"] <= 5    # allow small reversion (within noise)
        cot_delta_ok_sell = df["cot_delta"] >= -5   # allow small reversion (within noise)

        ema_period = self.params.get("ema_filter", 50)
        df["ema_trend"] = df["close"].ewm(span=ema_period, adjust=False).mean()

        threshold      = self.params.get("sentiment_threshold", 85)
        sell_threshold = self.params.get("sell_threshold", 20)
        cot_valid      = df["cot_index"].notna() & df["cot_delta"].notna()

        rsi_p        = self.params.get("rsi_period",   14)
        rsi_buy_min  = self.params.get("rsi_buy_min",  52)
        rsi_sell_max = self.params.get("rsi_sell_max", 48)
        try:
            import ta_compat as ta
            df["rsi"] = ta.rsi(df["close"], length=rsi_p)
        except Exception:
            df["rsi"] = 50.0
        rsi_bull_ok = df["rsi"] > rsi_buy_min
        rsi_bear_ok = df["rsi"] < rsi_sell_max

        is_commodity = pair in self._COMMODITY_PAIRS

        if is_commodity:
            df["ema200"] = df["close"].ewm(span=200, adjust=False).mean()
            in_bull = df["close"] > df["ema200"]
            in_bear = df["close"] < df["ema200"]
        else:
            in_bull = df["close"] > df["ema_trend"]
            in_bear = df["close"] < df["ema_trend"]

        buy_cond = (
            cot_valid &
            (df["cot_index"] >= threshold) &
            cot_delta_ok_buy &    # NEW: COT not already reversing sharply from extreme
            (df["close"] > df["ema_trend"]) &
            in_bull &
            rsi_bull_ok
        )
        sell_cond = (
            cot_valid &
            (df["cot_index"] <= sell_threshold) &
            cot_delta_ok_sell &   # NEW: COT not already reversing sharply from extreme
            (df["close"] < df["ema_trend"]) &
            in_bear &
            rsi_bear_ok
        )

        signal_col = pd.Series(0, index=df.index, dtype=int)
        active = 0
        for i in range(len(df)):
            idx_val = df["cot_index"].iloc[i]
            if pd.isna(idx_val):
                signal_col.iloc[i] = 0
                continue

            if buy_cond.iloc[i]:
                active = 1
            elif sell_cond.iloc[i]:
                active = -1
            elif active == 1 and idx_val < 50:
                active = 0
            elif active == -1 and idx_val > 50:
                active = 0

            signal_col.iloc[i] = active

        df["signal"] = signal_col.values

        n_buy  = (df["signal"] == 1).sum()
        n_sell = (df["signal"] == -1).sum()
        latest_cot = df["cot_index"].dropna().iloc[-1] if cot_valid.any() else None
        cot_str = "{:.1f}".format(latest_cot) if latest_cot is not None else "N/A"
        latest_delta = df["cot_delta"].dropna().iloc[-1] if df["cot_delta"].notna().any() else None
        delta_str = "{:.1f}".format(latest_delta) if latest_delta is not None else "N/A"
        print("[COT_Sentiment] {} | COT: {} | Delta({}w): {} | Signals: {} BUY, {} SELL".format(
            pair, cot_str, delta_weeks, delta_str, n_buy, n_sell))

        return df

    def set_pair(self, pair):
        self._active_pair = pair

    def validate_params(self):
        t  = self.params.get("sentiment_threshold", 85)
        st = self.params.get("sell_threshold", 20)
        return 50 < t <= 100 and 0 < st < 50


# ═══════════════════════════════════════════════════════════════════════════
# ARCHIVED STRATEGY: crypto_rsi_extremes
# ═══════════════════════════════════════════════════════════════════════════
"""
strategies/crypto_rsi_extremes.py
===================================
Crypto RSI Extremes — Mean Reversion at RSI Extremes with BB Confirmation.

Designed for BTC/ETH corrections within bull markets and recovery from oversold
conditions. Bitcoin and Ethereum regularly drop 20–40% during bull markets before
recovering; this strategy aims to catch those entries.

Signal logic:
  Buy  (1):  RSI < oversold_threshold (default 25) AND close <= lower Bollinger Band
             AND ADX < adx_max (not in vertical sell-off — ranges and corrections only)
             AND tick_volume spike (confirms genuine selling climax, not noise)
  Sell (-1): RSI > overbought_threshold (default 75) AND close >= upper Bollinger Band
             AND ADX < adx_max (ranging/correction, not breakout)
             AND tick_volume spike

Why RSI + BB confirmation?
  RSI alone fires too often in trending crypto markets (RSI stays oversold for weeks).
  Adding BB lower/upper band touch requires price to have actually extended
  significantly before entry — higher hit rate on mean reversion.

ADX guard:
  When ADX > 35, crypto is in a strong trend and mean reversion is dangerous.
  The guard ensures we only take reversion trades in corrections, not waterfall declines.

Volume filter:
  Capitulation lows and blow-off tops typically coincide with a volume spike.
  tick_volume > vol_spike_mult × 20-bar average is the filter.
  NOTE: tick_volume on MT5 CFDs is tick count, not real dollar volume.
"""

import pandas as pd
import ta_compat as ta
from strategies.base_strategy import BaseStrategy

APPROVED_PAIRS = ["BTCUSD", "ETHUSD", "XAUUSD"]
APPROVED_TIMEFRAMES = ["H4", "D1"]


class CryptoRSIExtremesStrategy(BaseStrategy):
    """
    RSI Extremes + Bollinger Band + Volume spike mean reversion.
    Primary application: BTCUSD, ETHUSD corrections.
    """

    def __init__(self, params: dict = None):
        if params is None:
            params = {
                "rsi_period":           14,
                "rsi_oversold":         25,    # Tighter than standard 30 — reduces false signals
                "rsi_overbought":       75,    # Tighter than standard 70
                "bb_period":            20,
                "bb_deviation":          2.0,
                "adx_max":             35,    # Only trade when market is NOT in a strong trend
                "vol_spike_mult":       1.5,   # Require vol > 1.5x 20-bar average
                "atr_period":          14,
                "tp_atr_mult":          2.5,   # Generous TP for crypto bounces
                "sl_atr_mult":          1.0,
            }
        super().__init__(
            name="Crypto_RSI_Extremes",
            category="Mean Reversion",
            params=params,
            regime=["RANGING", "CHOPPY", "ANY"],
            timeframes=APPROVED_TIMEFRAMES,
            pairs=APPROVED_PAIRS,
        )

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        RSI extremes + BB band touch + volume spike + ADX guard.
        """
        df = data.copy()

        rsi_p       = self.params.get("rsi_period",    14)
        rsi_os      = self.params.get("rsi_oversold",  25)
        rsi_ob      = self.params.get("rsi_overbought", 75)
        bb_p        = self.params.get("bb_period",     20)
        bb_std      = self.params.get("bb_deviation",   2.0)
        adx_max     = self.params.get("adx_max",       35)
        vol_mult    = self.params.get("vol_spike_mult", 1.5)

        # ── RSI ───────────────────────────────────────────────────────────────
        df['rsi'] = ta.rsi(df['close'], length=rsi_p)

        # ── Bollinger Bands ───────────────────────────────────────────────────
        bb_df = ta.bbands(df['close'], length=bb_p, std=bb_std)
        df['bb_lower'] = bb_df[f"BBL_{bb_p}_{bb_std}"]
        df['bb_upper'] = bb_df[f"BBU_{bb_p}_{bb_std}"]

        # ── ADX ───────────────────────────────────────────────────────────────
        adx_df    = ta.adx(df['high'], df['low'], df['close'], length=14)
        df['adx'] = adx_df["ADX_14"]

        # ── Volume spike filter ───────────────────────────────────────────────
        df['vol_avg'] = df['tick_volume'].rolling(window=20).mean()
        vol_spike     = df['tick_volume'] > (df['vol_avg'] * vol_mult)

        # ── Market regime guard ───────────────────────────────────────────────
        not_trending = df['adx'] < adx_max

        # ── Signals ───────────────────────────────────────────────────────────
        df['signal'] = 0

        long_cond = (
            (df['rsi']   <= rsi_os) &
            (df['close'] <= df['bb_lower']) &
            not_trending &
            vol_spike
        )

        short_cond = (
            (df['rsi']   >= rsi_ob) &
            (df['close'] >= df['bb_upper']) &
            not_trending &
            vol_spike
        )

        df.loc[long_cond,  'signal'] =  1
        df.loc[short_cond, 'signal'] = -1

        # Suppress consecutive duplicates
        df.loc[(df['signal'] ==  1) & (df['signal'].shift(1) ==  1), 'signal'] = 0
        df.loc[(df['signal'] == -1) & (df['signal'].shift(1) == -1), 'signal'] = 0

        return df

    def validate_params(self) -> bool:
        return (
            self.params.get("rsi_oversold", 0) < self.params.get("rsi_overbought", 100) and
            self.params.get("bb_deviation", 0) > 0 and
            self.params.get("adx_max", 0) > 0
        )


# ═══════════════════════════════════════════════════════════════════════════
# ARCHIVED STRATEGY: ema_ribbon_scalp
# ═══════════════════════════════════════════════════════════════════════════
"""
EMA Ribbon Scalp - 1m/5m scalping
Fast EMA crosses mid EMA while mid>slow confirms trend direction.
"""

from strategies.base_strategy import BaseStrategy
import ta_compat as ta


class EMARibbonScalp(BaseStrategy):
    """Scalps with EMA ribbon — entry on fast-cross-mid with trend confirmation."""

    def __init__(self, params=None):
        params = params or {
            "fast_ema":              5,
            "mid_ema":               10,
            "slow_ema":              20,
            "atr_period":            14,
            "tp_atr_mult":           2.0,
            "sl_atr_mult":           1.0,
            "min_ribbon_separation": 0.0,
        }
        super().__init__(
            name="ema_ribbon_scalp",
            category="Scalping",
            params=params,
            regime=["TRENDING", "ANY"],
            timeframes=["M1", "M5"],
            pairs=["XAUUSD", "EURUSD", "GBPUSD", "USDJPY", "BTCUSD", "ETHUSD", "XAGUSD"]
        )

    def generate_signals(self, data):
        """Entry: fast EMA crosses mid EMA while mid > slow (trend established)."""
        df = data.copy()

        df['ema_fast'] = ta.ema(df['close'], self.params["fast_ema"])
        df['ema_mid']  = ta.ema(df['close'], self.params["mid_ema"])
        df['ema_slow'] = ta.ema(df['close'], self.params["slow_ema"])

        df['atr'] = ta.atr(df['high'], df['low'], df['close'],
                           self.params["atr_period"])

        df['ribbon_spread'] = (df['ema_fast'] - df['ema_slow']).abs() / df['close']
        spread_ok = df['ribbon_spread'] > self.params["min_ribbon_separation"]

        df['signal'] = 0

        # BUY: fast just crossed above mid, AND mid is above slow (uptrend confirmed)
        buy_signal = (
            (df['ema_fast'] > df['ema_mid']) &
            (df['ema_fast'].shift(1) <= df['ema_mid'].shift(1)) &
            (df['ema_mid'] > df['ema_slow']) &
            spread_ok
        )
        df.loc[buy_signal, 'signal'] = 1

        # SELL: fast just crossed below mid, AND mid is below slow (downtrend confirmed)
        sell_signal = (
            (df['ema_fast'] < df['ema_mid']) &
            (df['ema_fast'].shift(1) >= df['ema_mid'].shift(1)) &
            (df['ema_mid'] < df['ema_slow']) &
            spread_ok
        )
        df.loc[sell_signal, 'signal'] = -1

        return df

    def validate_params(self) -> bool:
        return (self.params.get("fast_ema", 0) > 0 and
                self.params.get("mid_ema", 0) > self.params.get("fast_ema", 0) and
                self.params.get("slow_ema", 0) > self.params.get("mid_ema", 0) and
                self.params.get("tp_atr_mult", 0) > 0)


# ═══════════════════════════════════════════════════════════════════════════
# ARCHIVED STRATEGY: ema_ribbon_trend
# ═══════════════════════════════════════════════════════════════════════════
"""
strategies/ema_ribbon_trend.py
==============================
EMA Ribbon Trend — Multi-EMA Alignment Trend Follower.

Designed for high-volatility assets with strong directional trends: BTCUSD, ETHUSD,
and XAUUSD in trending regimes.

Signal logic:
  Buy  (1):  All 3 EMAs aligned bullish (fast > mid > slow) AND close > fast EMA
             AND ADX confirms trend strength AND RSI > 50 (momentum above midline)
             AND close > EMA200 (macro trend filter — v2 2026-04-29)
  Sell (-1): All 3 EMAs aligned bearish (fast < mid < slow) AND close < fast EMA
             AND ADX confirms trend strength AND RSI < 50
             AND close < EMA200 (macro trend filter — v2 2026-04-29)
  Hold (0):  No alignment or mixed signals

Why 3 EMAs?
  A single crossover (2 EMAs) generates many false entries in volatile markets.
  A 3-EMA ribbon requires all three to agree — much higher conviction entries.
  The close > fast EMA filter additionally confirms price is not in a pullback.

Crypto-specific notes:
  - 24/7 market: no session filter needed
  - Higher ATR multipliers than FX: default TP=3.0x, SL=1.5x
  - Wider fast/mid/slow gaps than FX: 9/21/55 captures crypto's explosive moves
  - Works on H4 (primary) and D1 (secondary for longer-term positions)
"""

import pandas as pd
import ta_compat as ta
from strategies.base_strategy import BaseStrategy

APPROVED_PAIRS = ["BTCUSD", "ETHUSD", "XAUUSD", "EURUSD", "GBPUSD"]
APPROVED_TIMEFRAMES = ["H4", "D1"]


class EMARibbonTrendStrategy(BaseStrategy):
    """
    Multi-EMA Ribbon Trend Follower.
    Primary application: BTCUSD, ETHUSD (crypto — 24/7 signal generation).
    """

    def __init__(self, params: dict = None):
        if params is None:
            params = {
                "fast_ema":           9,      # Short-term trend (reacts fast)
                "mid_ema":           21,      # Medium-term trend
                "slow_ema":          55,      # Long-term trend (ribbon spine)
                "adx_min":           28,      # raised to 28 for stronger trend filtering
                "rsi_period":        14,      # RSI for momentum filter
                "atr_period":        14,
                "tp_atr_mult":        3.0,    # Larger TP for crypto's bigger moves
                "sl_atr_mult":        1.0,    # was 1.5 — tighter SL lifts RR from 2:1 to 3:1
                "vol_threshold_mult": 0,      # disabled vol gate — killing too many setups
                "ema200_period":    200,      # Macro trend gate — added 2026-04-29
            }
        super().__init__(
            name="EMA_Ribbon_Trend",
            category="Trend Following",
            params=params,
            regime=["TRENDING", "ANY"],
            timeframes=APPROVED_TIMEFRAMES,
            pairs=APPROVED_PAIRS,
        )

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        3-EMA ribbon alignment + RSI momentum + ADX trend strength.
        Entry fires only when all three filters agree.
        """
        df = data.copy()

        fast_p    = self.params.get("fast_ema",           9)
        mid_p     = self.params.get("mid_ema",            21)
        slow_p    = self.params.get("slow_ema",           55)
        adx_min   = self.params.get("adx_min",            28)
        rsi_p     = self.params.get("rsi_period",         14)
        vol_p     = self.params.get("vol_lookback",       20)
        vol_mult  = self.params.get("vol_threshold_mult",  0.0)  # 0 = disabled
        ema200_p  = self.params.get("ema200_period",     200)

        # ── EMA ribbon ────────────────────────────────────────────────────────
        df['ema_fast'] = ta.ema(df['close'], length=fast_p)
        df['ema_mid']  = ta.ema(df['close'], length=mid_p)
        df['ema_slow'] = ta.ema(df['close'], length=slow_p)

        # ── EMA200 macro trend gate ───────────────────────────────────────────
        df['ema200'] = ta.ema(df['close'], length=ema200_p)
        macro_up   = df['close'] > df['ema200']
        macro_down = df['close'] < df['ema200']

        # ── Supporting indicators ─────────────────────────────────────────────
        df['rsi']    = ta.rsi(df['close'], length=rsi_p)
        adx_df       = ta.adx(df['high'], df['low'], df['close'], length=14)
        df['adx']    = adx_df["ADX_14"]

        df['atr']    = ta.atr(df['high'], df['low'], df['close'], length=14)
        df['atr_ma'] = ta.sma(df['atr'], length=vol_p)

        # ── Ribbon alignment filters ──────────────────────────────────────────
        bullish_ribbon = (
            (df['ema_fast'] > df['ema_mid']) &
            (df['ema_mid']  > df['ema_slow']) &
            (df['close']    > df['ema_fast'])   # price above the ribbon
        )
        bearish_ribbon = (
            (df['ema_fast'] < df['ema_mid']) &
            (df['ema_mid']  < df['ema_slow']) &
            (df['close']    < df['ema_fast'])   # price below the ribbon
        )

        trend_ok = df['adx'] >= adx_min
        vol_ok   = (df['atr'] >= df['atr_ma'] * vol_mult) if vol_mult > 0 else True

        # ── Signal generation — fire only on the bar the ribbon flips ─────────
        # Use shift(1) to detect a NEW alignment (first bar of ribbon agreement)
        prev_bullish = (
            (df['ema_fast'].shift(1) > df['ema_mid'].shift(1)) &
            (df['ema_mid'].shift(1)  > df['ema_slow'].shift(1))
        )
        prev_bearish = (
            (df['ema_fast'].shift(1) < df['ema_mid'].shift(1)) &
            (df['ema_mid'].shift(1)  < df['ema_slow'].shift(1))
        )

        # NEW bullish alignment = ribbon just turned bullish this bar
        new_bullish = bullish_ribbon & ~prev_bullish
        # NEW bearish alignment = ribbon just turned bearish this bar
        new_bearish = bearish_ribbon & ~prev_bearish

        df['signal'] = 0
        long_cond  = new_bullish & trend_ok & vol_ok & (df['rsi'] > 50) & macro_up
        short_cond = new_bearish & trend_ok & vol_ok & (df['rsi'] < 50) & macro_down

        df.loc[long_cond,  'signal'] =  1
        df.loc[short_cond, 'signal'] = -1

        return df

    def validate_params(self) -> bool:
        fast = self.params.get("fast_ema", 0)
        mid  = self.params.get("mid_ema",  0)
        slow = self.params.get("slow_ema", 0)
        return fast > 0 and fast < mid < slow


# ═══════════════════════════════════════════════════════════════════════════
# ARCHIVED STRATEGY: ict_judas_swing
# ═══════════════════════════════════════════════════════════════════════════
import pandas as pd
import numpy as np
import ta_compat as ta
from strategies.base_strategy import BaseStrategy

class ICTJudasSwing(BaseStrategy):
    """
    ICT Judas Swing Strategy (Institutional Flow)
    
    Logic:
    1. Identify the Asian Range (pre-London consolidation).
    2. Look for a "Stop Hunt" (Judas Swing) at London Open (Fakeout of Asian high/low).
    3. Reversal: Price breaks back into the range and reverses the move.
    4. Entry: Market Structure Break (MSB) on M5/M15 timeframe.
    """

    def __init__(self, params: dict = None):
        if params is None:
            params = {
                "ny_offset_hours": 7,
                "asian_range_start": 20,    # 8:00 PM NY
                "asian_range_end": 2,       # 2:00 AM NY (London Open)
                "judas_window_start": 2,    # 2:00 AM NY
                "judas_window_end": 5,      # 5:00 AM NY
                "fakeout_magnitude_pct": 0.001, 
                "atr_period": 14
            }
        super().__init__(
            name="ICT_Judas_Swing",
            category="SMC",
            params=params,
            regime=["LOW_VOL", "TRENDING"],
            timeframes=["M15", "H1"],
            pairs=["GBPUSD", "EURUSD", "USDJPY"]
        )

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()
        offset = self.params.get("ny_offset_hours", 7)
        
        # 1. Define Sessions (Local Time)
        df['hour_ny'] = (df.index.hour - offset) % 24
        
        # 2. Asian Range High/Low
        # This is tricky in a vectorized way. We'll use a expanding max/min reset daily.
        df['date'] = df.index.date
        
        # Identify bars in Asian session
        df['is_asian'] = (df['hour_ny'] >= self.params['asian_range_start']) | (df['hour_ny'] < self.params['asian_range_end'])
        
        # Calculate daily Asian High/Low
        asian_high = df[df['is_asian']].groupby('date')['high'].max()
        asian_low = df[df['is_asian']].groupby('date')['low'].min()
        
        df['asian_h'] = df['date'].map(asian_high)
        df['asian_l'] = df['date'].map(asian_low)
        
        # 3. Judas Window (London Open)
        df['is_judas'] = (df['hour_ny'] >= self.params['judas_window_start']) & (df['hour_ny'] < self.params['judas_window_end'])
        
        vol_p  = self.params.get("vol_lookback", 20)
        vol_m  = self.params.get("vol_threshold_mult", 0.0) # 0 = disabled
        sweep  = self.params.get("liquidity_sweep_pips", 0) # Min pips penetration
        
        # 4. Volume Filter
        df['vol_ma'] = ta.sma(df['tick_volume'], length=vol_p)
        df['vol_ok'] = df['tick_volume'] > (df['vol_ma'] * vol_m) if vol_m > 0 else True
        
        # 5. Fakeout detection (with sweep depth)
        mask_buy = (df['low'] < df['asian_l'] - (sweep * 0.0001)) & (df['close'] > df['asian_l'])
        mask_sell = (df['high'] > df['asian_h'] + (sweep * 0.0001)) & (df['close'] < df['asian_h'])
        
        df['fake_buy'] = df['is_judas'] & mask_buy & df['vol_ok']
        df['fake_sell'] = df['is_judas'] & mask_sell & df['vol_ok']
        
        # 6. Signal
        df['signal'] = 0
        df.loc[df['fake_buy'], 'signal'] = 1
        df.loc[df['fake_sell'], 'signal'] = -1
        
        return df

    def validate_params(self) -> bool:
        return True


# ═══════════════════════════════════════════════════════════════════════════
# ARCHIVED STRATEGY: institutional_silver_bullet
# ═══════════════════════════════════════════════════════════════════════════
import pandas as pd
import numpy as np
from strategies.base_strategy import BaseStrategy

class InstitutionalSilverBullet(BaseStrategy):
    """
    ICT Silver Bullet Strategy (Institutional Flow)
    
    Logic:
    1. Timed Entry Window: 10:00-11:00 AM NY, 2:00-3:00 AM NY, or 2:00-3:00 PM NY.
    2. Liquidity Sweep: Price must sweep a recent high/low (liquidity pool).
    3. Market Structure Shift (MSS): Price must break the previous swing high/low in the reversal direction.
    4. Fair Value Gap (FVG): Entry on a retracement into a 5-minute or 15-minute FVG.
    
    Note: Time is adjusted based on 'ny_offset' parameter to align with server time.
    """

    def __init__(self, params: dict = None):
        if params is None:
            params = {
                "ny_offset_hours": 7,      # Adjust based on broker server time (e.g., MT5 is usually UTC+2/3)
                "lookback_sweep": 20,      # Look back this many bars for liquidity pools
                "fvg_min_size_pct": 0.0001, # Minimum size of FVG as % of price
                "risk_reward": 2.0,        # Fixed RR for simplicity
                "atr_period": 14
            }
        super().__init__(
            name="Institutional_Silver_Bullet",
            category="SMC",
            params=params,
            regime=["TRENDING", "ANY"],
            timeframes=["M5", "M15"],
            pairs=["XAUUSD", "GBPUSD", "EURUSD"]
        )

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()
        
        offset = self.params.get("ny_offset_hours", 7)
        lookback = self.params.get("lookback_sweep", 20)
        
        # 1. Time Session Detection (Simplified to Hour of Day)
        # Assuming NY 10:00-11:00 is (10 + offset) in server time
        df['hour'] = df.index.hour
        
        # Silver Bullet Windows (NY Time): 
        # 02:00-03:00 (London), 10:00-11:00 (NY AM), 14:00-15:00 (NY PM)
        sb_windows = [2, 10, 14]
        df['is_sb_window'] = df['hour'].apply(lambda x: (x - offset) % 24 in sb_windows)

        # 2. Identify Liquidity Levels (High/Low of previous lookback)
        df['prev_high'] = df['high'].rolling(window=lookback).max().shift(1)
        df['prev_low'] = df['low'].rolling(window=lookback).min().shift(1)
        
        # 3. Detect Sweeps
        df['swept_high'] = df['high'] > df['prev_high']
        df['swept_low'] = df['low'] < df['prev_low']
        
        # 4. Market Structure Shift (Simplified: Reversal from sweep)
        # A buy signal happens if we swept low and then close above the previous bar's high
        df['mss_buy'] = (df['swept_low'].shift(1)) & (df['close'] > df['high'].shift(1))
        df['mss_sell'] = (df['swept_high'].shift(1)) & (df['close'] < df['low'].shift(1))
        
        # 5. Fair Value Gap (FVG)
        # Bullish FVG: Low of Bar 3 > High of Bar 1
        df['bull_fvg'] = (df['low'] > df['high'].shift(2))
        # Bearish FVG: High of Bar 3 < Low of Bar 1
        df['bear_fvg'] = (df['high'] < df['low'].shift(2))
        
        # 6. Final Signal
        df['signal'] = 0
        
        # Entry logic: Within SB window AND (MSS + FVG)
        df.loc[df['is_sb_window'] & df['mss_buy'] & df['bull_fvg'], 'signal'] = 1
        df.loc[df['is_sb_window'] & df['mss_sell'] & df['bear_fvg'], 'signal'] = -1
        
        return df

    def validate_params(self) -> bool:
        return True


# ═══════════════════════════════════════════════════════════════════════════
# ARCHIVED STRATEGY: ma_crossover
# ═══════════════════════════════════════════════════════════════════════════
import pandas as pd
import ta_compat as ta
from strategies.base_strategy import BaseStrategy

# Pairs and timeframes this strategy is approved to trade.
# Tune fast/slow periods per pair in strategies.yaml — defaults here are fallbacks.
APPROVED_PAIRS = ["XAUUSD", "EURUSD", "GBPUSD", "USDJPY", "XAGUSD"]
APPROVED_TIMEFRAMES = ["H1", "H4", "D1"]

class MACrossoverStrategy(BaseStrategy):
    """
    Moving Average Crossover — Trend Following.

    Signal logic:
      Buy  (1):  Fast EMA crosses ABOVE Slow EMA
      Sell (-1): Fast EMA crosses BELOW Slow EMA
      Hold (0):  No crossover on this bar

    Regime: TRENDING preferred (ADX > 25). Avoid RANGING markets.
    Works on all 5 approved pairs; parameter defaults tuned for H1 timeframe.
    Per-pair parameter overrides loaded from strategies.yaml at runtime.
    """

    def __init__(self, params: dict = None):
        if params is None:
            params = {
                "fast_period": 10,       # Widened from 9 — more separation = fewer whipsaws
                "slow_period": 50,       # Widened from 21 — clear trend filter
                "ma_type": "EMA",
                "atr_period": 14,
                "tp_atr_mult": 2.0,
                "sl_atr_mult": 1.0,
                "adx_filter": 20         # loosened 25→20: catch more trends
            }
        super().__init__(
            name="MA_Crossover",
            category="Trend Following",
            params=params,
            regime=["TRENDING", "ANY"],
            timeframes=APPROVED_TIMEFRAMES,
            pairs=APPROVED_PAIRS
        )

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Returns the input DataFrame with a 'signal' column (1 / -1 / 0).

        Entry logic:
          - Fast EMA crosses above Slow EMA → BUY, if ADX filter passes
          - Fast EMA crosses below Slow EMA → SELL, if ADX filter passes
          - ADX filter: skip signal if ADX < adx_filter (choppy market guard)
        """
        df = data.copy()

        fast_period = self.params.get("fast_period", 10)
        slow_period = self.params.get("slow_period", 50)
        ma_type     = self.params.get("ma_type", "EMA").upper()
        adx_min     = self.params.get("adx_filter", 25)

        # ── Moving averages ──────────────────────────────────────────────────
        if ma_type == "EMA":
            df['fast_ma'] = ta.ema(df['close'], length=fast_period)
            df['slow_ma'] = ta.ema(df['close'], length=slow_period)
        else:
            df['fast_ma'] = ta.sma(df['close'], length=fast_period)
            df['slow_ma'] = ta.sma(df['close'], length=slow_period)

        # ── ADX trend-strength filter ────────────────────────────────────────
        adx_df = ta.adx(df['high'], df['low'], df['close'], length=14)
        df['adx'] = adx_df[f"ADX_14"]
        adx_ok = (adx_min == 0) | (df['adx'] >= adx_min)

        # ── Crossover signal (fires only on the bar the bias changes) ────────
        df['signal_val'] = 0
        df.loc[df['fast_ma'] > df['slow_ma'], 'signal_val'] = 1
        df.loc[df['fast_ma'] < df['slow_ma'], 'signal_val'] = -1

        df['signal'] = 0
        df.loc[
            (df['signal_val'] == 1) & (df['signal_val'].shift(1) == -1) & adx_ok,
            'signal'
        ] = 1
        df.loc[
            (df['signal_val'] == -1) & (df['signal_val'].shift(1) == 1) & adx_ok,
            'signal'
        ] = -1

        # ── Meta-Labeling (Win Rate Push) ────────────────────────────────────
        # Use RSI 55/45 and 1.2x Volume as secondary gates
        df = self.apply_meta_labeling(
            df, 
            rsi_long=self.params.get("rsi_long_min", 55),
            rsi_short=self.params.get("rsi_short_max", 45),
            vol_mult=self.params.get("vol_threshold_mult", 1.2)
        )

        return df

    def validate_params(self) -> bool:
        fast = self.params.get("fast_period", 0)
        slow = self.params.get("slow_period", 0)
        tp = self.params.get("tp_atr_mult", 0)
        sl = self.params.get("sl_atr_mult", 0)
        return (
            fast > 0
            and slow > fast
            and tp > sl > 0
        )


# ═══════════════════════════════════════════════════════════════════════════
# ARCHIVED STRATEGY: multi_ema_crypto_scalper
# ═══════════════════════════════════════════════════════════════════════════
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


# ═══════════════════════════════════════════════════════════════════════════
# ARCHIVED STRATEGY: power_of_3_amd
# ═══════════════════════════════════════════════════════════════════════════
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


# ═══════════════════════════════════════════════════════════════════════════
# ARCHIVED STRATEGY: rsi_bounce
# ═══════════════════════════════════════════════════════════════════════════
import pandas as pd
import ta_compat as ta
from strategies.base_strategy import BaseStrategy

APPROVED_PAIRS = ["XAUUSD", "EURUSD", "GBPUSD", "USDJPY"]
APPROVED_TIMEFRAMES = ["H4", "D1"]


class RSIBounceStrategy(BaseStrategy):
    """
    RSI Mean Reversion Strategy — v3.1 Threshold Correction.

    v3 upgrades (2026-05-01) — targeting 70%+ WR:
    - Confirmation candle filter: after the RSI crossover, the NEXT bar must be a
      bullish close (close > open for longs) or bearish close (close < open for shorts).
      This one-bar confirmation dramatically reduces false crossover entries.

    v3.1 fix (2026-05-09) — RSI 15/85 + ADX max 18 produced ZERO signals in WFO.
    - RSI extremes relaxed back to 20/80: RSI 15/85 is statistically rare on H1-D1;
      combined with ADX max 18, the strategy fired literally 0 trades across all windows.
    - ADX max raised 18->25: ADX 18-25 is still a ranging regime but fires signals.
      ADX 30+ (strong trend) remains excluded to avoid mean-reversion into a trend.
    - Vol threshold loosened 1.2->1.0: the vol gate stacked with ADX+RSI gates was
      over-filtering. Remove as a redundant layer — RSI extreme IS the vol proxy.
    """

    def __init__(self, params: dict = None):
        if params is None:
            params = {
                "rsi_period":          14,
                "oversold":            20,    # relaxed 15->20: 15 almost never fires
                "overbought":          80,    # relaxed 85->80: 85 almost never fires
                "ema_trend":          200,
                "adx_max":             25,    # raised 18->25: 18 is too quiet, still excludes trends
                "vol_threshold_mult":   1.0,  # loosened 1.2->1.0: vol gate redundant with RSI extreme
                "atr_period":          14,
                "session_start_utc":    7,
                "session_end_utc":     17,
                "tp_atr_mult":          2.0,
                "sl_atr_mult":          1.0,
                "use_partial_tp":       False,
            }
        super().__init__(
            name="RSI_Bounce",
            category="Mean Reversion",
            params=params,
            regime=["RANGING", "ANY"],
            timeframes=APPROVED_TIMEFRAMES,
            pairs=APPROVED_PAIRS,
        )

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()

        rsi_period       = self.params.get("rsi_period",         14)
        overbought       = self.params.get("overbought",         80)
        oversold         = self.params.get("oversold",           20)
        ema_trend_period = self.params.get("ema_trend",         200)
        adx_max          = self.params.get("adx_max",            25)
        vol_mult         = self.params.get("vol_threshold_mult",  1.0)
        atr_p            = self.params.get("atr_period",         14)
        sess_start       = self.params.get("session_start_utc",   7)
        sess_end         = self.params.get("session_end_utc",    17)

        # ── Indicators ────────────────────────────────────────────────────────
        df['rsi']       = ta.rsi(df['close'], length=rsi_period)
        df['ema_trend'] = ta.ema(df['close'], length=ema_trend_period)
        df['atr']       = ta.atr(df['high'], df['low'], df['close'], length=atr_p)
        df['atr_avg']   = df['atr'].rolling(20).mean()

        try:
            adx_df    = ta.adx(df['high'], df['low'], df['close'], length=14)
            df['adx'] = adx_df.iloc[:, 0]
        except Exception:
            df['adx'] = 15.0

        # ── Gates ─────────────────────────────────────────────────────────────
        in_uptrend   = df['close'] > df['ema_trend']
        in_downtrend = df['close'] < df['ema_trend']
        ranging      = df['adx'] < adx_max
        vol_ok       = df['atr'] >= df['atr_avg'] * vol_mult

        # Confirmation candle: current bar must be bullish (for longs) or bearish (shorts)
        bar_bullish = df['close'] > df['open']
        bar_bearish = df['close'] < df['open']

        # Session gate
        try:
            hour       = df.index.hour
            in_session = (hour >= sess_start) & (hour < sess_end)
        except Exception:
            in_session = True

        # ── Signals: RSI crossover + confirmation candle ───────────────────────
        # RSI crossed back above oversold on PREVIOUS bar — current bar is the confirmation
        rsi_crossed_up   = (df['rsi'].shift(1) > oversold) & (df['rsi'].shift(2) <= oversold)
        rsi_crossed_down = (df['rsi'].shift(1) < overbought) & (df['rsi'].shift(2) >= overbought)

        df['signal'] = 0

        long_cond = (
            in_uptrend &
            ranging &
            vol_ok &
            in_session &
            rsi_crossed_up &
            bar_bullish        # confirmation: current bar closes bullish
        )
        short_cond = (
            in_downtrend &
            ranging &
            vol_ok &
            in_session &
            rsi_crossed_down &
            bar_bearish        # confirmation: current bar closes bearish
        )

        df.loc[long_cond,  'signal'] =  1
        df.loc[short_cond, 'signal'] = -1

        return df

    def validate_params(self) -> bool:
        return (self.params.get("rsi_period", 0) > 0 and
                0 < self.params.get("oversold",   15) < 50 and
                50 < self.params.get("overbought", 85) < 100)


# ═══════════════════════════════════════════════════════════════════════════
# ARCHIVED STRATEGY: silver_bullet_crypto
# ═══════════════════════════════════════════════════════════════════════════
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


# ═══════════════════════════════════════════════════════════════════════════
# ARCHIVED STRATEGY: vwap_momentum
# ═══════════════════════════════════════════════════════════════════════════
import pandas as pd
import numpy as np
import ta_compat as ta
from strategies.base_strategy import BaseStrategy

class VWAPMomentum(BaseStrategy):
    """
    VWAP Momentum Shift (Mean Reversion) v3.

    v3 upgrades (2026-05-01) — targeting 70%+ WR:
    - ADX max tightened 30->22: only trade in clearly ranging markets
    - RSI zones tightened: rsi_buy_max 45->35 (deep oversold), rsi_sell_min 55->65 (deep overbought)
    - VWAP deviation filter: price must be >= 0.8x ATR beyond VWAP band (not just touching it)
    - Volume direction filter: volume must be DECREASING over last 3 bars (exhaustion signal)
      before the reversal bar. A spike into the band on rising volume is momentum, not exhaustion.
    """

    def __init__(self, params: dict = None):
        if params is None:
            params = {
                "std_dev_mult":           2.0,
                "atr_period":            14,
                "tp_atr_mult":            2.0,
                "sl_atr_mult":            1.0,
                "min_std_periods":        5,
                "use_partial_tp":        False,
                "adx_max":               22,    # tightened 30->22
                "rsi_period":            14,
                "rsi_buy_max":           35,    # tightened 45->35 (deep oversold only)
                "rsi_sell_min":          65,    # tightened 55->65 (deep overbought only)
                "vol_threshold_mult":     1.2,  # reversal bar volume gate
                "vwap_atr_min_excess":    0.8,  # NEW: min excess beyond band in ATR units
                "vol_exhaustion_bars":    3,    # NEW: volume must be declining this many bars
                "session_start_utc":      7,
                "session_end_utc":       17,
            }
        super().__init__(
            name="VWAP_Momentum",
            category="Mean Reversion",
            params=params,
            regime=["RANGING", "HIGH_VOL"],
            timeframes=["M15", "M30", "H1"],
            pairs=["GBPUSD", "EURUSD", "XAUUSD"]
        )

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()

        std_mult        = self.params.get("std_dev_mult",          2.0)
        adx_max         = self.params.get("adx_max",               22)
        rsi_p           = self.params.get("rsi_period",            14)
        rsi_buy_max     = self.params.get("rsi_buy_max",           35)
        rsi_sell_min    = self.params.get("rsi_sell_min",          65)
        vol_mult        = self.params.get("vol_threshold_mult",     1.2)
        vwap_excess_atr = self.params.get("vwap_atr_min_excess",    0.8)
        vol_exhaust_n   = self.params.get("vol_exhaustion_bars",    3)
        session_start   = self.params.get("session_start_utc",     7)
        session_end     = self.params.get("session_end_utc",       17)

        # 1. Daily VWAP
        df['date'] = df.index.date
        df['pv']   = df['close'] * df['tick_volume']
        df['cum_pv'] = df.groupby('date')['pv'].cumsum()
        df['cum_v']  = df.groupby('date')['tick_volume'].cumsum()
        df['vwap']   = df['cum_pv'] / df['cum_v']

        # 2. VWAP std deviation
        df['vwap_std'] = df.groupby('date')['close'].transform(lambda x: x.expanding().std())
        valid_std = df['vwap_std'].notna() & (df['vwap_std'] > 0)

        # 3. ATR
        df['atr'] = ta.atr(df['high'], df['low'], df['close'], length=14)

        # 4. VWAP bands
        df['vwap_upper'] = df['vwap'] + std_mult * df['vwap_std']
        df['vwap_lower'] = df['vwap'] - std_mult * df['vwap_std']

        # 5. Overextended with minimum excess beyond band (in ATR units)
        df['excess_up']   = df['close'] - df['vwap_upper']   # positive = above upper band
        df['excess_down'] = df['vwap_lower'] - df['close']   # positive = below lower band
        df['is_overbought'] = df['excess_up']   >= vwap_excess_atr * df['atr']
        df['is_oversold']   = df['excess_down'] >= vwap_excess_atr * df['atr']

        # 6. ADX gate
        try:
            adx_df    = ta.adx(df['high'], df['low'], df['close'], length=14)
            df['adx'] = adx_df["ADX_14"]
        except Exception:
            df['adx'] = 15.0
        not_trending = df['adx'] < adx_max

        # 7. RSI gate (deeper extreme zones)
        df['rsi']    = ta.rsi(df['close'], length=rsi_p)
        rsi_buy_ok   = df['rsi'] <= rsi_buy_max
        rsi_sell_ok  = df['rsi'] >= rsi_sell_min

        # 8. Volume exhaustion: volume must be declining over last N bars before reversal
        #    vol_exhaust_n=3: vol[i-1] < vol[i-2] < vol[i-3] => declining momentum into band
        if vol_exhaust_n >= 2 and 'tick_volume' in df.columns:
            # Check that each successive bar has lower volume than the one before
            vol_declining = df['tick_volume'].shift(1) < df['tick_volume'].shift(2)
            for k in range(2, vol_exhaust_n):
                vol_declining = vol_declining & (df['tick_volume'].shift(k) < df['tick_volume'].shift(k + 1))
        else:
            vol_declining = True

        # 9. Reversal bar volume confirmation
        if vol_mult > 0 and 'tick_volume' in df.columns:
            df['vol_avg'] = df['tick_volume'].rolling(window=20).mean()
            vol_ok = df['tick_volume'] >= (df['vol_avg'] * vol_mult)
        else:
            vol_ok = True

        # 10. Session gate
        try:
            hour = df.index.hour
            in_session = (hour >= session_start) & (hour < session_end)
        except Exception:
            in_session = True

        # 11. Signals
        df['signal'] = 0

        buy_gate  = valid_std & not_trending & rsi_buy_ok  & vol_ok & vol_declining & in_session
        sell_gate = valid_std & not_trending & rsi_sell_ok & vol_ok & vol_declining & in_session

        df.loc[buy_gate  & df['is_oversold'].shift(1)   & (df['close'] > df['high'].shift(1)), 'signal'] =  1
        df.loc[sell_gate & df['is_overbought'].shift(1) & (df['close'] < df['low'].shift(1)),  'signal'] = -1

        return df

    def validate_params(self) -> bool:
        return True


# ═══════════════════════════════════════════════════════════════════════════
# ARCHIVED STRATEGY: volatility_contraction
# ═══════════════════════════════════════════════════════════════════════════
import pandas as pd
import ta_compat as ta
from strategies.base_strategy import BaseStrategy

class VolatilityContraction(BaseStrategy):
    """
    Volatility Contraction Breakout
    
    Logic:
    1. Contraction: ATR(20) is at its lowest level in 100 bars.
    2. Range: Define a 'squeeze range' of recent N bars.
    3. Signal: Entry when price breaks out of the squeeze range with high volume.
    4. Guard: ADX must be low (< 20) during the squeeze and rising during breakout.
    """

    def __init__(self, params: dict = None):
        if params is None:
            params = {
                "atr_period": 20,
                "atr_lookback": 100,
                "range_bars": 10,
                "vol_spike": 1.5,
                "tp_atr_mult": 3.0,
                "sl_atr_mult": 1.5
            }
        super().__init__(
            name="Volatility_Contraction",
            category="Breakout",
            params=params,
            regime=["LOW_VOL", "ANY"],
            timeframes=["D1", "H4"],
            pairs=["USDJPY", "ETHUSD"]
        )

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()
        
        # 1. Volatility Contraction
        df['atr'] = ta.atr(df['high'], df['low'], df['close'], length=self.params['atr_period'])
        df['min_atr'] = df['atr'].rolling(window=self.params['atr_lookback']).min()
        df['is_contracted'] = df['atr'] <= (df['min_atr'] * 1.1) # Within 10% of minimum
        
        # 2. Squeeze Range
        df['range_h'] = df['high'].rolling(window=self.params['range_bars']).max().shift(1)
        df['range_l'] = df['low'].rolling(window=self.params['range_bars']).min().shift(1)
        
        # 3. Volume spike
        df['avg_vol'] = df['tick_volume'].rolling(window=50).mean()
        df['vol_ok'] = df['tick_volume'] > (df['avg_vol'] * self.params['vol_spike'])
        
        # 4. Signals
        df['signal'] = 0
        df.loc[df['is_contracted'].shift(1) & (df['close'] > df['range_h']) & df['vol_ok'], 'signal'] = 1
        df.loc[df['is_contracted'].shift(1) & (df['close'] < df['range_l']) & df['vol_ok'], 'signal'] = -1
        
        return df

    def validate_params(self) -> bool:
        return True
