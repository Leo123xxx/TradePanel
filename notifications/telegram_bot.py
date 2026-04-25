import os
import sys
import asyncio

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.constants import ParseMode
from dotenv import load_dotenv
from notifications import templates
from notifications.router import CommandRouter
import subprocess

class TelegramBot:
    def __init__(self):
        load_dotenv()
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.router = CommandRouter()
        self.app = None
        self.dashboard_process = None

    async def start(self):
        """Starts the bot to listen for inbound commands."""
        if not self.token:
            print("Error: TELEGRAM_BOT_TOKEN not found.")
            return

        self.app = Application.builder().token(self.token).build()

        # Register handlers
        self.app.add_handler(CommandHandler("start", self.help_command))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(CommandHandler("status", self.status_command))
        self.app.add_handler(CommandHandler("balance", self.balance_command))
        self.app.add_handler(CommandHandler("health", self.health_command))
        self.app.add_handler(CommandHandler("mode",   self.mode_command))
        self.app.add_handler(CommandHandler("signals", self.signals_command))
        self.app.add_handler(CommandHandler("analysis", self.analysis_command))
        self.app.add_handler(CommandHandler("risk",    self.risk_command))
        self.app.add_handler(CommandHandler("active",  self.active_command))
        self.app.add_handler(CommandHandler("dashboard",       self.dashboard_command))
        self.app.add_handler(CommandHandler("backtest_report", self.backtest_report_command))
        self.app.add_handler(CommandHandler("best_pairs",      self.best_pairs_command))
        self.app.add_handler(CommandHandler("top_strategies",  self.top_strategies_command))
        self.app.add_handler(CommandHandler("backtest_status", self.backtest_status_command))
        self.app.add_handler(CommandHandler("params",          self.strategy_params_command))

        print("Telegram bot is starting...")
        await self.app.initialize()
        await self.app.start()
        await self.app.updater.start_polling()
        
        # Start Dashboard in background
        print("Starting Web Dashboard...")
        dashboard_script = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dashboard.py")
        self.dashboard_process = subprocess.Popen([sys.executable, dashboard_script, "--port", "5000"], 
                                                  stdout=subprocess.DEVNULL, 
                                                  stderr=subprocess.DEVNULL)
        
        print(f"Telegram bot is polling. Dashboard: http://localhost:5000")

    async def stop(self):
        if self.app:
            await self.app.updater.stop()
            await self.app.stop()
            await self.app.shutdown()
        
        if self.dashboard_process:
            print("Stopping Web Dashboard API...")
            self.dashboard_process.terminate()

    # Command Handlers
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_html(self.router.get_help())

    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_html(self.router.get_status())

    async def balance_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_html(self.router.get_balance())

    async def health_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_html(self.router.get_health())

    async def mode_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_html(self.router.get_mode())

    async def signals_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_html(self.router.get_signals())

    async def analysis_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_html(self.router.get_analysis())

    async def risk_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_html(self.router.get_risk())

    async def active_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_html(self.router.get_active())

    async def dashboard_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Sends the link to the local web dashboard."""
        msg = "<b>📊 TradePanel Pro Dashboard</b>\n\n"
        msg += "Your live analytics are ready at:\n"
        msg += "🌐 <a href='http://localhost:5000'>http://localhost:5000</a>\n\n"
        msg += "<i>Note: This is a local server. Ensure the bot is running on your machine to access.</i>"
        await update.message.reply_html(msg)

    async def backtest_report_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Send the most recent overnight backtest report."""
        await update.message.reply_html(self.router.get_backtest_report())

    async def best_pairs_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show top pairs by win rate from last backtest."""
        await update.message.reply_html(self.router.get_best_pairs())

    async def top_strategies_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show top 5 strategies by Sharpe ratio from last backtest."""
        await update.message.reply_html(self.router.get_top_strategies())

    async def backtest_status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Report whether overnight backtest has run today and key stats."""
        await update.message.reply_html(self.router.get_backtest_status())

    async def strategy_params_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show current parameter tweak suggestions from last backtest."""
        await update.message.reply_html(self.router.get_strategy_params())

    # Outbound Utility (Standalone)
    async def send_direct_message(self, text: str):
        from telegram import Bot
        chat_id = os.getenv("TELEGRAM_CHAT_ID")
        bot = Bot(token=self.token)
        async with bot:
            await bot.send_message(chat_id=chat_id, text=text, parse_mode=ParseMode.HTML)

    def send_sync_message(self, text: str):
        """Synchronous wrapper for send_direct_message."""
        import asyncio
        import nest_asyncio
        nest_asyncio.apply() # Allow nested loops if already in one
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
        loop.run_until_complete(self.send_direct_message(text))

if __name__ == "__main__":
    bot = TelegramBot()
    async def run_bot():
        await bot.start()
        # Keep running until interrupted
        try:
            while True:
                await asyncio.sleep(1)
        except (KeyboardInterrupt, SystemExit):
            await bot.stop()

    asyncio.run(run_bot())
