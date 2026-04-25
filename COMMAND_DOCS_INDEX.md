# TradePanel Command Documentation Index

Complete guide to all command reference documents.

---

## 📖 Available Documents

### 1. **CHEAT_SHEET.txt** ⭐ START HERE
**Best for:** Quick lookup, printing, desk reference  
**Format:** Plain text (TXT) - easily printable  
**Contains:** 
- Side-by-side Windows/Linux command comparison
- All essential commands at a glance
- Emergency commands
- Quick start sequences
- Status check scripts
- Key directories and ports

**When to use:** 
- Need a command RIGHT NOW
- Want to print something for your desk
- Looking for command syntax quickly

---

### 2. **QUICK_COMMANDS.md** ⚡ DAILY USE
**Best for:** Daily workflows, common tasks  
**Format:** Markdown - readable and searchable  
**Contains:**
- Start everything commands
- Test everything commands
- Common tasks table
- API endpoint quick list
- Shell shortcuts/aliases
- Status check scripts
- Emergency fixes
- 30-second setup

**When to use:**
- Starting your workday
- Need to run a common task
- Creating aliases for your shell
- Testing the system

---

### 3. **COMMAND_REFERENCE.md** 📚 COMPREHENSIVE
**Best for:** Deep reference, learning, documentation  
**Format:** Markdown with detailed tables  
**Contains:**
- 12 major command categories
- Detailed command explanations
- Side-by-side Windows/Linux comparisons
- Common workflows (setup, development, backtest, deployment)
- API endpoint reference
- File operations guide
- Monitoring & diagnostics
- Git operations
- Environment variable management
- Troubleshooting guide
- Emergency commands with context

**When to use:**
- Need detailed explanation of a command
- Learning the system
- Setting up for the first time
- Doing complex operations
- Troubleshooting

---

### 4. **POWERSHELL_COMMANDS.md** 🪟 WINDOWS FOCUSED
**Best for:** Windows users, detailed Windows commands  
**Format:** Markdown with many examples  
**Contains:**
- All commands in Windows PowerShell syntax
- 12 command categories with examples
- PowerShell-specific tips
- Quick start instructions
- Status check commands
- Troubleshooting for Windows

**When to use:**
- You exclusively use Windows
- Need Windows-specific syntax
- Setting up Python environment on Windows
- Windows troubleshooting

---

### 5. **QUICK_CHECK.md** ✅ VERIFICATION
**Best for:** Checking if everything works  
**Format:** Markdown - quick reference  
**Contains:**
- Run-everything commands
- Individual quick checks (5-30 seconds each)
- Starting API server
- Testing API endpoints
- Verification commands
- Expected output examples

**When to use:**
- After installation/setup
- Before starting work
- After making changes
- To verify system health

---

## 🎯 Quick Navigation

### I need to...

**Start the application**
→ See: QUICK_COMMANDS.md → "Start Everything"

**Check if everything works**
→ See: QUICK_CHECK.md → "Run Everything at Once"

**Run a backtest**
→ See: COMMAND_REFERENCE.md → "3. Trading Bot Commands"

**View application logs**
→ See: CHEAT_SHEET.txt → "ESSENTIAL COMMANDS"

**Fix a problem**
→ See: COMMAND_REFERENCE.md → "12. Troubleshooting"

**Test the analytics API**
→ See: QUICK_COMMANDS.md → "Test Everything"

**Set up for first time**
→ See: COMMAND_REFERENCE.md → "Common Workflows → Setup & Installation"

**Create shell shortcuts**
→ See: QUICK_COMMANDS.md → "Shortcuts for Your Shell"

**Kill a stuck process**
→ See: CHEAT_SHEET.txt → "EMERGENCY COMMANDS"

**Check database connection**
→ See: COMMAND_REFERENCE.md → "5. Database Commands"

**Monitor performance**
→ See: COMMAND_REFERENCE.md → "9. Monitoring & Diagnostics"

**Deploy to production**
→ See: COMMAND_REFERENCE.md → "Common Workflows → Deployment Checklist"

---

## 📋 Command Categories Matrix

