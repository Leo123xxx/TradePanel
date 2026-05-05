"""
scheduler/recommendations.py
TradePanel — Intelligent Recommendation Engine

Runs automatically after each overnight backtest. Analyses the latest
results across three dimensions:

  1. STRATEGY TRIAGE
     - Regressions  : strategies that moved PASS → REVIEW since last run
     - Improvements : strategies that moved REVIEW → PASS (celebrate!)
     - Near-pass    : REVIEW strategies with Sharpe closest to 1.0 (act here first)
     - Removal queue: strategies with consecutive_fails approaching deadline

  2. PARAMETER TUNING HINTS
     Rule-based guidance keyed to each strategy's WR/DD/Sharpe/trade-count
     profile. Augments (does not replace) the `parameter_tweaks` already in
     the backtest report. One actionable hint per strategy, max.

  3. DELIVERY
     - Telegram : concise summary (top picks, not all 118 REVIEW entries)
     - Markdown  : full detail saved to results/recommendations/

Usage:
    from scheduler.recommendations import RecommendationEngine
    engine = RecommendationEngine()
    engine.run(report_path="results/overnight/20260428_backtest_report.json")

Or standalone:
    python -m scheduler.recommendations results/overnight/20260428_backtest_report.json
"""

from __future__ import annotations

import glob
import json
import logging
import os
import sys
from dataclasses import dataclass, field
from datetime import datetime, date
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

# ── Thresholds (match OPTIMIZATION_SCHEDULE.md) ───────────────────────────────
PASS_SHARPE        = 1.0
PASS_WIN_RATE      = 60.0   # must match MIN_WIN_RATE in scripts/run_overnight_backtest.py
NEAR_PASS_SHARPE   = 0.6   # REVIEW strategies above this get priority attention
REMOVAL_FAILS      = 15    # consecutive backtest fails → escalate to removal queue
ESCALATE_FAILS     = 6     # consecutive fails → active tuning required
CRITICAL_FAILS     = 10    # consecutive fails → strong removal candidate

# Known hard-deadline removal rules from OPTIMIZATION_SCHEDULE.md
REMOVAL_DEADLINES: dict[str, date] = {
    "orb|EURUSD": date(2026, 6, 1),
}


# ── Data classes ──────────────────────────────────────────────────────────────

@dataclass
class StrategyResult:
    key: str          # "strategy|pair|timeframe"
    strategy: str
    pair: str
    timeframe: str
    status: str       # PASS / REVIEW / SKIP
    sharpe: float
    win_rate: float
    max_dd: float
    total_trades: int
    profit_factor: float
    total_pnl: float
    avg_win: float
    avg_loss: float
    long_wr: float
    short_wr: float
    existing_tweaks: list[str]
    tier: int


@dataclass
class Analysis:
    generated: str
    report_date: str
    pass_count: int
    review_count: int
    skip_count: int
    total: int
    regressions: list[dict]       = field(default_factory=list)
    improvements: list[dict]      = field(default_factory=list)
    near_pass: list[dict]         = field(default_factory=list)
    removal_queue: list[dict]     = field(default_factory=list)
    tuning_hints: list[dict]      = field(default_factory=list)


# ── Core engine ───────────────────────────────────────────────────────────────

