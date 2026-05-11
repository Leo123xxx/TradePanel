# 🤖 TradePanel Telegram Bot Setup

This bot provides real-time control, monitoring, and authorization logging for your trading system.

## 🚀 Quick Start (Whitelisting)

1.  **Get Your Chat ID**: Send `/start` to your bot. It will respond with an **Unauthorized** error and display your unique Chat ID.
2.  **Whitelist Yourself**: Open the `.env` file and add/update:
    ```bash
    ALLOWED_CHAT_IDS=5838483717  # Replace with your ID
    ```
3.  **Restart the Bot**:
    - **Docker**: `docker-compose restart telegram-bot`
    - **Manual**: `python scripts/start_telegram_bot.py`
4.  **Test**: Send `/help` to see the full list of 30+ commands.

---

## 📖 Detailed Guides

- [**Full Command Reference**](file:///f:/REPOS/leo123xxx/TradePanel/TELEGRAM_BOT_DOCUMENTATION.md) — Complete list of all 30+ commands with examples.
- [**Whitelist Setup Guide**](file:///f:/REPOS/leo123xxx/TradePanel/TELEGRAM_WHITELIST_SETUP.md) — Detailed steps for adding multiple users and troubleshooting.
- [**Auth Logging System**](file:///f:/REPOS/leo123xxx/TradePanel/AUTHORIZATION_LOGGING_IMPLEMENTATION.md) — How the new security and logging system works.

---

## 🛠 New Authorization Commands (Admin Only)

| Command | Description |
| :--- | :--- |
| `/extract_chat_id` | Shows your current Chat ID (even if already authorized). |
| `/auth_log` | Displays recent unauthorized access attempts. |
| `/auth_users` | Lists all authorized users and their activity stats. |
| `/auth_daily` | Shows a daily summary of bot access. |
| `/suspicious` | Identifies IP addresses with multiple failed attempts. |

---

## 🏥 Troubleshooting

- **Unauthorized Error?** Copy the Chat ID from the message and add it to `ALLOWED_CHAT_IDS` in `.env`.
- **Bot Not Responding?** Ensure the bot service is running and has internet access.
- **Database Errors?** Ensure the `telegram_auth_log` table migration has been applied.

**Last Updated:** May 10, 2026
**Status:** ✅ Fully Integrated & Tested
