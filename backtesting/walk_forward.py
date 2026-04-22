"""
backtesting/walk_forward.py — Rolling Walk-Forward Optimizer
"""

import sys
import os
import itertools
import json
import pandas as pd
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.db_client import DBClient
from backtesting.engine import BacktestEngine
from backtesting.metrics import BacktestMetrics
from scripts.run_backtest import STRATEGY_MAP
from logging_.event_logger import EventLogger

PARAM_GRIDS = {
    "range_breakout": {
        "consolidation_bars": [10, 15, 20],
        "vol_threshold_mult": [1.0, 1.3, 1.5],
        "tp_atr_mult": [2, 3],
        "sl_atr_mult": [1.5]
    },
    "rsi_pullback": {
        "rsi_period": [10, 14],
        "rsi_pullback_lower": [25, 30, 35],
        "tp_atr_mult": [2, 3],
        "sl_atr_mult": [1, 1.5]
    },
    "swing_pullback": {
        "swing_lookback": [5, 10, 15],
        "min_adx_filter": [15, 20, 25],
        "tp_atr_mult": [2, 3],
        "sl_atr_mult": [1, 1.5]
    },
    "stoch_divergence": {
        "stoch_period": [10, 14],
        "divergence_lookback": [8, 10, 14],
        "stoch_oversold": [20, 25, 30],
        "tp_atr_mult": [2, 3],
        "sl_atr_mult": [1.0, 1.5]
    },
    "ma_crossover": {
        "fast_period": [9, 10, 12],
        "slow_period": [30, 50, 75],
        "adx_filter": [22, 25, 30],
        "tp_atr_mult": [2, 3]
    },
    "bb_mean_reversion": {
        "bb_period": [20],
        "bb_deviation": [2.0, 2.5],
        "adx_max": [22],
        "tp_atr_mult": [1.5, 2],
        "sl_atr_mult": [1]
    },
    "session_momentum": {
        "session_start_utc": [13],
        "session_end_utc": [17],
        "pre_session_bars": [6, 8],
        "tp_atr_mult": [2, 3],
        "sl_atr_mult": [1.0]
    },
    # ── New crypto + cross-asset strategies (added 2026-04-18) ────────────────
    "ema_ribbon_trend": {
        "fast_ema":     [8, 12],
        "mid_ema":      [13, 26],
        "slow_ema":     [34, 55],
        "adx_min":      [25],
        "vol_threshold_mult": [1.0, 1.3],
        "tp_atr_mult":  [3.0, 4.0],
        "sl_atr_mult":  [1.5]
    },
    "crypto_rsi_extremes": {
        "rsi_oversold":   [20, 25, 30],
        "rsi_overbought": [70, 75, 80],
        "bb_deviation":   [1.8, 2.0, 2.2],
        "adx_max":        [30, 35, 40],
        "vol_spike_mult": [1.2, 1.5, 2.0],
        "tp_atr_mult":    [2.0, 2.5, 3.0],
        "sl_atr_mult":    [1.0, 1.5]
    },
    "volatility_squeeze_breakout": {
        "squeeze_pct":   [0.02, 0.03, 0.04],
        "squeeze_bars":  [2, 3, 4],
        "tp_atr_mult":   [2.5, 3.0, 4.0],
        "sl_atr_mult":   [1.0, 1.5, 2.0]
    },
    # ── Institutional Flow (LeoDeX V2) ────────────────────────────────────────
    "institutional_silver_bullet": {
        "lookback_sweep":    [15, 20, 25],
        "fvg_min_size_pct":  [0.0001, 0.0002],
        "risk_reward":       [2.0, 3.0]
    },
    "ict_judas_swing": {
        "asian_range_start": [20],
        "asian_range_end":   [2],
        "fakeout_magnitude_pct": [0.001, 0.002],
        "vol_threshold_mult": [1.0, 1.2, 1.5],
        "liquidity_sweep_pips": [5, 10, 15]
    },
    "turtle_soup": {
        "lookback":             [20, 30],
        "min_penetration_pips": [5, 10],
        "tp_atr_mult":          [2.0, 3.0]
    },
    # ── Trend Following (LeoDeX V2) ───────────────────────────────────────────
    "dual_ema_momentum": {
        "fast_ema":    [20, 30],
        "slow_ema":    [50, 100],
        "adx_min":     [20, 25, 30],
        "tp_atr_mult": [2.5, 3.0]
    },
    "triple_macd_scalping": {
        "tp_atr_mult": [1.5, 2.0],
        "sl_atr_mult": [1.0]
    },
    "dual_ema_fractal": {
        "ema_period":  [100, 200],
        "tp_atr_mult": [2.0, 3.0]
    },
    # ── Mean Reversion (LeoDeX V2) ────────────────────────────────────────────
    "rsi_2": {
        "rsi_period": [2],
        "oversold":   [10, 15, 20],
        "overbought": [80, 85, 90]
    },
    "vwap_momentum": {
        "std_dev_mult": [2.0, 2.5],
        "tp_atr_mult":  [1.5, 2.0]
    },
    "hikkake_trap": {
        "lookback_bars": [2, 3, 5],
        "tp_atr_mult":   [2.0, 3.0]
    },
    # ── Breakout (LeoDeX V2) ──────────────────────────────────────────────────
    "orb": {
        "range_duration_mins": [30, 60],
        "vol_filter":          [1.2, 1.5],
        "tp_atr_mult":         [2.0, 3.0]
    },
    "rvgi_cci_confluence": {
        "rvgi_period": [10, 14],
        "cci_period":  [20, 30],
        "tp_atr_mult": [1.5, 2.5]
    },
    "volatility_contraction": {
        "atr_lookback": [50, 100],
        "range_bars":   [5, 10, 20],
        "vol_spike":    [1.5, 2.0]
    },
    # ── Advanced (LeoDeX V2) ──────────────────────────────────────────────────
    "stat_arb_gold_silver": {
        "window":  [100, 200],
        "z_entry": [2.0, 2.5]
    },
    "naked_price_action": {
        "level_lookback":    [50, 100],
        "engulf_buffer_pct": [0.05, 0.1]
    },
    "cot_sentiment": {
        "sentiment_threshold": [80]
    }
}

