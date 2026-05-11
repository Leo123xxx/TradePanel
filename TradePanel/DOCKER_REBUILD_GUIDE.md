# Docker Container Rebuild Guide

**Status:** Ready to execute  
**Date:** May 10, 2026  
**Time Needed:** 5-10 minutes

---

## 🎯 What This Does

Rebuilds the Docker containers to:
- ✅ Include new auth logging modules (auth_logger.py, auth_commands.py)
- ✅ Update telegram_bot.py with authorization logging
- ✅ Sync all .env changes (ALLOWED_CHAT_IDS)
- ✅ Ensure database schema is up to date

---

## 📋 Step-by-Step Guide

### Step 1: Stop All Running Containers

```powershell
cd F:\REPOS\leo123xxx\TradePanel\TradePanel

# Stop all containers
docker-compose down

# This will:
# - Stop tradepanel-db
# - Stop tradepanel-telegram
# - Stop tradepanel-backend
# - Stop tradepanel-scheduler
# - Stop tradepanel-frontend
# - Stop tradepanel-waha
# - Stop tradepanel-db-backup
# - Stop tradepanel-adminer
```

**Wait 10 seconds after this completes.**

---

### Step 2: Rebuild the Images

```powershell
# Rebuild all images (pulls fresh code)
docker-compose build --no-cache

# This will rebuild:
# - tradepanel-backend
# - tradepanel-frontend
# - tradepanel-telegram
# - tradepanel-scheduler
# - tradepanel-db-backup
```

**This takes 2-5 minutes. Be patient.**

---

### Step 3: Start the Containers in Order

```powershell
# Start all containers
docker-compose up -d

# This will start in dependency order:
# 1. Database (5433)
# 2. Backend (8000)
# 3. Frontend (3000)
# 4. Telegram Bot
# 5. Scheduler
# 6. WAHA (8025)
# 7. Adminer (8090)
# 8. Backup service
```

**Wait 30 seconds for database to become healthy.**

---

### Step 4: Verify All Containers Are Running

```powershell
# Check status
docker-compose ps

# Expected output:
# NAME                  STATUS              PORTS
# tradepanel-db         Up (healthy)        5433->5432/tcp
# tradepanel-backend    Up                  8000->8000/tcp
# tradepanel-frontend   Up                  3000->80/tcp
# tradepanel-telegram   Up                  (no ports)
# tradepanel-scheduler  Up                  (no ports)
# tradepanel-waha       Up                  8025->3000/tcp
# tradepanel-db-backup  Up                  (no ports)
# tradepanel-adminer    Up                  8090->8080/tcp
```

---

### Step 5: Test Telegram Bot

Send commands to your bot:

```
/status           → Should show account info
/extract_chat_id  → Should show your Chat ID
/auth_log         → Should show auth attempt logs
/auth_users       → Should show authorized users
```

---

## 🔍 Verify Authorization Logging

### Check Database

Connect to adminer at `http://localhost:8090`:
- Server: db
- Username: postgres
- Password: (from .env)
- Database: trading_platform

Then run:

```sql
SELECT * FROM telegram_auth_log ORDER BY timestamp DESC LIMIT 20;
```

Should show your authorization attempts.

---

## 📊 Expected Result After Rebuild

```
✅ All containers running
✅ Database schema created
✅ telegram_bot.py initialized with auth logging
✅ /auth_log command returns results
✅ /auth_users command returns results
✅ Database has telegram_auth_log table populated
```

---

## 🆘 Troubleshooting

### Database fails to start

```powershell
# Check database logs
docker-compose logs db

# If it says "already in use", stop the port:
# In Windows Task Manager: find "postgres" and end it
# Or change port in docker-compose.yml from 5433 to 5434
```

### Telegram bot not responding

```powershell
# Check telegram bot logs
docker-compose logs telegram-bot

# Common issues:
# 1. Database not healthy yet (wait 30s)
# 2. TELEGRAM_BOT_TOKEN not in .env
# 3. Port conflict (check if port 8000 is in use)
```

### "Cannot connect to database"

```powershell
# Wait longer for database to be healthy
docker-compose ps db

# If status shows "Up (healthy)" but still failing:
# 1. Stop containers: docker-compose down
# 2. Clear database: docker volume rm tradepanel_postgres_data
# 3. Start again: docker-compose up -d
# 4. Rerun schema: psql -h localhost -p 5433 -U postgres -d trading_platform -f database/migrations/auth_logging.sql
```

### Auth log commands return empty

```powershell
# Check if telegram_auth_log table exists
docker-compose exec db psql -U postgres -d trading_platform -c "SELECT * FROM telegram_auth_log LIMIT 5;"

# If table doesn't exist:
docker-compose exec db psql -U postgres -d trading_platform -f /database/migrations/auth_logging.sql

# Or use adminer to create it manually
```

---

## 📝 Complete Rebuild (One Command)

If you want a fresh start from scratch:

```powershell
cd F:\REPOS\leo123xxx\TradePanel\TradePanel

# WARNING: This deletes all data!
docker-compose down -v
docker system prune -f

# Then rebuild:
docker-compose build --no-cache
docker-compose up -d

# Wait 60 seconds
# Then run the SQL schema
docker-compose exec db psql -U postgres -d trading_platform -f /database/migrations/auth_logging.sql
```

---

## ✅ Quick Checklist

- [ ] Ran `docker-compose down`
- [ ] Ran `docker-compose build --no-cache`
- [ ] Ran `docker-compose up -d`
- [ ] Waited 30 seconds
- [ ] Verified with `docker-compose ps` (all Up)
- [ ] Tested `/status` command
- [ ] Tested `/extract_chat_id` command
- [ ] Tested `/auth_log` command
- [ ] Database schema verified in adminer

---

## 🚀 Commands to Copy-Paste

**For Windows PowerShell:**

```powershell
cd F:\REPOS\leo123xxx\TradePanel\TradePanel
docker-compose down
Start-Sleep -Seconds 10
docker-compose build --no-cache
docker-compose up -d
Start-Sleep -Seconds 30
docker-compose ps
```

**For Windows CMD:**

```cmd
cd F:\REPOS\leo123xxx\TradePanel\TradePanel
docker-compose down
timeout /t 10
docker-compose build --no-cache
docker-compose up -d
timeout /t 30
docker-compose ps
```

---

## 📞 Next Steps

1. **Execute the rebuild** (commands above)
2. **Verify all containers** are running (docker-compose ps)
3. **Test in Telegram** (/status, /auth_log, etc.)
4. **Check database** via adminer if needed
5. **Monitor logs** with `docker-compose logs telegram-bot` if issues occur

