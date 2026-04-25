# TradePanel Command Reference
## Windows PowerShell vs Linux Bash

Complete command sheet for managing TradePanel on both operating systems.

---

## 🚀 Quick Start

### Windows (PowerShell)
```powershell
cd F:\REPOS\leo123xxx\TradePanel
python -m uvicorn webapp.main:app --host 0.0.0.0 --port 8000 --reload
```

### Linux (Bash)
```bash
cd ~/repos/leo123xxx/TradePanel
python -m uvicorn webapp.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## 📋 Command Comparison Table

### 1. Navigation

| Task | Windows (PowerShell) | Linux (Bash) |
|------|----------------------|--------------|
| Go to project | `cd F:\REPOS\leo123xxx\TradePanel` | `cd ~/repos/leo123xxx/TradePanel` |
| List files | `Get-ChildItem` or `ls` | `ls` or `ls -la` |
| Show current dir | `Get-Location` or `pwd` | `pwd` |
| Create directory | `New-Item -Type Directory analytics` | `mkdir analytics` |
| Delete directory | `Remove-Item -Recurse analytics` | `rm -rf analytics` |

---

### 2. API Server Management

| Task | Windows (PowerShell) | Linux (Bash) |
|------|----------------------|--------------|
| Start API server | `python -m uvicorn webapp.main:app --host 0.0.0.0 --port 8000` | `python -m uvicorn webapp.main:app --host 0.0.0.0 --port 8000` |
| Start with auto-reload | `python -m uvicorn webapp.main:app --host 0.0.0.0 --port 8000 --reload` | `python -m uvicorn webapp.main:app --host 0.0.0.0 --port 8000 --reload` |
| Check if running | `netstat -ano \| findstr :8000` | `netstat -tuln \| grep 8000` or `lsof -i :8000` |
| Kill API server | `Get-Process python \| Stop-Process -Force` | `pkill -f uvicorn` or `lsof -i :8000 -t \| xargs kill` |
| Check logs | `Get-Content logs\main.log -Tail 50` | `tail -50 logs/main.log` |
| Watch logs in real-time | `Get-Content -Path logs\main.log -Wait` | `tail -f logs/main.log` |

---

### 3. Trading Bot Commands

| Task | Windows (PowerShell) | Linux (Bash) |
|------|----------------------|--------------|
| Paper trading | `python main.py --mode paper-trade` | `python main.py --mode paper-trade` |
| Validate strategies | `python main.py --mode validate` | `python main.py --mode validate` |
| Run backtest | `python main.py --mode backtest` | `python main.py --mode backtest` |
| Health check | `python main.py --mode health` | `python main.py --mode health` |
| Full pipeline | `python main.py --mode full` | `python main.py --mode full` |
| Run scheduler | `python main.py --mode scheduler` | `python main.py --mode scheduler` |
| Paper trade specific pair | `python main.py --mode paper-trade --pair EURUSD` | `python main.py --mode paper-trade --pair EURUSD` |
| Backtest on H1 | `python main.py --mode backtest --timeframe H1` | `python main.py --mode backtest --timeframe H1` |

---

### 4. Analytics Commands

| Task | Windows (PowerShell) | Linux (Bash) |
|------|----------------------|--------------|
| Generate report | `python -m analytics.performance_calculator` | `python -m analytics.performance_calculator` |
| Test module | `python -c "from analytics import PerformanceCalculator; print('OK')"` | `python -c "from analytics import PerformanceCalculator; print('OK')"` |

---

### 5. Database Commands

| Task | Windows (PowerShell) | Linux (Bash) |
|------|----------------------|--------------|
| Test connection | `python -c "from data.db_client import DBClient; db = DBClient(); print('✓ OK')"` | `python -c "from data.db_client import DBClient; db = DBClient(); print('✓ OK')"` |
| Check PostgreSQL | `netstat -ano \| findstr :5432` | `netstat -tuln \| grep 5432` or `lsof -i :5432` |
| Start PostgreSQL (if installed) | `pg_ctl start -D "C:\Program Files\PostgreSQL\data"` | `sudo systemctl start postgresql` or `brew services start postgresql` |
| Stop PostgreSQL | `pg_ctl stop -D "C:\Program Files\PostgreSQL\data"` | `sudo systemctl stop postgresql` or `brew services stop postgresql` |

---

### 6. API Endpoint Testing

| Task | Windows (PowerShell) | Linux (Bash) |
|------|----------------------|--------------|
| Health check | `curl http://localhost:8000/api/analytics/health -UseBasicParsing` | `curl http://localhost:8000/api/analytics/health` |
| Summary | `curl "http://localhost:8000/api/analytics/summary?lookback_days=30" -UseBasicParsing` | `curl "http://localhost:8000/api/analytics/summary?lookback_days=30"` |
| By strategy | `curl "http://localhost:8000/api/analytics/by-strategy?lookback_days=30" -UseBasicParsing` | `curl "http://localhost:8000/api/analytics/by-strategy?lookback_days=30"` |
| By asset | `curl "http://localhost:8000/api/analytics/by-asset?lookback_days=30" -UseBasicParsing` | `curl "http://localhost:8000/api/analytics/by-asset?lookback_days=30"` |
| Daily P&L | `curl "http://localhost:8000/api/analytics/daily?lookback_days=30" -UseBasicParsing` | `curl "http://localhost:8000/api/analytics/daily?lookback_days=30"` |
| Heatmap | `curl "http://localhost:8000/api/analytics/heatmap?lookback_days=30" -UseBasicParsing` | `curl "http://localhost:8000/api/analytics/heatmap?lookback_days=30"` |
| Dashboard | `curl "http://localhost:8000/api/analytics/dashboard?lookback_days=30" -UseBasicParsing` | `curl "http://localhost:8000/api/analytics/dashboard?lookback_days=30"` |
| Save to file | `curl "..." -UseBasicParsing -OutFile response.json` | `curl "..." > response.json` |
| Pretty print JSON | `curl "..." -UseBasicParsing \| ConvertFrom-Json \| ConvertTo-Json` | `curl "..." \| jq` or `curl "..." \| python -m json.tool` |

