"""
notifications/telegram_bot.py (UPDATED WITH AUTH LOGGING)
===========================================================
TradePanel Telegram Bot — inbound command handler + outbound push notifications.

CHANGES FROM ORIGINAL:
- Added auth_logger import and initialization
- Added auth_commands import and initialization
- Updated auth_required decorator to log all attempts (authorized + unauthorized)
- Added 5 new command handlers for auth monitoring
- New commands: /extract_chat_id, /auth_log, /auth_users, /auth_daily, /suspicious

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

  Auth Monitoring:
  /extract_chat_id   — Get your Chat ID from logs
  /auth_log [hrs]    — Show unauthorized attempts (admin)
  /auth_users [lim]  — Show authorized users (admin)
  /auth_daily [days] — Daily summary (admin)
  /suspicious [thr]  — Find suspicious patterns (admin)

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
from notifications.auth_logger import AuthorizationLogger  # NEW
from notifications.auth_commands import AuthorizationCommands  # NEW
import subprocess

logger = logging.getLogger(__name__)


# ── Auth decorator (UPDATED WITH LOGGING) ────────────────────────────────────

def auth_required(func):
    @wraps(func)
    async def wrapper(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = str(update.effective_chat.id)
        username = update.effective_user.username
        first_name = update.effective_user.first_name
        last_name = update.effective_user.last_name

        allowed = os.getenv("ALLOWED_CHAT_IDS", "").split(",")
        primary = os.getenv("TELEGRAM_CHAT_ID")
        if primary:
            allowed.append(primary)

        # Extract command name
        command_text = update.message.text.split()[0] if update.message.text else "unknown"
        command_name = command_text.lstrip("/")

        if chat_id not in [a.strip() for a in allowed if a.strip()]:
            # NEW: Log unauthorized attempt
            try:
                self.auth_logger.log_attempt(
                    chat_id=int(chat_id),
                    status="unauthorized",
                    command=command_name,
                    username=username,
                    first_name=first_name,
                    last_name=last_name
                )
            except Exception as e:
                logger.error(f"Failed to log unauthorized attempt: {e}")

            logger.warning(f"Unauthorized access attempt: {chat_id} | command: {command_name}")
            await update.message.reply_html(
                f"⛔ <b>Unauthorized</b>\n\n"
                f"Your Chat ID:\n<code>{chat_id}</code>\n\n"
                f"Add this to <code>.env</code> file:\n<code>ALLOWED_CHAT_IDS={chat_id}</code>"
            )
            return

        # NEW: Log authorized attempt
        try:
            self.auth_logger.log_attempt(
                chat_id=int(chat_id),
                status="authorized",
                command=command_name,
                username=username,
                first_name=first_name,
                last_name=last_name
            )
        except Exception as e:
            logger.error(f"Failed to log authorized attempt: {e}")

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

        # NEW: Initialize auth logger and commands
        # Set db_connection=None for log-only mode (safe, no DB required)
        # If you have a DB connection object, pass it here for full logging
        self.auth_logger = AuthorizationLogger(db_connection=None)
        self.auth_commands = AuthorizationCommands(db_connection=None)

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
            ("backups",         self.backups_command),
            # NEW: Auth monitoring commands
            ("extract_chat_id", self.auth_commands.extract_chat_id_command),
            ("auth_log",        self.auth_commands.auth_log_command),
            ("auth_users",      self.auth_commands.auth_users_command),
            ("auth_daily",      self.auth_commands.auth_daily_command),
            ("suspicious",      self.auth_commands.suspicious_command),
        ]
        for name, handler in handlers:
            self.app.add_handler(CommandHandler(name, handler))

        await self.app.initialize()
        await self.app.start()
        await self.app.idle()

    # ── Command implementations (existing) ──────────────────────────────────

    @auth_required
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        msg = await self.router.help()
        await self._safe_reply_html(update, msg)

    @auth_required
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        msg = await self.router.status()
        await self._safe_reply_html(update, msg)

    @auth_required
    async def balance_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        msg = await self.router.balance()
        await self._safe_reply_html(update, msg)

    @auth_required
    async def health_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        msg = await self.router.health()
        await self._safe_reply_html(update, msg)

    @auth_required
    async def mode_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        msg = await self.router.mode()
        await self._safe_reply_html(update, msg)

    @auth_required
    async def signals_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        msg = await self.router.signals()
        await self._safe_reply_html(update, msg)

    @auth_required
    async def analysis_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        msg = await self.router.analysis()
        await self._safe_reply_html(update, msg)

    @auth_required
    async def risk_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        msg = await self.router.risk()
        await self._safe_reply_html(update, msg)

    @auth_required
    async def active_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        msg = await self.router.active()
        await self._safe_reply_html(update, msg)

    @auth_required
    async def wfo_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        msg = await self.router.wfo()
        await self._safe_reply_html(update, msg)

    @auth_required
    async def demotion_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        msg = await self.router.demotion()
        await self._safe_reply_html(update, msg)

    @auth_required
    async def data_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        msg = await self.router.data()
        await self._safe_reply_html(update, msg)

    @auth_required
    async def enable_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        name = " ".join(context.args) if context.args else ""
        msg = await self.router.enable(name)
        await self._safe_reply_html(update, msg)

    @auth_required
    async def disable_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        name = " ".join(context.args) if context.args else ""
        msg = await self.router.disable(name)
        await self._safe_reply_html(update, msg)

    @auth_required
    async def dashboard_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        msg = templates.dashboard_link()
        await update.message.reply_html(msg)

    @auth_required
    async def backtest_report_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        msg = await self.router.backtest_report()
        await self._safe_reply_html(update, msg)

    @auth_required
    async def best_pairs_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        msg = await self.router.best_pairs()
        await self._safe_reply_html(update, msg)

    @auth_required
    async def top_strategies_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        msg = await self.router.top_strategies()
        await self._safe_reply_html(update, msg)

    @auth_required
    async def backtest_status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        msg = await self.router.backtest_status()
        await self._safe_reply_html(update, msg)

    @auth_required
    async def strategy_params_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        msg = await self.router.strategy_params()
        await self._safe_reply_html(update, msg)

    @auth_required
    async def signal_performance_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        msg = await self.router.signal_performance()
        await self._safe_reply_html(update, msg)

    @auth_required
    async def pause_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        minutes = int(context.args[0]) if context.args else 30
        msg = await self.router.pause(minutes)
        await self._safe_reply_html(update, msg)

    @auth_required
    async def resume_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        msg = await self.router.resume()
        await self._safe_reply_html(update, msg)

    @auth_required
    async def news_blackout_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        minutes = int(context.args[0]) if context.args else 60
        msg = await self.router.news_blackout(minutes)
        await self._safe_reply_html(update, msg)

    @auth_required
    async def trade_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if len(context.args) < 3:
            await update.message.reply_text("Usage: /trade <symbol> <BUY|SELL> <lots>")
            return
        symbol, direction, lots = context.args[0], context.args[1], context.args[2]
        msg = await self.router.trade(symbol, direction, lots)
        await self._safe_reply_html(update, msg)

    @auth_required
    async def close_manual_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not context.args:
            await update.message.reply_text("Usage: /close_manual <ticket>")
            return
        ticket = context.args[0]
        msg = await self.router.close_manual(ticket)
        await self._safe_reply_html(update, msg)

    @auth_required
    async def backups_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        msg = await self.router.backups()
        await self._safe_reply_html(update, msg)


# ── Entry point ───────────────────────────────────────────────────────────────

async def main():
    bot = TelegramBot()
    await bot.start()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
