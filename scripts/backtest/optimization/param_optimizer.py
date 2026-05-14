#!/usr/bin/env python3
"""
param_optimizer.py -- Grid-search parameter optimizer for 22 strategies.

Generates realistic synthetic OHLCV data per pair/timeframe, runs real
strategy classes through the actual backtest engine, and finds the parameter
set that maximises win rate toward 60%+ target.

Usage:
    python scripts/param_optimizer.py              # all strategies, full grid
    python scripts/param_optimizer.py --strategy dual_ema_fractal rsi_bounce
    python scripts/param_optimizer.py --quick      # fewer grid points (~50 combos max)
"""

import sys, os, json, argparse, itertools
from pathlib import Path
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# EventLogger handles missing DB gracefully (try/except in __init__)
from backtesting.engine import BacktestEngine

# ── Realistic pair characteristics ──────────────────────────────────────────
PAIR_SPECS = {
    "XAUUSD": {"price": 2350.0,  "daily_vol": 18.0,  "pip": 0.10,  "trend_strength": 0.55},
    "EURUSD": {"price": 1.0850,  "daily_vol": 0.007, "pip": 0.0001,"trend_strength": 0.45},
    "GBPUSD": {"price": 1.2700,  "daily_vol": 0.010, "pip": 0.0001,"trend_strength": 0.48},
    "USDJPY": {"price": 154.0,   "daily_vol": 1.0,   "pip": 0.01,  "trend_strength": 0.50},
    "XAGUSD": {"price": 28.0,    "daily_vol": 0.45,  "pip": 0.001, "trend_strength": 0.50},
    "BTCUSD": {"price": 67000.0, "daily_vol": 1800.0,"pip": 1.0,   "trend_strength": 0.60},
    "ETHUSD": {"price": 3200.0,  "daily_vol": 120.0, "pip": 1.0,   "trend_strength": 0.58},
}

TF_BARS = {"M1": 8000, "M5": 4000, "M15": 2880, "M30": 1440,
           "H1": 1200, "H4": 500, "D1": 300, "W1": 120}
TF_MINS = {"M1": 1, "M5": 5, "M15": 15, "M30": 30,
           "H1": 60, "H4": 240, "D1": 1440, "W1": 10080}


