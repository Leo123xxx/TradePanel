"""
scripts/run_overnight_backtest.py
==================================
Overnight batch backtest runner — Tier 1 & Tier 2 strategies only.

Runs automatically at 02:00 UTC Mon–Fri via APScheduler.
Can also be triggered manually:
    python scripts/run_overnight_backtest.py
    python scripts/run_overnight_backtest.py --tier 1          # Tier 1 only
    python scripts/run_overnight_backtest.py --strategy rsi_bounce  # Single strategy

Output:
    results/overnight/YYYYMMDD_backtest_report.json   (full metrics per combo)
    results/overnight/YYYYMMDD_backtest_report.md     (human-readable summary)
    Telegram message with top performers + parameter tweak suggestions
"""

import sys
import os
import argparse
import json
import traceback
from datetime import datetime, date
from pathlib import Path
from multiprocessing import Pool, cpu_count
import math

# ── project root on path ─────────────────────────────────────────────────────
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import yaml
import pandas as pd
from data.db_client import DBClient
from backtesting.engine import BacktestEngine
from backtesting.metrics import BacktestMetrics

# ── Strategy import map (Tier 1 & 2 only) ────────────────────────────────────
from strategies.ma_crossover import MACrossoverStrategy
from strategies.rsi_bounce import RSIBounceStrategy
from strategies.gold_momentum_breakout import GoldMomentumBreakoutStrategy
from strategies.macd_trend import MACDTrendStrategy
from strategies.range_breakout import RangeBreakoutStrategy
from strategies.rsi_pullback import RSIPullbackStrategy
from strategies.bb_mean_reversion import BBMeanReversionStrategy
from strategies.session_momentum import SessionMomentumStrategy
from strategies.stoch_divergence import StochDivergenceStrategy
from strategies.ema_ribbon_trend import EMARibbonTrendStrategy
from strategies.turtle_soup import TurtleSoup
from strategies.dual_ema_momentum import DualEMAMomentum
from strategies.dual_ema_fractal import DualEMAFractal
from strategies.vwap_momentum import VWAPMomentum
from strategies.hikkake_trap import HikkakeTrap
from strategies.orb import ORBStrategy
from strategies.rvgi_cci_confluence import RVGICCIConfluence
from strategies.stat_arb_gold_silver import StatArbGoldSilver
from strategies.cot_sentiment import COTSentimentStrategy
from strategies.bb_squeeze_scalp import BBSqueezeScalp
from strategies.rsi_extremes_scalp import RSIExtremesScalp
from strategies.crypto_rsi_extremes import CryptoRSIExtremesStrategy
from strategies.multi_ema_crypto_scalper import MultiEmaCryptoScalper
from strategies.silver_bullet_crypto import SilverBulletCrypto
from strategies.power_of_3_amd import PowerOf3AMD

from strategies.donchian_trend import DonchianTrendStrategy
from strategies.supertrend import SuperTrendStrategy
from strategies.ttm_squeeze import TTMSqueezeStrategy
from strategies.bb_squeeze_scalp import BBSqueezeScalp
from strategies.rsi_extremes_scalp import RSIExtremesScalp
from strategies.multi_ema_crypto_scalper import MultiEmaCryptoScalper
from strategies.silver_bullet_crypto import SilverBulletCrypto
from strategies.power_of_3_amd import PowerOf3AMD
from strategies.fast_ma_scalper import FastMAScalper
from strategies.ema_ribbon_scalp import EMARibbonScalp
from strategies.macd_zero_scalp import MACDZeroScalp
from strategies.volatility_breakout_scalp import VolatilityBreakoutScalp
from strategies.institutional_silver_bullet import InstitutionalSilverBullet
from strategies.ict_judas_swing import ICTJudasSwing
from strategies.swing_pullback import SwingPullbackStrategy
from strategies.volatility_contraction import VolatilityContraction
from strategies.naked_price_action import NakedPriceAction
from strategies.ensemble import EnsembleStrategy
from strategies.rsi_2 import RSITwoStrategy
from strategies.volatility_squeeze_breakout import VolatilitySqueezeBreakoutStrategy

