# 📋 GIT CLEANUP & PREPARATION CHECKLIST
**Date:** 2026-04-22  
**Objective:** Clean up unnecessary files and prepare project for git  
**Status:** Ready to Execute

---

## 🧹 CLEANUP STEPS (Execute in Order)

### Step 1: Archive Old Backups (Optional)
```powershell
cd F:\REPOS\leo123xxx\TradePanel

# Check what's in backup folder
dir backup_2026-04-22

# OPTIONAL: Compress and archive (only if keeping)
# 7z a backup_archive_2026-04-22.7z backup_2026-04-22

# Or delete if not needed (backups from development)
Remove-Item -Path "backup_2026-04-22" -Recurse -Force
```

**Keep?** ❓ Only if you need version history from earlier today. Otherwise delete.

---

### Step 2: Clean Up Temporary Test Files
```powershell
cd F:\REPOS\leo123xxx\TradePanel

# Find and list temporary files
dir -Recurse -Filter "*.tmp" -ErrorAction SilentlyContinue
dir -Recurse -Filter "*.bak" -ErrorAction SilentlyContinue
dir -Recurse -Filter "test_*.py" -ErrorAction SilentlyContinue

# Delete them
Remove-Item -Path "*\*.tmp" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "*\*.bak" -Recurse -Force -ErrorAction SilentlyContinue
```

---

### Step 3: Clean Up Python Cache
```powershell
cd F:\REPOS\leo123xxx\TradePanel

# Remove Python cache directories
Get-ChildItem -Path . -Recurse -Name "__pycache__" -ErrorAction SilentlyContinue | ForEach-Object {
    Remove-Item -Path $_ -Recurse -Force -ErrorAction SilentlyContinue
}

# Remove .pyc files
Get-ChildItem -Path . -Recurse -Filter "*.pyc" | Remove-Item -Force -ErrorAction SilentlyContinue
```

---

### Step 4: Organize Old Documentation (CLEANUP)

Files to delete or archive (these were for development phases):

```powershell
cd F:\REPOS\leo123xxx\TradePanel

# These are agent handover docs - KEEP THEM (they're useful)
# AGENT_CODE_FIX_REFERENCE.md       - KEEP
# AGENT_TESTING_AND_FIX_INSTRUCTIONS.md - KEEP

# These can be archived or deleted (duplicates/interim docs)
# Check each one:
# COMPLETE_REDEPLOY_STEPS.md        - ARCHIVE (reference only)
# QUICK_ACTION_DEMO.md              - ARCHIVE (got it into docs)
# DEMO_LIVE_TRADING_SETUP.md        - ARCHIVE (reference)

# Old/deprecated docs (DELETE):
dir *.md | Where-Object {$_.Name -like "*OLD*" -or $_.Name -like "*DEPRECATED*"}
```

**Decide:** Keep docs that are useful for future reference, delete truly obsolete ones.

---

### Step 5: Verify .gitignore is Complete

```powershell
cd F:\REPOS\leo123xxx\TradePanel

# Check .gitignore is properly set
type .gitignore | Select-String -Pattern "\.env|__pycache__|\.pyc|backup|\.log"

# Should see entries for:
# - .env files
# - __pycache__
# - *.pyc
# - backup folders
# - *.log files
```

---

### Step 6: Verify Important Files Exist

```powershell
cd F:\REPOS\leo123xxx\TradePanel

# MUST EXIST (core)
Test-Path "main.py"                           # ✅ Must be TRUE
Test-Path "dashboard.py"                      # ✅ Must be TRUE
Test-Path "config/strategies.yaml"            # ✅ Must be TRUE
Test-Path ".env"                              # ✅ Must be TRUE (but in .gitignore)

# DOCUMENTATION (keep key ones)
Test-Path "PROJECT_CLOSEOUT_SUMMARY.md"       # ✅ Should exist
Test-Path "AGENT_CODE_FIX_REFERENCE.md"       # ✅ Should exist
Test-Path "SETUP_AND_RUN.md"                  # ✅ Should exist
Test-Path "WINDOWS_SETUP.md"                  # ✅ Should exist

# Show results
"Results: all critical files present"
```

---

### Step 7: Create README.md (Git Repo)

If one doesn't exist, create:

