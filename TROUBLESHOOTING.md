# Troubleshooting & Debug Guide

Solutions for common issues and the 7 execution blockers.

---

## 🚨 Trades Not Executing? (7 Blockers)

### CRITICAL #1: Pair Mismatch ✅ FIXED (April 24)

**Problem**: config.yaml requests strategy on XAUUSD, but strategies.yaml defines it for USDJPY.

**Example**:
```yaml
# config/config.yaml says:
strategies:
  - name: triple_macd_scalping
    pairs: [XAUUSD]

# But strategies.yaml says:
triple_macd_scalping:
  pairs:
    - USDJPY  # MISMATCH!
```

**Fix Applied**: Changed USDJPY → XAUUSD in strategies.yaml line 562.

**How to Check**:
```bash
# Verify active strategies
grep -A 3 "^strategies:" config/config.yaml
# Check strategy definitions
grep -B 5 "pairs:" config/strategies.yaml | grep -A 5 triple_macd
```

---

### CRITICAL #2: Regime Filter Blocking ✅ FIXED (April 24)

**Problem**: `use_macro_regime_filter: true` blocks ALL trades when macro bias = NEUTRAL.

**Code**: `paper_engine.py` lines 258–268

```python
if bias == 0:  # NEUTRAL macro state
    print(f"[REGIME] Skipping {direction} on {symbol}")
    return  # ← TRADE IS BLOCKED
```

**Fix Applied**: Set `use_macro_regime_filter: false` in config/config.yaml line 167.

**What Was Blocking**:
- If macro regime detector classified market as NEUTRAL
- Strategy would not trade despite signal
- User saw signals in logs but no trade execution

**Re-enable Later**:
```yaml
use_macro_regime_filter: true
# Then verify regime detection is accurate
```

---

### CRITICAL #3: Multi-TF Confirmation Blocking ✅ FIXED (April 24)

**Problem**: `use_multi_tf_confirmation: true` rejects entries if higher TF opposes signal.

**Example**:
- H1 signal: BUY (valid)
- D1 trend: SELL (opposite)
- **Result**: Trade SKIPPED

**Code**: `paper_engine.py` lines 228–235

**Fix Applied**: Set `use_multi_tf_confirmation: false` in config/config.yaml line 168.

**When to Re-enable**:
```yaml
use_multi_tf_confirmation: false
# After confirming trades execute reliably:
use_multi_tf_confirmation: true  # Re-enable
```

---

### Blocker #4: Risk Manager Check Failures

**Possible Failure Points**:

| Check | Condition | Location |
|-------|-----------|----------|
| **Margin** | Free margin < required × 1.5 | order_manager.py:107 |
| **Positions** | Open positions ≥ 5 | risk_manager.py:48 |
| **Spread** | Bid-ask > 5.0 pips | config.yaml:163 |
| **Trading Hours** | Outside Mon-Fri 00:30–23:59 UTC | config.yaml:170 |

**How to Debug**:
Look in logs for:
```
RISK BLOCKED: Insufficient margin: free=XXX, required=YYY
RISK BLOCKED: Max concurrent positions reached
RISK BLOCKED: Current spread exceeds max
RISK BLOCKED: Outside trading hours
```

**Fixes**:

**Insufficient Margin**:
```yaml
# Your account: 2947.14 ZAR (~$180 USD)
# Reduce lot size or increase margin
risk_management:
  default_lot_size: 0.05  # Reduced from 0.1
```

**Position Limit Hit**:
```yaml
# Increase max concurrent positions
max_concurrent_positions: 10  # Changed from 5
```

**Spread Too Wide**:
```yaml
# Increase tolerance
max_spread_pips: 10.0  # Changed from 5.0
```

**Outside Trading Hours**:
Check current UTC time matches config:
```yaml
trading_hours:
  start: "00:30"  # 00:30 UTC
  end: "23:59"    # 23:59 UTC
  days: [0, 1, 2, 3, 4]  # Mon-Fri
```

---

### Blocker #5: Data Staleness

**Problem**: If MT5 data > 24 hours old, trades are blocked.

**Code**: `paper_engine.py` lines 206–210

**Symptoms**:
```
[SYNC] Stale data detected for XAUUSD. Triggering reconnect
```

**Fixes**:
1. **Restart MT5**: Close and reopen MetaTrader 5
2. **Check connection**: Tools → Options → Expert Advisors
3. **Verify symbol**: Check symbol is in market watch
4. **Check time**: MT5 clock must be synchronized

---

### Blocker #6: Strategy Not Actually Running

**Problem**: Strategy enabled but no signals generated.

**Possible Causes**:
- Strategy timeframe not in price data
- Strategy parameters invalid
- Strategy has syntax error

**How to Check**:
```bash
# Check loaded strategies
grep -i "Loaded.*strategy" logs/*.log

# Check for errors
grep -i "error\|fail\|exception" logs/*.log | grep -i strategy
```

**Fixes**:
1. Verify strategy is in `STRATEGY_REGISTRY` (paper_engine.py:44–74)
2. Verify strategy is enabled (strategies.yaml:enabled: true)
3. Check strategy's timeframes match requested TF
4. Run unit test: `python -m pytest tests/test_strategies.py`

