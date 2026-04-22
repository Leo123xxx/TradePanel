# 📖 STRATEGY GUIDE (LEODEX V2)

This guide documents the 25 strategies currently integrated into the **TradePanel** ecosystem. Strategies are ranked from TIER 1 (Production Ready) to TIER 3 (Experimental).

## 🏆 TIER 1: CORE PORTFOLIO
These strategies have passed multiple Walk-Forward windows with a Profit Factor > 1.3 and stable win rates.

| Strategy | Category | Description |
| :--- | :--- | :--- |
| **Triple MACD** | Trend | 3-layer alignment (M5/H1/H4) with trend filter. |
| **Swing Pullback** | Trend | Enters the dominant trend on deep Fibonacci/ATR pullbacks. |
| **Range Breakout** | Breakout | High-resolution H4 range expansion detection. |
| **EMA Ribbon** | Trend | Scalping entries based on EMA cross-alignment in crypto. |

## 🧪 TIER 2: VALIDATION QUEUE
Strategies that show promise but require tighter session tuning or regime filtering.

### 🏛️ Institutional Flow (SMC)
- **ICT Silver Bullet**: Killzone-based liquidity sweeps and FVG entries.
- **Judas Swing**: Asian range fakeouts at London Open.
- **Turtle Soup**: Major historical liquidity pool sweeps.

### 📉 Mean Reversion
- **RSI-2 Extremes**: Professional-grade oscillator overextension logic.
- **VWAP Shift**: Statistical deviation from volume-weighted price.
- **Hikkake Trap**: Inside bar breakout failure and reversal.

## 🔬 TIER 3: EXPERIMENTAL / ARCHIVE
Strategies that currently have a Profit Factor < 1.1 or are undergoing significant rewrite.
- **MA Crossover**: Standard lagging cross; requires heavy regime filtering.
- **BB Mean Reversion**: Mean reversion without sufficient volatility confirmation.

---
## 🛠️ Configuration
Parameters for all strategies are maintained in [config/strategies.yaml](../config/strategies.yaml).

> [!TIP]
> Always run `scripts/run_walk_forward.py` before promoting a strategy from Tier 2 to Tier 1.

---
*Back to [GETTING_STARTED.md](GETTING_STARTED.md).*
