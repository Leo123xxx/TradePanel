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

STRATEGY_MAP = {
    # ── TIER 1 ──────────────────────────────────────────────────────────────
    "dual_ema_fractal":         (DualEMAFractal,           1),
    "rsi_bounce":               (RSIBounceStrategy,        1),
    "stat_arb_gold_silver":     (StatArbGoldSilver,        1),
    "moving_average_crossover": (MACrossoverStrategy,      1),
    "bb_mean_reversion":        (BBMeanReversionStrategy,  1),
    "stoch_divergence":         (StochDivergenceStrategy,  1),
    "macd_trend":               (MACDTrendStrategy,        1),
    "gold_momentum_breakout":   (GoldMomentumBreakoutStrategy, 1),
    "range_breakout":           (RangeBreakoutStrategy,    1),
    "ema_ribbon_trend":         (EMARibbonTrendStrategy,   1),
    "cot_sentiment":            (COTSentimentStrategy,        1),   # #2: 52.55% WR
    # ── TIER 2 ──────────────────────────────────────────────────────────────
    "session_momentum":         (SessionMomentumStrategy,  2),
    "rsi_pullback":             (RSIPullbackStrategy,      2),
    "turtle_soup":              (TurtleSoup,               2),
    "dual_ema_momentum":        (DualEMAMomentum,          2),
    "vwap_momentum":            (VWAPMomentum,             2),
    "hikkake_trap":             (HikkakeTrap,              2),
    "orb":                      (ORBStrategy,              2),
    "rvgi_cci_confluence":      (RVGICCIConfluence,        2),
}

# Canonical pair–timeframe combos per strategy (derived from strategies.yaml)
STRATEGY_COMBOS = {
    "dual_ema_fractal":         [("EURUSD", "H1"), ("GBPUSD", "H1"), ("XAUUSD", "H1")],
    "rsi_bounce":               [("EURUSD", "H1"), ("XAUUSD", "H1"), ("GBPUSD", "H1")],
    "stat_arb_gold_silver":     [("XAUUSD", "H4")],
    "moving_average_crossover": [("EURUSD", "H1"), ("GBPUSD", "H1"), ("USDJPY", "H1")],
    "bb_mean_reversion":        [("XAUUSD", "H1"), ("EURUSD", "H1")],
    "stoch_divergence":         [("EURUSD", "H4"), ("USDJPY", "H4")],
    "macd_trend":               [("EURUSD", "H1"), ("USDJPY", "H1")],
    "gold_momentum_breakout":   [("XAUUSD", "H1")],           # GBPUSD removed — wrong pair for a gold squeeze strategy
    "range_breakout":           [("XAUUSD", "H4")],
    "ema_ribbon_trend":         [("BTCUSD", "H4"), ("ETHUSD", "H4")],
    "cot_sentiment":            [("XAUUSD", "D1"), ("EURUSD", "D1"),
                                  ("GBPUSD", "D1"), ("USDJPY", "D1")],
    "session_momentum":         [("XAUUSD", "H1"), ("GBPUSD", "H1")],
    "rsi_pullback":             [("XAUUSD", "H4"), ("USDJPY", "H4")],
    "turtle_soup":              [("EURUSD", "H4")],            # H1 removed — 900+ trades/Sharpe -4 on H1; H4 only
    "dual_ema_momentum":        [("XAUUSD", "H1"), ("XAUUSD", "H4")],
    "vwap_momentum":            [("GBPUSD", "M15"), ("EURUSD", "M15")],
    "hikkake_trap":             [("XAUUSD", "H4")],
    "orb":                      [("XAGUSD", "M15"), ("EURUSD", "M15")],
    "rvgi_cci_confluence":      [("EURUSD", "H1"), ("GBPUSD", "H1")],
}

# Thresholds for parameter tweak suggestions
MIN_WIN_RATE   = 48.0   # Below → tighten TP or loosen SL
MIN_TRADES     = 30     # Below → widen entry conditions
MIN_SHARPE     = 0.8    # Below → reduce position size or avoid pair
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


