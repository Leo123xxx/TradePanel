# Strategies Documentation

Complete reference for all 23+ trading strategies in TradePanel.

---

## Overview

This framework includes **23+ fully implemented strategies** covering:
- **Trend Following** — MA Crossover, EMA Ribbon, MACD Trend, Dual EMA
- **Mean Reversion** — RSI Bounce, Bollinger Bands, Stochastic, VWAP
- **Breakout** — Range Breakout, Volatility Squeeze, Opening Range
- **Scalping** — Triple MACD, Institutional Silver Bullet
- **SMC** — ICT Judas Swing, Turtle Soup, Hikkake Trap
- **Advanced** — Stat Arb, Price Action, COT Sentiment

---

## How Strategies Work

### Strategy Structure
Each strategy inherits from `BaseStrategy`:

```python
class MyStrategy(BaseStrategy):
    def __init__(self, params=None):
        super().__init__(
            name="my_strategy",
            category="Trend",
            params={
                "period": 20,
                "tp_atr_mult": 2.0,
                "sl_atr_mult": 1.0,
            },
            regime=["TRENDING", "ANY"],
            timeframes=["H1", "H4"],
            pairs=["EURUSD", "XAUUSD"]
        )
    
    def generate_signals(self, data):
        # data is DataFrame with OHLCV
        # Return DataFrame with 'signal' column: 1=BUY, -1=SELL, 0=HOLD
        ...
```

### Signal Generation
- **Input**: OHLCV DataFrame for symbol/timeframe
- **Output**: DataFrame with 'signal' column
- **Timing**: Entry on next bar open after signal close
- **Exit**: Via take profit (TP) or stop loss (SL)

### Parameters
All strategies use `{param: [min, max]}` bounds to prevent overfitting:

```yaml
parameters:
  fast_period: [5, 20]        # Range: 5 to 20
  slow_period: [20, 100]      # Range: 20 to 100
  tp_atr_mult: [1.0, 4.0]     # TP: 1–4 × ATR
  sl_atr_mult: [0.5, 2.0]     # SL: 0.5–2 × ATR
```

---

## Top 5 Performers

### 1. Dual EMA Fractal (55.62% Win Rate) ⭐ BEST

**Type**: Trend Following  
**Assets**: EURUSD  
**Timeframes**: H1  
**Regime**: TRENDING

**How It Works**:
- Uses 200-period EMA as trend filter
- Identifies fractal support/resistance levels
- Enters on fractal breakout in trend direction
- TP/SL based on ATR

**Parameters**:
```yaml
ema_period: [150, 250]        # Default: 200
tp_atr_mult: [1.5, 3.0]       # Default: 2.0
sl_atr_mult: [1.0, 2.0]       # Default: 1.5
```

**Best For**: Trending markets, EURUSD during London/NY overlap

---

### 2. COT Sentiment (52.55% Win Rate)

**Type**: Advanced / Sentiment  
**Assets**: XAUUSD, EURUSD, GBPUSD  
**Timeframes**: D1, W1  
**Regime**: TRENDING

**How It Works**:
- Reads COT (Commitments of Traders) sentiment
- Long entries when large traders are bullish
- Short entries when sentiment is bearish
- Filters with EMA for trend confirmation

**Parameters**:
```yaml
sentiment_threshold: [70, 90]  # Conviction level
ema_filter: [40, 60]           # Trend confirmation
```

**Best For**: Longer-term trades, fundamental analysis

---

### 3. RSI Bounce (52.16% Win Rate)

**Type**: Mean Reversion  
**Assets**: EURUSD  
**Timeframes**: H1  
**Regime**: RANGING

**How It Works**:
- Enters when RSI oversold/overbought
- Waits for bounce confirmation
- Exits on RSI mean reversion completion
- Works best in choppy markets

**Parameters**:
```yaml
rsi_period: [10, 20]           # Default: 14
oversold: [20, 35]             # Default: 30
overbought: [65, 80]           # Default: 70
tp_atr_mult: [1.0, 2.0]        # Default: 1.5
```