---

### 7. Python Environment

| Task | Windows (PowerShell) | Linux (Bash) |
|------|----------------------|--------------|
| Check Python | `python --version` | `python --version` or `python3 --version` |
| Create virtual env | `python -m venv venv` | `python -m venv venv` or `python3 -m venv venv` |
| Activate venv | `.\venv\Scripts\Activate.ps1` | `source venv/bin/activate` |
| Deactivate venv | `deactivate` | `deactivate` |
| Install requirements | `pip install -r requirements.txt` | `pip install -r requirements.txt` |
| List packages | `pip list` | `pip list` |
| Upgrade pip | `python -m pip install --upgrade pip` | `pip install --upgrade pip` |

---

### 8. File Operations

| Task | Windows (PowerShell) | Linux (Bash) |
|------|----------------------|--------------|
| View file | `Get-Content config/config.yaml` | `cat config/config.yaml` |
| View with line numbers | `Get-Content -Path config/config.yaml \| Select -Property @{n="LineNumber";e={$_}},*` | `cat -n config/config.yaml` |
| Edit file | `code config/config.yaml` | `nano config/config.yaml` or `vim config/config.yaml` |
| Search in file | `Select-String "pattern" config/config.yaml` | `grep "pattern" config/config.yaml` |
| Search recursively | `Get-ChildItem -Recurse \| Select-String "pattern"` | `grep -r "pattern" .` |
| Copy file | `Copy-Item source.py backup.py` | `cp source.py backup.py` |
| Move file | `Move-Item old.py new.py` | `mv old.py new.py` |
| Delete file | `Remove-Item file.py` | `rm file.py` |
| Show file size | `(Get-Item file.py).Length` | `ls -lh file.py` or `du -h file.py` |

---

### 9. Monitoring & Diagnostics

