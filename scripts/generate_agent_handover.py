"""
scripts/generate_agent_handover.py
===================================
Generates a dated agent handover report consolidating the current state of
the TradePanel system. Designed to run after the Saturday full maintenance job.

Output: results/agent_handover_YYYYMMDD.md

The report includes:
  - System status (mode, account, enabled strategy count)
  - Data coverage summary (latest bar date per pair/TF)
  - WFO master results (pass/fail per strategy)
  - Demotion tracker (strategies at risk of auto-demotion)
  - Overnight backtest trends (last 7 days win rate)
  - Prioritised action list for the next agent session

Usage:
    python scripts/generate_agent_handover.py
    python scripts/generate_agent_handover.py --out results/my_handover.md
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import argparse
import json
import yaml
import re
from pathlib import Path
from datetime import datetime, timedelta
from data.db_client import DBClient


# ── Paths ────────────────────────────────────────────────────────────────────
ROOT          = Path(__file__).parent.parent
CFG_PATH      = ROOT / "config" / "strategies.yaml"
CONFIG_PATH   = ROOT / "config" / "config.yaml"
WFO_SUMMARY   = ROOT / "results" / "wfo_master_summary.md"
DEMOTION_PATH = ROOT / "results" / "demotion_tracker.json"
OVERNIGHT_DIR = ROOT / "results" / "overnight"
PAIRS         = ["XAUUSD", "EURUSD", "GBPUSD", "USDJPY", "XAGUSD", "BTCUSD", "ETHUSD"]
KEY_TFS       = ["M1", "M30", "H1", "H4", "D1", "W1"]


# ── Loaders ──────────────────────────────────────────────────────────────────

def load_strategies():
    with open(CFG_PATH, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    enabled, disabled = [], []
    for name, val in cfg.items():
        if not isinstance(val, dict):
            continue
        if val.get("enabled", False):
            enabled.append({"name": name, "tier": val.get("tier", "?"), "pairs": val.get("pairs", [])})
        else:
            disabled.append(name)
    return enabled, disabled


def load_system_mode():
    try:
        with open(CONFIG_PATH, encoding="utf-8") as f:
            cfg = yaml.safe_load(f)
        return cfg.get("system", {}).get("mode", "unknown")
    except Exception:
        return "unknown"


def load_wfo_summary():
    if not WFO_SUMMARY.exists():
        return None, []
    content = WFO_SUMMARY.read_text(encoding="utf-8")
    rows = []
    in_table = False
    for line in content.splitlines():
        if line.startswith("| Strategy"):
            in_table = True
            continue
        if in_table and line.startswith("|--"):
            continue
        if in_table and line.startswith("|"):
            parts = [p.strip() for p in line.strip("|").split("|")]
            if len(parts) >= 6:
                rows.append({
                    "strategy": parts[0],
                    "pair":     parts[1],
                    "tf":       parts[2],
                    "pass_rate": parts[3],
                    "windows":  parts[4],
                    "verdict":  parts[5],
                })
        elif in_table and not line.startswith("|"):
            break
    # Extract generated date
    gen_date = None
    m = re.search(r"\*\*Generated:\*\* (.+?)  ", content)
    if m:
        gen_date = m.group(1).strip()
    return gen_date, rows


def load_demotion_tracker():
    if not DEMOTION_PATH.exists():
        return {}
    try:
        with open(DEMOTION_PATH) as f:
            return json.load(f)
    except Exception:
        return {}


def load_overnight_trend():
    """Read last 7 overnight reports and extract per-strategy WR."""
    if not OVERNIGHT_DIR.exists():
        return {}
    reports = sorted(OVERNIGHT_DIR.glob("*.md"))[-7:]
    wr_by_strategy = {}
    for report in reports:
        content = report.read_text(encoding="utf-8", errors="ignore")
        for line in content.splitlines():
            m = re.search(r"\|\s*(\w+)\s*\|.*?\|\s*([\d.]+)%\s*\|", line)
            if m:
                strat = m.group(1)
                wr    = float(m.group(2))
                wr_by_strategy.setdefault(strat, []).append(wr)
    return {k: sum(v)/len(v) for k, v in wr_by_strategy.items() if v}


def load_data_coverage():
    try:
        db = DBClient()
        rows = db.execute_query(
            "SELECT pair, timeframe, MAX(timestamp), COUNT(*) "
            "FROM market_data GROUP BY pair, timeframe ORDER BY pair, timeframe"
        )
        coverage = {}
        for pair, tf, latest, count in (rows or []):
            coverage.setdefault(pair, {})[tf] = {"latest": latest, "count": count}
        return coverage
    except Exception:
        return {}


# ── Report builder ────────────────────────────────────────────────────────────

def build_report(out_path: Path):
    now       = datetime.now()
    date_str  = now.strftime("%Y-%m-%d")
    ts_str    = now.strftime("%Y-%m-%d %H:%M:%S")

    enabled, disabled   = load_strategies()
    mode                = load_system_mode()
    wfo_date, wfo_rows  = load_wfo_summary()
    demotion            = load_demotion_tracker()
    wr_trend            = load_overnight_trend()
    coverage            = load_data_coverage()

    # ── Derive action items ───────────────────────────────────────────────
    actions = []

    # WFO failures
    failing_wfo = {}
    for row in wfo_rows:
        verdict = row["verdict"]
        if "FAIL" in verdict or "ERROR" in verdict:
            failing_wfo.setdefault(row["strategy"], []).append(
                f"{row['pair']} {row['tf']} ({row['pass_rate']})"
            )
    for strat, combos in failing_wfo.items():
        actions.append({
            "priority": "HIGH",
            "type": "WFO_FAIL",
            "strategy": strat,
            "detail": f"WFO FAIL on {', '.join(combos)} — review params or demote",
        })

    # Demotion risk (consecutive fails)
    for strat, info in demotion.items():
        consec = info.get("consecutive_fails", 0)
        if consec >= 3:
            actions.append({
                "priority": "HIGH" if consec >= 5 else "MEDIUM",
                "type": "DEMOTION_RISK",
                "strategy": strat,
                "detail": f"{consec} consecutive days WR < 50% — auto-demotion at 5",
            })

    # Low win rate trend
    for strat, avg_wr in wr_trend.items():
        if avg_wr < 50:
            actions.append({
                "priority": "MEDIUM",
                "type": "LOW_WR_TREND",
                "strategy": strat,
                "detail": f"7-day avg WR = {avg_wr:.1f}% (below 50% threshold)",
            })

    # Data staleness
    cutoff = now - timedelta(days=2)
    for pair in PAIRS:
        pair_data = coverage.get(pair, {})
        m1_info = pair_data.get("M1", {})
        latest  = m1_info.get("latest")
        if latest and latest < cutoff:
            actions.append({
                "priority": "HIGH",
                "type": "STALE_DATA",
                "strategy": pair,
                "detail": f"M1 data last updated {latest.date()} — run data sync",
            })

    actions.sort(key=lambda a: (0 if a["priority"] == "HIGH" else 1, a["type"]))

    # ── Write report ──────────────────────────────────────────────────────
    lines = [
        f"# TradePanel Agent Handover — {date_str}",
        "",
        f"**Generated:** {ts_str}  ",
        f"**System mode:** `{mode}`  ",
        f"**Enabled strategies:** {len(enabled)}  ",
        f"**Disabled strategies:** {len(disabled)}  ",
        "",
        "---",
        "",
        "## System Status",
        "",
        f"| Item | Value |",
        f"|------|-------|",
        f"| Mode | `{mode}` |",
        f"| Enabled strategies | {len(enabled)} |",
        f"| Disabled strategies | {len(disabled)} |",
        f"| WFO last run | {wfo_date or 'not found'} |",
        f"| Report generated | {ts_str} |",
        "",
        "---",
        "",
        "## Prioritised Action List",
        "",
    ]

    if not actions:
        lines.append("**No actions required — all systems nominal.**")
    else:
        lines += [
            "| Priority | Type | Strategy/Pair | Detail |",
            "|----------|------|---------------|--------|",
        ]
        for a in actions:
            pri_icon = "🔴" if a["priority"] == "HIGH" else "🟡"
            lines.append(
                f"| {pri_icon} {a['priority']} | {a['type']} "
                f"| {a['strategy']} | {a['detail']} |"
            )

    lines += [
        "",
        "---",
        "",
        "## WFO Results",
        f"_(from {wfo_date or 'unknown'})_",
        "",
        "| Strategy | Pair | TF | Pass Rate | Verdict |",
        "|----------|------|----|-----------|---------|",
    ]
    for row in wfo_rows:
        lines.append(
            f"| {row['strategy']} | {row['pair']} | {row['tf']} "
            f"| {row['pass_rate']} | {row['verdict']} |"
        )
    if not wfo_rows:
        lines.append("_No WFO results found — run RUN_WFO_AND_UPDATE.bat first._")

    lines += [
        "",
        "---",
        "",
        "## Demotion Tracker",
        "",
        "| Strategy | Consecutive Fails | Last WR | Status |",
        "|----------|-------------------|---------|--------|",
    ]
    for strat, info in demotion.items():
        consec = info.get("consecutive_fails", 0)
        last_wr = info.get("last_wr", "-")
        status = "⚠️ AT RISK" if consec >= 3 else ("🔴 DEMOTE NOW" if consec >= 5 else "OK")
        last_wr_str = f"{last_wr:.1f}%" if isinstance(last_wr, float) else str(last_wr)
        lines.append(f"| {strat} | {consec} | {last_wr_str} | {status} |")
    if not demotion:
        lines.append("_No demotion events recorded._")

    lines += [
        "",
        "---",
        "",
        "## 7-Day Overnight Backtest WR Trend",
        "",
        "| Strategy | Avg WR (7d) | Status |",
        "|----------|------------|--------|",
    ]
    for strat, avg_wr in sorted(wr_trend.items(), key=lambda x: x[1]):
        status = "✅" if avg_wr >= 60 else ("⚠️" if avg_wr >= 50 else "❌")
        lines.append(f"| {strat} | {avg_wr:.1f}% | {status} |")
    if not wr_trend:
        lines.append("_No overnight backtest history found._")

    lines += [
        "",
        "---",
        "",
        "## Data Coverage",
        "",
        f"{'Pair':<10} {'TF':<6} {'Latest Bar':<14} {'Bars':>10}",
        "-" * 44,
    ]
    for pair in PAIRS:
        pair_data = coverage.get(pair, {})
        for tf in KEY_TFS:
            info = pair_data.get(tf, {})
            latest = info.get("latest")
            count  = info.get("count", 0)
            latest_str = str(latest.date()) if latest else "-"
            stale  = " ⚠️" if (latest and latest < cutoff) else ""
            lines.append(f"{pair:<10} {tf:<6} {latest_str:<14} {count:>10,}{stale}")

    lines += [
        "",
        "---",
        "",
        "## Enabled Strategies",
        "",
        "| Strategy | Tier | Pairs |",
        "|----------|------|-------|",
    ]
    for s in enabled:
        pairs_str = ", ".join(s["pairs"][:3]) + ("…" if len(s["pairs"]) > 3 else "")
        lines.append(f"| {s['name']} | {s['tier']} | {pairs_str} |")

    lines += [
        "",
        "---",
        f"_Generated by scripts/generate_agent_handover.py on {ts_str}_",
    ]

    out_path.parent.mkdir(exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  Handover report written: {out_path}")
    return out_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate agent handover report.")
    parser.add_argument(
        "--out", type=str, default=None,
        help="Output path (default: results/agent_handover_YYYYMMDD.md)"
    )
    args = parser.parse_args()

    date_str = datetime.now().strftime("%Y%m%d")
    out_path = Path(args.out) if args.out else ROOT / "results" / f"agent_handover_{date_str}.md"

    print(f"\nGenerating agent handover report...")
    build_report(out_path)
    print(f"Done.\n")
