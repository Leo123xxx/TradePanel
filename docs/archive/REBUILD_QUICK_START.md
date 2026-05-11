# Docker Rebuild - Quick Start

**Status:** Ready to execute  
**Time:** 10 minutes total  
**Complexity:** Low (4 commands)

---

## 🚀 Execute These Commands (Copy-Paste)

**Open PowerShell in your TradePanel directory and run:**

```powershell
cd F:\REPOS\leo123xxx\TradePanel\TradePanel

# 1. Stop all containers (wait 10 seconds)
docker-compose down

# 2. Rebuild (takes 2-5 minutes)
docker-compose build --no-cache

# 3. Start everything (wait 30 seconds for DB)
docker-compose up -d

# 4. Verify all running
docker-compose ps
```

---

## ✅ What This Does

✅ Stops all running containers  
✅ Rebuilds images with new code (auth_logger.py, auth_commands.py)  
✅ Updates telegram_bot.py with auth logging integration  
✅ Restarts all services in dependency order  
✅ Database becomes available again  
✅ Telegram bot ready to log authorization attempts  

---

## 🔍 Verify It Worked

After the commands complete, test in Telegram:

```
/status              → Should work ✅
/extract_chat_id     → Should show your Chat ID ✅
/auth_log            → Should show auth logs ✅
/auth_users          → Should show authorized users ✅
```

---

## 📊 Check Logs If Something Fails

```powershell
# See telegram bot logs
docker-compose logs telegram-bot

# See database logs
docker-compose logs db

# See backend logs
docker-compose logs backend
```

---

## 🆘 If Database Won't Start

```powershell
# Wait 60 seconds (database takes time to initialize)
# Then try:
docker-compose logs db

# If still failing, full reset:
docker-compose down -v
docker volume rm tradepanel_postgres_data
docker-compose up -d
```

---

## 📝 Files You Need

All files are already created:

- ✅ `notifications/auth_logger.py`
- ✅ `notifications/auth_commands.py`
- ✅ `database/migrations/auth_logging.sql`
- ✅ `telegram_bot_with_auth_logging.py` (reference, optional copy)

**Important:** You may need to manually update `notifications/telegram_bot.py` with the imports if the rebuild doesn't pick them up. See `telegram_bot_with_auth_logging.py` for the exact changes needed.

---

## 🎯 Expected Result

After rebuild completes:

```
NAME                 STATUS              PORTS
tradepanel-db        Up (healthy)        5433->5432/tcp
tradepanel-backend   Up                  8000->8000/tcp
tradepanel-frontend  Up                  3000->80/tcp
tradepanel-telegram  Up                  (no ports)
tradepanel-scheduler Up                  (no ports)
tradepanel-waha      Up                  8025->3000/tcp
tradepanel-db-backup Up                  (no ports)
tradepanel-adminer   Up                  8090->8080/tcp
```

All should show **Up (healthy)** or **Up**

---

## 💡 Pro Tips

1. **First rebuild takes longer** (pulls base images)
2. **Don't interrupt the build** (let it complete even if it seems slow)
3. **Check container health** with `docker-compose ps` frequently
4. **Adminer available at** http://localhost:8090 to view database
5. **Logs are your friend** when debugging

---

## 🚀 Ready? Go!

Run the 4 commands above. Takes about 5-10 minutes total.

Then test with `/status` in Telegram.

Questions? Check `DOCKER_REBUILD_GUIDE.md` for detailed troubleshooting.

