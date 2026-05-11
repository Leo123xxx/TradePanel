# Overnight Backtest Report — 09 May 2026

Generated: 2026-05-09 03:27 UTC

## Summary

| | Count |
|---|---|
| ✅ PASS | 1 |
| ⚠️ REVIEW | 37 |
| ❌ ERROR/SKIP | 0 |
| **Total combos** | **38** |

---

## ✅ Passing Strategies

| Strategy | Pair | TF | Tier | WR% | Sharpe | MaxDD% | Trades | PF |
|---|---|---|---|---|---|---|---|---|
| ema_ribbon_trend | ETHUSD | D1 | T0 | 100.0 | 14.07 | 0.0 | 2 | 999.00 |

---

## ⚠️ Strategies Needing Review


### ema_ribbon_trend | ETHUSD | H4
WR=71.4%  Sharpe=-5.60  MaxDD=0.3%  Trades=7

**Parameter Tweaks:**
- Win rate 71.4% — consider increasing TP mult (tp_atr_mult +0.5) to capture more profit
- Only 7 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -5.60 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.24 — marginal edge, consider disabling on ETHUSD unless confirmed by live data

### donchian_trend | BTCUSD | D1
WR=58.9%  Sharpe=2.92  MaxDD=12.4%  Trades=73

**Parameter Tweaks:**
- Win rate 58.9% < 70.0% → tighten entry filter (increase ADX min or add regime check)

### donchian_trend | BTCUSD | H4
WR=56.4%  Sharpe=0.56  MaxDD=25.8%  Trades=307

**Parameter Tweaks:**
- Win rate 56.4% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 25.8% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe 0.56 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 1.09 — marginal edge, consider disabling on BTCUSD unless confirmed by live data

### donchian_trend | ETHUSD | H4
WR=52.4%  Sharpe=-0.55  MaxDD=2.8%  Trades=340

**Parameter Tweaks:**
- Win rate 52.4% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -0.55 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.92 — marginal edge, consider disabling on ETHUSD unless confirmed by live data

### donchian_trend | ETHUSD | H1
WR=48.6%  Sharpe=-2.63  MaxDD=10.7%  Trades=1152

**Parameter Tweaks:**
- Win rate 48.6% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.63 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.66 — marginal edge, consider disabling on ETHUSD unless confirmed by live data

### donchian_trend | BTCUSD | H1
WR=47.9%  Sharpe=-1.41  MaxDD=93.1%  Trades=1105

**Parameter Tweaks:**
- Win rate 47.9% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 93.1% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -1.41 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.80 — marginal edge, consider disabling on BTCUSD unless confirmed by live data

### donchian_trend | ETHUSD | D1
WR=46.5%  Sharpe=-0.97  MaxDD=2.9%  Trades=86

**Parameter Tweaks:**
- Win rate 46.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -0.97 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.85 — marginal edge, consider disabling on ETHUSD unless confirmed by live data

### crypto_rsi_extremes | BTCUSD | H1
WR=42.9%  Sharpe=-3.46  MaxDD=35.1%  Trades=210

**Parameter Tweaks:**
- Win rate 42.9% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 35.1% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -3.46 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.58 — marginal edge, consider disabling on BTCUSD unless confirmed by live data

### ema_ribbon_trend | BTCUSD | H1
WR=42.6%  Sharpe=-3.84  MaxDD=12.6%  Trades=54

**Parameter Tweaks:**
- Win rate 42.6% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -3.84 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.54 — marginal edge, consider disabling on BTCUSD unless confirmed by live data

### crypto_rsi_extremes | BTCUSD | M15
WR=42.3%  Sharpe=-4.11  MaxDD=54.1%  Trades=537

**Parameter Tweaks:**
- Win rate 42.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 54.1% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -4.11 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.52 — marginal edge, consider disabling on BTCUSD unless confirmed by live data

### silver_bullet_crypto | BTCUSD | M5
WR=40.3%  Sharpe=-3.74  MaxDD=12.8%  Trades=186

**Parameter Tweaks:**
- Win rate 40.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -3.74 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.59 — marginal edge, consider disabling on BTCUSD unless confirmed by live data