| Task | Windows (PowerShell) | Linux (Bash) |
|------|----------------------|--------------|
| List processes | `Get-Process` | `ps aux` or `top` |
| Find Python processes | `Get-Process python` | `ps aux \| grep python` |
| Memory usage | `Get-Process python \| select-object Name,@{Name="Memory";Expression={$_.PM/1024/1024}}` | `ps aux \| grep python` (4th column) |
| CPU usage | `Get-Process python \| select-object Name,CPU` | `top -p $(pgrep -f python)` |
| Open ports | `netstat -ano \| findstr LISTENING` | `netstat -tuln` or `ss -tuln` |
| Disk space | `Get-Volume` | `df -h` |
| Directory size | `(Get-ChildItem -Recurse \| Measure-Object -Sum Length).Sum / 1GB` | `du -sh .` or `du -sh *` |

---

### 10. Git Operations

| Task | Windows (PowerShell) | Linux (Bash) |
|------|----------------------|--------------|
| Check status | `git status` | `git status` |
| View log | `git log --oneline` | `git log --oneline` |
| Add changes | `git add .` | `git add .` |
| Commit | `git commit -m "message"` | `git commit -m "message"` |
| Push | `git push` | `git push` |
| Pull | `git pull` | `git pull` |
| View diff | `git diff` | `git diff` |
| Branch list | `git branch -a` | `git branch -a` |
| Switch branch | `git checkout main` | `git checkout main` |

---

### 11. Environment Variables

| Task | Windows (PowerShell) | Linux (Bash) |
|------|----------------------|--------------|
| View all env vars | `Get-ChildItem Env:` | `env` or `printenv` |
| View specific var | `$env:DB_HOST` | `echo $DB_HOST` |
| Set temporary | `$env:DB_HOST="localhost"` | `export DB_HOST=localhost` |
| Set permanent (Windows) | `[Environment]::SetEnvironmentVariable("DB_HOST", "localhost", "User")` | `echo 'export DB_HOST=localhost' >> ~/.bashrc` |
| Check .env file | `Get-Content .env` | `cat .env` |

---

### 12. Troubleshooting

| Task | Windows (PowerShell) | Linux (Bash) |
|------|----------------------|--------------|
| Clear screen | `Clear-Host` or `cls` | `clear` |
| Show Python path | `python -c "import sys; print(sys.path)"` | `python -c "import sys; print(sys.path)"` |
| Check module location | `python -c "import analytics; print(analytics.__file__)"` | `python -c "import analytics; print(analytics.__file__)"` |
| Verify imports | `python -c "from analytics import PerformanceCalculator"` | `python -c "from analytics import PerformanceCalculator"` |
| Run tests | `pytest` or `python -m pytest` | `pytest` or `python -m pytest` |
| Run with verbose logging | `python main.py --mode paper-trade --verbose` | `python main.py --mode paper-trade --verbose` |
| Kill hanging process | `Stop-Process -Name python -Force` | `killall python` or `pkill -9 python` |
| Check for errors | `Get-Content logs/main.log \| Select-String "ERROR"` | `grep ERROR logs/main.log` |
| Monitor in real-time | `Get-Content logs/main.log -Wait \| Select-String "ERROR"` | `tail -f logs/main.log \| grep ERROR` |

---

## 🔗 Common Workflows

### Setup & Installation (One-time)

**Windows:**
```powershell
cd F:\REPOS\leo123xxx\TradePanel
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**Linux:**
```bash
cd ~/repos/leo123xxx/TradePanel
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

### Daily Development Workflow

**Windows:**
```powershell
# 1. Activate virtual environment
.\venv\Scripts\Activate.ps1

# 2. Start API server
python -m uvicorn webapp.main:app --host 0.0.0.0 --port 8000 --reload

# 3. In another PowerShell window, run trading bot
python main.py --mode paper-trade

# 4. Test analytics
curl http://localhost:8000/api/analytics/health -UseBasicParsing
```

**Linux:**
```bash
# 1. Activate virtual environment
source venv/bin/activate

# 2. Start API server (in tmux/screen or background)
python -m uvicorn webapp.main:app --host 0.0.0.0 --port 8000 --reload &

# 3. Run trading bot
python main.py --mode paper-trade

# 4. Test analytics (in another terminal)
curl http://localhost:8000/api/analytics/health
```