class RecommendationEngine:

    def __init__(
        self,
        results_dir: str = "results",
        config_path: str = "config/config.yaml",
        notif_bot=None,
    ):
        self.results_dir   = Path(results_dir)
        self.overnight_dir = self.results_dir / "overnight"
        self.reco_dir      = self.results_dir / "recommendations"
        self.reco_dir.mkdir(parents=True, exist_ok=True)

        self.tracker_path  = self.results_dir / "demotion_tracker.json"
        self.notif_bot     = notif_bot   # injected by TradingScheduler; None in standalone mode

    # ── Public entry point ────────────────────────────────────────────────────

    def run(self, report_path: str | None = None) -> Analysis:
        """
        Full pipeline: load → analyse → deliver.
        If report_path is None, uses the most recent overnight report.
        """
        # 1. Load reports
        current_path, current = self._load_report(report_path)
        previous_results      = self._load_previous_results(exclude=current_path)
        tracker               = self._load_tracker()

        report_date = Path(current_path).stem[:8]  # "20260428"
        logger.info(
            f"RecommendationEngine: analysing {report_date} "
            f"({len(current)} results)"
        )

        # 2. Parse into typed objects
        results = [self._parse(r) for r in current if r.get("status") != "SKIP"]

        # 3. Build analysis
        analysis = Analysis(
            generated   = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
            report_date = report_date,
            pass_count  = sum(1 for r in results if r.status == "PASS"),
            review_count= sum(1 for r in results if r.status == "REVIEW"),
            skip_count  = sum(1 for r in current if r.get("status") == "SKIP"),
            total       = len(current),
        )

        analysis.regressions  = self._detect_regressions(results, previous_results)
        analysis.improvements = self._detect_improvements(results, previous_results)
        analysis.near_pass    = self._near_pass_candidates(results)
        analysis.removal_queue= self._removal_candidates(results, tracker)
        analysis.tuning_hints = self._generate_tuning_hints(results)

        # 4. Deliver
        md_path = self._write_markdown(analysis)
        if self.notif_bot:
            self._send_telegram(analysis, md_path)
        else:
            logger.info("No notif_bot configured — Telegram skipped (standalone mode).")

        logger.info(f"Recommendations written → {md_path}")
        return analysis

    # ── Loaders ───────────────────────────────────────────────────────────────

    def _load_report(self, path: str | None) -> tuple[str, list[dict]]:
        if path and Path(path).exists():
            target = Path(path)
        else:
            files = sorted(self.overnight_dir.glob("*_backtest_report.json"))
            if not files:
                raise FileNotFoundError(f"No backtest reports in {self.overnight_dir}")
            target = files[-1]
        data = json.loads(target.read_text(encoding="utf-8"))
        return str(target), data.get("results", [])

    def _load_previous_results(self, exclude: str, n: int = 3) -> list[list[dict]]:
        """Load up to n previous reports for trend comparison."""
        files = sorted(self.overnight_dir.glob("*_backtest_report.json"))
        files = [f for f in files if str(f) != exclude]
        out = []
        for f in files[-n:]:
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
                out.append(data.get("results", []))
            except Exception:
                pass
        return out

    def _load_tracker(self) -> dict:
        if self.tracker_path.exists():
            try:
                return json.loads(self.tracker_path.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {}

    def _parse(self, r: dict) -> StrategyResult:
        stats = r.get("stats", {})
        return StrategyResult(
            key       = f"{r['strategy']}|{r['pair']}|{r['timeframe']}",
            strategy  = r["strategy"],
            pair      = r["pair"],
            timeframe = r["timeframe"],
            status    = r.get("status", "REVIEW"),
            sharpe    = r.get("sharpe_ratio", 0.0),
            win_rate  = r.get("win_rate", 0.0),
            max_dd    = r.get("max_drawdown_pct", 0.0),
            total_trades = r.get("total_trades", 0),
            profit_factor= r.get("profit_factor", 0.0),
            total_pnl = r.get("total_pnl", 0.0),
            avg_win   = stats.get("avg_win", 0.0),
            avg_loss  = stats.get("avg_loss", 0.0),
            long_wr   = stats.get("long_win_rate", 0.0),
            short_wr  = stats.get("short_win_rate", 0.0),
            existing_tweaks = r.get("parameter_tweaks", []),
            tier      = r.get("tier", 1),
        )

    # ── Analysis components ───────────────────────────────────────────────────

    def _detect_regressions(
        self, current: list[StrategyResult], previous_reports: list[list[dict]]
    ) -> list[dict]:
        """Strategies that were PASS in the most recent prior report but are now REVIEW."""
        if not previous_reports:
            return []
        prev = {
            f"{r['strategy']}|{r['pair']}|{r['timeframe']}": r.get("status")
            for r in previous_reports[-1]
        }
        regressions = []
        for r in current:
            if r.status == "REVIEW" and prev.get(r.key) == "PASS":
                regressions.append({
                    "key": r.key,
                    "strategy": r.strategy,
                    "pair": r.pair,
                    "timeframe": r.timeframe,
                    "sharpe": r.sharpe,
                    "win_rate": r.win_rate,
                })
        return regressions

    def _detect_improvements(
        self, current: list[StrategyResult], previous_reports: list[list[dict]]
    ) -> list[dict]:
        """Strategies that just moved REVIEW → PASS."""
        if not previous_reports:
            return []
        prev = {
            f"{r['strategy']}|{r['pair']}|{r['timeframe']}": r.get("status")
            for r in previous_reports[-1]
        }
        improvements = []
        for r in current:
            if r.status == "PASS" and prev.get(r.key) == "REVIEW":
                improvements.append({
                    "key": r.key,
                    "strategy": r.strategy,
                    "pair": r.pair,
                    "timeframe": r.timeframe,
                    "sharpe": r.sharpe,
                    "win_rate": r.win_rate,
                })
        return improvements

    def _near_pass_candidates(self, results: list[StrategyResult]) -> list[dict]:
        """
        Top 5 REVIEW strategies with the most potential — high Sharpe but
        blocked by WR, or WR fine but Sharpe just below threshold.

        Returns the actual blocker so the hint is actionable.
        """
        candidates = [
            r for r in results
            if r.status == "REVIEW" and r.sharpe >= NEAR_PASS_SHARPE
        ]
        candidates.sort(key=lambda r: r.sharpe, reverse=True)

        out = []
        for r in candidates[:5]:
            sharpe_ok = r.sharpe >= PASS_SHARPE
            wr_ok     = r.win_rate >= PASS_WIN_RATE

            if sharpe_ok and not wr_ok:
                blocker = f"WR {r.win_rate:.1f}% needs +{PASS_WIN_RATE - r.win_rate:.1f}pp"
                gap_label = blocker
            elif wr_ok and not sharpe_ok:
                blocker = f"Sharpe {r.sharpe:.2f} needs +{PASS_SHARPE - r.sharpe:.2f}"
                gap_label = blocker
            elif not sharpe_ok and not wr_ok:
                blocker = (
                    f"Sharpe {r.sharpe:.2f} (+{PASS_SHARPE - r.sharpe:.2f} needed), "
                    f"WR {r.win_rate:.1f}% (+{PASS_WIN_RATE - r.win_rate:.1f}pp needed)"
                )
                gap_label = blocker
            else:
                blocker = "Review criteria — check backtest runner thresholds"
                gap_label = blocker

            out.append({
                "key": r.key,
                "strategy": r.strategy,
                "pair": r.pair,
                "timeframe": r.timeframe,
                "sharpe": round(r.sharpe, 3),
                "win_rate": round(r.win_rate, 1),
                "max_dd": round(r.max_dd, 1),
                "blocker": gap_label,
            })
        return out

    def _removal_candidates(
        self, results: list[StrategyResult], tracker: dict
    ) -> list[dict]:
        """
        Strategies flagged for removal based on:
        - consecutive_fails in demotion_tracker >= ESCALATE_FAILS
        - Hard-coded deadlines from OPTIMIZATION_SCHEDULE.md
        """
        today = date.today()
        queue = []

        for r in results:
            if r.status != "REVIEW":
                continue

            entry = tracker.get(r.key, {})
            fails = entry.get("consecutive_fails", 0)

            # Hard-deadline check
            deadline_key = f"{r.strategy}|{r.pair}"
            deadline = REMOVAL_DEADLINES.get(deadline_key)
            days_to_deadline = (deadline - today).days if deadline else None

            if fails < ESCALATE_FAILS and days_to_deadline is None:
                continue

            severity = (
                "🔴 REMOVE"    if (fails >= CRITICAL_FAILS or
                                    (days_to_deadline is not None and days_to_deadline <= 14))
                else "🟠 ESCALATE" if fails >= ESCALATE_FAILS
                else "🟡 WATCH"
            )

            queue.append({
                "key": r.key,
                "strategy": r.strategy,
                "pair": r.pair,
                "timeframe": r.timeframe,
                "sharpe": round(r.sharpe, 3),
                "consecutive_fails": fails,
                "days_to_deadline": days_to_deadline,
                "severity": severity,
            })

        queue.sort(key=lambda x: (-x["consecutive_fails"], x.get("days_to_deadline") or 999))
        return queue

    def _generate_tuning_hints(self, results: list[StrategyResult]) -> list[dict]:
        """
        Rule-based tuning hints for REVIEW strategies.
        Returns one primary action per strategy, ordered by priority.
        Also includes the existing backtest parameter_tweaks for reference.
        """
        hints = []
        for r in results:
            if r.status != "REVIEW":
                continue

            action, priority = self._classify_hint(r)
            hints.append({
                "key": r.key,
                "strategy": r.strategy,
                "pair": r.pair,
                "timeframe": r.timeframe,
                "sharpe": round(r.sharpe, 3),
                "win_rate": round(r.win_rate, 1),
                "max_dd": round(r.max_dd, 1),
                "profit_factor": round(r.profit_factor, 3),
                "total_trades": r.total_trades,
                "priority": priority,          # 1=critical → 5=low
                "action": action,
                "existing_tweaks": r.existing_tweaks,
                "direction_note": self._direction_note(r),
            })

        hints.sort(key=lambda h: (h["priority"], -h["sharpe"]))
        return hints

    def _classify_hint(self, r: StrategyResult) -> tuple[str, int]:
        """
        Returns (action_string, priority_1_to_5).
        Rules evaluated top-down — first match wins.
        """
        wr  = r.win_rate
        dd  = r.max_dd
        sh  = r.sharpe
        pf  = r.profit_factor
        tr  = r.total_trades
        avg_w = abs(r.avg_win)
        avg_l = abs(r.avg_loss)

        # ── No trades → almost certainly a filter/timezone bug ─────────────
        if tr == 0:
            return (
                "⚠️ ZERO TRADES — Check session filter: SAST/UTC mismatch may be "
                "zeroing all signals (see ORB EURUSD debugging pattern). "
                "Add diagnostic print inside generate_signals() to count raw signals.",
                1,
            )

        # ── Too few trades → statistics unreliable ─────────────────────────
        if tr < 10:
            return (
                f"📉 Only {tr} trades — sample too small for reliable stats. "
                "Extend backtest window or relax entry filters before tuning parameters.",
                2,
            )

        # ── Deeply negative Sharpe → fundamental signal quality issue ──────
        if sh < -1.0:
            return (
                f"🚫 Sharpe {sh:.2f} — strategy is actively losing money. "
                "Do not tune parameters yet. Diagnose signal logic: check "
                "entry condition direction, ensure spread/commission are "
                "accounted for, and verify data alignment (SAST vs UTC).",
                1,
            )

        # ── Good WR but drowning in large losses ───────────────────────────
        if wr >= 55 and avg_l > 2.5 * avg_w:
            return (
                f"💡 WR {wr:.0f}% is healthy but avg_loss ({avg_l:.1f}) is "
                f"{avg_l/max(avg_w,0.01):.1f}× avg_win. "
                "SL too wide — try sl_atr_mult × 0.75, or add partial close "
                "at 1R to protect winners.",
                2,
            )

        # ── Good WR, high DD → position sizing or SL width ────────────────
        if wr >= 50 and dd > 20:
            return (
                f"💡 WR {wr:.0f}% but max DD {dd:.0f}%. "
                "Position sizing too aggressive or SL too wide. "
                "Try sl_atr_mult - 0.2, or cap lot size at 50% current level "
                "and re-test.",
                2,
            )

        # ── Near-pass: WR at/above threshold, Sharpe heading right ───────
        if sh >= 0.6 and pf >= 1.0:
            if wr >= PASS_WIN_RATE:
                return (
                    f"🎯 Near-PASS (Sharpe {sh:.2f}, WR {wr:.0f}% ✓). "
                    "WR gate is clear. Try increasing TP: tp_atr_mult +0.5 "
                    "to push Sharpe above 1.0.",
                    2,
                )
            elif wr >= PASS_WIN_RATE - 5:
                # WR within 5pp of threshold — almost there
                return (
                    f"🎯 Near-PASS (Sharpe {sh:.2f}, WR {wr:.0f}% — "
                    f"needs +{PASS_WIN_RATE - wr:.1f}pp). "
                    "Add a regime filter (ADX > 20 or EMA200 gate) to prune "
                    "losing trades and close the WR gap.",
                    2,
                )
            else:
                return (
                    f"📈 Sharpe {sh:.2f} is promising but WR {wr:.0f}% needs "
                    f"+{PASS_WIN_RATE - wr:.1f}pp to reach 60%. "
                    "Tighten entry: add ADX filter or restrict to higher-TF "
                    "trend direction only.",
                    3,
                )

        # ── Win rate 40-50%, PF barely above 1 ────────────────────────────
        if 40 <= wr < 50 and 1.0 <= pf < 1.3:
            return (
                f"🔧 Marginal edge (WR {wr:.0f}%, PF {pf:.2f}). "
                "Check long_win_rate vs short_win_rate — if one direction is "
                ">10% better, disable the weaker side. "
                "Also try tightening TP to improve hit rate: tp_atr_mult - 0.3.",
                3,
            )

        # ── Low WR, positive PF → big winners but rare ────────────────────
        if wr < 40 and pf > 1.0:
            return (
                f"🔧 Low WR ({wr:.0f}%) but PF {pf:.2f} — system captures "
                "large wins rarely. Typical of trend-following. "
                "Add a regime filter (EMA200 gate) to trade only in trending "
                "conditions; avoid in ranging regimes.",
                3,
            )

        # ── Low WR, negative PF ────────────────────────────────────────────
        if wr < 40 and pf < 1.0:
            return (
                f"❌ WR {wr:.0f}%, PF {pf:.2f} — no edge detected. "
                "Entry signal does not predict direction better than random. "
                "Consider disabling and rebuilding entry logic from scratch.",
                4,
            )

        # ── Default: moderate underperformer ──────────────────────────────
        return (
            f"📋 WR {wr:.0f}%, Sharpe {sh:.2f}. "
            "Investigate avg_trade_duration — if trades close in < 1h on H1, "
            "TP is too tight. If > 48h, consider trailing SL.",
            4,
        )

    def _direction_note(self, r: StrategyResult) -> str | None:
        """Flag significant long/short win rate divergence."""
        diff = abs(r.long_wr - r.short_wr)
        if diff >= 12 and r.total_trades >= 20:
            better    = "LONG" if r.long_wr > r.short_wr else "SHORT"
            worse     = "SHORT" if better == "LONG" else "LONG"
            better_wr = max(r.long_wr, r.short_wr)
            worse_wr  = min(r.long_wr, r.short_wr)
            return (
                f"Directional bias: {better} ({better_wr:.0f}%) >> "
                f"{worse} ({worse_wr:.0f}%) — consider disabling {worse} trades."
            )
        return None

    # ── Delivery ──────────────────────────────────────────────────────────────

    def _write_markdown(self, a: Analysis) -> str:
        lines = [
            f"# TradePanel Recommendations — {a.report_date}",
            f"",
            f"Generated: {a.generated}  ",
            f"Report: `results/overnight/{a.report_date}_backtest_report.json`",
            f"",
            f"---",
            f"",
            f"## Summary",
            f"",
            f"| Metric | Value |",
            f"|--------|-------|",
            f"| Total results | {a.total} |",
            f"| ✅ PASS | {a.pass_count} ({a.pass_count/max(a.total,1)*100:.0f}%) |",
            f"| 🔄 REVIEW | {a.review_count} ({a.review_count/max(a.total,1)*100:.0f}%) |",
            f"| ⏭ SKIP | {a.skip_count} |",
            f"",
        ]

        # ── Improvements ──────────────────────────────────────────────────
        if a.improvements:
            lines += ["## 🎉 New PASSes Since Last Run", ""]
            for imp in a.improvements:
                lines.append(
                    f"- **{imp['strategy']}** {imp['pair']} {imp['timeframe']} "
                    f"— Sharpe {imp['sharpe']:.2f}, WR {imp['win_rate']:.0f}%"
                )
            lines.append("")

        # ── Regressions ───────────────────────────────────────────────────
        if a.regressions:
            lines += ["## ⚠️ Regressions (PASS → REVIEW)", ""]
            for reg in a.regressions:
                lines.append(
                    f"- **{reg['strategy']}** {reg['pair']} {reg['timeframe']} "
                    f"— Sharpe now {reg['sharpe']:.2f}, WR {reg['win_rate']:.0f}% "
                    f"— **Investigate immediately**"
                )
            lines.append("")

        # ── Removal queue ─────────────────────────────────────────────────
        if a.removal_queue:
            lines += ["## 🗑️ Removal / Escalation Queue", ""]
            for item in a.removal_queue:
                dl = f", deadline in {item['days_to_deadline']}d" if item["days_to_deadline"] else ""
                lines.append(
                    f"- {item['severity']} **{item['strategy']}** "
                    f"{item['pair']} {item['timeframe']} "
                    f"— {item['consecutive_fails']} consecutive fails{dl} "
                    f"(Sharpe {item['sharpe']:.2f})"
                )
            lines.append("")

        # ── Near-pass ─────────────────────────────────────────────────────
        if a.near_pass:
            lines += ["## 🎯 Near-PASS Candidates (prioritise these)", ""]
            lines += [
                "| Strategy | Pair | TF | Sharpe | WR% | DD% | Blocker |",
                "|----------|------|----|--------|-----|-----|---------|",
            ]
            for np in a.near_pass:
                lines.append(
                    f"| {np['strategy']} | {np['pair']} | {np['timeframe']} "
                    f"| {np['sharpe']} | {np['win_rate']} | {np['max_dd']} "
                    f"| {np['blocker']} |"
                )
            lines.append("")

        # ── Tuning hints (priority 1 and 2 only in summary; all in appendix) ─
        critical_hints = [h for h in a.tuning_hints if h["priority"] <= 2]
        if critical_hints:
            lines += [
                "## 🔧 Priority Tuning Hints (P1 + P2)",
                "",
                "_P1 = immediate action required / P2 = high value next test_",
                "",
            ]
            for h in critical_hints:
                lines.append(f"### {h['strategy']} — {h['pair']} {h['timeframe']}")
                lines.append(f"**Action:** {h['action']}")
                if h["direction_note"]:
                    lines.append(f"**Direction:** {h['direction_note']}")
                if h["existing_tweaks"]:
                    lines.append("**Backtest suggestions:**")
                    for t in h["existing_tweaks"]:
                        lines.append(f"  - {t}")
                lines.append("")

        # ── Full tuning appendix ──────────────────────────────────────────
        lines += [
            "---",
            "",
            "## Appendix — Full REVIEW Strategy Tuning List",
            "",
            "| Priority | Strategy | Pair | TF | Sharpe | WR% | Action |",
            "|----------|----------|------|----|--------|-----|--------|",
        ]
        for h in a.tuning_hints:
            action_short = h["action"][:80].replace("|", "\\|")
            lines.append(
                f"| P{h['priority']} | {h['strategy']} | {h['pair']} "
                f"| {h['timeframe']} | {h['sharpe']} | {h['win_rate']} "
                f"| {action_short}… |"
            )
        lines.append("")

        md = "\n".join(lines)
        out_path = self.reco_dir / f"{a.report_date}_recommendations.md"
        out_path.write_text(md, encoding="utf-8")
        return str(out_path)

    def _send_telegram(self, a: Analysis, md_path: str):
        """
        Send a concise Telegram summary. Full detail is in the markdown report.
        Keeps message under ~2000 chars to stay within Telegram limits.
        """
        pass_rate = a.pass_count / max(a.total, 1) * 100
        status_icon = "🟢" if pass_rate >= 15 else "🟡" if pass_rate >= 8 else "🔴"

        msg_lines = [
            f"🧠 <b>STRATEGY RECOMMENDATIONS</b>",
            f"━━━━━━━━━━━━━━━",
            f"{status_icon} <b>Pass rate:</b> {a.pass_count}/{a.total} ({pass_rate:.0f}%)",
            f"📅 <b>Report:</b> {a.report_date}",
            "",
        ]

        if a.improvements:
            msg_lines.append("🎉 <b>New PASS strategies:</b>")
            for imp in a.improvements[:3]:
                msg_lines.append(
                    f"  ✅ {imp['strategy']} {imp['pair']} {imp['timeframe']} "
                    f"(Sharpe {imp['sharpe']:.2f})"
                )
            msg_lines.append("")

        if a.regressions:
            msg_lines.append("⚠️ <b>Regressions (investigate now):</b>")
            for reg in a.regressions[:3]:
                msg_lines.append(
                    f"  📉 {reg['strategy']} {reg['pair']} {reg['timeframe']} "
                    f"→ Sharpe {reg['sharpe']:.2f}"
                )
            msg_lines.append("")

        if a.removal_queue:
            critical = [r for r in a.removal_queue if "REMOVE" in r["severity"]]
            if critical:
                msg_lines.append("🗑️ <b>Removal candidates:</b>")
                for item in critical[:3]:
                    dl = f" ({item['days_to_deadline']}d left)" if item["days_to_deadline"] else ""
                    msg_lines.append(
                        f"  {item['severity']} {item['strategy']} "
                        f"{item['pair']}{dl}"
                    )
                msg_lines.append("")

        if a.near_pass:
            msg_lines.append("🎯 <b>Near-PASS — act here first:</b>")
            for np in a.near_pass[:3]:
                msg_lines.append(
                    f"  📈 {np['strategy']} {np['pair']} {np['timeframe']} "
                    f"— Sharpe {np['sharpe']} | {np['blocker']}"
                )
            msg_lines.append("")

        p1_hints = [h for h in a.tuning_hints if h["priority"] == 1]
        if p1_hints:
            msg_lines.append("🚨 <b>Critical issues (P1):</b>")
            for h in p1_hints[:3]:
                short = h["action"][:120]
                msg_lines.append(f"  ⚡ {h['strategy']} {h['pair']}: {short}")
            msg_lines.append("")

        msg_lines += [
            "━━━━━━━━━━━━━━━",
            f"📄 Full report: <code>results/recommendations/{a.report_date}_recommendations.md</code>",
        ]

        try:
            self.notif_bot.send_sync_message("\n".join(msg_lines))
        except Exception as e:
            logger.error(f"Failed to send recommendations via Telegram: {e}")


# ── Standalone entry point ────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(name)s — %(levelname)s — %(message)s",
    )

    parser = argparse.ArgumentParser(
        description="TradePanel Recommendation Engine — standalone mode"
    )
    parser.add_argument(
        "report", nargs="?", default=None,
        help="Path to backtest report JSON (default: latest in results/overnight/)",
    )
    parser.add_argument(
        "--results-dir", default="results",
        help="Results root directory (default: results)",
    )
    args = parser.parse_args()

    engine = RecommendationEngine(results_dir=args.results_dir)
    analysis = engine.run(report_path=args.report)

    # Print summary to stdout
    print(f"\n{'='*60}")
    print(f"RECOMMENDATIONS COMPLETE — {analysis.report_date}")
    print(f"{'='*60}")
    print(f"  PASS:        {analysis.pass_count}/{analysis.total}")
    print(f"  REVIEW:      {analysis.review_count}")
    print(f"  Improvements:{len(analysis.improvements)}")
    print(f"  Regressions: {len(analysis.regressions)}")
    print(f"  Near-pass:   {len(analysis.near_pass)}")
    print(f"  Removal queue:{len(analysis.removal_queue)}")
    print(f"  P1 hints:    {sum(1 for h in analysis.tuning_hints if h['priority']==1)}")
    print(f"  P2 hints:    {sum(1 for h in analysis.tuning_hints if h['priority']==2)}")
