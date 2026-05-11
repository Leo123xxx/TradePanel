# Quick Start: Running Integrated Daily Automation Locally

**Time to deploy:** 5 minutes  
**Prerequisites:** Environment variables already configured ✅  

---

## Step 1: Verify Environment Variables Are Set

Run this in PowerShell to verify your credentials are configured:

```powershell
# Check Telegram (from previous setup)
echo $env:TELEGRAM_TOKEN
echo $env:TELEGRAM_CHAT_ID

# Check AWS S3
echo $env:S3_BUCKET
echo $env:AWS_PROFILE
echo $env:S3_REGION

# Check Cloudflare R2
echo $env:R2_ACCOUNT_ID
echo $env:R2_ACCESS_KEY
echo $env:R2_SECRET_KEY
```

All should return values. If any are blank, set them:

```powershell
# Example: AWS S3
$env:S3_BUCKET = "tradepanel-backups"
$env:AWS_PROFILE = "default"
$env:S3_REGION = "us-east-1"

# Example: Cloudflare R2
$env:R2_ACCOUNT_ID = "your-account-id"
$env:R2_ACCESS_KEY = "your-key"
$env:R2_SECRET_KEY = "your-secret"

# Example: Telegram (from previous setup)
$env:TELEGRAM_TOKEN = "your-token"
$env:TELEGRAM_CHAT_ID = "your-chat-id"
```

---

## Step 2: Test the Script (Dry Run)

```powershell
# Navigate to project
cd F:\REPOS\leo123xxx\TradePanel\TradePanel

# Activate virtual environment
venv\Scripts\Activate.ps1

# Run WITHOUT cleanup (test mode)
python scripts/daily_automation_v2.py --no-cleanup
```

**Expected Output:**
- ✅ All components validate
- ✅ Docker status checked
- ⏭️ Cleanup skipped
- ✅ Logs written

---

## Step 3: Run Full Automation (With Backup)

```powershell
cd F:\REPOS\leo123xxx\TradePanel\TradePanel
venv\Scripts\Activate.ps1

# Full automation including cleanup & backup
python scripts/daily_automation_v2.py
```

**Expected Output:**
- ✅ All 5 steps complete
- ✅ Files archived
- ✅ S3 sync completed
- ✅ R2 sync completed
- ✅ Logs written

---

## Step 4: Verify Backup in Cloud Storage

### Verify S3
```powershell
# List S3 contents
aws s3 ls s3://tradepanel-backups/tradepanel/ --recursive --region us-east-1

# Expected output (something like):
# 2026-05-10 14:57:49    1524523 tradepanel/overnight/20260504_backtest_report.md
# 2026-05-10 14:57:50     854123 tradepanel/recommendations/20260506_recommendations.md
```

### Verify R2
```powershell
# List R2 contents (using AWS CLI with R2 endpoint)
aws s3 ls s3://tradepanel-backups/tradepanel/ `
  --endpoint-url https://{YOUR_ACCOUNT_ID}.r2.cloudflarestorage.com `
  --region auto

# OR: Check the Cloudflare Dashboard
# https://dash.cloudflare.com → R2 → tradepanel-backups → tradepanel/
```

---

## Step 5: Check Logs

### Recent Validation Log
```powershell
# View last 5 entries of validation log
Get-Content results/validation_daily.log -Tail 5

# Example output:
# [2026-05-10 14:57:49 UTC] MODE=daily-v2-integrated | PASS=72/1411 (5.1%) | DOCKER=OFFLINE | BACKUP=COMPLETE | STATUS=WARN
```

### Recent Cleanup Log
```powershell
# View last 5 entries of cleanup log
Get-Content results/cleanup_backup.log -Tail 5

# Example output:
# [2026-05-10 14:57:49] CLEANUP_BACKUP | Files=42 | Size=156.23MB | Archive=backup_20260510_145747 | Errors=0
```

---

## Step 6: Schedule for Daily Execution

### Option A: Windows Task Scheduler (Recommended)

```powershell
# 1. Create task to run at 2 AM daily
$taskPath = "TradePanel\DailyAutomation"
$taskName = "DailyAutomation-v2-Integrated"