---

### Backtest & Validation

**Windows:**
```powershell
# Run full validation
python main.py --mode validate

# Run backtest
python main.py --mode backtest

# Generate analytics report
python -m analytics.performance_calculator
```

**Linux:**
```bash
# Run full validation
python main.py --mode validate

# Run backtest
python main.py --mode backtest

# Generate analytics report
python -m analytics.performance_calculator
```

---

### Deployment Checklist

**Windows:**
```powershell
# 1. Check status
python main.py --mode health

# 2. Verify database
python -c "from data.db_client import DBClient; DBClient().execute_query('SELECT 1')"

# 3. Test API
curl http://localhost:8000/api/analytics/health -UseBasicParsing

# 4. Check logs
Get-Content logs/main.log -Tail 20

# 5. Run full pipeline
python main.py --mode full
```

**Linux:**
```bash
# 1. Check status
python main.py --mode health

# 2. Verify database
python -c "from data.db_client import DBClient; DBClient().execute_query('SELECT 1')"

# 3. Test API
curl http://localhost:8000/api/analytics/health

# 4. Check logs
tail -20 logs/main.log

# 5. Run full pipeline
python main.py --mode full
```

---

## 📊 API Endpoint Reference

All endpoints accept `lookback_days` parameter (default: 30)

```
GET /api/analytics/health                    → Health check
GET /api/analytics/summary                   → Account summary
GET /api/analytics/by-strategy               → By strategy
GET /api/analytics/by-asset                  → By pair
GET /api/analytics/daily                     → Daily P&L
GET /api/analytics/weekly                    → Weekly P&L
GET /api/analytics/monthly                   → Monthly P&L
GET /api/analytics/heatmap                   → Strategy × Asset heatmap
GET /api/analytics/correlation               → Pair correlations
GET /api/analytics/dashboard                 → Complete dashboard data
```

---

## ⚡ Quick Reference Cards

### Windows PowerShell Shortcuts
```powershell
# Function to start everything
function Start-TradePanel {
    .\venv\Scripts\Activate.ps1
    python -m uvicorn webapp.main:app --host 0.0.0.0 --port 8000 --reload
}

# Function to test analytics
function Test-Analytics {
    curl http://localhost:8000/api/analytics/health -UseBasicParsing
}

# Function to view logs
function Watch-Logs {
    Get-Content logs/main.log -Wait
}
```

### Linux Bash Aliases
```bash
# Add to ~/.bashrc or ~/.bash_profile
alias tp='cd ~/repos/leo123xxx/TradePanel'
alias venv='source venv/bin/activate'
alias logs='tail -f logs/main.log'
alias api='python -m uvicorn webapp.main:app --host 0.0.0.0 --port 8000'
alias bot='python main.py --mode paper-trade'
alias health='curl http://localhost:8000/api/analytics/health'
alias report='python -m analytics.performance_calculator'
```

---

## 🆘 Emergency Commands

| Situation | Windows | Linux |
|-----------|---------|-------|
| API crashed | `Get-Process python \| Stop-Process -Force` then restart | `pkill -9 python` then restart |
| Port 8000 in use | `netstat -ano \| findstr :8000` then kill PID | `lsof -i :8000 -t \| xargs kill` |
| Database won't connect | Restart PostgreSQL service | `sudo systemctl restart postgresql` |
| High memory usage | Check `Get-Process python` | `ps aux \| grep python` |
| Frozen terminal | Close window and reopen | Press `Ctrl+C` or open new tab |

---

## 📝 Notes

- **Windows**: Use PowerShell (not CMD) for best compatibility
- **Linux**: Use bash or zsh, commands are similar
- **API Port**: Default 8000, change with `--port XXXX`
- **Database**: Requires PostgreSQL running on localhost:5432
- **Virtual Env**: Always activate before running bot/API
- **Logs**: Check `logs/main.log` for debugging
- **Telegram**: Requires `.env` with `TELEGRAM_CHAT_ID` and `TELEGRAM_TOKEN`

---

**Version:** 1.0  
**Last Updated:** April 24, 2026  
**Status:** Complete Reference
