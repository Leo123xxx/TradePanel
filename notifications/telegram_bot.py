"""
notifications/telegram_bot.py
==============================
TradePanel Telegram Bot — inbound command handler + outbound push notifications.

Commands:
  /start /help       — help menu
  /status            — account + open positions
  /balance           — balance, equity, margin
  /active            — open positions with TP/SL
  /risk              — drawdown, margin, daily P&L
  /signals           — latest 24h strategy signals
  /analysis          — multi-TF market regime summary
  /mode              — active strategies (reads enabled: flag)
  /wfo               — WFO master summary (pass/fail per strategy)
  /demotion          — demotion tracker (strategies at risk)
  /data              — data coverage (latest bar per pair)
  /enable <name>     — enable a strategy in strategies.yaml
  /disable <name>    — disable a strategy in strategies.yaml
  /backtest_report   — last overnight backtest summary
  /best_pairs        — top pairs by win rate
  /top_strategies    — top 5 strategies by Sharpe
  /backtest_status   — when last backtest ran
  /params            — parameter tweak suggestions
  /health            — system health + heartbeat
  /dashboard         — link to web dashboard

Push notifications (automatic):
  08:00 daily        — morning brief (account + backtest status)
  On demotion event  — strategy demotion alert
  On trade open/close — via send_sync_message() from engine
"""

import os
import sys
import asyncio
import logging
from datetime import datetime, time as dtime
from functools import wraps

try:
    import MetaTrader5 as mt5
except ImportError:
    from mt5_bridge.docker_mock import setup_mock
    setup_mock()

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.constants import ParseMode
from dotenv import load_dotenv
from notifications import templates
from notifications.router import CommandRouter
import subprocess

logger = logging.getLogger(__name__)


# ── Auth decorator ────────────────────────────────────────────────────────────

