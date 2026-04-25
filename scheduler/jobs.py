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
        self.last_pos_count = None
        self.hb_interval_mins = self.config.get("scheduler", {}).get("telegram_heartbeat_interval_mins", 60) # Send report every X mins

    def start(self):
        """Register all 11 jobs and start the scheduler."""

        self.scheduler.add_job(
            self._heartbeat_wrapper,
            IntervalTrigger(seconds=self.config.get("scheduler", {}).get("heartbeat_interval_sec", 60)),
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
        # Data ingest runs 4× daily (00:05, 06:05, 12:05, 18:05 UTC)
        # Ensures the DB always has fresh bars for backtests and live signals
        ingest_hours = self.config.get("scheduler", {}).get("data_ingest_hours", "0,6,12,18")
        ingest_min   = self.config.get("scheduler", {}).get("data_ingest_minute", 5)
        self.scheduler.add_job(
            self._ingest_daily_data,
            CronTrigger(hour=ingest_hours, minute=ingest_min),
            id="data_ingest_6h",
            name="6-Hour Market Data Ingest",
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
        # Overnight backtest: runs at 02:00 UTC Mon–Fri after the 00:05 ingest
        bt_hour = self.config.get("scheduler", {}).get("overnight_backtest_hour", 2)
        bt_min  = self.config.get("scheduler", {}).get("overnight_backtest_minute", 0)
        self.scheduler.add_job(
            self._run_overnight_backtest,
            CronTrigger(day_of_week="mon-fri", hour=bt_hour, minute=bt_min),
            id="overnight_backtest",
            name="Overnight Strategy Backtest",
        )
        # COT data refresh — every Friday at 21:00 UTC (after CFTC release ~20:30 UTC)
        self.scheduler.add_job(
            self._refresh_cot_data,
            CronTrigger(day_of_week="fri", hour=21, minute=0),
            id="cot_refresh",
            name="CFTC COT Weekly Refresh",
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
        print(f"[{datetime.now()}] APScheduler started with {n}/14 jobs.")

    def stop(self):
        self.scheduler.shutdown()
        if hasattr(self, "dashboard_process") and self.dashboard_process:
            self.dashboard_process.terminate()

    def _heartbeat_wrapper(self):
        """Wrapper to track heartbeats, send Telegram updates, and launch dashboard."""
        self.health_monitor.logger.heartbeat()
        self.heartbeat_count += 1
        
        # Get current positions from MT5
        current_positions = mt5.positions_get()
        current_count = len(current_positions) if current_positions else 0
        
        # Detect manual position changes
        pos_changed = False
        if self.last_pos_count is not None and current_count != self.last_pos_count:
            pos_changed = True
        
        self.last_pos_count = current_count
        
        # Check for trade activity since last check
        activity = self._get_recent_activity()
        
        # Send Telegram update if activity found or on interval or if position count changed
        is_interval = (self.heartbeat_count % self.hb_interval_mins == 0)
        
        if activity or is_interval or pos_changed:
            self._send_telegram_heartbeat(activity, external_change=pos_changed)
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

    def _send_telegram_heartbeat(self, activity: str = "", external_change: bool = False):
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
            elif external_change:
                msg += f"\n⚠️ <b>EXTERNAL CHANGE:</b>\nManual position update detected.\n"
            
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
        """Checks MT5 connection and retries with backoff before alerting."""
        if not self.engine.connector.connected:
            # Use retry logic — alerts Telegram only if all 3 attempts fail
            self.engine.connector.connect_with_retry(
                max_attempts=3,
                delays=[5, 15, 30],
                notify_fn=self.notif_bot.send_sync_message
            )

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
        # ZAR account config — used for both P&L conversion and drawdown %
        acct        = self.config.get("account", {})
        usdzar      = float(acct.get("backtesting_usdzar_rate", 18.50))
        balance_zar = float(acct.get("backtesting_balance_zar", 180000.0))

        cutoff = datetime.now() - timedelta(hours=1)
        # Use net_pnl (USD, populated by backtest engine) where available;
        # fall back to raw price-diff for legacy paper trades missing net_pnl.
        rows = self.db.execute_query(
            """SELECT COALESCE(SUM(net_pnl), SUM(
                   CASE WHEN direction='BUY'  THEN (exit_price - entry_price)
                        WHEN direction='SELL' THEN (entry_price - exit_price)
                        ELSE 0 END
               )), COUNT(*)
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

        # Drawdown alert — daily_summary.total_pnl is now in ZAR
        try:
            warn_pct = self.config.get("risk_management", {}).get("max_drawdown_warning_pct", 12.0)
            hard_pct = self.config.get("risk_management", {}).get("max_drawdown_hard_pct", 15.0)
            bal_rows = self.db.execute_query(
                "SELECT total_pnl FROM daily_summary WHERE date = %s", (today,)
            )
            if bal_rows:
                daily_loss_zar  = float(bal_rows[0][0])
                daily_loss_pct  = abs(daily_loss_zar) / balance_zar * 100
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
        acct        = self.config.get("account", {})
        usdzar      = float(acct.get("backtesting_usdzar_rate", 18.50))
        balance_zar = float(acct.get("backtesting_balance_zar", 180000.0))

        rows = self.db.execute_query(
            "SELECT total_pnl, trade_count FROM daily_summary WHERE date = %s", (today,)
        )
        # total_pnl stored in ZAR (after _rollup_pnl fix)
        total_pnl_zar = float(rows[0][0] or 0) if rows else 0.0
        total_trades  = int(rows[0][1] or 0) if rows else 0

        # Direction-aware win count: BUY wins when exit > entry, SELL wins when exit < entry
        win_rows = self.db.execute_query(
            """SELECT COUNT(*) FROM trades
               WHERE status='CLOSED' AND mode='PAPER' AND DATE(close_time)=%s
               AND ((direction='BUY'  AND exit_price > entry_price)
                 OR (direction='SELL' AND exit_price < entry_price))""",
            (today,),
        )
        wins = int(win_rows[0][0]) if win_rows else 0

        # Max drawdown for the day vs ZAR balance
        max_dd_pct = round(abs(min(total_pnl_zar, 0)) / balance_zar * 100, 2)

        win_rate = round(wins / total_trades * 100, 1) if total_trades > 0 else 0.0
        stats = {
            "date":         str(today),
            "total_pnl":   f"R {total_pnl_zar:,.2f}",
            "win_rate":    win_rate,
            "total_trades": total_trades,
            "max_dd":      max_dd_pct,
            "currency":    "ZAR",
        }
        self.notif_bot.send_sync_message(self.notif_router.format_daily_summary(stats))

    def _send_weekly_report(self):
        week_start  = datetime.now() - timedelta(days=7)
        acct        = self.config.get("account", {})
        usdzar      = float(acct.get("backtesting_usdzar_rate", 18.50))
        balance_zar = float(acct.get("backtesting_balance_zar", 180000.0))

        rows = self.db.execute_query(
            """SELECT
                 COALESCE(SUM(net_pnl), SUM(
                   CASE WHEN direction='BUY'  THEN (exit_price - entry_price)
                        WHEN direction='SELL' THEN (entry_price - exit_price)
                        ELSE 0 END
                 )),
                 COUNT(*),
                 SUM(CASE WHEN (direction='BUY'  AND exit_price > entry_price)
                            OR (direction='SELL' AND exit_price < entry_price)
                          THEN 1 ELSE 0 END),
                 SUM(CASE WHEN (direction='BUY'  AND exit_price <= entry_price)
                            OR (direction='SELL' AND exit_price >= entry_price)
                          THEN 1 ELSE 0 END)
               FROM trades
               WHERE status='CLOSED' AND mode='PAPER' AND close_time>=%s""",
            (week_start,),
        )
        if rows and rows[0][0] is not None:
            pnl_usd, total, wins, losses = float(rows[0][0]), int(rows[0][1]), int(rows[0][2]), int(rows[0][3])
        else:
            pnl_usd, total, wins, losses = 0.0, 0, 0, 0
        pnl_zar = round(pnl_usd * usdzar, 2)

        strat_rows = self.db.execute_query(
            """SELECT s.name,
                 COALESCE(SUM(t.net_pnl), SUM(
                   CASE WHEN t.direction='BUY'  THEN (t.exit_price - t.entry_price)
                        WHEN t.direction='SELL' THEN (t.entry_price - t.exit_price)
                        ELSE 0 END
                 )) * %s AS pnl_zar
               FROM trades t
               JOIN strategies s ON t.strategy_id = s.strategy_id
               WHERE t.status='CLOSED' AND t.mode='PAPER' AND t.close_time>=%s
               GROUP BY s.name
               ORDER BY pnl_zar DESC""",
            (usdzar, week_start),
        )

        # Weekly max drawdown
        max_dd_pct = round(abs(min(pnl_zar, 0)) / balance_zar * 100, 2)

        stats = {
            "week":           f"{week_start.strftime('%b %d')} - {datetime.now().strftime('%b %d')}",
            "total_pnl":     pnl_zar,
            "winning_trades": wins,
            "losing_trades":  losses,
            "max_dd":         max_dd_pct,
            "best_strategy":  strat_rows[0][0]  if strat_rows else "N/A",
            "worst_strategy": strat_rows[-1][0] if strat_rows else "N/A",
            "currency":       "ZAR",
        }
        self.notif_bot.send_sync_message(self.notif_router.format_weekly_report(stats))

    def _db_cleanup(self):
        cutoff90 = datetime.now() - timedelta(days=90)
        cutoff30 = datetime.now() - timedelta(days=30)
        self.db.execute_query("DELETE FROM regime_log WHERE timestamp < %s", (cutoff90,))
        self.db.execute_query("DELETE FROM bot_health WHERE timestamp < %s", (cutoff30,))
        print(f"[{datetime.now()}] db_cleanup done.")

    def _run_overnight_backtest(self):
        """Run full backtest on all Tier 1 & 2 strategies and send Telegram report."""
        try:
            import subprocess, sys
            script = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                  "scripts", "run_overnight_backtest.py")
            if not os.path.exists(script):
                self.notif_bot.send_sync_message("⚠️ Overnight backtest script not found.")
                return
            self.notif_bot.send_sync_message(
                "\U0001f319 <b>Overnight Backtest Started</b>\n"
                "Running full Tier 1 & 2 strategy suite\u2026\n"
                "<i>Results will be posted when complete (~30 min)</i>"
            )
            result = subprocess.run(
                [sys.executable, script],
                capture_output=True, text=True, timeout=3600
            )
            if result.returncode != 0:
                self.notif_bot.send_sync_message(
                    f"\u274c <b>Overnight Backtest Failed</b>\n"
                    f"<pre>{result.stderr[-500:]}</pre>"
                )
        except subprocess.TimeoutExpired:
            self.notif_bot.send_sync_message("⏱ Overnight backtest timed out (>60 min).")
        except Exception as e:
            self.notif_bot.send_sync_message(f"❌ Overnight backtest error: {e}")

    def _refresh_cot_data(self):
        """Fetch latest CFTC COT data and update the cot_data table."""
        try:
            from data.cot_feed import COTFeed
            feed = COTFeed()
            results = feed.fetch_latest()
            total = sum(results.values())
            pairs_ok = [p for p, n in results.items() if n > 0]
            pairs_fail = [p for p, n in results.items() if n == 0]
            msg = (
                f"\U0001f4ca <b>COT Data Updated</b>\n"
                f"Rows upserted: <b>{total}</b>\n"
                f"\u2705 {', '.join(pairs_ok) if pairs_ok else 'None'}\n"
            )
            if pairs_fail:
                msg += f"\u26a0\ufe0f Failed: {', '.join(pairs_fail)}"
            self.notif_bot.send_sync_message(msg)
        except Exception as e:
            self.notif_bot.send_sync_message(f"\u274c COT refresh failed: {e}")

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