def _dict_product(d):
    """Yields dictionaries representing Cartesian product of parameter lists."""
    keys = d.keys()
    for element in itertools.product(*d.values()):
        yield dict(zip(keys, element))

class WalkForwardOptimizer:
    def __init__(self, db: DBClient, lot_size=0.1, initial_balance=10000.0):
        self.db = db
        self.lot_size = lot_size
        self.initial_balance = initial_balance
        self.logger = EventLogger()

    def run(self, strategy_key: str, symbol: str, timeframe: str, df: pd.DataFrame, is_pct: float, oos_pct: float, n_windows: int):
        if strategy_key not in STRATEGY_MAP:
            print(f"Unknown strategy: {strategy_key}")
            return []
        
        self.logger.log_event(
            "BACKTEST_START", "INFO",
            f"Starting Walk-Forward Optimization for {symbol}.",
            {"strategy": strategy_key, "symbol": symbol, "timeframe": timeframe, "windows": n_windows}
        )
        
        strat_class = STRATEGY_MAP[strategy_key]
        grid = PARAM_GRIDS.get(strategy_key, {})
        
        total_len = len(df)
        engine = BacktestEngine(lot_size=self.lot_size, initial_balance=self.initial_balance)
        
        dummy_strat = strat_class()
        strat_row = self.db.execute_query("SELECT strategy_id FROM strategies WHERE name = %s", (dummy_strat.name,))
        if not strat_row:
            strat_row = self.db.execute_query(
                "INSERT INTO strategies (name, category) VALUES (%s, %s) RETURNING strategy_id",
                (dummy_strat.name, dummy_strat.category)
            )
        strategy_id = strat_row[0][0]

        oos_results = []
        
        # Calculate window sizes
        # The remaining segment is what shifts 
        fw_pct = 1.0 - (is_pct + oos_pct)
        if fw_pct < 0:
            fw_pct = 0
            
        step_pct = fw_pct if fw_pct > 0 else 1.0 / n_windows
        window_size = int(total_len / (1 + (n_windows - 1) * step_pct))
        
        if window_size > total_len:
            window_size = total_len
            step_pct = 0

        for w in range(n_windows):
            start_idx = int(w * step_pct * window_size)
            end_idx = min(start_idx + window_size, total_len)
            act_w_len = end_idx - start_idx
            
            train_len = int(act_w_len * is_pct)
            test_len = int(act_w_len * oos_pct)
            
            # If train is too small to even contain data
            if train_len < 10:
                continue
                
            train_start = start_idx
            train_end = start_idx + train_len
            test_start = train_end
            test_end = min(train_end + test_len, total_len)

            train_df = df.iloc[train_start:train_end]
            test_df = df.iloc[test_start:test_end]

            if train_df.empty or test_df.empty:
                continue

            train_start_date = train_df.index[0].to_pydatetime()
            train_end_date = train_df.index[-1].to_pydatetime()
            test_start_date = test_df.index[0].to_pydatetime()
            test_end_date = test_df.index[-1].to_pydatetime()

            print(f"\n[{w+1}/{n_windows}] Train: {train_start_date.date()} -> {train_end_date.date()} ({len(train_df)} bars)", flush=True)
            print(f"[{w+1}/{n_windows}] Test : {test_start_date.date()} -> {test_end_date.date()} ({len(test_df)} bars)", flush=True)

            best_sharpe = -9999.0
            best_params = None
            
            grid_list = list(_dict_product(grid)) if grid else [{}]
            
            for combo in grid_list:
                strategy = strat_class(params=combo)
                # Suppress output of the engine to keep console clean
                old_stdout = sys.stdout
                sys.stdout = open(os.devnull, 'w')
                try:
                    trades_df, signals_df = engine.run(strategy, symbol, timeframe, train_df)
                    metrics = BacktestMetrics(signals_df, trades_df, self.initial_balance).calculate_all()
                except Exception as e:
                    metrics = {"error": str(e)}
                finally:
                    sys.stdout.close()
                    sys.stdout = old_stdout
                
                if "error" not in metrics:
                    sharpe = metrics.get("sharpe_ratio", 0.0)
                    if sharpe > best_sharpe:
                        best_sharpe = sharpe
                        best_params = combo

            if best_params is None:
                best_params = dummy_strat.params
                best_sharpe = 0.0
            
            param_str = ", ".join(f"{k}: {v}" for k, v in best_params.items())
            print(f"  Best IS Params:  {param_str}  [Sharpe: {best_sharpe:.2f}]", flush=True)

            print(f"  Running OOS validation with best IS params...", flush=True)
            test_strategy = strat_class(params=best_params)
            
            old_stdout = sys.stdout
            sys.stdout = open(os.devnull, 'w')
            try:
                test_trades_df, test_signals_df = engine.run(test_strategy, symbol, timeframe, test_df)
                test_metrics = BacktestMetrics(test_signals_df, test_trades_df, self.initial_balance).calculate_all()
            finally:
                sys.stdout.close()
                sys.stdout = old_stdout

            test_sharpe = test_metrics.get("sharpe_ratio", 0.0)
            test_pf = test_metrics.get("profit_factor", 0.0)
            test_trades_count = test_metrics.get("total_trades", 0)
            print(f"  Validation OOS:  Sharpe: {test_sharpe:.2f} | PF: {test_pf:.2f}", flush=True)

            # Save window result and persist to DB
            window_result = {
                "window_index": w + 1,
                "is_start": train_start_date,
                "is_end": train_end_date,
                "oos_start": test_start_date,
                "oos_end": test_end_date,
                "best_params": best_params,
                "is_sharpe": best_sharpe,
                "oos_sharpe": test_sharpe,
                "oos_profit_factor": test_pf,
                "oos_trades": test_trades_count,
            }
            oos_results.append(window_result)

            self.db.execute_query(
                """INSERT INTO walk_forward_results
                   (strategy_id, symbol, timeframe, window_index,
                    is_start, is_end, oos_start, oos_end,
                    best_params, is_sharpe, oos_sharpe, oos_profit_factor, oos_trades)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                   ON CONFLICT DO NOTHING""",
                (
                    strategy_id, symbol, timeframe, w + 1,
                    train_start_date, train_end_date,
                    test_start_date, test_end_date,
                    json.dumps(best_params),
                    best_sharpe, test_sharpe, test_pf, test_trades_count,
                ),
            )

        self.logger.log_event(
            "BACKTEST_END", "SUCCESS",
            f"Walk-forward optimization completed for {symbol} on {timeframe}.",
            {
                "strategy": strategy_key,
                "symbol": symbol,
                "timeframe": timeframe,
                "windows": n_windows,
                "results": oos_results
            }
        )
        return oos_results
