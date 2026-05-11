# Telegram Bot Whitelist: Quick Setup

## 3-Step Process (2 Minutes)

### 1️⃣ Get Your Chat ID
```
Telegram → Raw-Demo bot → Send: /start

Response shows:
⛔ Unauthorized
Your Chat ID: 5838483717    ← COPY THIS
```

### 2️⃣ Add to .env
```
File: F:\REPOS\leo123xxx\TradePanel\TradePanel\.env

Add this line:
ALLOWED_CHAT_IDS=5838483717
```

### 3️⃣ Restart Bot & Test
```
Restart:
  Option A) python scripts/start_telegram_bot.py
  Option B) Task Scheduler → Run

Test:
  Telegram → /start
  Expected: See help menu ✅
```

---

## Already Works?

If you want to use the same Chat ID that's already in .env:
```
.env already has:
TELEGRAM_CHAT_ID=5838483717

That's your Chat ID! Just make sure bot is using it:
ALLOWED_CHAT_IDS=5838483717
```

---

## Multiple Users?

```
ALLOWED_CHAT_IDS=ID1,ID2,ID3

Example:
ALLOWED_CHAT_IDS=5838483717,1234567890,9876543210
```

Each user gets their Chat ID from the bot error, then you add all of them here.

---

**Done!** Your bot is now whitelisted 🚀
