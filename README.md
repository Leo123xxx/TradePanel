# TradePanel — MT5 Algorithmic Trading Bot

**A production-grade Python trading bot for MetaTrader 5 with 23+ strategies, risk management, and real-time monitoring.**

---

## 🎯 Pick Your Path

### 🚀 "I want to get trading NOW"
1. [README.md](README.md) (2 min read)
2. [GETTING_STARTED.md](docs/GETTING_STARTED.md) → Installation section
3. Run: `.\trade.bat start`

### 📖 "I want to understand the system"
1. [README.md](README.md)
2. [STRATEGIES.md](docs/STRATEGIES.md) (all strategies explained)
3. [ARCHITECTURE.md](docs/ARCHITECTURE.md) (system design)

### 🐛 "Something isn't working"
1. [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) (7 blockers + 10+ fixes)
2. Check logs: `.\trade.bat logs`

---

## ✨ Status: ✅ Stabilized & Operational
**Latest Update**: May 5, 2026 — Documentation & Script Consolidation

- **23+ Strategies** — Trend, mean reversion, breakouts, scalping
- **Risk Management** — Position sizing, drawdown limits, margin checks
- **Multi-Timeframe** — M5, M15, M30, H1, H4, D1, W1
- **Multi-Asset** — Gold, Silver, FX, Crypto
- **Paper & Live** — Test before going live
- **Dashboard** — Real-time P&L and metrics
- **Alerts** — Telegram notifications

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| **[README.md](README.md)** | Overview & quick start (this file) |
| **[GETTING_STARTED](docs/GETTING_STARTED.md)** | Install, configure, run |
| **[STRATEGIES](docs/STRATEGIES.md)** | All 23+ strategies explained |
| **[TROUBLESHOOTING](docs/TROUBLESHOOTING.md)** | Debug guides & common fixes |
| **[ARCHITECTURE](docs/ARCHITECTURE.md)** | System design & API reference |

**Archive:** Older documentation can be found in `archive/docs/`.

---

## 🔧 Management CLI

Use the unified `trade.bat` script for all operations:

```powershell
.\trade.bat start    # Start all services (Docker + MT5 Bridge)
.\trade.bat stop     # Stop all services
.\trade.bat status   # Show container status
.\trade.bat logs     # Tail all service logs
.\trade.bat rebuild  # Force rebuild and restart
```

---

**Status**: ✅ Production Ready | **Updated**: May 5, 2026