STRATEGY_MAP = {
    "donchian_trend":           (DonchianTrendStrategy,    2),
    "supertrend":               (SuperTrendStrategy,       2),
    "ttm_squeeze":              (TTMSqueezeStrategy,       2),
    "bb_squeeze_scalp":         (BBSqueezeScalp,           2),
    "rsi_extremes_scalp":       (RSIExtremesScalp,         2),
    "multi_ema_crypto_scalper": (MultiEmaCryptoScalper,    2),
    "silver_bullet_crypto":     (SilverBulletCrypto,       2),
    "power_of_3_amd":           (PowerOf3AMD,              2),
    "fast_ma_scalper":          (FastMAScalper,            2),
    "ema_ribbon_scalp":         (EMARibbonScalp,           2),
    "macd_zero_scalp":          (MACDZeroScalp,            2),
    "volatility_breakout_scalp": (VolatilityBreakoutScalp, 2),
    "institutional_silver_bullet": (InstitutionalSilverBullet, 2),
    "ict_judas_swing":          (ICTJudasSwing,            2),
    "swing_pullback":           (SwingPullbackStrategy,    2),
    "volatility_contraction":   (VolatilityContraction,    2),
    "naked_price_action":       (NakedPriceAction,         2),
    "ensemble":                 (EnsembleStrategy,         2),
    "rsi_2":                    (RSITwoStrategy,           2),
    "volatility_squeeze_breakout": (VolatilitySqueezeBreakoutStrategy, 2),
    # ── TIER 1 ──────────────────────────────────────────────────────────────
    "dual_ema_fractal":         (DualEMAFractal,           1),
    "rsi_bounce":               (RSIBounceStrategy,        1),
    "stat_arb_gold_silver":     (StatArbGoldSilver,        1),
    "ma_crossover":             (MACrossoverStrategy,      1),
    "bb_mean_reversion":        (BBMeanReversionStrategy,  1),
    "stoch_divergence":         (StochDivergenceStrategy,  1),
    "macd_trend":               (MACDTrendStrategy,        1),
    "gold_momentum_breakout":   (GoldMomentumBreakoutStrategy, 1),
    "range_breakout":           (RangeBreakoutStrategy,    1),
    "ema_ribbon_trend":         (EMARibbonTrendStrategy,   1),
    "cot_sentiment":            (COTSentimentStrategy,     1),
    # ── TIER 2 ──────────────────────────────────────────────────────────────
    "session_momentum":         (SessionMomentumStrategy,  2),
    "rsi_pullback":             (RSIPullbackStrategy,      2),
    "turtle_soup":              (TurtleSoup,               2),
    "dual_ema_momentum":        (DualEMAMomentum,          2),
    "vwap_momentum":            (VWAPMomentum,             2),
    "hikkake_trap":             (HikkakeTrap,              2),
    "orb":                      (ORBStrategy,              2),
    "rvgi_cci_confluence":      (RVGICCIConfluence,        2),
    "crypto_rsi_extremes":      (CryptoRSIExtremesStrategy, 2),
}

# Combinations are now derived dynamically from the config file.
STRATEGY_COMBOS = {}

# Thresholds for parameter tweak suggestions
MIN_WIN_RATE   = 70.0   # Below → tighten entry filter or disable pair
MIN_TRADES     = 30     # Below → widen entry conditions
MIN_SHARPE     = 2.0    # Below → reduce position size or avoid pair
MAX_DRAWDOWN   = 20.0   # Above → tighten SL mult


