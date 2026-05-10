"""
scheduler/docker_jobs.py — TradePanel APScheduler (canonical, Docker-aware)

Single source of truth for all scheduled jobs. jobs.py (native mode) imports
from here so fixes only need to be made in one place.

Bridge selection:
  - If MetaTrader5 is importable → native mode (direct MT5 SDK calls)
  - Otherwise              → bridge mode (HTTP calls to mt5_bridge service)
"""

import sys
import os
import logging
import threading

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("TradingScheduler")

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    from mt5_bridge.docker_mock import setup_mock
    setup_mock()
    import MetaTrader5 as mt5
    MT5_AVAILABLE = False

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime, timedelta
import subprocess
import yaml
import requests
import json

from forward_test.paper_engine import PaperEngine
from risk.regime_detector import RegimeDetector
from logging_.health_monitor import HealthMonitor
from notifications.telegram_bot import TelegramBot
from notifications.router import CommandRouter
from data.db_client import DBClient
from utils.event_bus import bus
from functools import wraps


class TradingScheduler:
    """
    Runs all TradePanel scheduled jobs via APScheduler.

    Detects at startup whether the MetaTrader5 SDK is available (native mode)
    or whether it should talk to the HTTP bridge (Docker mode).
    """

    def __init__(self, config_path: str = "config/config.yaml"):
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)

        self.scheduler = BackgroundScheduler()
        self.engine = PaperEngine(config_path)
        self.regime_detector = RegimeDetector()
        self.health_monitor = HealthMonitor()
        self.notif_bot = TelegramBot()
        self.notif_router = CommandRouter()
        self.db = DBClient()

        self.heartbeat_count = 0
        self.last_trade_check = datetime.now()
        self.last_pos_count = None
        self.hb_interval_mins = self.config.get("scheduler", {}).get(
            "telegram_heartbeat_interval_mins", 60
        )
        self.mt5_bridge_url = os.getenv(
            "MT5_BRIDGE_URL", "http://host.docker.internal:8001"
        )

        # Overnight backtest state (non-blocking run)
        self._backtest_thread: threading.Thread | None = None
        
        # Task 3.3: Subscribe to health errors to trigger circuit breaker
        bus.subscribe("HEALTH_ERROR", self._handle_health_error)
        bus.subscribe("CIRCUIT_BREAKER_RESET", self._handle_cb_reset)
        self._cb_active = False

    # ──────────────────────────────────────────────────────────────────────────
    # MT5 helpers (bridge-aware)
    # ──────────────────────────────────────────────────────────────────────────

    def _get_positions(self):
        if MT5_AVAILABLE:
            return mt5.positions_get()
        try:
            r = requests.get(f"{self.mt5_bridge_url}/positions", timeout=5)
            if r.status_code == 200:
                return r.json()
        except Exception:
            pass
        return None

    def _get_history(self, ticket):
        if MT5_AVAILABLE:
            return mt5.history_deals_get(ticket=ticket)
        try:
            r = requests.get(f"{self.mt5_bridge_url}/history/{ticket}", timeout=5)
            if r.status_code == 200:
                return r.json()
        except Exception:
            pass
        return None

    def _mt5_connected(self) -> bool:
        if MT5_AVAILABLE:
            return self.engine.connector.connected
        try:
            r = requests.get(f"{self.mt5_bridge_url}/health", timeout=5)
            return r.status_code == 200 and r.json().get("mt5_connected", False)
        except Exception:
            return False

    # ──────────────────────────────────────────────────────────────────────────
    # Task 3.2: Circuit Breaker Logic
    # ──────────────────────────────────────────────────────────────────────────

    def circuit_breaker_guard(self, func):
        """Decorator to skip job execution if circuit breaker is active."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            if self._cb_active:
                logger.warning(f"Circuit Breaker active: Skipping job {func.__name__}")
                return
            return func(*args, **kwargs)
        return wrapper

    def _handle_health_error(self, data):
        """Triggered via EventBus when a critical error occurs."""
        logger.error(f"EventBus: Health error received - {data}")
        # Automatically trigger breaker on critical MT5 errors
        if "MT5" in str(data):
            self._cb_active = True
            self.db.execute_query(
                "INSERT INTO bot_health (event_type, status, message) VALUES ('CIRCUIT_BREAKER', 'PAUSED', %s)",
                (f"Auto-pause due to: {data}",)
            )

    def _handle_cb_reset(self, data):
        """Resets the circuit breaker."""
        logger.info("Circuit Breaker reset received.")
        self._cb_active = False

    # ──────────────────────────────────────────────────────────────────────────
    # Scheduler setup
    # ──────────────────────────────────────────────────────────────────────────

    def start(self):
        sched_cfg = self.config.get("scheduler", {})
        notif_cfg = self.config.get("notifications", {})

        # ── High-frequency jobs ───────────────────────────────────────────────
        self.scheduler.add_job(
            self._heartbeat_wrapper,
            IntervalTrigger(seconds=sched_cfg.get("heartbeat_interval_sec", 60)),
            id="heartbeat", name="Heartbeat Monitor",
        )
        self.scheduler.add_job(
            self._check_mt5_connection,
            IntervalTrigger(seconds=60),
            id="mt5_conn", name="MT5 Connection Watcher",
        )
        self.scheduler.add_job(
            self._sync_positions,
            IntervalTrigger(minutes=5),
            id="position_sync", name="Position Sync MT5→DB",
        )
        self.scheduler.add_job(
            self.circuit_breaker_guard(self.engine.run_detect),
            IntervalTrigger(minutes=1),
            id="signal_detect", name="Signal Detection (1m)",
        )
        self.scheduler.add_job(
            self.circuit_breaker_guard(self.engine.run_execute),
            IntervalTrigger(minutes=5),
            id="trade_execute", name="Trade Execution (5m)",
        )
        self.scheduler.add_job(
            self._rollup_pnl,
            IntervalTrigger(hours=1),
            id="pnl_rollup", name="Hourly PnL Roll-Up",
        )
        self.scheduler.add_job(
            self._run_regime_detection,
            IntervalTrigger(hours=1),
            id="regime_detect", name="Market Regime Detector (1h)",
        )

        # ── Cron jobs ─────────────────────────────────────────────────────────
        ingest_hours = sched_cfg.get("data_ingest_hours", "0,6,12,18")
        ingest_min   = sched_cfg.get("data_ingest_minute", 5)
        self.scheduler.add_job(
            self._ingest_daily_data,
            CronTrigger(hour=ingest_hours, minute=ingest_min),
            id="data_ingest_6h", name="6-Hour Market Data Ingest",
        )

        summary_h, summary_m = (
            notif_cfg.get("daily_summary_time", "18:00").split(":")
        )
        self.scheduler.add_job(
            self._send_daily_summary,
            CronTrigger(hour=int(summary_h), minute=int(summary_m)),
            id="daily_summary", name="Daily Performance Summary",
        )
        self.scheduler.add_job(
            self._send_weekly_report,
            CronTrigger(day_of_week="mon", hour=8, minute=0),
            id="weekly_report", name="Weekly Performance Report",
        )

        bt_hour = sched_cfg.get("overnight_backtest_hour", 2)
        bt_min  = sched_cfg.get("overnight_backtest_minute", 0)
        self.scheduler.add_job(
            self._run_overnight_backtest,
            CronTrigger(day_of_week="mon-fri", hour=bt_hour, minute=bt_min),
            id="overnight_backtest", name="Overnight Strategy Backtest",
        )
        self.scheduler.add_job(
            self._run_wfo_suite,
            CronTrigger(day_of_week="wed,sun", hour=3, minute=0),
            id="wfo_biweekly", name="Bi-Weekly Walk-Forward Optimisation",
        )
        self.scheduler.add_job(
            self._run_yahoo_history_fill,
            CronTrigger(day_of_week="sun", hour=1, minute=30),
            id="yahoo_history_fill", name="Weekly Yahoo CFD History Fill",
        )
        self.scheduler.add_job(
            self._refresh_cot_data,
            CronTrigger(day_of_week="fri", hour=21, minute=0),
            id="cot_refresh", name="CFTC COT Weekly Refresh",
        )
        self.scheduler.add_job(
            self._db_cleanup,
            CronTrigger(day_of_week="sun", hour=0, minute=30),
            id="db_cleanup", name="Weekly DB Cleanup",
        )
        self.scheduler.add_job(
            self._strategy_correlation_check,
            CronTrigger(day_of_week="mon", hour=9, minute=0),
            id="correlation_check", name="Weekly Strategy Correlation Check",
        )
        self.scheduler.add_job(
            self._check_signal_outcomes,
            CronTrigger(hour=23, minute=0, timezone='UTC'),  # 23:00 UTC = 01:00 SAST
            id="signal_outcome_check", name="Nightly Signal Outcome Check",
        )
        self.scheduler.add_job(
            self._sync_mt5_history,
            IntervalTrigger(hours=4),
            id="mt5_history_sync", name="4-Hour Account History Sync",
        )
        self.scheduler.add_job(
            self._run_weekly_archive,
            CronTrigger(day_of_week="thu", hour=23, minute=59),
            id="weekly_archive", name="Weekly Strategy Intelligence Archival",
        )


        self.scheduler.start()
        job_count = len(self.scheduler.get_jobs())
        logger.info(f"APScheduler started — {job_count} jobs registered.")

    def stop(self):
        self.scheduler.shutdown()

    # ──────────────────────────────────────────────────────────────────────────
    # Heartbeat & position monitoring
    # ──────────────────────────────────────────────────────────────────────────

    def _heartbeat_wrapper(self):
        self.health_monitor.logger.heartbeat()
        self.heartbeat_count += 1

        positions = self._get_positions()
        current_count = len(positions) if positions else 0
        pos_changed = (
            self.last_pos_count is not None
            and current_count != self.last_pos_count
        )
        self.last_pos_count = current_count

        activity = self._get_recent_activity()
        is_interval = (self.heartbeat_count % self.hb_interval_mins == 0)

        if activity or is_interval or pos_changed:
            self._send_telegram_heartbeat(activity, external_change=pos_changed)
            self.last_trade_check = datetime.now()

    def _get_recent_activity(self) -> str:
        try:
            new_rows = self.db.execute_query(
                "SELECT pair, direction, strategy_id FROM trades "
                "WHERE open_time > %s AND mode = 'PAPER'",
                (self.last_trade_check,),
            )
            closed_rows = self.db.execute_query(
                "SELECT pair, exit_price - entry_price, close_reason FROM trades "
                "WHERE close_time > %s AND mode = 'PAPER'",
                (self.last_trade_check,),
            )
            lines = []
            if new_rows:
                for sym, direction, _ in new_rows:
                    lines.append(f"🆕 <b>OPEN:</b> {sym} {direction}")
            if closed_rows:
                for sym, pnl, reason in closed_rows:
                    icon = "💰" if pnl >= 0 else "📉"
                    lines.append(f"{icon} <b>CLOSE:</b> {sym} ({pnl:+.2f}) — {reason}")
            return "\n".join(lines)
        except Exception as e:
            logger.error(f"_get_recent_activity error: {e}")
            return ""

    def _send_telegram_heartbeat(self, activity: str = "", external_change: bool = False):
        try:
            mt5_status = "🟢 CONNECTED" if self._mt5_connected() else "🔴 DISCONNECTED"
            positions = self._get_positions()
            pos_count = len(positions) if positions else 0

            msg = (
                f"💓 <b>SYSTEM HEARTBEAT</b>\n"
                f"━━━━━━━━━━━━━━━\n"
                f"🖥 <b>MT5:</b> {mt5_status}\n"
                f"📊 <b>Active Positions:</b> {pos_count}\n"
            )
            if activity:
                msg += f"\n⚡ <b>RECENT ACTIVITY:</b>\n{activity}\n"
            elif external_change:
                msg += "\n⚠️ <b>EXTERNAL CHANGE:</b>\nManual position update detected.\n"
            msg += f"━━━━━━━━━━━━━━━\n🕒 <i>Next report in {self.hb_interval_mins}m</i>"

            self.notif_bot.send_sync_message(msg)
        except Exception as e:
            logger.error(f"_send_telegram_heartbeat error: {e}")

    # ──────────────────────────────────────────────────────────────────────────
    # MT5 connection & position sync
    # ──────────────────────────────────────────────────────────────────────────

    def _check_mt5_connection(self):
        if MT5_AVAILABLE:
            if not self.engine.connector.connected:
                self.engine.connector.connect_with_retry(
                    max_attempts=3,
                    delays=[5, 15, 30],
                    notify_fn=self.notif_bot.send_sync_message,
                )
        else:
            if not self._mt5_connected():
                self.notif_bot.send_sync_message(
                    "🔴 <b>MT5 CONNECTION FAILED</b>\nBridge unreachable or disconnected."
                )

    def _sync_positions(self):
        if MT5_AVAILABLE:
            if not self.engine.connector.connect():
                return
        else:
            if not self._mt5_connected():
                return

        positions = self._get_positions()
        live_tickets = set()
        if positions:
            live_tickets = (
                {p.ticket for p in positions}
                if MT5_AVAILABLE
                else {p["ticket"] for p in positions}
            )

        rows = self.db.execute_query(
            "SELECT mt5_ticket, trade_id FROM trades "
            "WHERE status = 'OPENED' AND mode = 'PAPER'"
        )
        if rows:
            for mt5_ticket, trade_id in rows:
                if mt5_ticket not in live_tickets:
                    history = self._get_history(mt5_ticket)
                    exit_price = (
                        history[-1].price if MT5_AVAILABLE and history
                        else (history[-1]["price"] if history else 0.0)
                    )
                    self.db.execute_query(
                        "UPDATE trades SET status='CLOSED', close_reason='EXTERNAL_CLOSE', "
                        "close_time=%s, exit_price=%s WHERE trade_id=%s",
                        (datetime.now(), exit_price, trade_id),
                    )

    # ──────────────────────────────────────────────────────────────────────────
    # P&L, regime, data
    # ──────────────────────────────────────────────────────────────────────────

    def _rollup_pnl(self):
        acct = self.config.get("account", {})
        usdzar      = float(acct.get("backtesting_usdzar_rate", 18.50))
        balance_zar = float(acct.get("backtesting_balance_zar", 180_000.0))

        cutoff = datetime.now() - timedelta(hours=1)
        rows = self.db.execute_query(
            """SELECT COALESCE(SUM(net_pnl), SUM(
                   CASE WHEN direction='BUY'  THEN (exit_price - entry_price)
                        WHEN direction='SELL' THEN (entry_price - exit_price)
                        ELSE 0 END)), COUNT(*)
               FROM trades
               WHERE status='CLOSED' AND close_time >= %s AND mode='PAPER'""",
            (cutoff,),
        )
        if not rows or rows[0][0] is None:
            return

        hourly_pnl_usd, trade_count = float(rows[0][0]), int(rows[0][1])
        hourly_pnl_zar = round(hourly_pnl_usd * usdzar, 2)
        today = datetime.now().date()

        self.db.execute_query(
            """INSERT INTO daily_summary (date, total_pnl, trade_count, updated_at)
               VALUES (%s, %s, %s, %s)
               ON CONFLICT (date) DO UPDATE
               SET total_pnl   = daily_summary.total_pnl + EXCLUDED.total_pnl,
                   trade_count = daily_summary.trade_count + EXCLUDED.trade_count,
                   updated_at  = EXCLUDED.updated_at""",
            (today, hourly_pnl_zar, trade_count, datetime.now()),
        )

        # Drawdown alert
        try:
            risk_cfg = self.config.get("risk_management", {})
            warn_pct = risk_cfg.get("max_drawdown_warning_pct", 12.0)
            hard_pct = risk_cfg.get("max_drawdown_hard_pct", 15.0)

            bal_rows = self.db.execute_query(
                "SELECT total_pnl FROM daily_summary WHERE date = %s", (today,)
            )
            if bal_rows:
                daily_loss_zar = float(bal_rows[0][0])
                daily_loss_pct = abs(daily_loss_zar) / balance_zar * 100
                if daily_loss_pct >= warn_pct:
                    threshold = hard_pct if daily_loss_pct >= hard_pct else warn_pct
                    data = {"current_drawdown": round(daily_loss_pct, 2), "threshold": threshold}
                    
                    if daily_loss_pct >= hard_pct:
                        self._trigger_circuit_breaker(daily_loss_pct)
                    else:
                        self.notif_bot.send_sync_message(
                            self.notif_router.format_drawdown_warning(data)
                        )
        except Exception as e:
            logger.error(f"_rollup_pnl drawdown check: {e}")

    def _trigger_circuit_breaker(self, daily_loss_pct: float):
        """
        Triggered when max_drawdown_hard_pct is reached.
        Closes all bot positions and pauses new entries.
        """
        logger.warning(f"🚨 CIRCUIT BREAKER TRIGGERED — Daily loss: {daily_loss_pct:.2f}%")
        
        try:
            # 1. Log to bot_health
            self.db.execute_query(
                "INSERT INTO bot_health (event_type, status, message, timestamp) "
                "VALUES ('CIRCUIT_BREAKER', 'PAUSED', %s, %s)",
                (f"Hard drawdown reached: {daily_loss_pct:.2f}%", datetime.now())
            )
            
            # 2. Close all bot positions
            positions = self._get_positions()
            if positions:
                closed_count = 0
                for p in positions:
                    # Filter for bot positions (magic != 0)
                    # Bridge returns dict, native returns object
                    magic = p.magic if hasattr(p, 'magic') else p.get('magic', 0)
                    ticket = p.ticket if hasattr(p, 'ticket') else p.get('ticket', 0)
                    
                    if magic != 0:
                        res, msg = self.engine.order_manager.close_position(ticket, "CIRCUIT_BREAKER")
                        if res and (hasattr(res, 'retcode') and res.retcode == mt5.TRADE_RETCODE_DONE):
                            closed_count += 1
                
                logger.info(f"Circuit Breaker: Closed {closed_count} bot positions.")
            
            # 3. Notify Telegram
            msg = (
                f"🚨 <b>CIRCUIT BREAKER TRIGGERED</b>\n"
                f"━━━━━━━━━━━━━━━\n"
                f"🛑 <b>Status:</b> BOT PAUSED\n"
                f"📉 <b>Daily Loss:</b> {daily_loss_pct:.2f}%\n"
                f"💼 <b>Action:</b> All bot positions closed.\n"
                f"━━━━━━━━━━━━━━━\n"
                f"⚠️ <i>Run /resume via Telegram to re-enable trading.</i>"
            )
            self.notif_bot.send_sync_message(msg)
            
        except Exception as e:
            logger.error(f"Error in _trigger_circuit_breaker: {e}")

    def _run_regime_detection(self):
        pairs = [
            # FX majors + crosses
            "XAUUSD", "XAGUSD", "EURUSD", "GBPUSD", "USDJPY",
            "GBPJPY", "AUDUSD", "USDCAD", "USDZAR",
            # Crypto
            "BTCUSD", "ETHUSD",
            # Commodities + Indices
            "USOIL", "US500", "USTEC",
            # Stock CFDs
            "NVDA", "AMD", "MSFT", "AAPL",
        ]
        for pair in pairs:
            try:
                self.regime_detector.run_update(pair, "H1")
            except Exception as e:
                logger.error(f"regime_detect {pair}: {e}")

    def _ingest_daily_data(self):
        try:
            from data.ingestion import run_full_ingestion
            run_full_ingestion()
        except Exception as e:
            self.notif_bot.send_sync_message(f"Daily ingest failed: {e}")

    def _check_signal_outcomes(self):
        try:
            from scheduler.signal_outcome_checker import SignalOutcomeChecker
            checker = SignalOutcomeChecker()
            checker.run(last_n_hours=24)
        except Exception as e:
            logger.error(f"SignalOutcomeChecker failed: {e}")

    # ──────────────────────────────────────────────────────────────────────────
    # Reporting
    # ──────────────────────────────────────────────────────────────────────────

    def _send_daily_summary(self):
        today = datetime.now().date()
        acct = self.config.get("account", {})
        usdzar      = float(acct.get("backtesting_usdzar_rate", 18.50))
        balance_zar = float(acct.get("backtesting_balance_zar", 180_000.0))

        rows = self.db.execute_query(
            "SELECT total_pnl, trade_count FROM daily_summary WHERE date = %s", (today,)
        )
        total_pnl_zar = float(rows[0][0] or 0) if rows else 0.0
        total_trades  = int(rows[0][1] or 0) if rows else 0

        win_rows = self.db.execute_query(
            """SELECT COUNT(*) FROM trades
               WHERE status='CLOSED' AND mode='PAPER' AND DATE(close_time)=%s
                 AND net_pnl > 0""",
            (today,),
        )
        wins = int(win_rows[0][0]) if win_rows else 0
        win_rate = round(wins / total_trades * 100, 1) if total_trades > 0 else 0.0
        max_dd_pct = round(abs(min(total_pnl_zar, 0)) / balance_zar * 100, 2)

        self.notif_bot.send_sync_message(
            self.notif_router.format_daily_summary({
                "date": str(today),
                "total_pnl": f"R {total_pnl_zar:,.2f}",
                "win_rate": win_rate,
                "total_trades": total_trades,
                "max_dd": max_dd_pct,
                "currency": "ZAR",
            })
        )

    def _send_weekly_report(self):
        week_start = datetime.now() - timedelta(days=7)
        acct = self.config.get("account", {})
        usdzar      = float(acct.get("backtesting_usdzar_rate", 18.50))
        balance_zar = float(acct.get("backtesting_balance_zar", 180_000.0))

        rows = self.db.execute_query(
            """SELECT
                 COALESCE(SUM(net_pnl), SUM(
                   CASE WHEN direction='BUY'  THEN (exit_price - entry_price)
                        WHEN direction='SELL' THEN (entry_price - exit_price)
                        ELSE 0 END)),
                 COUNT(*),
                 SUM(CASE WHEN (direction='BUY'  AND exit_price > entry_price)
                            OR (direction='SELL' AND exit_price < entry_price)
                          THEN 1 ELSE 0 END),
                 SUM(CASE WHEN (direction='BUY'  AND exit_price <= entry_price)
                            OR (direction='SELL' AND exit_price >= entry_price)
                          THEN 1 ELSE 0 END)
               FROM trades
               WHERE status='CLOSED' AND mode='PAPER' AND close_time >= %s""",
            (week_start,),
        )
        pnl_usd, total, wins, losses = (
            (float(rows[0][0]), int(rows[0][1]), int(rows[0][2]), int(rows[0][3]))
            if rows and rows[0][0] is not None
            else (0.0, 0, 0, 0)
        )
        pnl_zar = round(pnl_usd * usdzar, 2)

        strat_rows = self.db.execute_query(
            """SELECT s.name,
                 COALESCE(SUM(t.net_pnl), SUM(
                   CASE WHEN t.direction='BUY'  THEN (t.exit_price - t.entry_price)
                        WHEN t.direction='SELL' THEN (t.entry_price - t.exit_price)
                        ELSE 0 END)) * %s AS pnl_zar
               FROM trades t
               JOIN strategies s ON t.strategy_id = s.strategy_id
               WHERE t.status='CLOSED' AND t.mode='PAPER' AND t.close_time >= %s
               GROUP BY s.name
               ORDER BY pnl_zar DESC""",
            (usdzar, week_start),
        )
        max_dd_pct = round(abs(min(pnl_zar, 0)) / balance_zar * 100, 2)

        self.notif_bot.send_sync_message(
            self.notif_router.format_weekly_report({
                "week": f"{week_start.strftime('%b %d')} – {datetime.now().strftime('%b %d')}",
                "total_pnl": pnl_zar,
                "winning_trades": wins,
                "losing_trades": losses,
                "max_dd": max_dd_pct,
                "best_strategy":  strat_rows[0][0]  if strat_rows else "N/A",
                "worst_strategy": strat_rows[-1][0] if strat_rows else "N/A",
                "currency": "ZAR",
            })
        )

    # ──────────────────────────────────────────────────────────────────────────
    # Overnight backtest — NON-BLOCKING (runs in a daemon thread)
    # ──────────────────────────────────────────────────────────────────────────

    def _run_overnight_backtest(self):
        """
        Launch the overnight backtest in a background daemon thread so the
        APScheduler thread-pool is not blocked for up to 60 minutes.
        A guard prevents a second launch if the previous run is still active.
        """
        if self._backtest_thread and self._backtest_thread.is_alive():
            logger.warning("Overnight backtest still running — skipping this trigger.")
            self.notif_bot.send_sync_message(
                "⏭ <b>Overnight Backtest Skipped</b>\nPrevious run still in progress."
            )
            return
        self._backtest_thread = threading.Thread(
            target=self._backtest_worker, daemon=True, name="overnight-backtest"
        )
        self._backtest_thread.start()

    def _backtest_worker(self):
        """Worker executed in a background thread — safe to block here."""
        script = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "scripts", "run_overnight_backtest.py",
        )
        if not os.path.exists(script):
            self.notif_bot.send_sync_message("⚠️ Overnight backtest script not found.")
            return

        self.notif_bot.send_sync_message(
            "🌙 <b>Overnight Backtest Started</b>\n"
            "Running full Tier 1 & 2 strategy suite…\n"
            "<i>Results will be posted when complete (~30 min)</i>"
        )
        try:
            result = subprocess.run(
                [sys.executable, script],
                capture_output=True, text=True, timeout=3600,
            )
            if result.returncode != 0:
                self.notif_bot.send_sync_message(
                    f"❌ <b>Overnight Backtest Failed</b>\n"
                    f"<pre>{result.stderr[-500:]}</pre>"
                )
            else:
                logger.info("Overnight backtest completed successfully.")
                self._run_recommendations()
        except subprocess.TimeoutExpired:
            self.notif_bot.send_sync_message(
                "⏱ Overnight backtest timed out (>60 min)."
            )
        except Exception as e:
            logger.error(f"_backtest_worker: {e}")
            self.notif_bot.send_sync_message(f"❌ Overnight backtest error: {e}")

    def _run_wfo_suite(self):
        """
        Launch the bi-weekly WFO suite in a background daemon thread so the
        APScheduler thread-pool is not blocked for up to 90 minutes.
        A guard prevents a second launch if the previous run is still active.
        Scheduled: Wednesday and Sunday at 03:00 UTC.
        """
        if hasattr(self, '_wfo_thread') and self._wfo_thread and self._wfo_thread.is_alive():
            logger.warning("WFO suite still running -- skipping this trigger.")
            self.notif_bot.send_sync_message(
                "WFO Suite Skipped -- Previous run still in progress."
            )
            return
        self._wfo_thread = threading.Thread(
            target=self._wfo_worker, daemon=True, name="wfo-suite"
        )
        self._wfo_thread.start()

    def _wfo_worker(self):
        """Worker executed in a background thread -- safe to block for up to 90 min."""
        script = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "scripts", "run_wfo_all.py",
        )
        if not os.path.exists(script):
            self.notif_bot.send_sync_message("WFO script not found: scripts/run_wfo_all.py")
            return

        self.notif_bot.send_sync_message(
            "WFO Suite Started -- Running walk-forward optimisation for all enabled strategies. 3 windows | IS=70% | OOS=20% | ~30-90 min"
        )
        try:
            result = subprocess.run(
                [sys.executable, script,
                 "--n_windows", "3",
                 "--is_pct", "0.70",
                 "--oos_pct", "0.20"],
                capture_output=True, text=True, timeout=5400,
            )
            if result.returncode != 0:
                self.notif_bot.send_sync_message(
                    "WFO Suite Failed: " + result.stderr[-500:]
                )
            else:
                logger.info("WFO suite completed successfully.")
                summary_path = os.path.join(
                    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "results", "wfo_master_summary.md",
                )
                pass_count = fail_count = error_count = 0
                if os.path.exists(summary_path):
                    with open(summary_path) as sf:
                        for line in sf:
                            if "| PASS |" in line:
                                pass_count += 1
                            elif "| FAIL |" in line:
                                fail_count += 1
                            elif "| ERROR |" in line:
                                error_count += 1
                self.notif_bot.send_sync_message(
                    "WFO Suite Complete -- PASS: " + str(pass_count) +
                    " | FAIL: " + str(fail_count) +
                    " | ERROR: " + str(error_count) +
                    " -- Full report: results/wfo_master_summary.md"
                )
        except subprocess.TimeoutExpired:
            self.notif_bot.send_sync_message(
                "WFO suite timed out (>90 min) -- partial results may exist."
            )
        except Exception as e:
            logger.error("_wfo_worker: " + str(e))
            self.notif_bot.send_sync_message("WFO suite error: " + str(e))

    def _run_recommendations(self):
        """Run the recommendation engine after a successful overnight backtest."""
        try:
            from scheduler.recommendations import RecommendationEngine
            engine = RecommendationEngine(
                results_dir=os.path.join(
                    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "results",
                ),
                notif_bot=self.notif_bot,
            )
            engine.run()
        except Exception as e:
            logger.error(f"RecommendationEngine failed: {e}")
            self.notif_bot.send_sync_message(
                f"⚠️ <b>Recommendations engine error:</b> {e}"
            )
    def _refresh_cot_data(self):
        try:
            from data.cot_feed import COTFeed
            feed = COTFeed()
            results = feed.fetch_latest()
            total = sum(results.values())
            pairs_ok   = [p for p, n in results.items() if n > 0]
            pairs_fail = [p for p, n in results.items() if n == 0]
            msg = (
                f"📊 <b>COT Data Updated</b>\n"
                f"Rows upserted: <b>{total}</b>\n"
                f"✅ {', '.join(pairs_ok) or 'None'}\n"
            )
            if pairs_fail:
                msg += f"⚠️ Failed: {', '.join(pairs_fail)}"
            self.notif_bot.send_sync_message(msg)
        except Exception as e:
            self.notif_bot.send_sync_message(f"❌ COT refresh failed: {e}")

    def _run_yahoo_history_fill(self):
        script = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "scripts", "pull_yahoo_history.py",
        )
        if not os.path.exists(script):
            self.notif_bot.send_sync_message(
                "⚠️ Yahoo history fill script not found: scripts/pull_yahoo_history.py"
            )
            return

        self.notif_bot.send_sync_message(
            "📈 Yahoo History Fill Started — topping up CFD history for "
            "NVDA / AMD / MSFT / AAPL / US500 / USTEC / USOIL"
        )
        try:
            result = subprocess.run(
                [sys.executable, script, "--d1-years", "10"],
                capture_output=True, text=True, timeout=600,
            )
            if result.returncode != 0:
                self.notif_bot.send_sync_message(
                    "⚠️ Yahoo history fill error: " + result.stderr[-400:]
                )
            else:
                total_line = next(
                    (line for line in result.stdout.splitlines() if "Total bars" in line),
                    "N/A"
                )
                self.notif_bot.send_sync_message(f"✅ Yahoo history fill complete: {total_line}")
        except Exception as e:
            logger.error(f"_run_yahoo_history_fill: {e}")

    def _run_weekly_archive(self):
        script = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "scripts", "weekly_archive.py",
        )
        try:
            result = subprocess.run([sys.executable, script], capture_output=True, text=True)
            if result.returncode == 0:
                logger.info("Weekly archival completed.")
                self.notif_bot.send_sync_message("📁 <b>Weekly Archival Complete</b>\nStrategy intelligence moved to long-term storage.")
            else:
                logger.error(f"Weekly archival failed: {result.stderr}")
        except Exception as e:
            logger.error(f"Error in _run_weekly_archive: {e}")

    def _db_cleanup(self):
        cutoff90 = datetime.now() - timedelta(days=90)
        cutoff30 = datetime.now() - timedelta(days=30)
        self.db.execute_query("DELETE FROM regime_log WHERE timestamp < %s", (cutoff90,))
        self.db.execute_query("DELETE FROM bot_health WHERE timestamp < %s",  (cutoff30,))
        logger.info("db_cleanup complete.")

    def _strategy_correlation_check(self):
        import pandas as pd

        month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        rows = self.db.execute_query(
            """SELECT s.name, DATE_TRUNC('day', t.close_time),
                      SUM(t.exit_price - t.entry_price)
               FROM trades t
               JOIN strategies s ON t.strategy_id = s.strategy_id
               WHERE t.status='CLOSED' AND t.mode='PAPER' AND t.close_time >= %s
               GROUP BY s.name, 2
               ORDER BY 2""",
            (month_start,),
        )
        if not rows or len(rows) < 5:
            return

        df = pd.DataFrame(rows, columns=["strategy", "day", "pnl"])
        pivot = df.pivot_table(
            index="day", columns="strategy", values="pnl", aggfunc="sum"
        ).fillna(0)
        if pivot.shape[1] < 2:
            return

        corr = pivot.corr()
        strategies = corr.columns.tolist()
        high = [
            (strategies[i], strategies[j], round(corr.loc[strategies[i], strategies[j]], 2))
            for i in range(len(strategies))
            for j in range(i + 1, len(strategies))
            if abs(corr.loc[strategies[i], strategies[j]]) > 0.85
        ]
        if high:
            msg = "📈 <b>Strategy Correlation Alert</b> (>0.85):\n" + "\n".join(
                f"  {a} vs {b}: {c}" for a, b, c in high
            )
            self.notif_bot.send_sync_message(msg)

    def _sync_mt5_history(self):
        """Runs the account history sync script every 4 hours."""
        script = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "scripts", "sync_mt5_account.py",
        )
        if not os.path.exists(script):
            logger.error(f"Sync script not found at {script}")
            return

        logger.info("Starting 4-hour account history sync...")
        try:
            result = subprocess.run(
                [sys.executable, script],
                capture_output=True, text=True, timeout=300
            )
            if result.returncode != 0:
                logger.error(f"4-hour sync failed: {result.stderr}")
            else:
                logger.info("4-hour account history sync completed.")
        except Exception as e:
            logger.error(f"Error in _sync_mt5_history: {e}")


# ──────────────────────────────────────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import time

    scheduler = TradingScheduler()
    scheduler.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        scheduler.stop()