def make_ohlcv(pair: str, timeframe: str, n_bars: int = None, seed: int = 42) -> pd.DataFrame:
    """Generate realistic OHLCV with regime-switching GBM."""
    spec = PAIR_SPECS.get(pair, PAIR_SPECS["EURUSD"])
    rng = np.random.default_rng(seed)
    n = n_bars or max(TF_BARS.get(timeframe, 500), 300)

    price = spec["price"]
    daily_vol = spec["daily_vol"]
    tf_mins = TF_MINS.get(timeframe, 60)
    bar_vol = daily_vol * np.sqrt(tf_mins / 1440)
    trend_str = spec["trend_strength"]

    closes = [price]
    regime = "trend"
    regime_length = 0
    regime_max = int(rng.integers(20, 80))
    trend_dir = rng.choice([-1, 1])

    for i in range(1, n):
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

    base_vol = rng.integers(200, 800, n).astype(float)
    hour_of_bar = (np.arange(n) * tf_mins // 60) % 24
    vol_mult = np.where((hour_of_bar >= 8) & (hour_of_bar < 17), 2.0,
               np.where((hour_of_bar >= 13) & (hour_of_bar < 20), 1.8, 0.7))
    volumes = (base_vol * vol_mult).astype(int)

    start_dt = datetime(2023, 1, 2, 7, 0)
    idx = [start_dt + timedelta(minutes=i * tf_mins) for i in range(n)]
    return pd.DataFrame({"open": opens, "high": highs, "low": lows,
                         "close": closes, "tick_volume": volumes}, index=idx)


def run_backtest(strategy_cls, params: dict, pair: str, timeframe: str,
                 n_bars: int = None, seed: int = 42) -> dict:
    """Run strategy through engine, return metrics or None."""
    try:
        inst = strategy_cls(params=params)
        if not inst.validate_params():
            return None
        df = make_ohlcv(pair, timeframe, n_bars, seed=seed)
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
        pf = gross_profit / gross_loss if gross_loss > 0 else (99.0 if gross_profit > 0 else 0)

        bal  = engine.initial_balance + trades_df["net_pnl_zar"].cumsum()
        peak = bal.cummax()
        dd   = ((peak - bal) / peak * 100).max()

        returns = trades_df["net_pnl_zar"].values
        sharpe  = (returns.mean() / returns.std() * np.sqrt(252)
                   if len(returns) > 1 and returns.std() > 0 else 0)

        return {
            "win_rate":      round(wr, 2),
            "trades":        total,
            "profit_factor": round(pf, 3),
            "max_dd":        round(dd, 2),
            "sharpe":        round(sharpe, 3),
            "pnl_zar":       round(trades_df["net_pnl_zar"].sum(), 2),
        }
    except Exception:
        return None


# ── Parameter grids (param names verified against each strategy's generate_signals) ──
GRIDS = {
    # --- TIER 1 ---
    "dual_ema_fractal": {
        "ema_period":    [50, 100, 200],
        "adx_min":       [22, 25, 28, 30],
        "tp_atr_mult":   [2.0],
        "sl_atr_mult":   [0.8, 1.0],
        "atr_period":    [14],
    },
    "moving_average_crossover": {
        "fast_period":   [5, 9, 15],
        "slow_period":   [30, 50, 100],
        "adx_filter":    [20, 25, 28],
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
    "gold_momentum_breakout": {
        "bb_length":     [14, 20],
        "rsi_length":    [14],
        "rsi_buy_min":   [50, 55, 60],
        "rsi_sell_max":  [40, 45, 50],
        "tp_atr_mult":   [2.0],
        "sl_atr_mult":   [0.8, 1.0],
        "atr_period":    [14],
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
    # --- TIER 2 ---
    "session_momentum": {
        "fast_ema":          [8, 12, 20],
        "slow_ema":          [21, 34, 50],
        "min_adx_filter":    [15, 20, 25],
        "vol_threshold_mult":[1.0, 1.2],
        "tp_atr_mult":       [2.0],
        "sl_atr_mult":       [0.8, 1.0],
        "atr_period":        [14],
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
    # --- TIER 2 SCALPERS ---
    "fast_ma_scalper": {
        "fast_period":   [3, 5, 7],
        "slow_period":   [10, 15, 20],
        "min_adx":       [20, 22, 25],
        "tp_atr_mult":   [2.0],
        "sl_atr_mult":   [0.8, 1.0],
        "atr_period":    [14],
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
}
# stat_arb_gold_silver and cot_sentiment use external data -- excluded from grid search

# ── Scalper guard ─────────────────────────────────────────────────────────────
# ROOT CAUSE (2026-04-26): Scalpers optimized on M5 synthetic data showed 60-83% WR,
# but the overnight backtest ran them on M1 (their strategies.yaml timeframes).
# Real M1 data has proportionally larger spread cost and much higher noise —
# strategies that look good on M5 GBM collapse to 11-17% WR on M1 real data.
#
# RULE: Scalpers must ONLY be optimized AND deployed on M5 or higher.
#       If a scalper strategy is re-enabled, its strategies.yaml `timeframes:` list
#       must NOT include M1. The optimizer will warn if timeframe mismatch is detected.
#
SCALPER_STRATEGIES = {
    "fast_ma_scalper", "bb_squeeze_scalp", "rsi_extremes_scalp",
    "macd_zero_scalp", "volatility_breakout_scalp", "ema_ribbon_scalp",
}
SCALPER_MIN_TF   = "M5"   # Minimum timeframe for scalper optimization
SCALPER_MIN_TF_MINS = 5   # minutes — M1 (1 min) is below this, M5+ is OK
SCALPER_MIN_TRADES = 20   # Higher trade floor for scalpers to avoid noise fits


def load_all_strategies() -> dict:
    """Import all strategy classes. Returns {name: (class, default_pair, default_tf)}."""
    from strategies.dual_ema_fractal        import DualEMAFractal
    from strategies.ma_crossover            import MACrossoverStrategy
    from strategies.rsi_bounce              import RSIBounceStrategy
    from strategies.bb_mean_reversion       import BBMeanReversionStrategy
    from strategies.macd_trend              import MACDTrendStrategy
    from strategies.stoch_divergence        import StochDivergenceStrategy
    from strategies.range_breakout          import RangeBreakoutStrategy
    from strategies.gold_momentum_breakout  import GoldMomentumBreakoutStrategy
    from strategies.ema_ribbon_trend        import EMARibbonTrendStrategy
    from strategies.session_momentum        import SessionMomentumStrategy
    from strategies.rsi_pullback            import RSIPullbackStrategy
    from strategies.turtle_soup             import TurtleSoup
    from strategies.dual_ema_momentum       import DualEMAMomentum
    from strategies.vwap_momentum           import VWAPMomentum
    from strategies.hikkake_trap            import HikkakeTrap
    from strategies.rvgi_cci_confluence     import RVGICCIConfluence
    from strategies.fast_ma_scalper         import FastMAScalper
    from strategies.bb_squeeze_scalp        import BBSqueezeScalp
    from strategies.rsi_extremes_scalp      import RSIExtremesScalp
    from strategies.macd_zero_scalp         import MACDZeroScalp
    from strategies.volatility_breakout_scalp import VolatilityBreakoutScalp
    from strategies.ema_ribbon_scalp        import EMARibbonScalp

    return {
        "dual_ema_fractal":          (DualEMAFractal,               "XAUUSD", "H1"),
        "moving_average_crossover":  (MACrossoverStrategy,          "EURUSD", "H1"),
        "rsi_bounce":                (RSIBounceStrategy,            "EURUSD", "H1"),
        "bb_mean_reversion":         (BBMeanReversionStrategy,      "XAUUSD", "H1"),
        "macd_trend":                (MACDTrendStrategy,            "EURUSD", "H1"),
        "stoch_divergence":          (StochDivergenceStrategy,      "EURUSD", "H4"),
        "range_breakout":            (RangeBreakoutStrategy,        "XAUUSD", "H4"),
        "gold_momentum_breakout":    (GoldMomentumBreakoutStrategy, "XAUUSD", "H1"),
        "ema_ribbon_trend":          (EMARibbonTrendStrategy,       "BTCUSD", "H4"),
        "session_momentum":          (SessionMomentumStrategy,      "XAUUSD", "H1"),
        "rsi_pullback":              (RSIPullbackStrategy,          "XAUUSD", "H4"),
        "turtle_soup":               (TurtleSoup,                   "EURUSD", "H4"),
        "dual_ema_momentum":         (DualEMAMomentum,              "XAUUSD", "H1"),
        "vwap_momentum":             (VWAPMomentum,                 "GBPUSD", "M15"),
        "hikkake_trap":              (HikkakeTrap,                  "XAUUSD", "H4"),
        "rvgi_cci_confluence":       (RVGICCIConfluence,            "EURUSD", "H1"),
        "fast_ma_scalper":           (FastMAScalper,                "EURUSD", "M5"),
        "bb_squeeze_scalp":          (BBSqueezeScalp,               "EURUSD", "M5"),
        "rsi_extremes_scalp":        (RSIExtremesScalp,             "XAUUSD", "M5"),
        "macd_zero_scalp":           (MACDZeroScalp,                "EURUSD", "M5"),
        "volatility_breakout_scalp": (VolatilityBreakoutScalp,      "XAUUSD", "M5"),
        "ema_ribbon_scalp":          (EMARibbonScalp,               "EURUSD", "M5"),
    }


def grid_search(name: str, cls, pair: str, tf: str, grid: dict,
                quick: bool = False, seeds=(42, 123, 777)) -> dict:
    """Exhaustive grid search averaged over seeds. Returns best params + metrics."""
    keys   = list(grid.keys())
    values = list(grid.values())
    all_combos = list(itertools.product(*values))

    max_combos = 50 if quick else 400
    if len(all_combos) > max_combos:
        rng = np.random.default_rng(42)
        idx = rng.choice(len(all_combos), max_combos, replace=False)
        all_combos = [all_combos[i] for i in sorted(idx)]

    # Scalpers need more trades to avoid noise fits on synthetic data
    min_trades = SCALPER_MIN_TRADES if name in SCALPER_STRATEGIES else 5

    best_score  = -999
    best_params = None
    best_result = None

    for combo in all_combos:
        params = dict(zip(keys, combo))

        seed_results = []
        for seed in seeds:
            r = run_backtest(cls, params, pair, tf, seed=seed)
            if r and r["trades"] >= min_trades:
                seed_results.append(r)

        if not seed_results:
            continue

        avg_wr  = np.mean([r["win_rate"]      for r in seed_results])
        avg_pf  = np.mean([r["profit_factor"] for r in seed_results])
        avg_dd  = np.mean([r["max_dd"]        for r in seed_results])
        avg_sh  = np.mean([r["sharpe"]        for r in seed_results])
        avg_pnl = np.mean([r["pnl_zar"]       for r in seed_results])
        avg_tr  = np.mean([r["trades"]        for r in seed_results])

        # Score: win_rate primary; profit_factor bonus if DD < 20%
        score = avg_wr + (avg_pf * 2.0 if avg_dd < 20 else 0)

        if score > best_score:
            best_score  = score
            best_params = params
            best_result = {
                "win_rate":      round(avg_wr, 2),
                "profit_factor": round(avg_pf, 3),
                "max_dd":        round(avg_dd, 2),
                "sharpe":        round(avg_sh, 3),
                "pnl_zar":       round(avg_pnl, 2),
                "trades":        round(avg_tr, 1),
            }

    return {"params": best_params, "metrics": best_result}


def run_all(target_strategies=None, quick=False):
    """Run grid search for all (or selected) strategies. Print summary and save JSON."""
    strats = load_all_strategies()
    if target_strategies:
        strats = {k: v for k, v in strats.items() if k in target_strategies}

    eligible = [s for s in strats if s in GRIDS]
    total = len(eligible)
    done  = 0

    print(f"\n{'='*72}")
    print(f"  TradePanel Parameter Optimizer  |  mode={'QUICK' if quick else 'FULL'}")
    print(f"  Strategies: {total}  |  Seeds: 3 (42, 123, 777)  |  Target WR: 60%+")
    print(f"{'='*72}\n")

    results = {}
    PASS_WR = 60.0

    for name, (cls, pair, tf) in strats.items():
        if name not in GRIDS:
            print(f"  [--] {name:<32} skipped (external data / not grid-searchable)")
            continue

        done += 1

        # Scalper timeframe guard — scalpers must be optimized on M5 or higher
        if name in SCALPER_STRATEGIES:
            tf_mins_actual = TF_MINS.get(tf, 60)
            if tf_mins_actual < SCALPER_MIN_TF_MINS:
                print(f"  [{done:>2}/{total}] {name:<32} ⚠ SKIPPED — "
                      f"timeframe {tf} ({tf_mins_actual}m) is below minimum {SCALPER_MIN_TF}. "
                      f"Update load_all_strategies() to use M5+.")
                results[name] = {"status": "SKIPPED_TF", "params": None, "metrics": None}
                continue

        print(f"  [{done:>2}/{total}] {name:<32} {pair} {tf} ...", end="", flush=True)

        best = grid_search(name, cls, pair, tf, GRIDS[name], quick=quick)

        if best["metrics"] is None:
            print(" NO TRADES")
            results[name] = {"status": "NO_TRADES", "params": best["params"], "metrics": None}
            continue

        m   = best["metrics"]
        wr  = m["win_rate"]
        status = "PASS" if wr >= PASS_WR else ("NEAR" if wr >= 50 else "FAIL")
        tag = {"PASS": "[PASS]", "NEAR": "[NEAR]", "FAIL": "[FAIL]"}[status]

        print(f" {tag}  WR={wr:.1f}%  PF={m['profit_factor']:.2f}"
              f"  Sh={m['sharpe']:.2f}  DD={m['max_dd']:.1f}%"
              f"  trades={m['trades']:.0f}  PnL=R{m['pnl_zar']:.0f}")
        print(f"          Best params: {best['params']}")

        results[name] = {"status": status, "params": best["params"], "metrics": m}

    # ── Summary ──────────────────────────────────────────────────────────────
    passed = [n for n, r in results.items() if r.get("status") == "PASS"]
    near   = [n for n, r in results.items() if r.get("status") == "NEAR"]
    failed = [n for n, r in results.items() if r.get("status") in ("FAIL", "NO_TRADES")]

    print(f"\n{'='*72}")
    print(f"  RESULTS:  {len(passed)} PASS  |  {len(near)} NEAR (50-60%)  |  {len(failed)} FAIL")
    print(f"{'='*72}")
    if passed:
        print(f"  Passed : {', '.join(passed)}")
    if near:
        print(f"  Near   : {', '.join(near)}")
    if failed:
        print(f"  Failed : {', '.join(failed)}")

    # Save JSON
    out_dir  = PROJECT_ROOT / "results" / "daily_validation"
    out_dir.mkdir(parents=True, exist_ok=True)
    ts       = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = out_dir / f"optimization_params_{ts}.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\n  Saved: {out_path}\n")

    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--strategy", nargs="+", help="Run only these strategies")
    parser.add_argument("--quick", action="store_true",
                        help="Quick mode: max 50 combos per strategy")
    args = parser.parse_args()
    run_all(target_strategies=args.strategy, quick=args.quick)


if __name__ == "__main__":
    main()
