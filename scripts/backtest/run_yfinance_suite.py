"""
run_yfinance_suite.py — Offline E2E backtest suite using yfinance data.
Runs all active strategy × pair × timeframe combos that yfinance supports.
Generates: results/overnight/YYYYMMDD_yf_backtest_report.json + .md
Usage: python scripts/backtest/run_yfinance_suite.py [--tier 1|2|all] [--quick]
"""
import sys, os, json, traceback, warnings
from pathlib import Path
from datetime import datetime, timedelta

warnings.filterwarnings("ignore")
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
os.chdir(PROJECT_ROOT)

import yaml
import pandas as pd
import numpy as np
import yfinance as yf

from backtesting.engine import BacktestEngine
from backtesting.metrics import BacktestMetrics
from strategies.registry import registry as STRATEGY_REGISTRY

# ── Yahoo Finance symbol map ──────────────────────────────────────────────────
YF_MAP = {
    "EURUSD": "EURUSD=X", "GBPUSD": "GBPUSD=X", "USDJPY": "JPY=X",
    "XAUUSD": "GC=F",     "XAGUSD": "SI=F",
    "BTCUSD": "BTC-USD",  "ETHUSD": "ETH-USD",
    "GBPJPY": "GBPJPY=X", "AUDUSD": "AUDUSD=X", "USDCAD": "USDCAD=X",
    "USOIL":  "CL=F",     "US500":  "^GSPC",     "USTEC":  "^NDX",
    "NVDA":   "NVDA",     "AMD":    "AMD",        "MSFT":   "MSFT",
    "AAPL":   "AAPL",
}

# yfinance interval map: TF → (yf_interval, period/start_date)
TF_MAP = {
    "M5":  ("5m",  "60d"),
    "M15": ("15m", "60d"),
    "M30": ("30m", "60d"),
    "H1":  ("1h",  "730d"),
    "H2":  ("1h",  "730d"),   # resample 1h→2h
    "H4":  ("1h",  "730d"),   # resample 1h→4h
    "H12": ("1d",  "5y"),     # resample D→12h approx
    "D1":  ("1d",  "5y"),
}

def fetch_yf(symbol: str, tf: str) -> pd.DataFrame | None:
    ticker = YF_MAP.get(symbol)
    if not ticker:
        return None
    yf_interval, period = TF_MAP.get(tf, (None, None))
    if not yf_interval:
        return None
    try:
        raw = yf.download(ticker, period=period, interval=yf_interval,
                          auto_adjust=True, progress=False)
        if raw.empty or len(raw) < 100:
            return None
        raw.columns = [c[0].lower() if isinstance(c, tuple) else c.lower()
                       for c in raw.columns]
        df = raw[["open", "high", "low", "close", "volume"]].copy()
        df.rename(columns={"volume": "tick_volume"}, inplace=True)
        df.index = pd.to_datetime(df.index, utc=True).tz_convert(None)
        df.index.name = "timestamp"
        df.dropna(inplace=True)
        # Resample if needed
        if tf == "H2":
            df = df.resample("2h").agg({"open":"first","high":"max","low":"min",
                                        "close":"last","tick_volume":"sum"}).dropna()
        elif tf == "H4":
            df = df.resample("4h").agg({"open":"first","high":"max","low":"min",
                                        "close":"last","tick_volume":"sum"}).dropna()
        return df if len(df) >= 100 else None
    except Exception:
        return None

def run_combo(strat_name, strat_obj, symbol, tf, initial_balance=180000.0):
    df = fetch_yf(symbol, tf)
    if df is None:
        return {"status": "SKIP", "reason": "no_data"}
    try:
        engine = BacktestEngine(lot_size=None, initial_balance=initial_balance)
        trades = engine.run(strat_obj, symbol, tf, df, silent=True)
        if not trades:
            return {"status": "SKIP", "reason": "no_trades"}
        metrics = BacktestMetrics(trades, initial_balance)
        stats = metrics.summary()
        trade_count = len(trades)
        wr = stats.get("win_rate", 0) * 100
        sharpe = stats.get("sharpe_ratio", stats.get("sharpe", 0))
        maxdd = stats.get("max_drawdown_pct", stats.get("max_drawdown", 0)) * 100
        pf = stats.get("profit_factor", 0)
        net_pnl = stats.get("net_pnl", stats.get("total_pnl", 0))
        passed = (wr >= 70.0 and sharpe >= 2.0 and trade_count >= 10)
        status = "PASS" if passed else "REVIEW"
        if sharpe < 0 or maxdd > 20:
            status = "P1_CRITICAL"
        return {
            "status": status,
            "wr": round(wr, 1),
            "sharpe": round(sharpe, 3),
            "maxdd": round(maxdd, 1),
            "pf": round(pf, 2),
            "trades": trade_count,
            "net_pnl_zar": round(net_pnl, 2),
            "bars": len(df),
            "valid": trade_count >= 10,
        }
    except Exception as e:
        return {"status": "ERROR", "reason": str(e)[:120]}

