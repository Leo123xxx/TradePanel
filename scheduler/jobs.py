from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime, timedelta
import yaml
import MetaTrader5 as mt5
import subprocess
import os
import sys

from forward_test.paper_engine import PaperEngine
from risk.regime_detector import RegimeDetector
from logging_.health_monitor import HealthMonitor
from notifications.telegram_bot import TelegramBot
from notifications.router import CommandRouter
from data.db_client import DBClient


class TradingScheduler:
    def __init__(self, config_path="config/config.yaml"):
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
        self.dashboard_started = False
        self.last_trade_check = datetime.now()
        self.hb_interval_mins = 5 # Send report every 5 mins

    def start(self):
        """Register all 11 jobs and start the scheduler."""

        self.scheduler.add_job(
            self._heartbeat_wrapper,
            IntervalTrigger(seconds=60),
            id="heartbeat",
            name="Heartbeat Monitor",
        )
        self.scheduler.add_job(
            self._check_mt5_connection,
            IntervalTrigger(seconds=60),
            id="mt5_conn",
            name="MT5 Connection Watcher",
        )
        self.scheduler.add_job(
            self._sync_positions,
            IntervalTrigger(minutes=5),
            id="position_sync",
            name="Position Sync MT5 to DB",
        )
        self.scheduler.add_job(
            self.engine.run_detect,
            IntervalTrigger(minutes=1),
            id="signal_detect",
            name="Signal Detection (1m)",
        )
        self.scheduler.add_job(
            self.engine.run_execute,
            IntervalTrigger(minutes=5),
            id="trade_execute",
            name="Trade Execution (5m)",
        )
        self.scheduler.add_job(
            self._rollup_pnl,
            IntervalTrigger(hours=1),
            id="pnl_rollup",
            name="Hourly PnL Roll-Up",
        )
        self.scheduler.add_job(
            self._run_regime_detection,
            IntervalTrigger(hours=1),
            id="regime_detect",
            name="Market Regime Detector",
        )
        self.scheduler.add_job(
            self._ingest_daily_data,
            CronTrigger(hour=0, minute=5),
            id="daily_ingest",
            name="Daily M1 Data Ingest",
        )
        summary_time = (
            self.config.get("notifications", {})
            .get("daily_summary_time", "18:00")
            .split(":")
        )
        self.scheduler.add_job(
            self._send_daily_summary,
            CronTrigger(hour=int(summary_time[0]), minute=int(summary_time[1])),
            id="daily_summary",
            name="Daily Performance Summary",
        )
        self.scheduler.add_job(
            self._send_weekly_report,
            CronTrigger(day_of_week="mon", hour=8, minute=0),
            id="weekly_report",
            name="Weekly Performance Report",
        )
        self.scheduler.add_job(
            self._db_cleanup,
            CronTrigger(day_of_week="sun", hour=0, minute=30),
            id="db_cleanup",
            name="Weekly DB Cleanup",
        )
        self.scheduler.add_job(
            self._strategy_correlation_check,
            CronTrigger(day=1, hour=9, minute=0),
            id="correlation_check",
            name="Monthly Strategy Correlation Check",
        )

        self.scheduler.start()
        n = len(self.scheduler.get_jobs())
        print(f"[{datetime.now()}] APScheduler started with {n}/12 jobs.")

    def stop(self):
        self.scheduler.shutdown()
        if hasattr(self, "dashboard_process") and self.dashboard_process:
            self.dashboard_process.terminate()

    def _heartbeat_wrapper(self):
        """Wrapper to track heartbeats, send Telegram updates, and launch dashboard."""
        self.health_monitor.logger.heartbeat()
        self.heartbeat_count += 1
        
        # Check for trade activity since last check
        activity = self._get_recent_activity()
        
        # Send Telegram update if activity found or on 5-min interval
        is_interval = (self.heartbeat_count % self.hb_interval_mins == 0)
        
        if activity or is_interval:
            self._send_telegram_heartbeat(activity)
            self.last_trade_check = datetime.now()

        # Note: Dashboard is now started by the TelegramBot class for immediate availability
        # if self.heartbeat_count >= 3 and not self.dashboard_started:
        #     self._launch_dashboard()

    def _get_recent_activity(self) -> str:
        """Fetch trades opened or closed since last_trade_check."""
        try:
            # New Trades (using correct column names: pair, open_time)
            new_rows = self.db.execute_query(
                "SELECT pair, direction, strategy_id FROM trades WHERE open_time > %s AND mode = 'PAPER'",
                (self.last_trade_check,)
            )
            # Closed Trades (using correct column names: pair, close_time)
            closed_rows = self.db.execute_query(
                "SELECT pair, exit_price - entry_price, close_reason FROM trades WHERE close_time > %s AND mode = 'PAPER'",
                (self.last_trade_check,)
            )
            
            lines = []
            if new_rows:
                for sym, dir, s_id in new_rows:
                    lines.append(f"🆕 <b>OPEN:</b> {sym} {dir}")
            if closed_rows:
                for sym, pnl, reason in closed_rows:
                    icon = "💰" if pnl >= 0 else "📉"
                    lines.append(f"{icon} <b>CLOSE:</b> {sym} ({pnl:+.2f}) - {reason}")
            
            return "\n".join(lines)
        except Exception as e:
            # Don't return the error as activity to avoid spamming
            print(f"Error checking activity: {e}")
            return ""

    def _send_telegram_heartbeat(self, activity: str = ""):
        """Sends a structured heartbeat report to Telegram."""
        try:
            # Get MT5 Info
            mt5_status = "🟢 CONNECTED" if self.engine.connector.connect() else "🔴 DISCONNECTED"
            
            # Get Active Positions
            positions = mt5.positions_get()
            pos_count = len(positions) if positions else 0
            
            msg = f"💓 <b>SYSTEM HEARTBEAT</b>\n"
            msg += f"━━━━━━━━━━━━━━━\n"
            msg += f"🖥 <b>MT5:</b> {mt5_status}\n"
            msg += f"📊 <b>Active Positions:</b> {pos_count}\n"
            
            if activity:
                msg += f"\n⚡ <b>RECENT ACTIVITY:</b>\n{activity}\n"
            
            msg += f"━━━━━━━━━━━━━━━\n"
            msg += f"🕒 <i>Next report in {self.hb_interval_mins}m</i>"
            
            self.notif_bot.send_sync_message(msg)
        except Exception as e:
            print(f"Failed to send heartbeat: {e}")

    def _launch_dashboard(self):
        """Launches the FastAPI dashboard in its own process."""
        try:
            print(f"[{datetime.now()}] 3 Heartbeats confirmed. Launching Web Dashboard...")
            
            # Start dashboard.py as a subprocess
            cmd = [sys.executable, "dashboard.py", "--port", "5000"]
            self.dashboard_process = subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                shell=False
            )
            
            self.dashboard_started = True
            msg = "📊 <b>SYSTEM READY:</b> 3 Heartbeats confirmed.\n🚀 <b>Dashboard Live:</b> http://localhost:5000"
            self.notif_bot.send_sync_message(msg)
            
        except Exception as e:
            print(f"Failed to launch dashboard: {e}")
            self.notif_bot.send_sync_message(f"❌ <b>Dashboard Startup Failed:</b> {e}")

    def _check_mt5_connection(self):
        """Checks MT5 connection and sends template-formatted alert on failure."""
        if not self.engine.connector.connect():
            msg = self.health_monitor.check_mt5_connection()
            if msg:
                self.notif_bot.send_sync_message(msg)

    def _sync_positions(self):
        if not self.engine.connector.connect():
            return
        live_tickets = set()
        positions = mt5.positions_get()
        if positions:
            live_tickets = {p.ticket for p in positions}
        rows = self.db.execute_query(
            "SELECT mt5_ticket, trade_id FROM trades WHERE status = 'OPENED' AND mode = 'PAPER'"
        )
        if rows:
            for mt5_ticket, trade_id in rows:
                if mt5_ticket not in live_tickets:
                    history = mt5.history_deals_get(ticket=mt5_ticket)
                    exit_price = history[-1].price if history else 0.0
                    self.db.execute_query(
                        "UPDATE trades SET status='CLOSED', close_reason='EXTERNAL_CLOSE', close_time=%s, exit_price=%s WHERE trade_id=%s",
                        (datetime.now(), exit_price, trade_id),
                    )
        # Connector stays connected for next job

    def _rollup_pnl(self):
        cutoff = datetime.now() - timedelta(hours=1)
        rows = self.db.execute_query(
            "SELECT SUM(exit_price - entry_price), COUNT(*) FROM trades WHERE status='CLOSED' AND close_time >= %s AND mode='PAPER'",
            (cutoff,),
        )
        if not rows or rows[0][0] is None:
            return
        hourly_pnl, trade_count = rows[0]
        today = datetime.now().date()
        self.db.execute_query(
            "INSERT INTO daily_summary (date, total_pnl, trade_count, updated_at) VALUES (%s, %s, %s, %s) ON CONFLICT (date) DO UPDATE SET total_pnl = daily_summary.total_pnl + EXCLUDED.total_pnl, trade_count = daily_summary.trade_count + EXCLUDED.trade_count, updated_at = EXCLUDED.updated_at",
            (today, float(hourly_pnl), trade_count, datetime.now()),
        )

        # Drawdown alert check
        try:
            warn_pct  = self.config.get("risk_management", {}).get("max_drawdown_warning_pct", 12.0)
            hard_pct  = self.config.get("risk_management", {}).get("max_drawdown_hard_pct", 15.0)
            bal_rows  = self.db.execute_query(
                "SELECT total_pnl FROM daily_summary WHERE date = %s", (today,)
            )
            if bal_rows:
                daily_loss_pct = abs(float(bal_rows[0][0])) / 10000.0 * 100  # assume $10k base
                threshold = hard_pct if daily_loss_pct >= hard_pct else warn_pct
                if daily_loss_pct >= warn_pct:
                    data = {"current_drawdown": round(daily_loss_pct, 2), "threshold": threshold}
                    self.notif_bot.send_sync_message(self.notif_router.format_drawdown_warning(data))
        except Exception as e:
            print(f"[{datetime.now()}] drawdown_check error: {e}")

    def _run_regime_detection(self):
        pairs = ["XAUUSD", "EURUSD", "GBPUSD", "USDJPY", "XAGUSD", "BTCUSD", "ETHUSD"]
        for pair in pairs:
            try:
                self.regime_detector.run_update(pair, "H1")
            except Exception as e:
                print(f"[{datetime.now()}] regime_detect: {pair} failed: {e}")

    def _ingest_daily_data(self):
        try:
            from data.ingestion import run_full_ingestion
            run_full_ingestion()
        except Exception as e:
            self.notif_bot.send_sync_message(f"Daily ingest failed: {e}")

    def _send_daily_summary(self):
        today = datetime.now().date()
        rows = self.db.execute_query(
            "SELECT total_pnl, trade_count FROM daily_summary WHERE date = %s", (today,)
        )
        total_pnl = float(rows[0][0] or 0) if rows else 0.0
        total_trades = int(rows[0][1] or 0) if rows else 0
        win_rows = self.db.execute_query(
            "SELECT COUNT(*) FROM trades WHERE status='CLOSED' AND mode='PAPER' AND DATE(close_time)=%s AND exit_price > entry_price",
            (today,),
        )
        wins = int(win_rows[0][0]) if win_rows else 0
        currency = "USD"
        if self.engine.connector.connect():
            info = mt5.account_info()
            if info:
                currency = info.currency
        
        stats = {"date": str(today), "total_pnl": round(total_pnl, 2),
                 "win_rate": round(win_rate, 1), "total_trades": total_trades,
                 "max_dd": 0, "currency": currency}
        self.notif_bot.send_sync_message(self.notif_router.format_daily_summary(stats))

    def _send_weekly_report(self):
        week_start = datetime.now() - timedelta(days=7)
        rows = self.db.execute_query(
            "SELECT SUM(exit_price-entry_price), COUNT(*), SUM(CASE WHEN exit_price>entry_price THEN 1 ELSE 0 END), SUM(CASE WHEN exit_price<=entry_price THEN 1 ELSE 0 END) FROM trades WHERE status='CLOSED' AND mode='PAPER' AND close_time>=%s",
            (week_start,),
        )
        if rows and rows[0][0] is not None:
            pnl, total, wins, losses = float(rows[0][0]), int(rows[0][1]), int(rows[0][2]), int(rows[0][3])
        else:
            pnl, total, wins, losses = 0.0, 0, 0, 0
        strat_rows = self.db.execute_query(
            "SELECT s.name, SUM(t.exit_price-t.entry_price) FROM trades t JOIN strategies s ON t.strategy_id=s.strategy_id WHERE t.status='CLOSED' AND t.mode='PAPER' AND t.close_time>=%s GROUP BY s.name ORDER BY 2 DESC",
            (week_start,),
        )
        currency = "USD"
        if self.engine.connector.connect():
            info = mt5.account_info()
            if info:
                currency = info.currency

        stats = {
            "week": f"{week_start.strftime('%b %d')} - {datetime.now().strftime('%b %d')}",
            "total_pnl": pnl, "winning_trades": wins, "losing_trades": losses,
            "max_dd": 0, "best_strategy": strat_rows[0][0] if strat_rows else "N/A",
            "worst_strategy": strat_rows[-1][0] if strat_rows else "N/A", "currency": currency,
        }
        self.notif_bot.send_sync_message(self.notif_router.format_weekly_report(stats))

    def _db_cleanup(self):
        cutoff90 = datetime.now() - timedelta(days=90)
        cutoff30 = datetime.now() - timedelta(days=30)
        self.db.execute_query("DELETE FROM regime_log WHERE timestamp < %s", (cutoff90,))
        self.db.execute_query("DELETE FROM bot_health WHERE timestamp < %s", (cutoff30,))
        print(f"[{datetime.now()}] db_cleanup done.")

    def _strategy_correlation_check(self):
        import pandas as pd
        month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0)
        rows = self.db.execute_query(
            "SELECT s.name, DATE_TRUNC('day', t.close_time), SUM(t.exit_price-t.entry_price) FROM trades t JOIN strategies s ON t.strategy_id=s.strategy_id WHERE t.status='CLOSED' AND t.mode='PAPER' AND t.close_time>=%s GROUP BY s.name, 2 ORDER BY 2",
            (month_start,),
        )
        if not rows or len(rows) < 5:
            return
        df = pd.DataFrame(rows, columns=["strategy", "day", "pnl"])
        pivot = df.pivot_table(index="day", columns="strategy", values="pnl", aggfunc="sum").fillna(0)
        if pivot.shape[1] < 2:
            return
        corr = pivot.corr()
        strategies = corr.columns.tolist()
        high = [(strategies[i], strategies[j], round(corr.loc[strategies[i], strategies[j]], 2))
                for i in range(len(strategies)) for j in range(i+1, len(strategies))
                if abs(corr.loc[strategies[i], strategies[j]]) > 0.85]
        if high:
            msg = "Strategy Correlation Alert (>0.85):\n" + "\n".join(f"  {a} vs {b}: {c}" for a, b, c in high)
            self.notif_bot.send_sync_message(msg)
