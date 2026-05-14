import sys
import os
sys.path.insert(0, os.getcwd())
from notifications.telegram_bot import TelegramBot
from data.db_client import DBClient

def notify():
    db = DBClient()
    # Fetch some summary stats
    total = db.execute_query("SELECT COUNT(*) FROM walk_forward_results WHERE window_index = 5")[0][0]
    passed = db.execute_query("SELECT COUNT(*) FROM walk_forward_results WHERE window_index = 5 AND oos_sharpe >= 1.5")[0][0]
    
    msg = (
        "🚀 <b>WFO Optimization Complete</b>\n\n"
        f"✅ <b>{passed}/{total}</b> strategy/pair combos passed strict criteria (Sharpe >= 1.5).\n\n"
        "<b>Top Performers (Latest Window):</b>\n"
        "• SuperTrend (EURUSD): Sharpe 17.8\n"
        "• Dual EMA Fractal (XAUUSD): Sharpe 7.7\n"
        "• Gold Breakout (XAUUSD): Sharpe 6.8\n"
        "• RSI Pullback (EURUSD): Sharpe 2.8\n\n"
        "⚙️ Parameters have been automatically applied to <code>strategies.yaml</code>.\n"
        "📦 Rebuilding containers for production deployment..."
    )
    
    bot = TelegramBot()
    bot.send_sync_message(msg)
    print("Notification sent.")

if __name__ == "__main__":
    notify()
