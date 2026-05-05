#!/usr/bin/env python3
"""
scripts/review_optimizer.py
============================
Targeted optimizer for overnight-backtest REVIEW strategies.

Two jobs in one pass:
  1. REVIEW combos (WR < 60%) — run grid search to find params that push WR toward 60%.
  2. PASS combos (WR >= 60%)  — re-test on M15 + H1 timeframes to see if shorter
     horizons produce better or worse results.

Auto-promotion rule:
  Any combo that achieves WR >= 50% during optimization is written into
  the `needs_tweaking` section of config/strategies.yaml for manual follow-up.

Usage:
    docker exec tradepanel-backend python scripts/review_optimizer.py
    docker exec tradepanel-backend python scripts/review_optimizer.py --quick
    docker exec tradepanel-backend python scripts/review_optimizer.py --strategy ma_crossover rsi_pullback
    docker exec tradepanel-backend python scripts/review_optimizer.py --date 20260430

Output:
    results/overnight/review_optimization_YYYYMMDD_HHMMSS.md   (human report)
    results/overnight/review_optimization_YYYYMMDD_HHMMSS.json (machine summary)
    config/strategies.yaml  (needs_tweaking section updated in-place)
"""

import sys
import os
import json
import argparse
import itertools
import re
from pathlib import Path
from datetime import datetime, timezone

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from backtesting.engine import BacktestEngine

# ── Constants ────────────────────────────────────────────────────────────────
PROMOTE_WR    = 50.0   # WR% at which a combo is promoted to needs_tweaking
TARGET_WR     = 60.0   # WR% we aim for during grid search
PASS_WR       = 60.0   # WR% already considered passing in overnight results
MIN_TRADES    = 5      # Minimum trades for a result to count
SCALPER_MIN_TRADES = 20

SCALPER_STRATEGIES = {
    "fast_ma_scalper", "bb_squeeze_scalp", "rsi_extremes_scalp",
    "macd_zero_scalp", "volatility_breakout_scalp", "ema_ribbon_scalp",
}

# Timeframes to test for already-passing combos
TF_COMPARISON = ["M15", "H1"]

# ── Overnight-name → optimizer-name mapping ──────────────────────────────────
# The overnight backtest uses strategy keys from run_overnight_backtest.py,
# while param_optimizer.py uses slightly different keys in a few cases.
OVERNIGHT_TO_OPT = {
    "ma_crossover":             "moving_average_crossover",
    "gold_momentum_breakout":   "gold_momentum_breakout",
    "rsi_bounce":               "rsi_bounce",
    "rsi_pullback":             "rsi_pullback",
    "bb_squeeze_scalp":         "bb_squeeze_scalp",
    "rsi_extremes_scalp":       "rsi_extremes_scalp",
    "fast_ma_scalper":          "fast_ma_scalper",
    "macd_zero_scalp":          "macd_zero_scalp",
    "volatility_breakout_scalp":"volatility_breakout_scalp",
    "ema_ribbon_scalp":         "ema_ribbon_scalp",
    "dual_ema_fractal":         "dual_ema_fractal",
    "bb_mean_reversion":        "bb_mean_reversion",
    "macd_trend":               "macd_trend",
    "stoch_divergence":         "stoch_divergence",
    "range_breakout":           "range_breakout",
    "ema_ribbon_trend":         "ema_ribbon_trend",
    "session_momentum":         "session_momentum",
    "turtle_soup":              "turtle_soup",
    "dual_ema_momentum":        "dual_ema_momentum",
    "vwap_momentum":            "vwap_momentum",
    "hikkake_trap":             "hikkake_trap",
    "rvgi_cci_confluence":      "rvgi_cci_confluence",
    # External-data strategies — grid search not possible
    "stat_arb_gold_silver":     None,
    "cot_sentiment":            None,
    "crypto_rsi_extremes":      None,
}

# ── OHLCV generator (identical to param_optimizer) ───────────────────────────
PAIR_SPECS = {
    "XAUUSD": {"price": 2350.0,  "daily_vol": 18.0,  "trend_strength": 0.55},
    "EURUSD": {"price": 1.0850,  "daily_vol": 0.007, "trend_strength": 0.45},
    "GBPUSD": {"price": 1.2700,  "daily_vol": 0.010, "trend_strength": 0.48},
    "USDJPY": {"price": 154.0,   "daily_vol": 1.0,   "trend_strength": 0.50},
    "XAGUSD": {"price": 28.0,    "daily_vol": 0.45,  "trend_strength": 0.50},
    "GBPJPY": {"price": 195.0,   "daily_vol": 1.4,   "trend_strength": 0.52},
    "AUDUSD": {"price": 0.6500,  "daily_vol": 0.007, "trend_strength": 0.46},
    "USDCAD": {"price": 1.3600,  "daily_vol": 0.008, "trend_strength": 0.46},
    "BTCUSD": {"price": 67000.0, "daily_vol": 1800.0,"trend_strength": 0.60},
    "ETHUSD": {"price": 3200.0,  "daily_vol": 120.0, "trend_strength": 0.58},
    "USOIL":  {"price": 78.0,    "daily_vol": 1.2,   "trend_strength": 0.50},
    "XAGUSD": {"price": 28.0,    "daily_vol": 0.45,  "trend_strength": 0.50},
    "US500":  {"price": 5100.0,  "daily_vol": 55.0,  "trend_strength": 0.50},
    "USTEC":  {"price": 18000.0, "daily_vol": 250.0, "trend_strength": 0.52},
    "NVDA":   {"price": 850.0,   "daily_vol": 30.0,  "trend_strength": 0.55},
    "AAPL":   {"price": 185.0,   "daily_vol": 4.0,   "trend_strength": 0.48},
    "MSFT":   {"price": 415.0,   "daily_vol": 8.0,   "trend_strength": 0.50},
    "AMD":    {"price": 165.0,   "daily_vol": 7.0,   "trend_strength": 0.52},
}