### power_of_3_amd | ETHUSD | H1
WR=39.9%  Sharpe=-2.97  MaxDD=4.4%  Trades=371

**Parameter Tweaks:**
- Win rate 39.9% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -2.97 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.65 — marginal edge, consider disabling on ETHUSD unless confirmed by live data

### power_of_3_amd | BTCUSD | H1
WR=39.7%  Sharpe=-1.61  MaxDD=35.1%  Trades=370

**Parameter Tweaks:**
- Win rate 39.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 35.1% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -1.61 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.79 — marginal edge, consider disabling on BTCUSD unless confirmed by live data

### silver_bullet_crypto | BTCUSD | M15
WR=39.6%  Sharpe=-1.51  MaxDD=7.2%  Trades=154

**Parameter Tweaks:**
- Win rate 39.6% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.51 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.80 — marginal edge, consider disabling on BTCUSD unless confirmed by live data

### power_of_3_amd | BTCUSD | M5
WR=39.5%  Sharpe=-5.23  MaxDD=11.2%  Trades=134

**Parameter Tweaks:**
- Win rate 39.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -5.23 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.49 — marginal edge, consider disabling on BTCUSD unless confirmed by live data

### crypto_rsi_extremes | ETHUSD | H1
WR=39.2%  Sharpe=-4.83  MaxDD=3.0%  Trades=227

**Parameter Tweaks:**
- Win rate 39.2% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -4.83 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.49 — marginal edge, consider disabling on ETHUSD unless confirmed by live data

### power_of_3_amd | BTCUSD | M15
WR=39.0%  Sharpe=-3.32  MaxDD=31.4%  Trades=351

**Parameter Tweaks:**
- Win rate 39.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 31.4% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -3.32 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.62 — marginal edge, consider disabling on BTCUSD unless confirmed by live data

### crypto_rsi_extremes | ETHUSD | D1
WR=37.5%  Sharpe=-7.86  MaxDD=0.6%  Trades=8

**Parameter Tweaks:**
- Win rate 37.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 8 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -7.86 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.30 — marginal edge, consider disabling on ETHUSD unless confirmed by live data

### power_of_3_amd | ETHUSD | M15
WR=37.5%  Sharpe=-6.48  MaxDD=3.2%  Trades=355

**Parameter Tweaks:**
- Win rate 37.5% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -6.48 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.39 — marginal edge, consider disabling on ETHUSD unless confirmed by live data

### ema_ribbon_trend | ETHUSD | H1
WR=37.2%  Sharpe=-4.74  MaxDD=0.7%  Trades=43

**Parameter Tweaks:**
- Win rate 37.2% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -4.74 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.49 — marginal edge, consider disabling on ETHUSD unless confirmed by live data

### multi_ema_crypto_scalper | ETHUSD | H1
WR=36.9%  Sharpe=-1.61  MaxDD=3.7%  Trades=623

**Parameter Tweaks:**
- Win rate 36.9% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -1.61 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.78 — marginal edge, consider disabling on ETHUSD unless confirmed by live data

### silver_bullet_crypto | ETHUSD | M15
WR=36.1%  Sharpe=-5.77  MaxDD=1.5%  Trades=169

**Parameter Tweaks:**
- Win rate 36.1% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -5.77 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.44 — marginal edge, consider disabling on ETHUSD unless confirmed by live data

### multi_ema_crypto_scalper | BTCUSD | M15
WR=34.9%  Sharpe=-2.36  MaxDD=92.0%  Trades=1277

**Parameter Tweaks:**
- Win rate 34.9% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 92.0% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -2.36 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.71 — marginal edge, consider disabling on BTCUSD unless confirmed by live data

### multi_ema_crypto_scalper | BTCUSD | H1
WR=34.8%  Sharpe=-0.53  MaxDD=38.1%  Trades=615

**Parameter Tweaks:**
- Win rate 34.8% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 38.1% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -0.53 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.92 — marginal edge, consider disabling on BTCUSD unless confirmed by live data

### silver_bullet_crypto | ETHUSD | H1
WR=34.8%  Sharpe=-3.09  MaxDD=1.1%  Trades=92

