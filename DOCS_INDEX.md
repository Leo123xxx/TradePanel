# Documentation Index

**All TradePanel documentation consolidated into 5 files.**

---

## Quick Navigation

| File | Purpose | When to Read |
|------|---------|--------------|
| **README.md** | Overview & features | New to the project |
| **GETTING_STARTED.md** | Setup & installation | Installing or configuring |
| **STRATEGIES.md** | All 23+ strategies explained | Understanding trading logic |
| **TROUBLESHOOTING.md** | Debug guides & common fixes | Something isn't working |
| **ARCHITECTURE.md** | System design & API reference | Technical deep dives |
| **DEBUG_SUMMARY.md** | Latest fixes (2026-04-24) | Understanding recent changes |

---

## Reading Order by Use Case

### 🚀 "I want to get started"
1. README.md
2. GETTING_STARTED.md
3. Start trading with `python main.py paper-trade`

### 💡 "I want to understand strategies"
1. STRATEGIES.md (Top 5 Performers section)
2. ARCHITECTURE.md (Trade Execution Flow)
3. Explore strategy files in `strategies/` directory

### 🐛 "Something isn't working"
1. TROUBLESHOOTING.md (Execution Blockers section)
2. DEBUG_SUMMARY.md (what was recently fixed)
3. Check logs: `tail -f logs/*.log`

### 🔧 "I want to configure everything"
1. ARCHITECTURE.md (Configuration Reference)
2. GETTING_STARTED.md (Configuration section)
3. Edit `config/config.yaml` and `config/strategies.yaml`

### 📊 "I want to understand the API"
1. ARCHITECTURE.md (API Reference section)
2. View OpenAPI docs: http://localhost:8000/docs

---

## File Sizes & Content

```
README.md              1.5 KB  - Project overview
GETTING_STARTED.md     5.7 KB  - Installation & setup guide
STRATEGIES.md          9.6 KB  - All strategies + validation
TROUBLESHOOTING.md     8.5 KB  - Debug guides + 7 blockers
ARCHITECTURE.md       15.0 KB  - System design + API reference
DEBUG_SUMMARY.md      ~4.0 KB  - Latest fixes applied
─────────────────────────────
TOTAL:               ~44.0 KB  - Complete documentation
```

---

## What's Documented

### ✅ Configuration
- System settings (config.yaml)
- Strategy definitions (strategies.yaml)
- Risk management parameters
- Trading hours
- Notification settings

### ✅ Installation
- Prerequisites
- Virtual environment setup
- Dependency installation
- Account configuration
- Database setup (optional)

### ✅ Strategies
- All 23+ strategies listed
- Top 5 performers explained
- Parameters and ranges
- Regime conditions
- Performance metrics

### ✅ Troubleshooting
- 7 execution blockers
- 10+ common issues & fixes
- Debug checklist
- Log viewing guide
- Recent fixes (2026-04-24)

### ✅ System Architecture
- Component diagram
- Trade execution flow
- Risk management checks
- API endpoints
- Database schema
- Scheduler jobs

### ✅ Monitoring
- Dashboard access
- Log locations
- Performance metrics
- Health checks

---

## What Was Removed

**Old Documentation** (consolidated into these 5 files):
- `validation/README.md` → STRATEGIES.md
- `validation/INDEX.md` → This file + DOCS_INDEX.md
- `validation/test_workflow.md` → STRATEGIES.md (Validation Framework)
- `docs/archive/Phase1_Execution_Plan.md` → Archived (obsolete)

**Validation folder** still exists for reference:
- `validation/strategies_structured.md`
- `validation/validation_config.yaml`
- `validation/test_runner.py`

These can be referenced but are not required for normal operation.

---

## How to Use This Documentation

1. **Start with README.md** — Get overview
2. **Jump to relevant section** — Use table above
3. **Search across files** — Most topics covered
4. **Check logs** — Real-time debugging
5. **Use ARCHITECTURE.md** — For technical details

---

## Keeping Documentation Updated

When you make changes:
1. Update relevant documentation file
2. Keep sections in same order for easy navigation
3. Add to DEBUG_SUMMARY.md if significant fix
4. Note date of changes

---

## Quick Links

| Need | File | Section |
|------|------|---------|
| Installation | GETTING_STARTED.md | Installation |
| Strategies | STRATEGIES.md | Top 5 Performers |
| Debugging | TROUBLESHOOTING.md | 7 Blockers |
| Configuration | ARCHITECTURE.md | Configuration Reference |
| API | ARCHITECTURE.md | API Reference |

---

**All documentation is in root folder for easy access.**