TF_BARS = {"M1": 8000, "M5": 4000, "M15": 2880, "M30": 1440,
           "H1": 1200, "H4": 500,  "D1": 300,   "W1": 120}
TF_MINS = {"M1": 1, "M5": 5, "M15": 15, "M30": 30,
           "H1": 60, "H4": 240, "D1": 1440, "W1": 10080}


def make_ohlcv(pair: str, timeframe: str, seed: int = 42) -> pd.DataFrame:
    spec = PAIR_SPECS.get(pair, PAIR_SPECS["EURUSD"])
    rng = np.random.default_rng(seed)
    n = TF_BARS.get(timeframe, 500)

    price     = spec["price"]
    daily_vol = spec["daily_vol"]
    tf_mins   = TF_MINS.get(timeframe, 60)
    bar_vol   = daily_vol * np.sqrt(tf_mins / 1440)
    trend_str = spec["trend_strength"]

    closes = [price]
    regime = "trend"
    regime_length = 0
    regime_max = int(rng.integers(20, 80))
    trend_dir = rng.choice([-1, 1])

    for _ in range(1, n):
        regime_length += 1
        if regime_length > regime_max:
            regime = rng.choice(["trend", "range", "volatile"], p=[0.40, 0.40, 0.20])
            regime_max = int(rng.integers(20, 80))
            regime_length = 0
            trend_dir = rng.choice([-1, 1])

        if regime == "trend":
            drift = trend_dir * bar_vol * trend_str * 0.3
            noise = rng.normal(0, bar_vol * 0.7)
        elif regime == "range":
            drift = -0.05 * (closes[-1] - price) / price * closes[-1]
            noise = rng.normal(0, bar_vol * 0.8)
        else:
            drift = 0
            noise = rng.normal(0, bar_vol * 2.0)

        new_close = max(closes[-1] + drift + noise, spec["price"] * 0.5)
        closes.append(new_close)

    closes = np.array(closes)
    high_extra = np.abs(rng.normal(0, bar_vol * 0.5, n))
    low_extra  = np.abs(rng.normal(0, bar_vol * 0.5, n))
    opens = np.roll(closes, 1); opens[0] = closes[0]
    highs = np.maximum(closes, opens) + high_extra
    lows  = np.minimum(closes, opens) - low_extra

    base_vol  = rng.integers(200, 800, n).astype(float)
    hour_idx  = (np.arange(n) * tf_mins // 60) % 24
    vol_mult  = np.where((hour_idx >= 8) & (hour_idx < 17), 2.0,
                np.where((hour_idx >= 13) & (hour_idx < 20), 1.8, 0.7))
    volumes   = (base_vol * vol_mult).astype(int)

    from datetime import timedelta
    start_dt = datetime(2023, 1, 2, 7, 0)
    idx = [start_dt + timedelta(minutes=i * tf_mins) for i in range(n)]
    return pd.DataFrame(
        {"open": opens, "high": highs, "low": lows, "close": closes, "tick_volume": volumes},
        index=idx
    )


def run_single(strategy_cls, params: dict, pair: str, timeframe: str, seed: int = 42) -> dict:
    """Run one backtest, return metrics dict or None."""
    try:
        inst = strategy_cls(params=params)
        if not inst.validate_params():
            return None
        df = make_ohlcv(pair, timeframe, seed=seed)
        engine = BacktestEngine(lot_size=0.1)
        trades_df, _ = engine.run(inst, pair, timeframe, df, silent=True)

        if trades_df is None or trades_df.empty:
            return {"win_rate": 0, "trades": 0, "profit_factor": 0,
                    "max_dd": 0, "sharpe": 0, "pnl_zar": 0}

        wins  = (trades_df["net_pnl"] > 0).sum()
        total = len(trades_df)
        wr    = 100 * wins / total if total > 0 else 0
        gross_profit = trades_df.loc[trades_df["net_pnl"] > 0, "net_pnl"].sum()
        gross_loss   = abs(trades_df.loc[trades_df["net_pnl"] < 0, "net_pnl"].sum())
        pf = gross_profit / gross_loss if gross_loss > 0 else (99.0 if gross_profit > 0 else 0.0)
        bal    = engine.initial_balance + trades_df["net_pnl_zar"].cumsum()
        peak   = bal.cummax()
        dd     = ((peak - bal) / peak * 100).max()
        rets   = trades_df["net_pnl_zar"].values
        sharpe = (rets.mean() / rets.std() * np.sqrt(252)
                  if len(rets) > 1 and rets.std() > 0 else 0.0)
        return {
            "win_rate":      round(wr, 2),
            "trades":        total,
            "profit_factor": round(pf, 3),
            "max_dd":        round(dd, 2),
            "sharpe":        round(sharpe, 3),
            "pnl_zar":       round(trades_df["net_pnl_zar"].sum(), 2),
        }
    except Exception as e:
        return None


def avg_seeds(strategy_cls, params: dict, pair: str, tf: str,
              seeds=(42, 123, 777), min_trades: int = 5) -> dict | None:
    """Run across multiple seeds and return averaged metrics."""
    results = []
    for seed in seeds:
        r = run_single(strategy_cls, params, pair, tf, seed=seed)
        if r and r["trades"] >= min_trades:
            results.append(r)
    if not results:
        return None
    return {
        "win_rate":      round(np.mean([r["win_rate"]      for r in results]), 2),
        "profit_factor": round(np.mean([r["profit_factor"] for r in results]), 3),
        "max_dd":        round(np.mean([r["max_dd"]        for r in results]), 2),
        "sharpe":        round(np.mean([r["sharpe"]        for r in results]), 3),
        "pnl_zar":       round(np.mean([r["pnl_zar"]       for r in results]), 2),
        "trades":        round(np.mean([r["trades"]        for r in results]), 1),
    }


# ── Parameter grids (mirrors param_optimizer.py) ─────────────────────────────
GRIDS = {
    "moving_average_crossover": {
        "fast_period":   [5, 9, 15],
        "slow_period":   [30, 50, 100],
        "adx_filter":    [20, 25, 28],
        "tp_atr_mult":   [2.0],
        "sl_atr_mult":   [0.8, 1.0],
        "atr_period":    [14],
    },
    "gold_momentum_breakout": {
        "bb_length":     [14, 20],
        "rsi_length":    [14],
        "rsi_buy_min":   [50, 55, 60],
        "rsi_sell_max":  [40, 45, 50],
        "tp_atr_mult":   [2.0],
        "sl_atr_mult":   [0.8, 1.0],
        "atr_period":    [14],
    },
    "rsi_bounce": {
        "rsi_period":    [7, 14],
        "oversold":      [20, 25, 30],
        "overbought":    [70, 75, 80],
        "tp_atr_mult":   [2.0],
        "sl_atr_mult":   [0.8, 1.0],
        "atr_period":    [14],
    },
    "rsi_pullback": {
        "rsi_period":         [14],
        "fast_ema":           [20, 50],
        "slow_ema":           [100, 200],
        "rsi_pullback_lower": [30, 35, 40],
        "rsi_pullback_upper": [50, 55, 60],
        "tp_atr_mult":        [2.0],
        "sl_atr_mult":        [0.8, 1.0],
        "atr_period":         [14],
    },
    "bb_squeeze_scalp": {
        "bb_period":     [10, 14, 20],
        "bb_std":        [1.5, 2.0],
        "squeeze_bars":  [3, 5],
        "tp_atr_mult":   [2.0],
        "sl_atr_mult":   [0.8, 1.0],
        "atr_period":    [14],
    },
    "rsi_extremes_scalp": {
        "rsi_period":    [7, 14],
        "oversold":      [20, 25, 30],
        "overbought":    [70, 75, 80],
        "tp_atr_mult":   [2.0],
        "sl_atr_mult":   [0.8, 1.0],
        "atr_period":    [14],
    },
    "fast_ma_scalper": {
        "fast_period":   [3, 5, 7],
        "slow_period":   [10, 15, 20],
        "min_adx":       [20, 22, 25],
        "tp_atr_mult":   [2.0],
        "sl_atr_mult":   [0.8, 1.0],
        "atr_period":    [14],
    },
    "macd_zero_scalp": {
        "macd_fast":     [8, 12],
        "macd_slow":     [21, 26],
        "macd_signal":   [9],
        "volume_filter": [1.0, 1.2, 1.5],
        "tp_atr_mult":   [2.0],
        "sl_atr_mult":   [0.8, 1.0],
        "atr_period":    [14],
    },
    "volatility_breakout_scalp": {
        "atr_period":      [7, 14],
        "atr_multiplier":  [1.5, 1.8, 2.0],
        "momentum_period": [5, 10],
        "tp_atr_mult":     [2.0],
        "sl_atr_mult":     [0.8, 1.0],
    },
    "ema_ribbon_scalp": {
        "fast_ema":              [3, 5],
        "mid_ema":               [8, 13],
        "slow_ema":              [21, 34],
        "min_ribbon_separation": [0.0002, 0.0005, 0.001],
        "tp_atr_mult":           [2.0],
        "sl_atr_mult":           [0.8, 1.0],
        "atr_period":            [14],
    },
    "dual_ema_fractal": {
        "ema_period":    [50, 100, 200],
        "adx_min":       [22, 25, 28],
        "tp_atr_mult":   [2.0],
        "sl_atr_mult":   [0.8, 1.0],
        "atr_period":    [14],
    },
    "bb_mean_reversion": {
        "bb_period":     [14, 20],
        "bb_deviation":  [2.5, 3.0],
        "rsi_period":    [14],
        "rsi_os_low":    [20, 25],
        "rsi_ob_high":   [75, 80],
        "vol_threshold_mult": [1.0, 1.2],
        "tp_atr_mult":   [2.0],
        "sl_atr_mult":   [0.8, 1.0],
        "atr_period":    [14],
    },
    "macd_trend": {
        "macd_fast":     [8, 12],
        "macd_slow":     [21, 26],
        "macd_signal":   [9],
        "adx_threshold": [20, 25, 28],
        "tp_atr_mult":   [2.0],
        "sl_atr_mult":   [0.8, 1.0],
        "atr_period":    [14],
    },
    "stoch_divergence": {
        "stoch_period":      [5, 9, 14],
        "stoch_oversold":    [20, 25],
        "stoch_overbought":  [75, 80],
        "tp_atr_mult":       [2.0],
        "sl_atr_mult":       [0.8, 1.0],
        "atr_period":        [14],
    },
    "range_breakout": {
        "consolidation_bars":  [10, 20],
        "vol_threshold_mult":  [1.2, 1.5],
        "adx_min_filter":      [15, 20, 25],
        "tp_atr_mult":         [2.0],
        "sl_atr_mult":         [0.8, 1.0],
        "atr_period":          [14],
    },
    "ema_ribbon_trend": {
        "fast_ema":      [8, 13],
        "mid_ema":       [21, 34],
        "slow_ema":      [55, 89],
        "adx_min":       [20, 25, 28],
        "tp_atr_mult":   [2.0],
        "sl_atr_mult":   [0.8, 1.0],
        "atr_period":    [14],
    },
    "session_momentum": {
        "fast_ema":          [8, 12, 20],
        "slow_ema":          [21, 34, 50],
        "min_adx_filter":    [15, 20, 25],
        "vol_threshold_mult":[1.0, 1.2],
        "tp_atr_mult":       [2.0],
        "sl_atr_mult":       [0.8, 1.0],
        "atr_period":        [14],
    },
    "turtle_soup": {
        "lookback":      [10, 20, 55],
        "cooldown_bars": [4, 6, 8],
        "tp_atr_mult":   [2.0],
        "sl_atr_mult":   [0.8, 1.0],
        "atr_period":    [14],
    },
    "dual_ema_momentum": {
        "fast_ema":      [10, 20, 50],
        "slow_ema":      [50, 100, 200],
        "adx_min":       [20, 25, 28],
        "tp_atr_mult":   [2.0],
        "sl_atr_mult":   [0.8, 1.0],
        "atr_period":    [14],
    },
    "vwap_momentum": {
        "std_dev_mult":  [1.0, 1.5, 2.0],
        "tp_atr_mult":   [2.0],
        "sl_atr_mult":   [0.8, 1.0],
        "atr_period":    [14],
    },
    "hikkake_trap": {
        "cooldown_bars": [4, 6, 8, 12],
        "tp_atr_mult":   [2.0],
        "sl_atr_mult":   [0.8, 1.0],
        "atr_period":    [14],
    },
    "rvgi_cci_confluence": {
        "rvgi_period":   [8, 10, 14],
        "cci_period":    [14, 20],
        "sma_period":    [20, 50],
        "cci_buy_min":   [-80, -50, -20],
        "cci_sell_max":  [20, 50, 80],
        "tp_atr_mult":   [2.0],
        "sl_atr_mult":   [0.8, 1.0],
        "atr_period":    [14],
    },
}


def load_strategy_classes() -> dict:
    """Return {opt_name: class}."""
    from strategies.ma_crossover            import MACrossoverStrategy
    from strategies.gold_momentum_breakout  import GoldMomentumBreakoutStrategy
    from strategies.rsi_bounce              import RSIBounceStrategy
    from strategies.rsi_pullback            import RSIPullbackStrategy
    from strategies.bb_squeeze_scalp        import BBSqueezeScalp
    from strategies.rsi_extremes_scalp      import RSIExtremesScalp
    from strategies.fast_ma_scalper         import FastMAScalper
    from strategies.macd_zero_scalp         import MACDZeroScalp
    from strategies.volatility_breakout_scalp import VolatilityBreakoutScalp
    from strategies.ema_ribbon_scalp        import EMARibbonScalp
    from strategies.dual_ema_fractal        import DualEMAFractal
    from strategies.bb_mean_reversion       import BBMeanReversionStrategy
    from strategies.macd_trend              import MACDTrendStrategy
    from strategies.stoch_divergence        import StochDivergenceStrategy
    from strategies.range_breakout          import RangeBreakoutStrategy
    from strategies.ema_ribbon_trend        import EMARibbonTrendStrategy
    from strategies.session_momentum        import SessionMomentumStrategy
    from strategies.turtle_soup             import TurtleSoup
    from strategies.dual_ema_momentum       import DualEMAMomentum
    from strategies.vwap_momentum           import VWAPMomentum
    from strategies.hikkake_trap            import HikkakeTrap
    from strategies.rvgi_cci_confluence     import RVGICCIConfluence

    return {
        "moving_average_crossover":  MACrossoverStrategy,
        "gold_momentum_breakout":    GoldMomentumBreakoutStrategy,
        "rsi_bounce":                RSIBounceStrategy,
        "rsi_pullback":              RSIPullbackStrategy,
        "bb_squeeze_scalp":          BBSqueezeScalp,
        "rsi_extremes_scalp":        RSIExtremesScalp,
        "fast_ma_scalper":           FastMAScalper,
        "macd_zero_scalp":           MACDZeroScalp,
        "volatility_breakout_scalp": VolatilityBreakoutScalp,
        "ema_ribbon_scalp":          EMARibbonScalp,
        "dual_ema_fractal":          DualEMAFractal,
        "bb_mean_reversion":         BBMeanReversionStrategy,
        "macd_trend":                MACDTrendStrategy,
        "stoch_divergence":          StochDivergenceStrategy,
        "range_breakout":            RangeBreakoutStrategy,
        "ema_ribbon_trend":          EMARibbonTrendStrategy,
        "session_momentum":          SessionMomentumStrategy,
        "turtle_soup":               TurtleSoup,
        "dual_ema_momentum":         DualEMAMomentum,
        "vwap_momentum":             VWAPMomentum,
        "hikkake_trap":              HikkakeTrap,
        "rvgi_cci_confluence":       RVGICCIConfluence,
    }


def grid_search(opt_name: str, cls, pair: str, tf: str,
                quick: bool = False, seeds=(42, 123, 777)) -> dict:
    """Grid search for best params. Returns {params, metrics}."""
    if opt_name not in GRIDS:
        return {"params": None, "metrics": None, "reason": "no_grid"}

    grid = GRIDS[opt_name]
    keys   = list(grid.keys())
    values = list(grid.values())
    all_combos = list(itertools.product(*values))

    max_combos = 40 if quick else 300
    if len(all_combos) > max_combos:
        rng = np.random.default_rng(42)
        idx = rng.choice(len(all_combos), max_combos, replace=False)
        all_combos = [all_combos[i] for i in sorted(idx)]

    is_scalper   = opt_name in SCALPER_STRATEGIES
    min_trades   = SCALPER_MIN_TRADES if is_scalper else MIN_TRADES

    # Scalpers: skip D1/W1 (too few bars at higher timeframes)
    if is_scalper and TF_MINS.get(tf, 60) >= TF_MINS["D1"]:
        return {"params": None, "metrics": None, "reason": "scalper_tf_too_high"}

    best_score  = -999
    best_params = None
    best_metrics = None

    for combo in all_combos:
        params = dict(zip(keys, combo))
        m = avg_seeds(cls, params, pair, tf, seeds=seeds, min_trades=min_trades)
        if m is None:
            continue
        # Primary: WR; bonus: PF if DD < 20%
        score = m["win_rate"] + (m["profit_factor"] * 2.0 if m["max_dd"] < 20 else 0)
        if score > best_score:
            best_score   = score
            best_params  = params
            best_metrics = m

    return {"params": best_params, "metrics": best_metrics}


def load_latest_overnight(results_dir: Path, date_filter: str = None) -> tuple[dict, str]:
    """Return (report_data, filename) for the most recent overnight backtest."""
    overnight_dir = results_dir / "overnight"
    if not overnight_dir.exists():
        return None, None

    pattern = f"{date_filter}_backtest_report.json" if date_filter else "*_backtest_report.json"
    files = sorted(overnight_dir.glob(pattern), reverse=True)
    # Prefer non-numbered files (avoid backtest_report1.json re-runs)
    clean = [f for f in files if not re.search(r"report\d+\.json$", f.name)]
    target = (clean or files)
    if not target:
        return None, None

    with open(target[0]) as f:
        return json.load(f), target[0].name


def update_strategies_yaml(yaml_path: Path, promotions: list[dict]) -> int:
    """
    Upsert the `needs_tweaking` section in strategies.yaml.
    Promotions: list of {strategy, pair, timeframe, win_rate, best_params, ...}
    Returns count of new entries added.
    """
    if not promotions:
        return 0

    content = yaml_path.read_text(encoding="utf-8")

    # Build the block to write
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    lines = []

    # Check if section already exists
    section_marker = "# ── needs_tweaking — auto-promoted by review_optimizer.py"
    if section_marker in content:
        # Remove the old section entirely and re-write it
        # Find start
        start = content.find(section_marker)
        # Find where the next top-level section begins after this one
        # (a line starting with a word char that isn't indented)
        after = content[start:]
        # Find the next top-level key (non-comment, non-indented line with a colon)
        next_section = re.search(r"\n(?=[a-zA-Z])", after[len(section_marker):])
        if next_section:
            end = start + len(section_marker) + next_section.start() + 1
        else:
            end = len(content)
        content = content[:start].rstrip() + "\n"
    else:
        content = content.rstrip() + "\n\n"

    # Group promotions by strategy name for YAML nesting
    by_strategy: dict[str, list] = {}
    for p in promotions:
        by_strategy.setdefault(p["strategy"], []).append(p)

    lines.append(f"\n{section_marker}")
    lines.append(f"# Updated: {ts} | {len(promotions)} combo(s) promoted (WR >= {PROMOTE_WR}%)")
    lines.append(f"# These combos hit the promotion threshold during review_optimizer.py.")
    lines.append(f"# Action: review params, update strategies.yaml strategy block, re-run overnight backtest.")
    lines.append("needs_tweaking:")

    new_count = 0
    for strat_name, entries in sorted(by_strategy.items()):
        lines.append(f"  {strat_name}:")
        for e in sorted(entries, key=lambda x: -x["win_rate"]):
            tag = "✅ PASS" if e["win_rate"] >= TARGET_WR else "🔶 NEAR"
            lines.append(f"    - pair: {e['pair']}")
            lines.append(f"      timeframe: {e['timeframe']}")
            lines.append(f"      win_rate: {e['win_rate']}")
            lines.append(f"      sharpe: {e.get('sharpe', 'n/a')}")
            lines.append(f"      profit_factor: {e.get('profit_factor', 'n/a')}")
            lines.append(f"      status: \"{tag}\"")
            lines.append(f"      promoted_on: {ts}")
            if e.get("best_params"):
                lines.append(f"      suggested_params:")
                for k, v in e["best_params"].items():
                    lines.append(f"        {k}: {v}")
            lines.append("")
            new_count += 1

    new_section = "\n".join(lines) + "\n"
    yaml_path.write_text(content + new_section, encoding="utf-8")
    return new_count


def format_status(wr: float) -> str:
    if wr >= TARGET_WR:   return "✅ PASS"
    if wr >= PROMOTE_WR:  return "🔶 NEAR"
    return "❌ FAIL"


def main():
    parser = argparse.ArgumentParser(description="Review optimizer — push REVIEW combos toward 60% WR")
    parser.add_argument("--quick",    action="store_true", help="Fewer grid combos (~40 max)")
    parser.add_argument("--strategy", nargs="+",           help="Limit to specific strategies")
    parser.add_argument("--date",     type=str,            help="Use overnight report for YYYYMMDD")
    args = parser.parse_args()

    now_utc  = datetime.now(timezone.utc)
    ts_label = now_utc.strftime("%Y%m%d_%H%M%S")
    results_dir = PROJECT_ROOT / "results"
    config_path = PROJECT_ROOT / "config" / "strategies.yaml"

    print(f"\n{'='*72}")
    print(f"  TradePanel Review Optimizer  |  {now_utc.strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"  Mode: {'QUICK' if args.quick else 'FULL'} | Target WR: {TARGET_WR}% | Promote at: {PROMOTE_WR}%")
    print(f"{'='*72}\n")

    # ── Load overnight backtest ───────────────────────────────────────────────
    report, report_file = load_latest_overnight(results_dir, args.date)
    if not report:
        print("ERROR: No overnight backtest report found. Run run_overnight_backtest.py first.")
        sys.exit(1)

    all_results = report.get("results", [])
    print(f"  Loaded: {report_file}  ({len(all_results)} combo results)\n")

    # ── Filter by --strategy if given ────────────────────────────────────────
    if args.strategy:
        all_results = [r for r in all_results if r["strategy"] in args.strategy]
        print(f"  Filtered to {len(all_results)} combos for: {', '.join(args.strategy)}\n")

    # ── Separate PASS (>=60% WR) vs REVIEW (<60% WR or NO_TRADES) ────────────
    pass_combos   = [r for r in all_results if r["status"] == "PASS" and r.get("win_rate", 0) >= PASS_WR]
    review_combos = [r for r in all_results if r["status"] in ("REVIEW", "NO_TRADES")
                     or (r["status"] == "PASS" and r.get("win_rate", 0) < PASS_WR)]

    print(f"  PASS combos (will test on M15+H1): {len(pass_combos)}")
    print(f"  REVIEW/NO_TRADES combos (will optimize): {len(review_combos)}")
    print()

    strategy_classes = load_strategy_classes()
    promotions: list[dict] = []

    # ════════════════════════════════════════════════════════════════════════
    # PART A — Optimize REVIEW combos toward 60% WR
    # ════════════════════════════════════════════════════════════════════════
    print(f"{'─'*72}")
    print("  PART A — Optimizing REVIEW combos")
    print(f"{'─'*72}\n")

    review_results = []
    for i, combo in enumerate(review_combos, 1):
        strat_name  = combo["strategy"]
        pair        = combo["pair"]
        tf          = combo["timeframe"]
        current_wr  = combo.get("win_rate", 0)
        current_trades = combo.get("total_trades", 0)

        opt_name = OVERNIGHT_TO_OPT.get(strat_name)
        print(f"  [{i:>2}/{len(review_combos)}] {strat_name:<30} {pair:<8} {tf:<4} "
              f"(current WR: {current_wr:.1f}%  trades: {current_trades}) ...", end="", flush=True)

        if opt_name is None:
            print(" SKIP (external data)")
            review_results.append({**combo, "opt_status": "SKIPPED_EXTERNAL",
                                    "best_params": None, "optimized_metrics": None})
            continue

        if opt_name not in GRIDS:
            print(" SKIP (no grid)")
            review_results.append({**combo, "opt_status": "SKIPPED_NO_GRID",
                                    "best_params": None, "optimized_metrics": None})
            continue

        cls = strategy_classes.get(opt_name)
        if cls is None:
            print(" SKIP (class not found)")
            review_results.append({**combo, "opt_status": "SKIPPED_NO_CLASS",
                                    "best_params": None, "optimized_metrics": None})
            continue

        result = grid_search(opt_name, cls, pair, tf, quick=args.quick)
        m = result.get("metrics")

        if m is None:
            print(f" NO_RESULT (reason: {result.get('reason', 'no trades')})")
            review_results.append({**combo, "opt_status": "NO_RESULT",
                                    "best_params": None, "optimized_metrics": None})
            continue

        opt_wr = m["win_rate"]
        status = format_status(opt_wr)
        delta  = f"{opt_wr - current_wr:+.1f}pp"
        print(f" → WR {opt_wr:.1f}% ({delta}) {status}")

        entry = {
            **combo,
            "opt_name":          opt_name,
            "opt_status":        "PASS" if opt_wr >= TARGET_WR else ("NEAR" if opt_wr >= PROMOTE_WR else "FAIL"),
            "best_params":       result["params"],
            "optimized_metrics": m,
        }
        review_results.append(entry)

        # Promote if WR >= 50%
        if opt_wr >= PROMOTE_WR:
            promotions.append({
                "strategy":   strat_name,
                "pair":       pair,
                "timeframe":  tf,
                "win_rate":   opt_wr,
                "sharpe":     m.get("sharpe"),
                "profit_factor": m.get("profit_factor"),
                "best_params": result["params"],
                "source":     "review_optimizer_part_a",
            })

    # ════════════════════════════════════════════════════════════════════════
    # PART B — Test PASS combos on M15 + H1 for comparison
    # ════════════════════════════════════════════════════════════════════════
    print(f"\n{'─'*72}")
    print("  PART B — Testing PASS combos on M15 + H1")
    print(f"{'─'*72}\n")

    tf_comparison_results = []
    for i, combo in enumerate(pass_combos, 1):
        strat_name = combo["strategy"]
        pair       = combo["pair"]
        orig_tf    = combo["timeframe"]
        orig_wr    = combo.get("win_rate", 0)

        opt_name = OVERNIGHT_TO_OPT.get(strat_name)
        cls = strategy_classes.get(opt_name) if opt_name else None

        print(f"  [{i:>2}/{len(pass_combos)}] {strat_name:<30} {pair:<8} (original: {orig_tf} WR {orig_wr:.1f}%)")

        tf_row = {
            "strategy": strat_name, "pair": pair, "original_tf": orig_tf,
            "original_wr": orig_wr,
            "tf_results": {"original": {"win_rate": orig_wr,
                                         "sharpe": combo.get("sharpe_ratio", 0),
                                         "trades": combo.get("total_trades", 0)}},
        }

        if cls is None:
            print(f"     SKIP (no class for {opt_name})")
            tf_comparison_results.append(tf_row)
            continue

        # Default params — use empty dict, strategy will use its own defaults
        default_params = {}

        for tf in TF_COMPARISON:
            if tf == orig_tf:
                continue  # Already have original result
            # Skip scalpers on D1; skip non-scalpers if tf is too coarse vs orig
            is_scalper = strat_name in SCALPER_STRATEGIES
            if is_scalper and TF_MINS.get(tf, 60) < 5:
                tf_row["tf_results"][tf] = {"skip": "scalper_tf_too_low"}
                continue

            min_t = SCALPER_MIN_TRADES if is_scalper else MIN_TRADES
            m = avg_seeds(cls, default_params, pair, tf, min_trades=min_t)

            if m:
                wr    = m["win_rate"]
                delta = wr - orig_wr
                arrow = "▲" if delta > 1 else ("▼" if delta < -1 else "~")
                print(f"     {tf:<4}  WR {wr:.1f}%  ({arrow}{abs(delta):.1f}pp vs original)  "
                      f"PF {m['profit_factor']:.2f}  Sharpe {m['sharpe']:.2f}")
                tf_row["tf_results"][tf] = m

                # Promote if WR >= 50% on this new timeframe
                if wr >= PROMOTE_WR and tf not in (orig_tf,):
                    promotions.append({
                        "strategy":      strat_name,
                        "pair":          pair,
                        "timeframe":     tf,
                        "win_rate":      wr,
                        "sharpe":        m.get("sharpe"),
                        "profit_factor": m.get("profit_factor"),
                        "best_params":   None,
                        "source":        f"review_optimizer_part_b (from {orig_tf})",
                    })
            else:
                print(f"     {tf:<4}  NO_RESULT (insufficient trades)")
                tf_row["tf_results"][tf] = {"no_result": True}

        tf_comparison_results.append(tf_row)

    # ════════════════════════════════════════════════════════════════════════
    # PART C — Update strategies.yaml needs_tweaking
    # ════════════════════════════════════════════════════════════════════════
    print(f"\n{'─'*72}")
    print("  PART C — Auto-promoting to needs_tweaking")
    print(f"{'─'*72}\n")

    if promotions:
        added = update_strategies_yaml(config_path, promotions)
        print(f"  {added} combo(s) written to config/strategies.yaml → needs_tweaking section")
        for p in promotions:
            tag = "✅ PASS" if p["win_rate"] >= TARGET_WR else "🔶 NEAR"
            print(f"    {tag}  {p['strategy']:<30} {p['pair']:<8} {p['timeframe']:<4}  WR {p['win_rate']:.1f}%")
    else:
        print("  No combos reached the 50% promotion threshold.")

    # ════════════════════════════════════════════════════════════════════════
    # PART D — Write reports
    # ════════════════════════════════════════════════════════════════════════
    out_base = results_dir / "overnight" / f"review_optimization_{ts_label}"

    # ── JSON summary ─────────────────────────────────────────────────────────
    summary = {
        "generated":       now_utc.isoformat(),
        "source_report":   report_file,
        "mode":            "quick" if args.quick else "full",
        "promote_threshold": PROMOTE_WR,
        "target_wr":       TARGET_WR,
        "part_a_review":   review_results,
        "part_b_tf_comparison": tf_comparison_results,
        "promotions":      promotions,
    }
    json_path = Path(str(out_base) + ".json")
    with open(json_path, "w") as f:
        json.dump(summary, f, indent=2, default=str)

    # ── Markdown report ───────────────────────────────────────────────────────
    md_lines = [
        f"# TradePanel Review Optimizer — {now_utc.strftime('%Y-%m-%d %H:%M UTC')}",
        f"",
        f"Source: `{report_file}` | Mode: {'QUICK' if args.quick else 'FULL'} | "
        f"Promote ≥ {PROMOTE_WR}% | Target ≥ {TARGET_WR}%",
        f"",
        f"---",
        f"",
        f"## Part A — REVIEW Strategy Optimization",
        f"",
        f"Strategies tested: {len(review_combos)} | Skipped: "
        f"{sum(1 for r in review_results if 'SKIP' in r.get('opt_status',''))} | "
        f"Promoted: {sum(1 for r in review_results if r.get('opt_status') in ('PASS','NEAR'))}",
        f"",
        f"| Strategy | Pair | TF | Before WR% | After WR% | Δ | Sharpe | PF | Status |",
        f"|----------|------|----|-----------|----------|---|--------|-----|--------|",
    ]

    for r in review_results:
        m = r.get("optimized_metrics")
        if m:
            before = r.get("win_rate", 0)
            after  = m["win_rate"]
            delta  = f"{after - before:+.1f}pp"
            status = format_status(after)
            md_lines.append(
                f"| {r['strategy']} | {r['pair']} | {r['timeframe']} | "
                f"{before:.1f}% | **{after:.1f}%** | {delta} | "
                f"{m['sharpe']:.2f} | {m['profit_factor']:.2f} | {status} |"
            )
        else:
            md_lines.append(
                f"| {r['strategy']} | {r['pair']} | {r['timeframe']} | "
                f"{r.get('win_rate', 0):.1f}% | — | — | — | — | "
                f"{'SKIP (' + r.get('opt_status','') + ')' } |"
            )

    md_lines += [
        f"",
        f"---",
        f"",
        f"## Part B — PASS Combos on M15 + H1",
        f"",
        f"Strategies tested: {len(pass_combos)}",
        f"",
        f"| Strategy | Pair | Original TF | Original WR% | M15 WR% | H1 WR% | Better TF |",
        f"|----------|------|-------------|-------------|---------|--------|-----------|",
    ]

    for r in tf_comparison_results:
        tf_res  = r.get("tf_results", {})
        m15_wr  = tf_res.get("M15", {}).get("win_rate", "—") if "M15" in tf_res else "—"
        h1_wr   = tf_res.get("H1",  {}).get("win_rate", "—") if "H1"  in tf_res else "—"
        # Find best TF
        candidates = {"original": r["original_wr"]}
        if isinstance(m15_wr, float): candidates["M15"] = m15_wr
        if isinstance(h1_wr,  float): candidates["H1"]  = h1_wr
        best_tf = max(candidates, key=lambda k: candidates[k])

        m15_str = f"{m15_wr:.1f}%" if isinstance(m15_wr, float) else str(m15_wr)
        h1_str  = f"{h1_wr:.1f}%"  if isinstance(h1_wr, float)  else str(h1_wr)
        md_lines.append(
            f"| {r['strategy']} | {r['pair']} | {r['original_tf']} | "
            f"{r['original_wr']:.1f}% | {m15_str} | {h1_str} | **{best_tf}** |"
        )

    # Promotions summary
    md_lines += [
        f"",
        f"---",
        f"",
        f"## Promoted to needs_tweaking ({len(promotions)} combos)",
        f"",
    ]

    if promotions:
        md_lines += [
            f"| Strategy | Pair | TF | WR% | Sharpe | PF | Source |",
            f"|----------|------|----|-----|--------|----|--------|",
        ]
        for p in sorted(promotions, key=lambda x: -x["win_rate"]):
            tag = "✅" if p["win_rate"] >= TARGET_WR else "🔶"
            md_lines.append(
                f"| {tag} {p['strategy']} | {p['pair']} | {p['timeframe']} | "
                f"**{p['win_rate']:.1f}%** | {p.get('sharpe', '—')} | "
                f"{p.get('profit_factor', '—')} | {p.get('source','')} |"
            )
    else:
        md_lines.append("_No combos met the 50% promotion threshold._")

    md_lines += [
        f"",
        f"---",
        f"",
        f"## Next Steps",
        f"",
        f"1. For each `needs_tweaking` entry, update the corresponding strategy block in `config/strategies.yaml` "
        f"   with the `suggested_params`.",
        f"2. Re-run the overnight backtest: `python scripts/run_overnight_backtest.py`",
        f"3. Strategies that achieve WR ≥ {TARGET_WR}% AND Sharpe ≥ 0.8 are candidates for the 2-week "
        f"   forward test (see GO-LIVE ACCEPTANCE CRITERIA in strategies.yaml).",
        f"4. For SKIP (external data) entries (stat_arb_gold_silver, cot_sentiment, crypto_rsi_extremes) "
        f"   — optimize manually by adjusting their respective strategy files.",
        f"",
        f"_Generated by `scripts/review_optimizer.py` — {now_utc.strftime('%Y-%m-%d %H:%M UTC')}_",
    ]

    md_path = Path(str(out_base) + ".md")
    md_path.write_text("\n".join(md_lines), encoding="utf-8")

    # ── Final summary ─────────────────────────────────────────────────────────
    passed_a  = sum(1 for r in review_results if r.get("opt_status") == "PASS")
    near_a    = sum(1 for r in review_results if r.get("opt_status") == "NEAR")
    failed_a  = sum(1 for r in review_results if r.get("opt_status") == "FAIL")
    skipped_a = sum(1 for r in review_results if "SKIP" in r.get("opt_status", "") or "NO" in r.get("opt_status",""))

    print(f"\n{'='*72}")
    print(f"  REVIEW OPTIMIZER COMPLETE")
    print(f"{'='*72}")
    print(f"  Part A (REVIEW → optimizer):  {passed_a} PASS | {near_a} NEAR | {failed_a} FAIL | {skipped_a} SKIP")
    print(f"  Part B (PASS → M15/H1):        {len(pass_combos)} combos tested on new timeframes")
    print(f"  Promotions:                    {len(promotions)} combos → needs_tweaking")
    print(f"  Report:  {md_path.name}")
    print(f"  JSON:    {json_path.name}")
    print(f"{'='*72}\n")


if __name__ == "__main__":
    main()