$action = New-ScheduledTaskAction `
  -Execute "python" `
  -Argument "scripts/daily_automation_v2.py" `
  -WorkingDirectory "F:\REPOS\leo123xxx\TradePanel\TradePanel"

$trigger = New-ScheduledTaskTrigger -Daily -At "02:00:00"

$principal = New-ScheduledTaskPrincipal -UserId "$env:USERNAME" -LogonType Interactive -RunLevel Highest

Register-ScheduledTask `
  -Action $action `
  -Trigger $trigger `
  -Principal $principal `
  -TaskPath $taskPath `
  -TaskName $taskName `
  -Description "TradePanel Daily Automation with Backup" `
  -Force

# 2. Verify task was created
Get-ScheduledTask -TaskPath "\TradePanel\" -TaskName "*DailyAutomation*"

# 3. Test the task
Start-ScheduledTask -TaskPath "\TradePanel\" -TaskName "DailyAutomation-v2-Integrated"

# 4. View task status
Get-ScheduledTaskInfo -TaskPath "\TradePanel\" -TaskName "DailyAutomation-v2-Integrated"
```

### Option B: Manual Scheduled Execution

Run manually whenever needed:
```powershell
cd F:\REPOS\leo123xxx\TradePanel\TradePanel
venv\Scripts\python scripts/daily_automation_v2.py
```

---

## Verification Checklist

After your first automated run, verify everything works:

- [ ] Script runs without errors
- [ ] Telegram message received with backup status
- [ ] Files appear in S3 bucket
- [ ] Files appear in R2 bucket
- [ ] `validation_daily.log` updated with COMPLETE entry
- [ ] `cleanup_backup.log` updated with stats
- [ ] Old files removed from `results/` directories
- [ ] Archive created with timestamped directory

---

## Runtime Examples

### Example 1: Normal Daily Run
```
[2026-05-10 14:57:47 UTC] INFO - 🚀 TradePanel Daily Automation v2 (Integrated)
[2026-05-10 14:57:47 UTC] INFO - ✅ Docker: UP (8 containers)
[2026-05-10 14:57:47 UTC] INFO - ✅ Backtest: 72/1411 PASS (5.1%)
[2026-05-10 14:57:47 UTC] INFO - ✅ Telegram message posted successfully
[2026-05-10 14:57:47 UTC] INFO - ✅ Archive directory: archive/backup_20260510_145747
[2026-05-10 14:57:48 UTC] INFO -   Files archived: 42
[2026-05-10 14:57:48 UTC] INFO -   Space freed: 156.23 MB
[2026-05-10 14:57:48 UTC] INFO - ✅ S3 sync completed successfully
[2026-05-10 14:57:48 UTC] INFO - ✅ R2 sync completed successfully
[2026-05-10 14:57:49 UTC] INFO - ✅ FULL AUTOMATION COMPLETE
```

### Example 2: Dry Run (No Cleanup)
```
python scripts/daily_automation_v2.py --no-cleanup

[2026-05-10 14:57:47 UTC] INFO - ✅ Validation complete
[2026-05-10 14:57:47 UTC] INFO - ✅ Docker: UP
[2026-05-10 14:57:47 UTC] INFO - ✅ Backtest: 72/1411 PASS
[2026-05-10 14:57:47 UTC] INFO - ✅ Telegram posted
[2026-05-10 14:57:47 UTC] INFO - ⏭️  Cleanup skipped (dry run mode)
[2026-05-10 14:57:48 UTC] INFO - ✅ FULL AUTOMATION COMPLETE
```

---

## Troubleshooting Quick Fixes

| Issue | Fix |
|-------|-----|
| "AWS CLI not found" | `pip install awscli` |
| "R2 credentials not found" | Set `R2_ACCOUNT_ID`, `R2_ACCESS_KEY`, `R2_SECRET_KEY` env vars |
| "No files archived" | Files must be >3 days old (use `--cleanup-days 0` to archive all) |
| "S3 sync failed" | Verify AWS profile: `aws sts get-caller-identity --profile default` |
| Script hangs | Press Ctrl+C; check Docker/network issues; retry with `--no-cleanup` |

---

## Support Files

- **Main Script:** `scripts/daily_automation_v2.py`
- **Detailed Report:** `INTEGRATION_REPORT.md`
- **Logs Location:** `results/validation_daily.log` + `results/cleanup_backup.log`
- **Archive Location:** `archive/backup_YYYYMMDD_HHMMSS/`

---

**You're all set! The integrated daily automation is ready for production use.** 🚀

---

**Questions?**
- Check `INTEGRATION_REPORT.md` for detailed documentation
- Review script logs in `results/` directory
- Test with `--no-cleanup` flag to verify setup
