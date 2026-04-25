# notifications/templates.py

TRADE_OPEN = """
🚀 <b>Trade Opened</b>
🏷 <b>Symbol:</b> {symbol}
📊 <b>Direction:</b> {direction}
💰 <b>Lot Size:</b> {lot_size}
💵 <b>Entry Price:</b> {entry_price}
🎯 <b>TP:</b> {tp} | 🛡 <b>SL:</b> {sl}
⏰ <b>Time:</b> {timestamp}
"""

TRADE_CLOSE = """
🏁 <b>Trade Closed</b>
🏷 <b>Symbol:</b> {symbol}
📊 <b>Direction:</b> {direction}
💰 <b>P&L (USD):</b> {pnl_usd:+.2f} | <b>ZAR:</b> R {pnl_zar:+,.2f}
📉 <b>Exit Price:</b> {exit_price}
📝 <b>Reason:</b> {reason}
⏱ <b>Duration:</b> {duration}
"""

DRAWDOWN_WARNING = """
⚠️ <b>Drawdown Warning</b>
📉 <b>Current Drawdown:</b> {current_drawdown}%
🛑 <b>Threshold:</b> {threshold}%
⚠️ <i>Please monitor your strategies.</i>
"""

HEARTBEAT_LOST = """
🚨 <b>HEARTBEAT LOST</b>
The bot has stopped sending heartbeats!
🕒 <b>Last Heartbeat:</b> {last_heartbeat}
🛠 <i>Check the server immediately.</i>
"""

DAILY_SUMMARY = """
📅 <b>Daily Summary - {date}</b>
💰 <b>Total P&L:</b> {total_pnl}
📈 <b>Win Rate:</b> {win_rate}%
🔄 <b>Total Trades:</b> {total_trades}
📉 <b>Max Drawdown:</b> {max_dd}%
"""

WEEKLY_REPORT = """
📊 <b>Weekly Report — {week}</b>
💰 <b>Net P&L:</b> R {total_pnl:,.2f}
📈 <b>Win Rate:</b> {win_rate:.1f}%  ({winning_trades}W / {losing_trades}L)
🔄 <b>Total Trades:</b> {total_trades}
📉 <b>Max Drawdown:</b> {max_dd:.2f}%
⭐ <b>Best Strategy:</b> {best_strategy}
🔻 <b>Worst Strategy:</b> {worst_strategy}
"""

MARKET_ANALYSIS_HEADER = "📊 <b>Market Analysis Summary</b>\n\n"

SIGNAL_ENTRY = """
⏰ <b>{timestamp}</b>
🏷 <b>{symbol} {direction}</b>
🎯 <b>Strategy:</b> {strategy}
⏳ <b>Validity:</b> {validity}
💵 <b>Entry:</b> {entry_range}
────────────────────
🛡 <b>SL:</b> {sl}
🎯 <b>TP1:</b> {tp1} | <b>TP2:</b> {tp2}
🎯 <b>TP3:</b> {tp3}
🏁 <b>Exit:</b> {exit}
────────────────────
"""

RISK_STATUS = """
🛡 <b>Account Risk Status</b>
💰 <b>Equity:</b> {equity} {currency}
📈 <b>Margin Level:</b> {margin_level}%
📉 <b>Drawdown:</b> {drawdown}%
📅 <b>Daily P&L:</b> {daily_pnl} {currency}
📅 <b>Weekly P&L:</b> {weekly_pnl} {currency}
"""

ACTIVE_TRADE_ENTRY = """
🏷 <b>{symbol} {direction}</b>
💰 <b>Profit:</b> {profit} {currency}
📊 <b>Lots:</b> {volume}
🛡 <b>SL:</b> {sl} | 🎯 <b>TP:</b> {tp}
🎯 <b>Targets:</b> {tp2} | {tp3}
⏰ <b>Open:</b> {open_time}
"""