def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true", help="H1+H4+D1 only")
    ap.add_argument("--strategy", default=None, help="Single strategy name")
    args = ap.parse_args()

    with open(PROJECT_ROOT / "config" / "strategies.yaml") as f:
        scfg = yaml.safe_load(f)

    active = scfg.get("active", [])
    if args.strategy:
        active = [s for s in active if s == args.strategy]

    QUICK_TFS = {"H1", "H4", "D1"}

    now_utc = datetime.utcnow()
    date_str = now_utc.strftime("%Y%m%d_%H%M%S")
    results = {}
    totals = {"PASS": 0, "REVIEW": 0, "P1_CRITICAL": 0, "ERROR": 0, "SKIP": 0}

    print(f"\n{'='*60}")
    print(f" TradePanel v3 — yfinance Backtest Suite")
    print(f" Run: {now_utc.strftime('%Y-%m-%d %H:%M UTC')} | Mode: {'QUICK' if args.quick else 'FULL'}")
    print(f"{'='*60}\n")

    for strat_name in active:
        scfg_s = scfg.get(strat_name, {})
        if not scfg_s.get("enabled", True):
            continue
        pairs = scfg_s.get("pairs", [])
        tfs   = scfg_s.get("timeframes", [])
        params = scfg_s.get("parameters", {})
        if args.quick:
            tfs = [t for t in tfs if t in QUICK_TFS]
        if not tfs:
            continue

        strat_cls = STRATEGY_REGISTRY.strategies.get(strat_name)
        if not strat_cls:
            print(f"  ⚠ {strat_name}: not in registry — skipping")
            continue

        try:
            strat_obj = strat_cls(params=params)
        except Exception as e:
            print(f"  ⚠ {strat_name}: instantiation error — {e}")
            continue

        print(f"\n▶ {strat_name} ({len(pairs)} pairs × {len(tfs)} TFs)")
        for pair in pairs:
            for tf in tfs:
                key = f"{strat_name}|{pair}|{tf}"
                r = run_combo(strat_name, strat_obj, pair, tf)
                results[key] = r
                status = r["status"]
                totals[status] = totals.get(status, 0) + 1
                if status == "PASS":
                    print(f"  ✅ {pair}/{tf}: WR={r['wr']}% Sharpe={r['sharpe']} DD={r['maxdd']}% T={r['trades']}")
                elif status == "P1_CRITICAL":
                    print(f"  🔴 {pair}/{tf}: WR={r['wr']}% Sharpe={r['sharpe']} DD={r['maxdd']}% — P1 CRITICAL")
                elif status == "REVIEW":
                    print(f"  ⚠  {pair}/{tf}: WR={r['wr']}% Sharpe={r['sharpe']} DD={r['maxdd']}% T={r['trades']}")
                elif status == "SKIP":
                    print(f"  -  {pair}/{tf}: SKIP ({r.get('reason','')})")
                else:
                    print(f"  ❌ {pair}/{tf}: ERROR — {r.get('reason','')[:80]}")

    # ── Build report ──────────────────────────────────────────────────────────
    passes = {k: v for k, v in results.items() if v["status"] == "PASS"}
    p1s    = {k: v for k, v in results.items() if v["status"] == "P1_CRITICAL"}
    near_pass = {k: v for k, v in results.items()
                 if v["status"] == "REVIEW" and v.get("sharpe", 0) >= 1.2 and v.get("wr", 0) >= 60}

    near_pass_sorted = sorted(near_pass.items(), key=lambda x: x[1].get("sharpe", 0), reverse=True)[:10]

    report = {
        "generated_utc": now_utc.isoformat() + "Z",
        "mode": "yfinance_offline",
        "quick": args.quick,
        "totals": totals,
        "total_combos": len(results),
        "pass_rate_pct": round(totals["PASS"] / max(len(results), 1) * 100, 1),
        "passes": passes,
        "p1_criticals": p1s,
        "near_pass": dict(near_pass_sorted),
        "all_results": results,
    }

    out_dir = PROJECT_ROOT / "results" / "overnight"
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / f"{date_str}_yf_backtest_report.json"
    with open(json_path, "w") as f:
        json.dump(report, f, indent=2)

    # ── Markdown summary ──────────────────────────────────────────────────────
    md_lines = [
        f"# TradePanel v3 — yfinance Backtest Report",
        f"",
        f"**Generated:** {now_utc.strftime('%Y-%m-%d %H:%M UTC')} | **Mode:** {'QUICK (H1/H4/D1)' if args.quick else 'FULL'}",
        f"**Data source:** Yahoo Finance (offline, no DB required)",
        f"**Pass thresholds:** WR ≥ 70% AND Sharpe ≥ 2.0 AND Trades ≥ 10",
        f"",
        f"## Summary",
        f"",
        f"| | Count |",
        f"|---|---|",
        f"| ✅ PASS | {totals['PASS']} |",
        f"| ⚠️ REVIEW | {totals['REVIEW']} |",
        f"| 🔴 P1 CRITICAL | {totals['P1_CRITICAL']} |",
        f"| ❌ ERROR | {totals['ERROR']} |",
        f"| — SKIP | {totals['SKIP']} |",
        f"| **Total combos** | **{len(results)}** |",
        f"| **Pass rate** | **{report['pass_rate_pct']}%** |",
        f"",
        f"## ✅ Passing Strategies (WR ≥ 70%, Sharpe ≥ 2.0, Trades ≥ 10)",
        f"",
        f"| Strategy | Pair | TF | WR% | Sharpe | MaxDD% | Trades | PF | Valid |",
        f"|---|---|---|---|---|---|---|---|---|",
    ]
    for k, v in sorted(passes.items(), key=lambda x: x[1].get("sharpe", 0), reverse=True):
        parts = k.split("|")
        md_lines.append(f"| {parts[0]} | {parts[1]} | {parts[2]} | {v['wr']} | {v['sharpe']} | {v['maxdd']} | {v['trades']} | {v['pf']} | {'✅' if v.get('valid') else '⚠ <10T'} |")
    if not passes:
        md_lines.append("| — | No passes | — | — | — | — | — | — | — |")

    md_lines += [
        f"",
        f"## 🎯 Near-Pass (Sharpe ≥ 1.2, WR ≥ 60%)",
        f"",
        f"| Strategy | Pair | TF | WR% | Sharpe | MaxDD% | Trades | Blocker |",
        f"|---|---|---|---|---|---|---|---|",
    ]
    for k, v in near_pass_sorted:
        parts = k.split("|")
        wr_gap = round(70 - v['wr'], 1)
        sh_gap = round(2.0 - v['sharpe'], 2)
        blocker = f"WR +{wr_gap}pp" if wr_gap > 0 else f"Sharpe +{sh_gap}" if sh_gap > 0 else "OK"
        md_lines.append(f"| {parts[0]} | {parts[1]} | {parts[2]} | {v['wr']} | {v['sharpe']} | {v['maxdd']} | {v['trades']} | {blocker} |")
    if not near_pass_sorted:
        md_lines.append("| — | None in near-pass range | — | — | — | — | — | — |")

    md_lines += [
        f"",
        f"## 🔴 P1 Critical (Sharpe < 0 or MaxDD > 20%)",
        f"",
        f"| Strategy | Pair | TF | WR% | Sharpe | MaxDD% | Trades |",
        f"|---|---|---|---|---|---|---|",
    ]
    for k, v in sorted(p1s.items(), key=lambda x: x[1].get("sharpe", 0))[:20]:
        parts = k.split("|")
        md_lines.append(f"| {parts[0]} | {parts[1]} | {parts[2]} | {v.get('wr','?')} | {v.get('sharpe','?')} | {v.get('maxdd','?')} | {v.get('trades','?')} |")
    if not p1s:
        md_lines.append("| — | None | — | — | — | — | — |")

    md_path = out_dir / f"{date_str}_yf_backtest_report.md"
    with open(md_path, "w") as f:
        f.write("\n".join(md_lines))

    print(f"\n{'='*60}")
    print(f" RESULTS: {totals['PASS']} PASS | {totals['REVIEW']} REVIEW | {totals['P1_CRITICAL']} P1 | {totals['ERROR']} ERR | {totals['SKIP']} SKIP")
    print(f" Pass rate: {report['pass_rate_pct']}% of {len(results)} combos")
    print(f" Report: {md_path.name}")
    print(f"{'='*60}\n")

    return report

if __name__ == "__main__":
    main()