```markdown
# TradePanel - Automated Trading System

## Overview
TradePanel is an automated forex/commodity trading system with 25 strategies,
real-time monitoring, and paper/live trading modes.

## Quick Start
\`\`\`bash
cd TradePanel
python main.py --mode health        # Check system health
python main.py --mode paper-trade   # Run paper trading cycle
python dashboard.py --port 5000     # Start web dashboard
python scripts/start_telegram_bot.py # Start Telegram bot
\`\`\`

## Status: Phase 3
Currently running **Phase 3: Paper Trading Validation** with top 10 strategies
on demo account. Target go-live: May 20, 2026 (Phase 4).

## Documentation
- **SETUP_AND_RUN.md** - Complete setup guide
- **WINDOWS_SETUP.md** - Windows automation setup
- **PROJECT_CLOSEOUT_SUMMARY.md** - Current project status
- **AGENT_CODE_FIX_REFERENCE.md** - Code change reference

## Strategies
**Top 10 Performers:**
1. dual_ema_fractal (55.62% win rate)
2. cot_sentiment (52.55%)
3. rsi_bounce (52.16%)
4. And 7 more...

See TOP_10_STRATEGIES_ANALYSIS.md for details.

## Contact
For support, check logs/ directory or Telegram bot status.
```

---

## ✅ FINAL VERIFICATION

Before committing to git, run these checks:

### Check 1: No Secrets Exposed
```powershell
cd F:\REPOS\leo123xxx\TradePanel

# Search for hardcoded passwords/tokens (should be empty)
grep -r "PASSWORD=\|TOKEN=\|SECRET=" --include="*.py" --include="*.md" | grep -v ".env" | grep -v "example"

# Should return: (empty - no results)
```

### Check 2: No Log Files
```powershell
# .gitignore should prevent logs, but verify
git status | grep -i ".log"

# Should return: (empty - no log files)
```

### Check 3: No Database Files
```powershell
# Verify no .db or .sqlite files will be committed
git status | grep -E "\.db|\.sqlite|\.dump"

# Should return: (empty)
```

### Check 4: Core Files Present
```powershell
git status

# Should show these UNTRACKED (because we're setting up):
# main.py
# dashboard.py
# scripts/
# config/
# And documentation files

# Should NOT show:
# .env (in .gitignore)
# logs/ (in .gitignore)
# backup_* (in .gitignore)
```

---

## 📦 GIT SETUP COMMANDS

```powershell
cd F:\REPOS\leo123xxx\TradePanel

# Initialize git (if not already done)
git init

# Add all non-ignored files
git add .

# Check what will be committed
git status

# Commit the project
git commit -m "feat: TradePanel Phase 3 - Production Ready

✅ COMPLETED:
- Top 10 strategy selection & validation
- Demo account connectivity
- Paper trading ready
- Complete documentation
- Agent handover procedures

📊 STATUS:
- Phase 3: In Progress (Paper Trading)
- All tests passing (125/125)
- Database logging enabled

⏭️ NEXT:
- Monitor paper trading results
- Prepare Phase 4 deployment (May 20)
"

# View commit
git log --oneline -1
```

---

## 📋 CLEANUP CHECKLIST

Execute each step and check off:

- [ ] Old backups archived or deleted
- [ ] Temporary test files cleaned up
- [ ] Python cache removed (__pycache__, .pyc)
- [ ] Old documentation organized
- [ ] .gitignore verified and updated
- [ ] Critical files exist and present
- [ ] No secrets exposed in code
- [ ] No log files will be committed
- [ ] No database files will be committed
- [ ] README.md created (if missing)
- [ ] git init completed
- [ ] git add . completed
- [ ] git status shows expected files
- [ ] Initial commit created

---

## 📊 EXPECTED GIT STATUS

After cleanup and git setup, you should see:

```
On branch main (or master)

Untracked files:
  .gitignore
  .env (should NOT appear - it's in .gitignore)
  main.py
  dashboard.py
  config/
  scripts/
  strategies/
  data/
  notifications/
  validation/
  requirements.txt
  README.md
  PROJECT_CLOSEOUT_SUMMARY.md
  [... documentation files ...]

nothing to commit but untracked files present
```

---

## 🔐 FILES THAT SHOULD BE IGNORED

These should NOT appear in `git status`:

```
.env                               # ✅ Secrets in .gitignore
logs/                              # ✅ Logs in .gitignore
backup_*/                          # ✅ Backups in .gitignore
__pycache__/                       # ✅ Cache in .gitignore
*.pyc                              # ✅ Compiled Python in .gitignore
*.log                              # ✅ Logs in .gitignore
.vscode/                           # ✅ IDE in .gitignore
```

---

## ⏭️ NEXT STEPS AFTER GIT SETUP

1. ✅ Push to remote repository (GitHub/GitLab)
2. ✅ Create branches for Phase 4 development
3. ✅ Start monitoring Phase 3 paper trading
4. ✅ Document results daily
5. ✅ Prepare Phase 4 go-live procedures

---

**Status:** Ready for Git Setup  
**Time Required:** 15-20 minutes  
**Risk Level:** LOW (cleanup only, no code changes)  

🚀 **Execute cleanup and commit to git!**
