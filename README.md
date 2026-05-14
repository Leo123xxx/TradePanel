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

## ✨ Status: 🚀 v1.1 — Dashboard Modernization
**Version**: 1.1.0 "Visual Intelligence"  
**Release Date**: May 11, 2026  
**Consolidation**: [Tier 1 & 2 Fleet](results/STRATEGY_TIER_CONSOLIDATION.md)  
**WFO Mastery**: 5-Window Validation Complete  

### Production Environment
- **Platform**: MetaTrader 5 (MT5)
- **Execution Mode**: `trade` (Tier 1) | `paper` (Tier 2/3)
- **Risk Profile**: 2% per trade | 20% Account Circuit Breaker
- **Dashboard**: http://tradepanel.mraskwhy.local/ (Modernized v1.1 Hub)
- **Caching**: SWR-enabled (TanStack) for high efficiency
- **Notifications**: Telegram (Active)

### Release Milestones (v1.1)
- ✅ **Dashboard Modernization**: Unified high-level overview of active strategy settings and configurations.
- ✅ **Efficiency Boost**: Integrated SWR caching to reduce redundant API requests and improve UI responsiveness.
- ✅ **Advanced Filtering**: Added server-side filtering for backtests (Win Rate, Sharpe, Profit Factor, Drawdown).
- ✅ **Intelligence Expansion**: Real-time cross-referencing between live config and performance metrics.
- ✅ **Fleet Consolidation**: 12 Tier 1 strategies promoted to production.

---

## 📊 V1.0 Strategy Performance Baseline

| Tier | Strategies | Selection Criteria |
|------|------------|--------------------|
| **TIER 1** | 12 | WR ≥ 65%, Sharpe > 5, Trades ≥ 6 (Mastered) |
| **TIER 2** | 20+ | WR ≥ 50%, Sharpe > 3, Trades ≥ 5 (High Conviction) |
| **TIER 3** | 50+ | WR ≥ 50%, Sharpe > 3, Trades ≥ 3 (Under Watch) |

Baseline WFO Validation: [wfo_master_summary.md](results/wfo_master_summary.md)

---

## 🏗 What's Live

- **23+ Strategies** — Trend, mean reversion, breakouts, scalping, ICT
- **Risk Management** — ATR-based lot sizing, 20% DD circuit breaker, breakeven SL at 1:1 RR
- **Multi-Timeframe** — M15, H1, H4, D1
- **18 Pairs** — Gold, Silver, FX, Crypto, Indices, US Stock CFDs
- **Paper + Live Mode** — Full paper engine with MT5 execution
- **Dashboard** — Real-time P&L, http://tradepanel.mraskwhy.local/, Signals tab (per-account signal monitor), Accounts tab
- **Telegram Bot** — Trade open/close alerts, signal digests (✅ TAKEN / ⏳ Not taken)
- **Scheduler** — Overnight backtests, daily data sync, recommendations engine

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| **[README.md](README.md)** | Overview & quick start (this file) |
| **[GETTING_STARTED](docs/GETTING_STARTED.md)** | Install, configure, run |
| **[STRATEGIES](docs/STRATEGIES.md)** | All 23+ strategies explained |
| **[TROUBLESHOOTING](docs/TROUBLESHOOTING.md)** | Debug guides & common fixes |
| **[ARCHITECTURE](docs/ARCHITECTURE.md)** | System design & API reference |
| **[TRADEPANEL_SKILLS](docs/TRADEPANEL_SKILLS.md)** | Session patterns & gotchas |
| **[Handover Doc](TradePanel/TradePanel_Handover_2026-05-06.docx)** | Full live-readiness handover |

**Archive:** Stale pre-launch docs are in `docs/archive/`.

---

## 🔧 Management CLI

```powershell
.\trade.bat start    # Start all services (Docker + MT5 Bridge)
.\trade.bat stop     # Stop all services
.\trade.bat status   # Show container status
.\trade.bat logs     # Tail all service logs
.\trade.bat rebuild  # Force rebuild and restart
```

### Docker Status Check
```powershell
docker compose ps        # All 7 containers should be healthy
docker compose logs -f   # Live log stream
```

### DB (Adminer)
- URL: http://localhost:8080
- Server: `host.docker.internal:5433` | DB: `trading_platform` | User: `trader` | Password: `traderpass`

---

**Status**: 🚀 v1.0 Bot Live | **Release Date**: May 10, 2026