| Category | CHEAT_SHEET | QUICK_COMMANDS | COMMAND_REFERENCE | POWERSHELL_COMMANDS |
|----------|:-----------:|:--------------:|:-----------------:|:------------------:|
| Startup | ✓ | ✓✓ | ✓ | ✓ |
| API Testing | ✓ | ✓✓ | ✓ | ✓ |
| Bot Modes | ✓✓ | ✓ | ✓✓ | ✓ |
| Logs | ✓ | ✓ | ✓ | ✓ |
| Database | ✓ | ✓ | ✓✓ | ✓ |
| File Ops | ✓ | - | ✓✓ | ✓✓ |
| Environment | - | - | ✓✓ | ✓ |
| Git | - | - | ✓ | - |
| Monitoring | ✓ | - | ✓✓ | ✓ |
| Emergency | ✓✓ | ✓ | ✓ | ✓ |

✓ = Covered | ✓✓ = Detailed coverage | - = Not covered

---

## 🔍 How to Search These Docs

### Searching CHEAT_SHEET.txt
- Open in any text editor (Notepad, VS Code, etc.)
- Use Ctrl+F to search for keywords
- Look for section headers in ALL CAPS

### Searching Markdown Files (.md)
- Open in VS Code or any markdown viewer
- Use Ctrl+F to search
- Click on table of contents links if available
- Use header hierarchy (# ## ###) to navigate

### Searching from Command Line
**Windows PowerShell:**
```powershell
Select-String "keyword" CHEAT_SHEET.txt
Select-String "keyword" COMMAND_REFERENCE.md
```

**Linux/Mac:**
```bash
grep -n "keyword" CHEAT_SHEET.txt
grep -n "keyword" COMMAND_REFERENCE.md
```

---

## 📖 Reading Guide by Role

### I'm a **Quick User** (just want to run the bot)
1. Start with: **QUICK_COMMANDS.md**
2. Refer to: **CHEAT_SHEET.txt**
3. Backup: **QUICK_CHECK.md**

### I'm a **Developer** (need deep understanding)
1. Start with: **COMMAND_REFERENCE.md**
2. Reference: **QUICK_COMMANDS.md**
3. Backup: **POWERSHELL_COMMANDS.md** (if on Windows)

### I'm on **Windows**
1. Start with: **CHEAT_SHEET.txt** or **QUICK_COMMANDS.md**
2. Deep dive: **POWERSHELL_COMMANDS.md**
3. Reference: **COMMAND_REFERENCE.md**

### I'm on **Linux/Mac**
1. Start with: **CHEAT_SHEET.txt** or **QUICK_COMMANDS.md**
2. Reference: **COMMAND_REFERENCE.md**
3. Backup: See bash/Linux examples in all docs

### I need to **Troubleshoot**
1. Quick fix: **CHEAT_SHEET.txt** → "EMERGENCY COMMANDS"
2. Detailed: **COMMAND_REFERENCE.md** → "12. Troubleshooting"
3. Search all: Use Ctrl+F for your error message

---

## 💾 Where to Keep These Files

### Recommended Setup
```
TradePanel/
├── CHEAT_SHEET.txt              ← Print this!
├── QUICK_COMMANDS.md            ← Daily use
├── COMMAND_REFERENCE.md         ← Keep for reference
├── POWERSHELL_COMMANDS.md       ← If on Windows
├── QUICK_CHECK.md               ← For verification
└── COMMAND_DOCS_INDEX.md        ← This file
```

### Print These
- **CHEAT_SHEET.txt** - Print and tape to monitor
- **QUICK_COMMANDS.md** - Print for your desk
- **QUICK_CHECK.md** - Print for daily checklist

### Bookmark These
- **COMMAND_REFERENCE.md** - For comprehensive reference
- **POWERSHELL_COMMANDS.md** - Windows users bookmark this

---

## 🔗 File Cross-References

### CHEAT_SHEET.txt References
- Quick command syntax for all major operations
- Status check examples for both platforms
- Key directories and ports
- Essential emergency commands

### QUICK_COMMANDS.md References
- Detailed startup instructions
- Full API endpoint list
- Alias/function creation instructions
- Daily workflow examples

### COMMAND_REFERENCE.md References
- Categorized by operation type (12 categories)
- Detailed explanations with context
- Workflow examples (Setup, Dev, Backtest, Deployment)
- Comprehensive troubleshooting

### POWERSHELL_COMMANDS.md References
- Windows-first perspective
- PowerShell-specific examples
- Windows environment setup
- Windows troubleshooting

---

## 📱 Mobile Reference

For quick lookup on mobile:
1. Keep **QUICK_COMMANDS.md** open in Notes app
2. Screenshot **CHEAT_SHEET.txt** for reference
3. Bookmark **COMMAND_REFERENCE.md** in browser

---

## 🆚 File Size & Format

| File | Size | Format | Best For | Printable |
|------|------|--------|----------|-----------|
| CHEAT_SHEET.txt | ~8 KB | TXT | Quick lookup | ✓✓ |
| QUICK_COMMANDS.md | ~6 KB | Markdown | Daily use | ✓ |
| QUICK_CHECK.md | ~3 KB | Markdown | Verification | ✓✓ |
| COMMAND_REFERENCE.md | ~25 KB | Markdown | Deep reference | ✓ |
| POWERSHELL_COMMANDS.md | ~18 KB | Markdown | Windows users | ✓ |

---

## ⚡ Most Used Commands (By Frequency)

**Daily (10+ times):**
```
python -m uvicorn webapp.main:app --host 0.0.0.0 --port 8000
python main.py --mode paper-trade
curl http://localhost:8000/api/analytics/health
Get-Content logs/main.log -Wait
tail -f logs/main.log
```

**Weekly (2-5 times):**
```
python main.py --mode backtest
python main.py --mode validate
python -m analytics.performance_calculator
```

**Monthly (0-2 times):**
```
python -m venv venv
pip install -r requirements.txt
git push
```

---

## 🎓 Learning Path

**Day 1:** Read QUICK_COMMANDS.md, print CHEAT_SHEET.txt  
**Day 2:** Use QUICK_CHECK.md to verify everything  
**Week 1:** Refer to COMMAND_REFERENCE.md as needed  
**Week 2+:** Have QUICK_COMMANDS.md open all day  

---

## ❓ FAQ About These Docs

**Q: Which file should I print?**
A: Print **CHEAT_SHEET.txt** - it's formatted for printing and has everything.

**Q: Which file has the most detail?**
A: **COMMAND_REFERENCE.md** - it's comprehensive with explanations.

**Q: I'm in a hurry, which file?**
A: **QUICK_COMMANDS.md** - it has what you need, fast.

**Q: I need to check if something works?**
A: **QUICK_CHECK.md** - it's specifically for verification.

**Q: I'm on Windows, which file?**
A: Start with **CHEAT_SHEET.txt**, then use **POWERSHELL_COMMANDS.md**.

**Q: I'm on Linux, which file?**
A: **CHEAT_SHEET.txt** or **COMMAND_REFERENCE.md** - both work great.

**Q: Can I search these files?**
A: Yes! Use Ctrl+F in any text editor or `grep` on Linux/Mac.

---

## 📞 Support

If you can't find a command:
1. Search **CHEAT_SHEET.txt** (Ctrl+F)
2. Search **QUICK_COMMANDS.md** (Ctrl+F)
3. Search **COMMAND_REFERENCE.md** (Ctrl+F) by category
4. Check **POWERSHELL_COMMANDS.md** (Windows only)
5. Check **QUICK_CHECK.md** for verification

---

## 📝 Document Maintenance

| Document | Last Updated | Version | Status |
|----------|--------------|---------|--------|
| CHEAT_SHEET.txt | Apr 24, 2026 | 1.0 | ✓ Current |
| QUICK_COMMANDS.md | Apr 24, 2026 | 1.0 | ✓ Current |
| COMMAND_REFERENCE.md | Apr 24, 2026 | 1.0 | ✓ Current |
| POWERSHELL_COMMANDS.md | Apr 24, 2026 | 1.0 | ✓ Current |
| QUICK_CHECK.md | Apr 24, 2026 | 1.0 | ✓ Current |
| COMMAND_DOCS_INDEX.md | Apr 24, 2026 | 1.0 | ✓ Current |

---

**Start with QUICK_COMMANDS.md or print CHEAT_SHEET.txt - both work great!**

Last Updated: April 24, 2026  
Version: 1.0  
Status: Complete
