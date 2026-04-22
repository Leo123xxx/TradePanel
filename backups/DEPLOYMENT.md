# TradePanel Deployment Guide (Migration to 24/7 Laptop)

This guide explains how to restore the TradePanel trading platform on a new machine.

## Prerequisites

1.  **Python 3.11+**: Install Python from [python.org](https://www.python.org/).
2.  **Docker Desktop**: Install from [docker.com](https://www.docker.com/).
3.  **MetaTrader 5 Terminal**: Install your broker's MT5 terminal and login to your account.

---

## 🏗️ Step 1: Database Setup (PostgreSQL)

Run the following command to start a PostgreSQL 16 container that matches your current setup:

docker run --name trading_platform_db \
  -e POSTGRES_PASSWORD=postgres \
  -p 5433:5432 \
  -v pgdata:/var/lib/postgresql/data \
  -d postgres:16

---

## 📁 Step 2: System Restore

1.  **Copy Files**: Copy the entire `TradePanel` folder to the new laptop.
2.  **Configure Environment**:
    *   Rename `backups/env.template` (or your existing `.env`) to `.env` in the root folder.
    *   Verify credentials (MT5 login, Telegram token).
3.  **Install Dependencies**:
    ```powershell
    pip install -r requirements.txt
    ```

---

## 💾 Step 3: Database Restoration

Use the provided SQL dumps in the `backups/` folder.

### Option A: Essential Restore (Recommended - Fast)
Restores your strategies, trades, and configurations. You can then re-ingest market data.
```powershell
# Get the file into the container and run
docker cp backups/db_essential.sql trading_platform_db:/db_essential.sql
docker exec -it trading_platform_db psql -U postgres -d postgres -c "CREATE DATABASE trading_platform;"
docker exec -it trading_platform_db psql -U postgres -d trading_platform -f /db_essential.sql
```

### Option B: Full Restore (Highly Recommended)
Restores everything including historical data. Since the file is in compressed format, use `pg_restore`.
```powershell
docker cp backups/db_full.dump trading_platform_db:/db_full.dump
docker exec -it trading_platform_db pg_restore -U postgres -d trading_platform /db_full.dump

> [!WARNING]
> **Encoding Issues (Relation Error)**: If the `.sql` restore fails with an "invalid byte sequence" or results in "relation does not exist" errors, the file might be in UTF-16 (default for some Windows exports). 
> **Fix**: Convert the file to UTF-8 without BOM before copying:
> ```powershell
> # PowerShell conversion
> Get-Content backups/db_essential.sql | Set-Content -Encoding utf8 backups/db_essential_utf8.sql
> ```
```

---

## 🚀 Step 4: Execution

Start the paper trading engine:
```powershell
python scripts/run_paper.py
```

> [!TIP]
> **24/7 Uptime**: Ensure the laptop's "Sleep" mode is disabled when plugged in. MetaTrader 5 must remain open and logged in for the system to receive live data.