def run_all_backtests(tier_filter: int | None = None,
                      strategy_filter: str | None = None,
                      initial_balance: float = 10_000.0,
                      lot_size: float = 0.1) -> list[dict]:
    db = DBClient()
    results = []
    data_cache: dict[tuple, pd.DataFrame] = {}

    strategies_to_run = {
        k: v for k, v in STRATEGY_MAP.items()
        if (tier_filter is None or v[1] == tier_filter)
        and (strategy_filter is None or k == strategy_filter)
    }

    total_combos = sum(len(STRATEGY_COMBOS.get(s, [])) for s in strategies_to_run)
    print(f"\n{'='*60}")
    print(f"OVERNIGHT BACKTEST  |  {date.today()}  |  {total_combos} combos")
    print(f"{'='*60}")

    for strat_name, (strat_class, tier) in strategies_to_run.items():
        combos = STRATEGY_COMBOS.get(strat_name, [])
        for pair, timeframe in combos:
            label = f"{strat_name} | {pair} | {timeframe}"
            print(f"\n▶ {label} ...")

            try:
                # Load & cache data
                cache_key = (pair, timeframe)
                if cache_key not in data_cache:
                    df = load_data(db, pair, timeframe)
                    if df is None or len(df) < 100:
                        print(f"  ⚠ Skipped — insufficient data ({len(df) if df is not None else 0} bars)")
                        results.append({
                            "strategy": strat_name, "pair": pair, "timeframe": timeframe,
                            "tier": tier, "status": "SKIP", "reason": "insufficient_data",
                        })
                        continue
                    data_cache[cache_key] = df
                df = data_cache[cache_key]

                # Run backtest
                strategy_instance = strat_class()
                bt = BacktestEngine(initial_balance=initial_balance, lot_size=lot_size)
                trades_df, signals_df = bt.run(strategy_instance, pair, timeframe, df)

                if trades_df is None or trades_df.empty:
                    print(f"  ⚠ No trades generated")
                    results.append({
                        "strategy": strat_name, "pair": pair, "timeframe": timeframe,
                        "tier": tier, "status": "NO_TRADES", "reason": "zero_signals",
                    })
                    continue

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

                print(f"  {'✓' if status == 'PASS' else '⚠'} WR={win_rate:.1f}%  "
                      f"Sharpe={sharpe:.2f}  DD={max_dd:.1f}%  Trades={n_trades}  [{status}]")

                results.append({
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
                })

            except Exception as e:
                print(f"  ✗ ERROR: {e}")
                results.append({
                    "strategy": strat_name, "pair": pair, "timeframe": timeframe,
                    "tier": tier, "status": "ERROR", "reason": str(e),
                })

    return results


def save_report(results: list[dict], out_dir: Path) -> tuple[Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = date.today().strftime("%Y%m%d")

    # ── JSON report ──────────────────────────────────────────────────────────
    json_path = out_dir / f"{stamp}_backtest_report.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({"generated": str(datetime.now()), "results": results}, f, indent=2, default=str)

    # ── Markdown report ──────────────────────────────────────────────────────
    md_path = out_dir / f"{stamp}_backtest_report.md"
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
            tweaks = r.get("parameter_tweaks", [])
            if tweaks and tweaks[0] != "✓ All metrics within acceptable range — no changes needed":
                msg += f"    💡 {tweaks[0][:80]}\n"

    if errors:
        msg += f"\n⚠️ <b>Skipped ({len(errors)}):</b> "
        msg += ", ".join(f"{r['strategy']}/{r['pair']}" for r in errors[:5])
        if len(errors) > 5:
            msg += f" +{len(errors)-5} more"
        msg += "\n"

    msg += f"\n📄 Full report saved to <code>results/overnight/</code>"
    return msg


def main():
    parser = argparse.ArgumentParser(description="Overnight backtest runner — Tier 1 & 2 strategies")
    parser.add_argument("--tier",     type=int,   default=None, help="Filter by tier (1 or 2)")
    parser.add_argument("--strategy", type=str,   default=None, help="Run a single strategy by name")
    parser.add_argument("--balance",  type=float, default=10_000.0, help="Starting balance (default 10000)")
    parser.add_argument("--lot",      type=float, default=0.1,      help="Lot size (default 0.1)")
    parser.add_argument("--no-telegram", action="store_true", help="Skip Telegram notification")
    args = parser.parse_args()

    print(f"\n[{datetime.now()}] Overnight backtest starting…")
    results = run_all_backtests(
        tier_filter=args.tier,
        strategy_filter=args.strategy,
        initial_balance=args.balance,
        lot_size=args.lot,
    )

    # Save reports
    out_dir = Path(__file__).parent.parent / "results" / "overnight"
    json_path, md_path = save_report(results, out_dir)
    print(f"\n[{datetime.now()}] Reports saved:")
    print(f"  JSON: {json_path}")
    print(f"  MD:   {md_path}")

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
