# Near-PASS Optimization Results

**Generated:** 2026-05-10T13:41:06.797251

## Overview

| Strategy | Pairs Tested | Best Sharpe | Best WR% | Status |
|----------|--------------|-------------|---------|--------|
| hikkake_trap | 1 | 2.67 | 60.0 | PARTIAL |
| session_momentum | - | - | - | [ERR] |
| range_breakout | - | - | - | [ERR] |
| dual_ema_momentum | - | - | - | [ERR] |
| rsi_pullback | - | - | - | [ERR] |
| rsi_extremes_scalp | 1 | -929.19 | 0.0 | WORKING |
| ema_ribbon_trend | - | - | - | [ERR] |


## Detailed Results

### HIKKAKE_TRAP

**Total combos tested:** 96

#### #1 — GBPUSD H4

- **Score:** 1.428
- **Sharpe:** 2.669
- **Win Rate:** 60.0%
- **Profit Factor:** 1.46
- **Max Drawdown:** 0.9%
- **Trades:** 10
- **PnL (ZAR):** R1461.34

**Parameters:**
```

  cooldown_bars: 2

  tp_atr_mult: 1.5

  sl_atr_mult: 0.6

  atr_period: 14

```

#### #2 — GBPUSD H4

- **Score:** 1.428
- **Sharpe:** 2.669
- **Win Rate:** 60.0%
- **Profit Factor:** 1.46
- **Max Drawdown:** 0.9%
- **Trades:** 10
- **PnL (ZAR):** R1461.34

**Parameters:**
```

  cooldown_bars: 3

  tp_atr_mult: 1.5

  sl_atr_mult: 0.6

  atr_period: 14

```

#### #3 — GBPUSD H4

- **Score:** 1.428
- **Sharpe:** 2.669
- **Win Rate:** 60.0%
- **Profit Factor:** 1.46
- **Max Drawdown:** 0.9%
- **Trades:** 10
- **PnL (ZAR):** R1461.34

**Parameters:**
```

  cooldown_bars: 4

  tp_atr_mult: 1.5

  sl_atr_mult: 0.6

  atr_period: 14

```

#### #4 — GBPUSD H4

- **Score:** 1.416
- **Sharpe:** 2.639
- **Win Rate:** 60.0%
- **Profit Factor:** 1.46
- **Max Drawdown:** 0.9%
- **Trades:** 10
- **PnL (ZAR):** R1484.58

**Parameters:**
```

  cooldown_bars: 2

  tp_atr_mult: 1.5

  sl_atr_mult: 0.6

  atr_period: 10

```

#### #5 — GBPUSD H4

- **Score:** 1.416
- **Sharpe:** 2.639
- **Win Rate:** 60.0%
- **Profit Factor:** 1.46
- **Max Drawdown:** 0.9%
- **Trades:** 10
- **PnL (ZAR):** R1484.58

**Parameters:**
```

  cooldown_bars: 3

  tp_atr_mult: 1.5

  sl_atr_mult: 0.6

  atr_period: 10

```

### RSI_EXTREMES_SCALP

**Total combos tested:** 12

#### #1 — USOIL M15

- **Score:** -371.676
- **Sharpe:** -929.190
- **Win Rate:** 0.0%
- **Profit Factor:** 0.00
- **Max Drawdown:** 2.3%
- **Trades:** 40
- **PnL (ZAR):** R-4228.30

**Parameters:**
```

  rsi_period: 7

  oversold: 30

  overbought: 80

  tp_atr_mult: 2.0

  sl_atr_mult: 0.8

  atr_period: 14

```

#### #2 — USOIL M15

- **Score:** -373.347
- **Sharpe:** -933.368
- **Win Rate:** 0.0%
- **Profit Factor:** 0.00
- **Max Drawdown:** 3.4%
- **Trades:** 59
- **PnL (ZAR):** R-6247.36

**Parameters:**
```

  rsi_period: 7

  oversold: 30

  overbought: 70

  tp_atr_mult: 2.0

  sl_atr_mult: 0.8

  atr_period: 14

```

#### #3 — USOIL M15

- **Score:** -380.646
- **Sharpe:** -951.616
- **Win Rate:** 0.0%
- **Profit Factor:** 0.00
- **Max Drawdown:** 3.1%
- **Trades:** 53
- **PnL (ZAR):** R-5611.54

**Parameters:**
```

  rsi_period: 7

  oversold: 25

  overbought: 70

  tp_atr_mult: 2.0

  sl_atr_mult: 0.8

  atr_period: 14

```

#### #4 — USOIL M15

- **Score:** -387.752
- **Sharpe:** -969.380
- **Win Rate:** 0.0%
- **Profit Factor:** 0.00
- **Max Drawdown:** 2.7%
- **Trades:** 47
- **PnL (ZAR):** R-4981.64

**Parameters:**
```

  rsi_period: 7

  oversold: 30

  overbought: 75

  tp_atr_mult: 2.0

  sl_atr_mult: 0.8

  atr_period: 14

```

#### #5 — USOIL M15

- **Score:** -399.386
- **Sharpe:** -998.464
- **Win Rate:** 0.0%
- **Profit Factor:** 0.00
- **Max Drawdown:** 0.6%
- **Trades:** 11
- **PnL (ZAR):** R-1168.24

**Parameters:**
```

  rsi_period: 14

  oversold: 25

  overbought: 70

  tp_atr_mult: 2.0

  sl_atr_mult: 0.8

  atr_period: 14

```


## Recommendations

### [NEAR] Near-PASS (Close to Promotion)

The following 2 strateg(y/ies) show improvement but need tuning:


- **hikkake_trap** — Review top parameter sets above

- **rsi_extremes_scalp** — Review top parameter sets above


## Next Steps

1. Review promoted strategies' parameters in detail

2. Validate promising parameters with extended backtest window

3. Update `config/strategies.yaml` with new parameters for promoted strategies

4. Re-run overnight backtest to confirm improvements