**Parameter Tweaks:**
- Win rate 34.8% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -3.09 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.63 — marginal edge, consider disabling on ETHUSD unless confirmed by live data

### multi_ema_crypto_scalper | BTCUSD | M5
WR=34.6%  Sharpe=-3.67  MaxDD=82.4%  Trades=1190

**Parameter Tweaks:**
- Win rate 34.6% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 82.4% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -3.67 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.60 — marginal edge, consider disabling on BTCUSD unless confirmed by live data

### power_of_3_amd | ETHUSD | M5
WR=34.0%  Sharpe=-8.09  MaxDD=1.1%  Trades=147

**Parameter Tweaks:**
- Win rate 34.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -8.09 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.31 — marginal edge, consider disabling on ETHUSD unless confirmed by live data

### ema_ribbon_trend | BTCUSD | H4
WR=33.3%  Sharpe=-5.55  MaxDD=6.5%  Trades=12

**Parameter Tweaks:**
- Win rate 33.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 12 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -5.55 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.43 — marginal edge, consider disabling on BTCUSD unless confirmed by live data

### multi_ema_crypto_scalper | ETHUSD | M15
WR=32.7%  Sharpe=-5.66  MaxDD=11.5%  Trades=1329

**Parameter Tweaks:**
- Win rate 32.7% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -5.66 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.45 — marginal edge, consider disabling on ETHUSD unless confirmed by live data

### crypto_rsi_extremes | BTCUSD | H4
WR=31.2%  Sharpe=-4.95  MaxDD=30.2%  Trades=64

**Parameter Tweaks:**
- Win rate 31.2% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 30.2% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -4.95 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.47 — marginal edge, consider disabling on BTCUSD unless confirmed by live data

### crypto_rsi_extremes | ETHUSD | H4
WR=31.2%  Sharpe=-6.10  MaxDD=2.0%  Trades=64

**Parameter Tweaks:**
- Win rate 31.2% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -6.10 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.41 — marginal edge, consider disabling on ETHUSD unless confirmed by live data

### multi_ema_crypto_scalper | ETHUSD | M5
WR=31.1%  Sharpe=-7.96  MaxDD=10.2%  Trades=1258

**Parameter Tweaks:**
- Win rate 31.1% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -7.96 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.33 — marginal edge, consider disabling on ETHUSD unless confirmed by live data

### silver_bullet_crypto | BTCUSD | H1
WR=30.2%  Sharpe=-4.56  MaxDD=22.8%  Trades=96

**Parameter Tweaks:**
- Win rate 30.2% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Max drawdown 22.8% > 20.0% → reduce sl_atr_mult by 0.2 or add trailing stop
- Sharpe -4.56 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.50 — marginal edge, consider disabling on BTCUSD unless confirmed by live data

### silver_bullet_crypto | ETHUSD | M5
WR=30.0%  Sharpe=-7.97  MaxDD=1.3%  Trades=160

**Parameter Tweaks:**
- Win rate 30.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -7.97 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.32 — marginal edge, consider disabling on ETHUSD unless confirmed by live data

### crypto_rsi_extremes | ETHUSD | M15
WR=28.4%  Sharpe=-6.40  MaxDD=6.1%  Trades=697

**Parameter Tweaks:**
- Win rate 28.4% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Sharpe -6.40 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.36 — marginal edge, consider disabling on ETHUSD unless confirmed by live data

### crypto_rsi_extremes | BTCUSD | D1
WR=14.3%  Sharpe=-6.22  MaxDD=8.2%  Trades=7

**Parameter Tweaks:**
- Win rate 14.3% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 7 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -6.22 < 2.0 → reduce lot size on this pair or pause strategy
- Profit factor 0.39 — marginal edge, consider disabling on BTCUSD unless confirmed by live data

### ema_ribbon_trend | BTCUSD | D1
WR=0.0%  Sharpe=-15.50  MaxDD=6.5%  Trades=3

**Parameter Tweaks:**
- Win rate 0.0% < 70.0% → tighten entry filter (increase ADX min or add regime check)
- Only 3 trades — widen oversold/overbought thresholds or relax ADX filter
- Sharpe -15.50 < 2.0 → reduce lot size on this pair or pause strategy

---

## ❌ Errors / Skipped