**Best For**: Ranging markets, intraday trading

---

### 4. VWAP Momentum (51.05% Win Rate)

**Type**: Mean Reversion  
**Assets**: GBPUSD  
**Timeframes**: M15, M30  
**Regime**: RANGING / HIGH_VOL

**How It Works**:
- Uses Volume Weighted Average Price
- Enters when price deviates >2 std devs from VWAP
- Expects mean reversion to VWAP
- Tight stops, quick exits

**Parameters**:
```yaml
std_dev_mult: [1.5, 3.0]       # Deviation threshold
atr_period: [10, 20]           # Volatility measure
tp_atr_mult: [1.0, 2.0]        # Default: 1.5
```

**Best For**: Scalping, volatile pairs

---

### 5. Session Momentum (50.70% Win Rate)

**Type**: Session-Based  
**Assets**: XAUUSD  
**Timeframes**: H1  
**Regime**: TRENDING / ANY

**How It Works**:
- Trades London/NY session overlaps
- Identifies high/low of previous session
- Enters on breakout confirmation
- Uses momentum confirmation

**Parameters**:
```yaml
session_start_utc: [13, 14]    # London 13:00 UTC
session_end_utc: [17, 18]      # End time
high_low_buffer_pips: [20, 50] # Default: 20
```

**Best For**: Gold trading, session-based entries

---

## All 23+ Strategies

### Trend Following (5)
| Strategy | Win % | Asset | TF | Regime |
|----------|-------|-------|----|----|
| Dual EMA Fractal | 55.62% | EURUSD | H1 | TRENDING |
| EMA Ribbon Trend | — | BTCUSD | H4 | TRENDING |
| MACD Trend | — | EURUSD, USDJPY | H1 | ANY |
| Dual EMA Momentum | — | XAUUSD | H1, H4 | TRENDING |
| MA Crossover | 50.38% | EURUSD | H1 | TRENDING |

### Mean Reversion (6)
| Strategy | Win % | Asset | TF |
|----------|-------|-------|-----|
| RSI Bounce | 52.16% | EURUSD | H1 |
| RSI 2 (Extreme RSI) | 49.98% | USDJPY | H4, D1 |
| Bollinger Band MR | — | XAUUSD | H1 |
| Stochastic Divergence | — | EURUSD | H4 |
| VWAP Momentum | 51.05% | GBPUSD | M15, M30 |
| Crypto RSI Extremes | — | USDJPY | H4, D1 |

### Breakout (5)
| Strategy | Win % | Asset | TF |
|----------|-------|-------|-----|
| Range Breakout | 49.59% | XAUUSD | H4 |
| Volatility Squeeze | — | GBPUSD | H4, D1 |
| Opening Range (ORB) | — | XAGUSD | M15, H1 |
| RVGI-CCI Confluence | — | EURUSD | H1 |
| Gold Momentum Breakout | — | XAUUSD, GBPUSD | H1 |

### Scalping (2)
| Strategy | Win % | Asset | TF |
|----------|-------|-------|-----|
| Triple MACD Scalping | — | **XAUUSD** | H1 |
| Institutional Silver Bullet | — | EURUSD | M5, M15 |

### SMC (3)
| Strategy | Win % | Asset | TF | Status |
|----------|-------|-------|-----|---------|
| Turtle Soup | 49.25% | EURUSD | H1, H4 | ACTIVE |
| ICT Judas Swing | — | EURUSD | M15, H1 | STAGING |
| Hikkake Trap | — | XAUUSD | H4, D1 | ACTIVE |

### Advanced (6+)
| Strategy | Win % | Asset | TF |
|----------|-------|-------|-----|
| COT Sentiment | 52.55% | XAU, EUR, GBP | D1, W1 |
| Stat Arb (Gold/Silver) | — | XAUUSD | H4 |
| Session Momentum | 50.70% | XAUUSD | H1 |
| Naked Price Action | — | USDJPY | H4 |
| Ensemble Voting | — | Multi | H1, H4, D1 |
| ML Classifier | — | XAUUSD | H1, H4 |