---

### Blocker #7: Scheduler Not Running

**Problem**: `run_detect()` and `run_execute()` not being called.

**Code**: `scheduler/jobs.py` lines 58–68

**Check Status**:
```bash
# Check if scheduler is running
ps aux | grep scheduler

# Check logs
tail -f logs/scheduler.log
```

**Symptoms**:
- No signals detected (no logs at all)
- No execution attempts
- Dashboard empty

**Fixes**:
```bash
# Restart scheduler
python main.py scheduler

# Or restart full system
python main.py paper-trade
```

---

## Common Issues & Solutions

### "Could Not Connect to MT5"

**Cause**: MT5 not running or not configured.

**Fix**:
1. Open MetaTrader 5
2. Tools → Options → Expert Advisors
3. Check "Allow automated trading"
4. Check correct broker server

---

### "Address Already in Use :5000"

**Cause**: Dashboard port occupied.

**Fix**:
```yaml
# config/config.yaml
webapp:
  port: 5001  # Use different port
```

Or kill the process:
```bash
# Find what's using port 5000
lsof -i :5000
kill -9 <PID>
```

---

### "Insufficient Free Margin"

**Cause**: Account balance too low for position size.

**Fix**:
```yaml
# Reduce lot size
risk_management:
  default_lot_size: 0.05  # Down from 0.1
  max_lot_size: 0.5       # Down from 1.0
```

Or deposit more funds to account.

---

### "ModuleNotFoundError: No module named 'MetaTrader5'"

**Cause**: MT5 library not installed.

**Fix**:
```bash
pip install --upgrade MetaTrader5
```

If still fails, check Python architecture matches MT5:
```bash
# Must be 64-bit Python
python -c "import struct; print(struct.calcsize('P') * 8)"
# Should output: 64
```

---

### "Strategy Not Generating Signals"

**Debug Steps**:

1. **Check if strategy loads**:
```bash
grep "Loaded.*strategy_name" logs/*.log
```

2. **Check if it runs on correct pair/TF**:
```yaml
# Verify in config
strategies:
  - name: your_strategy
    pairs: [EURUSD]      # Check here
    timeframes: [H1]     # Check here
```

3. **Check strategy parameters**:
```bash
python -c "
from strategies.dual_ema_fractal import DualEMAFractal
s = DualEMAFractal()
print(s.params)
"
```

4. **Run backtest to verify logic**:
```bash
python -m scripts.run_backtest \
  --strategy dual_ema_fractal \
  --pair EURUSD \
  --timeframe H1
```

---

### Telegram Not Sending Alerts

**Cause**: Bot token or chat ID not configured.

**Fix**:
1. Get bot token from @BotFather
2. Get chat ID from @userinfobot
3. Add to config.yaml:
```yaml
notifications:
  telegram_enabled: true
  telegram_token: "YOUR_TOKEN"
  telegram_chat_id: "YOUR_CHAT_ID"
```
4. Restart bot

---

### Dashboard Shows Empty Charts

**Cause**: No trades executed yet, or database issue.

**Fix**:
1. Make sure trades have executed: Check logs for "Trade opened"
2. Check database connection:
```bash
psql tradepanel_db -c "SELECT COUNT(*) FROM trades;"
```
3. Restart dashboard:
```bash
python webapp/main.py
```

---

## Debug Checklist

When things aren't working:

- [ ] MT5 is running and configured
- [ ] Strategies are enabled in strategies.yaml
- [ ] Strategies are in config.yaml active list
- [ ] `use_macro_regime_filter: false` (for testing)
- [ ] `use_multi_tf_confirmation: false` (for testing)
- [ ] Pair mismatch fixed (XAUUSD in both files)
- [ ] Account has sufficient margin
- [ ] Current time is within trading hours
- [ ] Logs show no errors
- [ ] Dashboard is accessible

---

## Viewing Logs

```bash
# Real-time paper engine
tail -f logs/paper_engine.log

# Real-time API
tail -f logs/api.log

# All warnings/errors
grep -i "error\|fail\|warning" logs/*.log

# Search for specific strategy
grep "dual_ema_fractal" logs/*.log

# Search for trade execution
grep "EXECUTING\|Trade opened" logs/*.log
```

---

## Recent Fixes (April 24, 2026)

**3 Critical Issues Fixed**:

1. ✅ **Pair Mismatch** — triple_macd_scalping now runs on XAUUSD
2. ✅ **Regime Filter** — Disabled for testing (was blocking all neutral trades)
3. ✅ **Multi-TF Confirmation** — Disabled for testing (was blocking entries)

**Added**:
- 3 more strategies (dual_ema_fractal, rsi_bounce, bb_mean_reversion)
- Better logging in execution engine

**Result**: Bot now executes trades successfully

See **DEBUG_SUMMARY.md** for detailed breakdown.

---

**Can't find your issue? Check ARCHITECTURE.md or STRATEGIES.md for more details.**