def load_data(db: DBClient, pair: str, timeframe: str) -> pd.DataFrame | None:
    rows = db.execute_query(
        "SELECT timestamp, open, high, low, close, tick_volume FROM market_data "
        "WHERE pair = %s AND timeframe = %s ORDER BY timestamp",
        (pair, timeframe)
    )
    if not rows:
        return None
    df = pd.DataFrame(rows, columns=["timestamp", "open", "high", "low", "close", "tick_volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df.set_index("timestamp", inplace=True)
    for col in ["open", "high", "low", "close", "tick_volume"]:
        df[col] = df[col].astype(float)
    return df


def suggest_tweaks(strategy_name: str, pair: str, stats: dict) -> list[str]:
    """Generate concrete parameter tweak suggestions based on backtest stats."""
    suggestions = []
    wr   = stats.get("win_rate", 0)
    dd   = stats.get("max_drawdown_pct", 0)
    sh   = stats.get("sharpe_ratio", 0)
    tr   = stats.get("total_trades", 0)
    pf   = stats.get("profit_factor", 1.0)

    if wr < MIN_WIN_RATE:
        suggestions.append(f"Win rate {wr:.1f}% < {MIN_WIN_RATE}% → tighten entry filter (increase ADX min or add regime check)")
    if wr > 60:
        suggestions.append(f"Win rate {wr:.1f}% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit")
    if dd > MAX_DRAWDOWN:
        suggestions.append(f"Max drawdown {dd:.1f}% > {MAX_DRAWDOWN}% → reduce sl_atr_mult by 0.2 or add trailing stop")
    if tr < MIN_TRADES:
        suggestions.append(f"Only {tr} trades — widen oversold/overbought thresholds or relax ADX filter")
    if sh < MIN_SHARPE:
        suggestions.append(f"Sharpe {sh:.2f} < {MIN_SHARPE} → reduce lot size on this pair or pause strategy")
    if pf and pf < 1.2:
        suggestions.append(f"Profit factor {pf:.2f} — marginal edge, consider disabling on {pair} unless confirmed by live data")
    if not suggestions:
        suggestions.append("✓ All metrics within acceptable range — no changes needed")
    return suggestions


def backtest_worker(args_tuple):
    """Worker function for parallel backtesting."""
    strat_name, strat_class, pair, timeframe, df, params, initial_balance, lot_size, tier = args_tuple
    try:
        # Run backtest
        strategy_instance = strat_class(params=params)
        bt = BacktestEngine(initial_balance=initial_balance, lot_size=lot_size)
        
        # Set running mode to BACKTEST for pool optimization
        os.environ["RUNNING_MODE"] = "BACKTEST"
        
        trades_df, signals_df = bt.run(strategy_instance, pair, timeframe, df, silent=True)

        if trades_df is None or trades_df.empty:
            return {
                "strategy": strat_name, "pair": pair, "timeframe": timeframe,
                "tier": tier, "status": "NO_TRADES", "reason": "zero_signals",
            }

        metrics = BacktestMetrics(signals_df, trades_df, initial_balance)
        stats = metrics.calculate_all()
        stats = {k: (round(v, 4) if isinstance(v, float) else v)
                 for k, v in stats.items()}

        tweaks = suggest_tweaks(strat_name, pair, stats)
        win_rate = stats.get("win_rate", 0)
        sharpe   = stats.get("sharpe_ratio", 0)
        max_dd   = stats.get("max_drawdown_pct", 0)
        n_trades = stats.get("total_trades", 0)

        status = "PASS" if (win_rate >= MIN_WIN_RATE and sharpe >= MIN_SHARPE) else "REVIEW"

        return {
            "strategy": strat_name,
            "pair": pair,
            "timeframe": timeframe,
            "tier": tier,
            "status": status,
            "win_rate": win_rate,
            "sharpe_ratio": sharpe,
            "max_drawdown_pct": max_dd,
            "total_trades": n_trades,
            "profit_factor": stats.get("profit_factor"),
            "total_pnl": stats.get("total_pnl"),
            "parameter_tweaks": tweaks,
            "stats": stats,
        }
    except Exception as e:
        return {
            "strategy": strat_name, "pair": pair, "timeframe": timeframe,
            "tier": tier, "status": "ERROR", "reason": str(e),
        }


def run_all_backtests(config_path: str,
                      tier_filter: int | None = None,
                      strategy_filter: str | None = None,
                      initial_balance: float = 10_000.0,
                      lot_size: float = 0.1) -> list[dict]:
    db = DBClient()
    results = []
    data_cache: dict[tuple, pd.DataFrame] = {}

    # Load strategy configuration
    if not os.path.exists(config_path):
        print(f"ERROR: Config file not found: {config_path}")
        return []

    with open(config_path, 'r') as f:
        full_config = yaml.safe_load(f)

    active_strategies = full_config.get("active", [])
    if not active_strategies:
        print("WARNING: No active strategies found in config.")
        return []

    # Map tier names to integers for filtering
    tier_map = {"TIER_1": 1, "TIER_2": 2, "DISABLED": 0}

    # Generate combos dynamically
    dynamic_combos = {}
    for strat_name in active_strategies:
        if strat_name not in full_config:
            continue
        
        strat_conf = full_config[strat_name]
        if not strat_conf.get("enabled", True):
            continue
            
        pairs = strat_conf.get("pairs", [])
        timeframes = strat_conf.get("timeframes", [])
        
        # Normalize timeframes to list
        if isinstance(timeframes, str):
            timeframes = [timeframes]
            
        combos = []
        for p in pairs:
            for tf in timeframes:
                combos.append((p, tf))
        dynamic_combos[strat_name] = combos

    strategies_to_run = {
        k: v for k, v in STRATEGY_MAP.items()
        if k in active_strategies
        and (strategy_filter is None or k in {s.strip() for s in strategy_filter.split(",")})
    }
    
    # Second pass: check tier filter
    if tier_filter is not None:
        strategies_to_run = {
            k: v for k, v in strategies_to_run.items()
            if tier_map.get(full_config[k].get("tier"), 0) == tier_filter
        }

    total_combos = sum(len(dynamic_combos.get(s, [])) for s in strategies_to_run)
    print(f"\n{'='*60}")
    print(f"OVERNIGHT BACKTEST  |  {date.today()}  |  {total_combos} combos")
    print(f"{'='*60}")

    # Prepare tasks for parallel execution
    tasks = []
    for strat_name, (strat_class, _) in strategies_to_run.items():
        combos = dynamic_combos.get(strat_name, [])
        tier_str = full_config[strat_name].get("tier", "UNKNOWN")
        tier = tier_map.get(tier_str, 0)
        
        for pair, timeframe in combos:
            # Load & cache data (main process does the heavy I/O)
            cache_key = (pair, timeframe)
            if cache_key not in data_cache:
                df = load_data(db, pair, timeframe)
                if df is None or len(df) < 100:
                    results.append({
                        "strategy": strat_name, "pair": pair, "timeframe": timeframe,
                        "tier": tier, "status": "SKIP", "reason": "insufficient_data",
                    })
                    continue
                data_cache[cache_key] = df
            
            df = data_cache[cache_key]
            
            # Prepare params
            params = full_config[strat_name].get("parameters", {}).copy()
            pair_overrides = full_config[strat_name].get("pair_overrides", {})
            if pair in pair_overrides:
                params.update(pair_overrides[pair])
            
            tf_key = f"{pair}:{timeframe}"
            if tf_key in pair_overrides:
                params.update(pair_overrides[tf_key])

            if not params.get("enabled", True):
                results.append({
                    "strategy": strat_name, "pair": pair, "timeframe": timeframe,
                    "tier": tier, "status": "SKIP", "reason": "disabled_in_overrides",
                })
                continue

            tasks.append((
                strat_name, strat_class, pair, timeframe, df, params, initial_balance, lot_size, tier
            ))

    # Run in parallel
    num_cores = min(cpu_count() - 1, 8) if cpu_count() > 1 else 1
    print(f"Launching {len(tasks)} backtests across {num_cores} cores...")
    
    with Pool(processes=num_cores) as pool:
        parallel_results = pool.map(backtest_worker, tasks)
        
    results.extend(parallel_results)
    
    # Summary of results
    passed = sum(1 for r in results if r.get("status") == "PASS")
    print(f"Parallel batch complete. Pass: {passed}/{len(results)}")
    
    return results


def save_report(results: list[dict], out_dir: Path, suffix: str = "") -> tuple[Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = date.today().strftime("%Y%m%d")

    # ── JSON report ──────────────────────────────────────────────────────────
    json_path = out_dir / f"{stamp}_backtest_report{suffix}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({"generated": str(datetime.now()), "results": results}, f, indent=2, default=str)

    # ── Markdown report ──────────────────────────────────────────────────────
    md_path  = out_dir / f"{stamp}_backtest_report{suffix}.md"
    passed  = [r for r in results if r.get("status") == "PASS"]
    reviews = [r for r in results if r.get("status") == "REVIEW"]
    errors  = [r for r in results if r.get("status") in ("ERROR", "SKIP", "NO_TRADES")]

    lines = [
        f"# Overnight Backtest Report — {date.today().strftime('%d %B %Y')}",
        f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}",
        f"\n## Summary\n",
        f"| | Count |",
        f"|---|---|",
        f"| ✅ PASS | {len(passed)} |",
        f"| ⚠️ REVIEW | {len(reviews)} |",
        f"| ❌ ERROR/SKIP | {len(errors)} |",
        f"| **Total combos** | **{len(results)}** |",
        f"\n---\n",
        f"## ✅ Passing Strategies\n",
        f"| Strategy | Pair | TF | Tier | WR% | Sharpe | MaxDD% | Trades | PF |",
        f"|---|---|---|---|---|---|---|---|---|",
    ]

    for r in sorted(passed, key=lambda x: -x.get("win_rate", 0)):
        lines.append(
            f"| {r['strategy']} | {r['pair']} | {r['timeframe']} | T{r['tier']} "
            f"| {r['win_rate']:.1f} | {r['sharpe_ratio']:.2f} "
            f"| {r['max_drawdown_pct']:.1f} | {r['total_trades']} "
            f"| {r.get('profit_factor', 0):.2f} |"
        )

    lines += [f"\n---\n", f"## ⚠️ Strategies Needing Review\n"]
    for r in sorted(reviews, key=lambda x: -x.get("win_rate", 0)):
        lines.append(f"\n### {r['strategy']} | {r['pair']} | {r['timeframe']}")
        lines.append(f"WR={r['win_rate']:.1f}%  Sharpe={r['sharpe_ratio']:.2f}  "
                     f"MaxDD={r['max_drawdown_pct']:.1f}%  Trades={r['total_trades']}")
        lines.append("\n**Parameter Tweaks:**")
        for t in r.get("parameter_tweaks", []):
            lines.append(f"- {t}")

    lines += [f"\n---\n", f"## ❌ Errors / Skipped\n"]
    for r in errors:
        lines.append(f"- {r['strategy']} | {r['pair']} | {r['timeframe']} "
                     f"→ {r['status']}: {r.get('reason', '')}")

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return json_path, md_path


def save_pair_reports(results: list[dict], out_dir: Path):
    """Save individual MD reports per pair for comparison."""
    pair_dir = out_dir / "pair_results"
    pair_dir.mkdir(parents=True, exist_ok=True)
    
    # Group results by pair
    by_pair = {}
    for r in results:
        p = r.get("pair")
        if not p: continue
        if p not in by_pair: by_pair[p] = []
        by_pair[p].append(r)
        
    stamp = date.today().strftime("%Y%m%d")
    
    for pair, p_results in by_pair.items():
        md_path = pair_dir / f"{stamp}_{pair}_report.md"
        passed = [r for r in p_results if r.get("status") == "PASS"]
        reviews = [r for r in p_results if r.get("status") == "REVIEW"]
        errors = [r for r in p_results if r.get("status") in ("ERROR", "SKIP", "NO_TRADES")]
        
        lines = [
            f"# Pair Backtest Report: {pair} — {date.today().strftime('%d %B %Y')}",
            f"\n## Summary\n",
            f"| Status | Count |",
            f"|---|---|",
            f"| ✅ PASS | {len(passed)} |",
            f"| ⚠️ REVIEW | {len(reviews)} |",
            f"| ❌ ERROR/SKIP | {len(errors)} |",
            f"| **Total Combos** | **{len(p_results)}** |",
            f"\n## Details\n",
            f"| Strategy | TF | WR% | Sharpe | PF | MaxDD% |",
            f"|---|---|---|---|---|---|",
        ]
        
        # Sort by WR descending
        for r in sorted(p_results, key=lambda x: -x.get("win_rate", 0) if x.get("win_rate") else 0):
            wr = r.get('win_rate', 0)
            sh = r.get('sharpe_ratio', 0)
            pf = r.get('profit_factor', 0)
            dd = r.get('max_drawdown_pct', 0)
            lines.append(f"| {r['strategy']} | {r['timeframe']} | {wr:.1f} | {sh:.2f} | {pf:.2f} | {dd:.1f} |")
            
        with open(md_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))


def build_telegram_summary(results: list[dict]) -> str:
    passed  = [r for r in results if r.get("status") == "PASS"]
    reviews = [r for r in results if r.get("status") == "REVIEW"]
    errors  = [r for r in results if r.get("status") in ("ERROR", "SKIP", "NO_TRADES")]

    # Top 5 by win rate
    top5 = sorted([r for r in results if r.get("win_rate")],
                  key=lambda x: -x.get("win_rate", 0))[:5]
    # Bottom 3 by win rate (for attention)
    bottom3 = sorted([r for r in results if r.get("win_rate")],
                     key=lambda x: x.get("win_rate", 100))[:3]

    msg = (
        f"🌙 <b>OVERNIGHT BACKTEST COMPLETE</b>\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"📅 <b>{date.today().strftime('%d %b %Y')}</b>\n"
        f"✅ Pass: <b>{len(passed)}</b>  "
        f"⚠️ Review: <b>{len(reviews)}</b>  "
        f"❌ Error: <b>{len(errors)}</b>\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"
        f"🏆 <b>Top 5 Performers</b>\n"
    )
    for r in top5:
        msg += (f"  • <b>{r['strategy']}</b> {r['pair']} {r['timeframe']}\n"
                f"    WR={r['win_rate']:.1f}% | Sharpe={r['sharpe_ratio']:.2f} "
                f"| T{r['tier']}\n")

    if bottom3:
        msg += f"\n🔻 <b>Needs Attention</b>\n"
        for r in bottom3:
            msg += f"  • {r['strategy']} {r['pair']} → WR={r['win_rate']:.1f}%\n"
            import html
            tweaks = r.get("parameter_tweaks", [])
            if tweaks and tweaks[0] != "✓ All metrics within acceptable range — no changes needed":
                msg += f"    💡 {html.escape(tweaks[0][:80])}\n"

    if errors:
        msg += f"\n⚠️ <b>Skipped ({len(errors)}):</b> "
        msg += ", ".join(f"{r['strategy']}/{r['pair']}" for r in errors[:5])
        if len(errors) > 5:
            msg += f" +{len(errors)-5} more"
        msg += "\n"

    msg += f"\n📄 Full report saved to <code>results/overnight/</code>"
    return msg


def save_results_to_db(results: list[dict], db: DBClient):
    import math
    def _sanitize(obj):
        if isinstance(obj, float):
            return None if (math.isinf(obj) or math.isnan(obj)) else obj
        if isinstance(obj, dict):
            return {k: _sanitize(v) for k, v in obj.items()}
        if isinstance(obj, (list, tuple)):
            return [_sanitize(v) for v in obj]
        return obj

    def _safe_num(val, clamp=9999.0):
        if val is None: return None
        if isinstance(val, float) and (math.isnan(val) or math.isinf(val)): return None
        return max(-clamp, min(clamp, float(val)))

    # Clear old overnight backtests to keep dashboard clean
    try:
        db.execute_query("DELETE FROM backtest_runs WHERE run_id LIKE 'BT-%'")
    except Exception as e:
        print(f"  ⚠ Could not clear old backtests: {e}")

    stamp = date.today().strftime("%Y%m%d")
    inserted = 0

    for i, r in enumerate(results):
        if r.get("status") in ("ERROR", "SKIP", "NO_TRADES"):
            continue

        run_id = f"BT-{stamp}-{i+1:04d}"
        strat_display = f"{r['strategy']} ({r['pair']} {r['timeframe']})"
        tweaks_str = "; ".join(r.get("parameter_tweaks", []))
        
        # Scale percentages down to fractions for DB schema
        wr = _safe_num(r.get("win_rate"))
        if wr is not None: wr = wr / 100.0
        
        dd = _safe_num(r.get("max_drawdown_pct"))
        if dd is not None: 
            # Make sure drawdown is negative for DB convention
            dd = -abs(dd) / 100.0

        try:
            db.execute_query(
                """
                INSERT INTO backtest_runs (
                    run_id, strategy_name, period_start, period_end,
                    win_rate, sharpe_ratio, profit_factor, net_profit_zar,
                    max_drawdown_pct, total_trades, status,
                    params_json, metrics_json, notes
                ) VALUES (
                    %s, %s, %s, %s,
                    %s, %s, %s, %s,
                    %s, %s, %s,
                    %s, %s, %s
                )
                ON CONFLICT (run_id) DO UPDATE SET
                    win_rate = EXCLUDED.win_rate,
                    sharpe_ratio = EXCLUDED.sharpe_ratio,
                    profit_factor = EXCLUDED.profit_factor,
                    net_profit_zar = EXCLUDED.net_profit_zar,
                    max_drawdown_pct = EXCLUDED.max_drawdown_pct,
                    total_trades = EXCLUDED.total_trades,
                    status = EXCLUDED.status,
                    metrics_json = EXCLUDED.metrics_json,
                    notes = EXCLUDED.notes,
                    updated_at = NOW()
                """,
                (
                    run_id,
                    strat_display,
                    None, None,
                    wr,
                    _safe_num(r.get("sharpe_ratio")),
                    _safe_num(r.get("profit_factor")),
                    _safe_num(r.get("total_pnl"), 999999999.0),
                    dd,
                    r.get("total_trades", 0),
                    r.get("status", "REVIEW"),
                    json.dumps({}),
                    json.dumps(_sanitize(r.get("stats", {}))),
                    tweaks_str
                )
            )
            inserted += 1
        except Exception as e:
            # Fallback to pure print if unicode fails
            sys.stdout.buffer.write(f"  [!] Failed to insert {run_id}: {e}\n".encode('utf-8'))

    print(f"  [OK] Saved {inserted} backtest runs to the database.")


def main():
    parser = argparse.ArgumentParser(description="Overnight backtest runner — Tier 1 & 2 strategies")
    parser.add_argument("--tier",     type=int,   default=None, help="Filter by tier (1 or 2)")
    parser.add_argument("--strategy", type=str,   default=None, help="Run a single strategy by name")
    parser.add_argument("--balance",  type=float, default=10_000.0, help="Starting balance (default 10000)")
    parser.add_argument("--lot",      type=float, default=0.1,      help="Lot size (default 0.1)")
    parser.add_argument("--no-telegram", action="store_true", help="Skip Telegram notification")
    parser.add_argument("--suffix",   type=str,   default="",    help="Suffix for report filename (e.g. _retest1)")
    parser.add_argument("--config",   type=str,   default="config/strategies.yaml", help="Path to config YAML file")
    args = parser.parse_args()

    print(f"\n[{datetime.now()}] Overnight backtest starting using config: {args.config}")
    results = run_all_backtests(
        config_path=args.config,
        tier_filter=args.tier,
        strategy_filter=args.strategy,  # may be comma-separated; handled in run_all_backtests
        initial_balance=args.balance,
        lot_size=args.lot,
    )

    # Save reports
    out_dir = Path(__file__).parent.parent / "results" / "overnight"
    json_path, md_path = save_report(results, out_dir, suffix=args.suffix)
    
    # Save per-pair reports
    save_pair_reports(results, out_dir)
    print(f"\n[{datetime.now()}] Reports saved:")
    print(f"  JSON: {json_path}")
    print(f"  MD:   {md_path}")

    # Save to Database
    print(f"\n[{datetime.now()}] Syncing results to database...")
    try:
        db = DBClient()
        save_results_to_db(results, db)
    except Exception as e:
        print(f"Failed to sync to database: {e}")

    # Print summary to console
    passed  = sum(1 for r in results if r.get("status") == "PASS")
    reviews = sum(1 for r in results if r.get("status") == "REVIEW")
    errors  = sum(1 for r in results if r.get("status") in ("ERROR", "SKIP", "NO_TRADES"))
    print(f"\n{'='*60}")
    print(f"RESULT  Pass={passed}  Review={reviews}  Error={errors}  Total={len(results)}")
    print(f"{'='*60}")

    # Send Telegram notification
    if not args.no_telegram:
        try:
            from notifications.telegram_bot import TelegramBot
            bot = TelegramBot()
            summary = build_telegram_summary(results)
            bot.send_sync_message(summary)
            print("\n[Telegram] Report sent successfully.")
        except Exception as e:
            print(f"\n[Telegram] Failed to send: {e}")

    return results



if __name__ == "__main__":
    main()