def auth_required(func):
    @wraps(func)
    async def wrapper(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = str(update.effective_chat.id)
        allowed = os.getenv("ALLOWED_CHAT_IDS", "").split(",")
        primary = os.getenv("TELEGRAM_CHAT_ID")
        if primary:
            allowed.append(primary)
        if chat_id not in [a.strip() for a in allowed if a.strip()]:
            logger.warning(f"Unauthorized access attempt: {chat_id}")
            await update.message.reply_text("⛔ Unauthorized. Your Chat ID is not whitelisted.")
            return
        return await func(self, update, context)
    return wrapper


# ── Bot ───────────────────────────────────────────────────────────────────────

class TelegramBot:
    MAX_MSG_LEN = 4096  # Telegram's maximum message length

    def __init__(self):
        load_dotenv()
        self.token  = os.getenv("TELEGRAM_BOT_TOKEN")
        self.router = CommandRouter()
        self.app    = None
        self.dashboard_process = None

    async def _safe_reply_html(self, update: Update, text: str):
        """Reply with HTML, auto-splitting if text exceeds Telegram's 4096 char limit."""
        if len(text) <= self.MAX_MSG_LEN:
            await update.message.reply_html(text)
            return
        # Split on newlines, keeping chunks under the limit
        lines = text.split('\n')
        chunk = ""
        for line in lines:
            if len(chunk) + len(line) + 1 > self.MAX_MSG_LEN:
                if chunk:
                    await update.message.reply_html(chunk)
                chunk = line
            else:
                chunk = chunk + '\n' + line if chunk else line
        if chunk:
            await update.message.reply_html(chunk)

    async def start(self):
        if not self.token:
            logger.error("TELEGRAM_BOT_TOKEN not set in .env")
            return

        self.app = Application.builder().token(self.token).build()

        # ── Register command handlers ────────────────────────────────────────
        handlers = [
            ("start",           self.help_command),
            ("help",            self.help_command),
            ("status",          self.status_command),
            ("balance",         self.balance_command),
            ("health",          self.health_command),
            ("mode",            self.mode_command),
            ("signals",         self.signals_command),
            ("analysis",        self.analysis_command),
            ("risk",            self.risk_command),
            ("active",          self.active_command),
            ("wfo",             self.wfo_command),
            ("demotion",        self.demotion_command),
            ("data",            self.data_command),
            ("enable",          self.enable_command),
            ("disable",         self.disable_command),
            ("dashboard",       self.dashboard_command),
            ("backtest_report", self.backtest_report_command),
            ("best_pairs",      self.best_pairs_command),
            ("top_strategies",  self.top_strategies_command),
            ("backtest_status", self.backtest_status_command),
            ("params",          self.strategy_params_command),
            ("signal_performance", self.signal_performance_command),
            ("pause",           self.pause_command),
            ("resume",          self.resume_command),
            ("news_blackout",   self.news_blackout_command),
            ("trade",           self.trade_command),
            ("close_manual",    self.close_manual_command),
        ]
        for name, handler in handlers:
            self.app.add_handler(CommandHandler(name, handler))

        await self.app.initialize()
        await self.app.start()
        await self.app.updater.start_polling()

        # ── Launch dashboard in background ───────────────────────────────────
        dashboard_script = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dashboard.py"
        )
        self.dashboard_process = subprocess.Popen(
            [sys.executable, dashboard_script, "--port", "5000"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

        # ── Start morning push background task ───────────────────────────────
        asyncio.create_task(self._morning_push_loop())

        logger.info("Telegram bot polling. Dashboard: http://localhost:5000")

    async def stop(self):
        if self.app:
            await self.app.updater.stop()
            await self.app.stop()
            await self.app.shutdown()
        if self.dashboard_process:
            self.dashboard_process.terminate()

    # ── Morning push loop ─────────────────────────────────────────────────────

    @auth_required
    async def news_blackout_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler for /news_blackout [minutes]"""
        try:
            minutes = 30
            if context.args:
                minutes = int(context.args[0])
                
            success, msg = self.router.set_news_blackout(minutes)
            if success:
                await update.message.reply_text(f"📰 {msg}")
            else:
                await update.message.reply_text(f"❌ Failed: {msg}")
        except ValueError:
            await update.message.reply_text("❌ Usage: /news_blackout [minutes]")
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {e}")

    @auth_required
    async def trade_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler for /trade <SYM> <BUY/SELL> <LOTS> [entry]"""
        try:
            if len(context.args) < 3:
                await update.message.reply_text("❌ Usage: /trade <SYM> <BUY/SELL> <LOTS> [entry]")
                return
                
            symbol = context.args[0].upper()
            direction = context.args[1].upper()
            lots = float(context.args[2])
            entry = float(context.args[3]) if len(context.args) > 3 else None
            
            success, msg = self.router.log_manual_trade(symbol, direction, lots, entry)
            if success:
                await update.message.reply_text(f"🖊️ {msg}")
            else:
                await update.message.reply_text(f"❌ Failed: {msg}")
        except ValueError:
            await update.message.reply_text("❌ Error: Invalid number format for lots/entry.")
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {e}")

    @auth_required
    async def close_manual_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler for /close_manual <ticket> [exit_price]"""
        try:
            if not context.args:
                await update.message.reply_text("❌ Usage: /close_manual <ticket> [exit_price]")
                return
                
            ticket = int(context.args[0])
            exit_price = float(context.args[1]) if len(context.args) > 1 else None
            
            success, msg = self.router.close_manual_trade(ticket, exit_price)
            if success:
                await update.message.reply_text(f"✅ {msg}")
            else:
                await update.message.reply_text(f"❌ Failed: {msg}")
        except ValueError:
            await update.message.reply_text("❌ Error: Ticket must be an integer.")
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {e}")

    async def _morning_push_loop(self):
        """Sends a morning brief every day at 08:00 local time."""
        chat_id = os.getenv("TELEGRAM_CHAT_ID")
        if not chat_id:
            logger.warning("TELEGRAM_CHAT_ID not set — morning push disabled")
            return

        while True:
            now    = datetime.now()
            target = now.replace(hour=8, minute=0, second=0, microsecond=0)
            if now >= target:
                # Already past 08:00 today — schedule for tomorrow
                from datetime import timedelta
                target += timedelta(days=1)
            wait_secs = (target - now).total_seconds()
            logger.info(f"Morning push scheduled in {wait_secs/3600:.1f}h at {target.strftime('%H:%M')}")
            await asyncio.sleep(wait_secs)
            try:
                msg = self.router.get_morning_brief()
                await self.send_direct_message(msg)
                logger.info("Morning brief sent")
            except Exception as e:
                logger.error(f"Morning push failed: {e}")

    # ── Existing command handlers ─────────────────────────────────────────────

    @auth_required
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        msg = (
            "🤖 <b>TradePanel Commands</b>\n\n"
            "<b>📊 Account</b>\n"
            "/status — account + open positions\n"
            "/balance — balance, equity, margin\n"
            "/active — open positions with TP/SL levels\n"
            "/risk — drawdown, margin level, daily P&amp;L\n\n"
            "<b>📡 Market &amp; Signals</b>\n"
            "/signals — latest 24h strategy signals\n"
            "/signal_performance — accuracy of last 7 days\n"
            "/analysis — multi-TF regime summary\n"
            "/mode — active strategies list\n"
            "/data — data coverage per pair\n\n"
            "<b>🔬 Backtesting &amp; WFO</b>\n"
            "/backtest_report — last overnight backtest\n"
            "/best_pairs — top pairs by win rate\n"
            "/top_strategies — top 5 by Sharpe ratio\n"
            "/backtest_status — when last backtest ran\n"
            "/params — parameter tweak suggestions\n"
            "/wfo — WFO master summary\n"
            "/demotion — strategies at demotion risk\n\n"
            "<b>⚙️ Strategy Control</b>\n"
            "/enable &lt;name&gt; — enable a strategy\n"
            "/disable &lt;name&gt; — disable a strategy\n\n"
            "<b>🛠 System</b>\n"
            "/health — system health + heartbeat\n"
            "/dashboard — web dashboard link\n"
            "/help — this list"
        )
        await update.message.reply_html(msg)

    @auth_required
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_html(self.router.get_status())

    @auth_required
    async def balance_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_html(self.router.get_balance())

    @auth_required
    async def health_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_html(self.router.get_health())

    @auth_required
    async def mode_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_html(self.router.get_mode())

    @auth_required
    async def signals_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await self._safe_reply_html(update, self.router.get_signals())

    @auth_required
    async def signal_performance_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_html(self.router.get_signal_performance())

    @auth_required
    async def analysis_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_html(self.router.get_analysis())

    @auth_required
    async def risk_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_html(self.router.get_risk())

    @auth_required
    async def active_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_html(self.router.get_active())

    # ── New command handlers ──────────────────────────────────────────────────

    @auth_required
    async def wfo_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show WFO master summary — pass/fail per strategy."""
        await self._safe_reply_html(update, self.router.get_wfo_summary())

    @auth_required
    async def demotion_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show demotion tracker — strategies at risk."""
        await self._safe_reply_html(update, self.router.get_demotion())

    @auth_required
    async def data_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show data coverage — latest bar date per pair."""
        await self._safe_reply_html(update, self.router.get_data_coverage())

    @auth_required
    async def enable_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Enable a strategy: /enable <strategy_name>"""
        if not context.args:
            await update.message.reply_html(
                "Usage: /enable &lt;strategy_name&gt;\n"
                "Example: /enable macd_trend\n\n"
                "Use /mode to see available strategy names."
            )
            return
        name = context.args[0].strip().lower()
        await update.message.reply_html(self.router.toggle_strategy(name, enable=True))

    @auth_required
    async def disable_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Disable a strategy: /disable <strategy_name>"""
        if not context.args:
            await update.message.reply_html(
                "Usage: /disable &lt;strategy_name&gt;\n"
                "Example: /disable macd_trend\n\n"
                "Use /mode to see enabled strategy names."
            )
            return
        name = context.args[0].strip().lower()
        await update.message.reply_html(self.router.toggle_strategy(name, enable=False))

    @auth_required
    async def pause_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Pause the bot: /pause [minutes]"""
        mins = None
        if context.args:
            try:
                mins = int(context.args[0])
            except ValueError:
                pass
        await update.message.reply_html(self.router.pause_bot(mins))

    @auth_required
    async def resume_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Resume the bot: /resume"""
        await update.message.reply_html(self.router.resume_bot())

    # ── Backtest command handlers ─────────────────────────────────────────────

    @auth_required
    async def dashboard_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        msg = (
            "<b>📊 TradePanel Dashboard</b>\n\n"
            "🌐 <a href='http://localhost:5000'>http://localhost:5000</a>\n\n"
            "<i>Local server — must be running on your machine.</i>"
        )
        await update.message.reply_html(msg)

    @auth_required
    async def backtest_report_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_html(self.router.get_backtest_report())

    @auth_required
    async def best_pairs_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_html(self.router.get_best_pairs())

    @auth_required
    async def top_strategies_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_html(self.router.get_top_strategies())

    @auth_required
    async def backtest_status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_html(self.router.get_backtest_status())

    @auth_required
    async def strategy_params_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_html(self.router.get_strategy_params())

    # ── Outbound push utilities ───────────────────────────────────────────────

    async def send_direct_message(self, text: str):
        """Send a push message to the primary chat ID."""
        # WhatsApp Integration
        try:
            from notifications.whatsapp_bot import WhatsAppBot
            wa = WhatsAppBot()
            if wa.default_phone:
                import asyncio
                loop = asyncio.get_event_loop()
                # send_alert is synchronous, run it in executor
                loop.run_in_executor(None, wa.send_alert, text)
        except Exception as e:
            logger.error(f"WhatsApp sending failed: {e}")

        chat_id = os.getenv("TELEGRAM_CHAT_ID")
        if not chat_id:
            logger.warning("TELEGRAM_CHAT_ID not set — cannot send push")
            return
        bot = Bot(token=self.token)
        async with bot:
            await bot.send_message(chat_id=chat_id, text=text, parse_mode=ParseMode.HTML)

    def send_sync_message(self, text: str):
        """Synchronous wrapper — call from non-async engine code."""
        import nest_asyncio
        nest_asyncio.apply()
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        loop.run_until_complete(self.send_direct_message(text))


# ── Entry point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    log_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs", "telegram_bot.log")
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_file)
        ]
    )
    bot = TelegramBot()

    async def run():
        await bot.start()
        try:
            while True:
                await asyncio.sleep(1)
        except (KeyboardInterrupt, SystemExit):
            await bot.stop()

    asyncio.run(run())