---

## Configuration Examples

### Enable a Strategy
```yaml
# config/strategies.yaml
dual_ema_fractal:
  enabled: true
  tier: TIER_3
  pairs: [EURUSD]
  timeframes: [H1]
  parameters:
    ema_period: 200
    tp_atr_mult: 2.0
    sl_atr_mult: 1.5
```

### Add to Active Trading
```yaml
# config/config.yaml
strategies:
  - name: dual_ema_fractal
    enabled: true
    pairs: [EURUSD]
    timeframes: [H1]
```

### Custom Parameters
```yaml
# Override defaults per pair
pair_overrides:
  XAUUSD:
    ema_period: 180      # Slightly shorter for gold
    tp_atr_mult: 2.5     # Wider targets
```

---

## Strategy Selection Guide

### For TRENDING Markets
→ Dual EMA Fractal, EMA Ribbon, MACD Trend, Session Momentum

### For RANGING Markets
→ RSI Bounce, Bollinger Bands, Stochastic Divergence, Turtle Soup

### For VOLATILE Markets
→ VWAP Momentum, Volatility Squeeze, Gold Momentum Breakout

### For SCALPING (1m-M30)
→ Triple MACD, Institutional Silver Bullet, VWAP Momentum

### For SWING TRADING (H4-D1)
→ Turtle Soup, Hikkake Trap, COT Sentiment, Stat Arb

---

## Validation Framework

All strategies go through **6-phase testing**:

| Phase | Duration | Tests | Pass Rate |
|-------|----------|-------|-----------|
| **1. Unit Test** | 1 hr | Syntax, logic | 100% |
| **2. Backtest** | 4 hrs | 2+ years data | >50% |
| **3. OOS Validation** | 2 hrs | 20% holdout data | >40% |
| **4. Forward Test** | 4 wks | Paper trading | >30% |
| **5. Acceptance** | 2 hrs | Final review | >20% |
| **6. Live Micro** | 6 wks | Real money (mini) | >10% |

**Acceptance Criteria**:
- Sharpe ≥ 1.0 (backtest)
- Win Rate ≥ 50%
- Max Drawdown ≤ 15%
- OOS Sharpe ≥ 70% of IS

---

## Creating Custom Strategies

See `strategies/base_strategy.py` for the template.

### Example: Simple MA Crossover
```python
from strategies.base_strategy import BaseStrategy
import ta_compat as ta

class MyMACrossover(BaseStrategy):
    def __init__(self, params=None):
        params = params or {
            "fast": 9,
            "slow": 21,
            "tp_atr_mult": 2.0,
            "sl_atr_mult": 1.0,
        }
        super().__init__(
            name="my_ma_crossover",
            category="Trend",
            params=params,
            timeframes=["H1"],
            pairs=["EURUSD"]
        )
    
    def generate_signals(self, data):
        # Add moving averages
        data['fast_ma'] = ta.sma(data['close'], self.params["fast"])
        data['slow_ma'] = ta.sma(data['close'], self.params["slow"])
        
        # Generate signals
        data['signal'] = 0
        data.loc[data['fast_ma'] > data['slow_ma'], 'signal'] = 1   # BUY
        data.loc[data['fast_ma'] < data['slow_ma'], 'signal'] = -1  # SELL
        
        return data[['signal']]
```

### Add to Engine
1. Save in `strategies/my_ma_crossover.py`
2. Import in `forward_test/paper_engine.py`
3. Add to `STRATEGY_REGISTRY`
4. Enable in `config/strategies.yaml`

---

## Performance Tracking

Monitor each strategy:

```bash
# View performance by strategy
python -m scripts.strategy_performance \
  --since 2026-01-01 \
  --metrics sharpe win_rate drawdown
```

Results show:
- Win rate per strategy
- Sharpe ratio
- Max drawdown
- Average trade duration
- Profit factor

---

**Need help? Check TROUBLESHOOTING.md or ARCHITECTURE.md**

