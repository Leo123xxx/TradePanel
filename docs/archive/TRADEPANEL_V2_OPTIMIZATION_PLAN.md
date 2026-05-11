# TradePanel Version 2: Optimization & Execution Plan

**Status**: Ready for Discussion & Finalization  
**Date**: May 10, 2026  
**Target Phase**: Production Release  
**Expected Duration**: 2–4 Weeks (Full Implementation)

---

## 📋 Executive Summary

TradePanel Version 2 represents a comprehensive optimization of the existing production trading system with focus on performance, stability, and scalability. The plan consolidates 6 optimization areas into 4 phased execution phases, delivering immediate quick wins followed by deeper architectural improvements.

This document outlines a structured path to achieve **10–25x improvement** across dashboard performance, backtesting speed, and overall system responsiveness while maintaining code quality and team productivity.

### Optimization Goals

- **Dashboard response time**: 2–5s → **200–500ms** (5–25x faster)
- **Overnight backtest**: 1–4 hours → **20–60 minutes** (1.5–4x faster)
- **Analytics calculations**: 2–5s → **100–500ms** (4–50x faster)
- **Database queries**: 100–500ms → **5–10ms** indexed (10–100x faster)
- **Signal generation latency**: 50–100ms → **30–40ms** (20–30% faster)

### Phase Overview & Timeline

| Phase | Duration | Focus Area | Expected Impact |
|-------|----------|-----------|-----------------|
| **Phase 1: Quick Wins** | 1–2 hours | Database & Caching | 50% improvement |
| **Phase 2: Medium Wins** | 4–8 hours | Backtesting & Ingestion | +30% improvement |
| **Phase 3: Architectural** | 8–16 hours | System Stability | +20% improvement |
| **Phase 4: Polish (Optional)** | 4–8 hours | Advanced Optimization | +10% improvement |

---

## 🎯 Optimization Areas at a Glance

### 1. Database & Query Performance
**Phase**: Phase 1 | **Effort**: 2–3 hours | **Impact**: 50–80% faster analytics (2–5s → 200–500ms)

**Key Tasks**:
- Add strategic indexes on `trades` & `market_data` tables
- Implement Redis caching for PerformanceCalculator
- Replace Python loops with PostgreSQL aggregation
- Increase connection pool size & monitoring

---

### 2. Backtesting Engine Performance
**Phase**: Phase 2 | **Effort**: 6–8 hours | **Impact**: 4–10x faster backtesting (1–4h → 20–60min)

**Key Tasks**:
- Vectorize signal generation (NumPy operations)
- Implement parallel backtest runs (multiprocessing)
- Optimize TP/SL hit detection
- Pre-calculate technical indicators

---

### 3. Data Ingestion Optimization
**Phase**: Phase 2 | **Effort**: 2–3 hours | **Impact**: 2–3x faster ingestion (45s → 15–20s)

**Key Tasks**:
- Parallel pair pulling with rate limiting
- Batch resampling (one read, multiple writes)
- Smart incremental updates by trading hours

---

### 4. Walk-Forward Optimizer
**Phase**: Phase 2 | **Effort**: 2–3 hours | **Impact**: 16–19x faster WFO (9.5h → 30–60min)

**Key Tasks**:
- Reduce parameter grids to top 2–3 params
- Implement Bayesian optimization (Optuna)
- Add early stopping for underperforming params
- Warm-start from yesterday's best params

---

### 5. Signal Generation & Strategies
**Phase**: Phase 3 | **Effort**: 3–4 hours | **Impact**: 20–30% faster signal generation (50ms → 35–40ms)

**Key Tasks**:
- Implement indicator memoization/caching
- Batch strategy calculations by timeframe
- Parameter importance analysis (Shapley values)
- Lock low-impact parameters

---

### 6. Frontend/API & Scheduler
**Phase**: Phase 3 | **Effort**: 3–4 hours | **Impact**: 10–100x EventBus faster; zero job collisions

**Key Tasks**:
- Async/thread pool for blocking calculations
- In-memory EventBus queue (fast delivery)
- Job scheduling circuit breaker
- Connection pool monitoring

---

## ⚡ Phase 1: Quick Wins (1–2 Hours)

Phase 1 focuses on immediate, high-impact improvements with minimal code changes. These are foundational optimizations that enable later phases.

### Task 1.1: Database Indexes

**File**: `db/init/schema.sql`

1. Add 4 strategic indexes:
   - `trades(created_at DESC)` — for date-range queries
   - `trades(strategy_id, pair)` — for grouping analytics
   - `market_data(pair, timeframe, timestamp DESC)` — for data lookups
   - `trades(mode)` partial `WHERE mode = 'LIVE'` — for live trade filtering

2. Expected improvement: **50–200x faster queries** (100ms → 1–5ms)

3. Validation: Run `EXPLAIN` on sample queries before/after

**SQL**:
```sql
CREATE INDEX idx_trades_created_at ON trades(created_at DESC);
CREATE INDEX idx_trades_strategy_pair ON trades(strategy_id, pair);
CREATE INDEX idx_market_data_symbol_tf ON market_data(pair, timeframe, timestamp DESC);
CREATE INDEX idx_trades_live ON trades(mode) WHERE mode = 'LIVE';
```

---

### Task 1.2: Redis Caching Layer

**File**: `analytics/performance_calculator.py`

1. Install Redis: `pip install redis`

2. Add `@cache(ttl=300)` decorator to `calculate_all_metrics()`

3. Cache keys:
   - `metrics:30d`
   - `metrics:7d`
   - `metrics:1d`

4. Expected improvement: **90% of requests < 10ms** (cached)

**Python**:
```python
from functools import lru_cache
from datetime import datetime, timedelta

@lru_cache(maxsize=5)
def get_cached_metrics(lookback_days: int = 30):
    # Cache expires after 5 minutes
    return PerformanceCalculator(lookback_days).calculate_all_metrics()
```

---

### Task 1.3: Database Aggregation

**File**: `analytics/performance_calculator.py`

1. Replace Python loops with PostgreSQL aggregation:
   - Move `daily_pnl` calculation to SQL
   - Move `by_strategy` calculation to SQL
   - Move `by_asset` calculation to SQL

2. Expected improvement: **80% faster calculations** (in-database aggregation)

**SQL Example**:
```sql
SELECT 
  DATE(created_at) as trade_date,
  COUNT(*) as total_trades,
  SUM(CASE WHEN net_pnl > 0 THEN 1 ELSE 0 END) as wins,
  SUM(net_pnl) as daily_pnl,
  STDDEV(net_pnl) as volatility
FROM trades
WHERE created_at >= NOW() - INTERVAL '30 days'
GROUP BY DATE(created_at);
```

---

### Task 1.4: Connection Pool Management

**File**: `data/db_client.py`

1. Increase `maxconn` based on `RUNNING_MODE`:
   - **LIVE**: 50 connections
   - **BACKTEST**: 10 connections
   - **DEFAULT**: 20 connections

2. Add timeout monitoring to prevent pool exhaustion

3. Expected improvement: **Graceful degradation under load**

**Python**:
```python
if RUNNING_MODE == "LIVE":
    maxconn = 50
elif RUNNING_MODE == "BACKTEST":
    maxconn = 10
else:
    maxconn = 20

DBClient._pool = pool.ThreadedConnectionPool(
    minconn=5,
    maxconn=maxconn,
    **self.conn_params
)
```

---

### Phase 1 Success Metrics

| Metric | Success Criteria |
|--------|------------------|
| Dashboard `/api/data` | < 500ms (from 2–5s) |
| Cache hit ratio | > 80% for repeat requests |
| DB pool exhaustion | Zero timeout errors in 1h load test |

---

## 📈 Phase 2: Medium Wins (4–8 Hours)

Phase 2 tackles backtesting and data ingestion performance through vectorization, parallelization, and algorithm optimization.

### Task 2.1: Vectorize Backtesting

**File**: `backtesting/engine.py`

1. Identify vectorizable patterns:
   - **Signal generation**: Replace for loops with `np.where()`
   - **TP/SL detection**: Vectorized array operations
   - **Indicators**: Pre-calculate (ATR, EMA, RSI) before backtest loop

2. Expected improvement: **4–10x faster backtest runs**

**Before (Slow)**:
```python
for i in range(len(df)):
    b_open = opens[i]
    b_high = highs[i]
    b_low = lows[i]
    
    if condition1 and condition2:
        signals[i] = 1
```

**After (Fast)**:
```python
# Vectorized
signals = np.where((condition1) & (condition2), 1, 0)  # 10–50x faster
```

---

### Task 2.2: Parallel Backtest Runs

**File**: `backtesting/engine.py` + `backtesting/runner.py` (new)

1. Implement `multiprocessing.Pool` with 4 workers

2. Split 76 combos across 4 cores: `76 × 3s ÷ 4 = ~60s`

3. Expected improvement: **228s → 60s** for full combo backtest

**Python**:
```python
from multiprocessing import Pool

def backtest_combo(strategy, pair, timeframe):
    engine = BacktestEngine()
    return engine.run(strategy, pair, timeframe, data)

def run_parallel_backtests(combos):
    with Pool(4) as pool:  # 4 cores
        results = pool.starmap(backtest_combo, combos)
    return results
```

---

### Task 2.3: Reduce WFO Parameter Grid

**File**: `backtesting/walk_forward.py`

1. **Analysis phase**:
   - Identify top 2–3 high-impact params per strategy
   - Use feature importance (Shapley values)
   - Lock low-impact params to defaults

2. Expected improvement: **162 combos → 4–12 combos** per strategy

**Example**:
```python
# Before (slow)
PARAM_GRIDS = {
    "ma_crossover": {
        "fast_period": [5, 7, 10],      # 3 values
        "slow_period": [21, 50, 75],    # 3 values
        "adx_filter": [20, 25, 30],     # 3 values
        "tp_atr_mult": [2.0, 3.0],      # 2 values
        "sl_atr_mult": [0.8, 1.0, 1.5]  # 3 values
    }
}
# Total: 3 × 3 × 3 × 2 × 3 = 162

# After (fast)
PARAM_GRIDS = {
    "ma_crossover": {
        "fast_period": [5, 10],         # 2 values (top params only)
        "slow_period": [21, 50],        # 2 values
    }
}
# Total: 2 × 2 = 4
```

---

### Task 2.4: Implement Bayesian Optimization

**File**: `backtesting/walk_forward.py`

1. Install Optuna: `pip install optuna`

2. Replace grid search with `optuna.optimize(n_trials=30)`

3. Expected improvement: **9.5h WFO → 30–60 minutes**

**Python**:
```python
import optuna

def objective(trial):
    fast = trial.suggest_int('fast_period', 5, 20)
    slow = trial.suggest_int('slow_period', 21, 100)
    # Run backtest
    sharpe = run_backtest_get_sharpe(fast, slow)
    return sharpe

study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=30)  # 30 trials instead of 162
best_params = study.best_params
```

---

### Task 2.5: Parallel Data Ingestion

**File**: `data/ingestion.py`

1. Implement concurrent pair pulling:
   - Use `asyncio.Semaphore(3)` for max 3 concurrent MT5 calls
   - Rate limiting to avoid broker throttling

2. Expected improvement: **45s → 15–20s** for 18 pairs

**Python**:
```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

async def pull_pair_concurrent(pair, semaphore):
    async with semaphore:
        return feed.pull_historical_data(pair, ...)

async def pull_all_pairs(pairs):
    semaphore = asyncio.Semaphore(3)
    tasks = [pull_pair_concurrent(pair, semaphore) for pair in pairs]
    results = await asyncio.gather(*tasks)
    return results
```

---

### Phase 2 Success Metrics

| Metric | Success Criteria |
|--------|------------------|
| Single backtest combo | < 500ms vectorized (from 1–3s) |
| Overnight backtest (76 combos) | < 60 minutes (from 1–4 hours) |
| WFO suite (full run) | 30–60 minutes (from 9.5 hours) |

---

## 🏗️ Phase 3: Architectural (8–16 Hours)

Phase 3 addresses system stability, scalability, and real-time performance through advanced caching, event handling, and scheduler coordination.

### Task 3.1: Materialized Views (PostgreSQL)

**File**: `db/init/schema.sql`

1. Create `mv_daily_metrics` view:
   - Aggregates trades by date: total trades, wins, daily_pnl, sharpe, drawdown

2. Refresh every hour via scheduler job

3. Expected improvement: **Real-time analytics without CPU spike**

**SQL**:
```sql
CREATE MATERIALIZED VIEW mv_daily_metrics AS
SELECT 
  DATE(created_at) as trade_date,
  COUNT(*) as total_trades,
  SUM(CASE WHEN net_pnl > 0 THEN 1 ELSE 0 END) as wins,
  SUM(net_pnl) as daily_pnl,
  STDDEV(net_pnl) as volatility,
  MAX(net_pnl) as max_win,
  MIN(net_pnl) as max_loss
FROM trades
GROUP BY DATE(created_at);

-- Refresh every hour
CREATE SCHEDULED JOB refresh_daily_metrics AS
  REFRESH MATERIALIZED VIEW mv_daily_metrics;
```

---

### Task 3.2: Indicator Memoization

**File**: `strategies/base_strategy.py`

1. Add `@lru_cache` to indicator calculations (EMA, RSI, ATR)

2. Incremental update for new bar: don't recalculate all 200 bars

3. Expected improvement: **20–30% faster signal generation**

**Python**:
```python
from functools import lru_cache

class BaseStrategy:
    @lru_cache(maxsize=128)
    def calculate_ema(self, prices_tuple, period):
        # Cache result; only recalculate when new bar added
        return talib.EMA(np.array(prices_tuple), period)
    
    def update_indicators(self, new_price):
        # Instead of recalculating all 200 bars:
        # prev_ema = indicator_cache.get('ema20')
        # new_ema = update_ema(prev_ema, new_price)  # Incremental
        pass
```

---

### Task 3.3: Scheduler Circuit Breaker

**File**: `scheduler/jobs.py`

1. **Prevent job overlap**:
   - If backtest running, skip data sync and signal checks
   - Max backtest duration: 2 hours (hard limit, stop gracefully)
   - Stagger job start times to avoid contention

2. Expected improvement: **Zero lock timeouts, predictable job execution**

**Python**:
```python
class SchedulerCircuitBreaker:
    def __init__(self):
        self.backtest_running = False
        self.backtest_start_time = None
    
    def can_run_backtest(self):
        if self.backtest_running:
            elapsed = time.time() - self.backtest_start_time
            if elapsed > 7200:  # 2 hour hard limit
                self.stop_backtest_gracefully()
                return True
            return False
        return True
    
    def start_backtest(self):
        self.backtest_running = True
        self.backtest_start_time = time.time()
    
    def end_backtest(self):
        self.backtest_running = False
```

---

### Task 3.4: In-Memory EventBus Queue

**File**: `webapp/bus.py`

1. Replace Postgres `LISTEN/NOTIFY` with `asyncio.Queue`:
   - Fast in-memory queue for trade events
   - Batch WebSocket broadcasts (no per-event overhead)

2. Expected improvement: **50–100x faster event delivery**

**Python**:
```python
from asyncio import Queue

event_queue = Queue(maxsize=1000)

async def publish_event(event):
    # Fast: add to memory queue
    await event_queue.put(event)
    # Separately: persist to DB for audit trail
    await db.log_event(event)

async def broadcast_to_clients():
    while True:
        event = await event_queue.get()
        # Batch send to all connected WebSocket clients
        for ws in connected_clients:
            await ws.send_json(event)
```

---

### Phase 3 Success Metrics

| Metric | Success Criteria |
|--------|------------------|
| Job execution stability | Zero lock timeouts; zero overlaps in 7-day run |
| Signal gen latency | < 40ms per bar (from 50–100ms) |
| EventBus message latency | < 10ms to WebSocket (from 500ms+ DB round-trip) |

---

## ✨ Phase 4: Polish (4–8 Hours, Optional)

Phase 4 is optional advanced optimization for post-launch refinement. Execute only after Phase 1–3 are stable in production.

### Task 4.1: Bayesian Strategy Parameter Importance

**File**: `backtesting/walk_forward.py`

1. Use Shapley values to rank parameter importance

2. Auto-remove low-impact params from config

3. Expected improvement: **Cleaner, more maintainable strategy configs**

---

### Task 4.2: Adaptive Parameter Grid

**File**: `backtesting/walk_forward.py`

1. Warm-start from yesterday's best params

2. Search neighborhood instead of full grid

3. Expected improvement: **Faster convergence; more stable results**

---

### Task 4.3: Advanced Caching Strategy

**File**: `webapp/main.py` + `frontend/dashboard.html`

1. Cache by `lookback_days`: 1d, 7d, 30d buckets

2. Invalidate cache only when new trade closes

3. Expected improvement: **95%+ cache hit ratio**

---

### Phase 4 Success Metrics

| Metric | Success Criteria |
|--------|------------------|
| WFO time (after Phase 2) | < 30 minutes (further 20–40% reduction) |
| System responsiveness | Sub-100ms analytics even during backtest |

---

## 📅 Resource Allocation & Timeline

### Team Composition

- **Backend Engineer**: Database indexes, caching, backtesting optimization
- **DevOps/Architect**: Connection pooling, job scheduling, monitoring
- **Optional QA**: Performance testing, validation scripts

### Effort Breakdown

| Phase | Effort (hours) | Timeline |
|-------|----------------|----------|
| Phase 1 | 1–2 | Day 1–2 (parallel execution) |
| Phase 2 | 4–8 | Days 3–5 |
| Phase 3 | 8–16 | Days 6–10 |
| Phase 4 (Optional) | 4–8 | Days 11+ (post-launch) |

**Total**: 17–32 hours of development work over 2–4 weeks

### Critical Path Dependencies

- **Phase 1 → Phase 2**: Phase 1 must complete before backtest optimization
- **Phase 2 → Phase 3**: Backtesting performance baseline needed for stability tests
- **Phase 3 → Phase 4**: System must be stable before advanced optimizations

---

## ✅ Implementation Checklist

### Pre-Launch Validation

- [ ] Set up performance baseline: current dashboard, backtest, analytics times
- [ ] Create test harness: load test scripts for validation
- [ ] Branch strategy: create `feature/v2-optimization` branch
- [ ] Backup: backup production database before starting

### Phase 1 Checklist

- [ ] Create database indexes (4 total)
- [ ] Install & configure Redis
- [ ] Add caching decorator to PerformanceCalculator
- [ ] Refactor analytics queries to SQL aggregation
- [ ] Update connection pool configuration
- [ ] Run `EXPLAIN` on sample queries to verify index usage
- [ ] Load test: verify < 500ms dashboard response

### Phase 2 Checklist

- [ ] Vectorize backtesting signal generation
- [ ] Implement `multiprocessing.Pool` for parallel backtests
- [ ] Reduce parameter grids (2–3 top params only)
- [ ] Install Optuna for Bayesian optimization
- [ ] Implement parallel data ingestion with Semaphore
- [ ] Run full overnight backtest: verify < 60 min
- [ ] Validate WFO completion: verify < 60 min

### Phase 3 Checklist

- [ ] Create PostgreSQL materialized views
- [ ] Schedule hourly view refresh job
- [ ] Implement indicator memoization (`@lru_cache`)
- [ ] Add scheduler circuit breaker logic
- [ ] Replace EventBus with in-memory queue
- [ ] Run 24-hour stability test (no errors, no overlaps)
- [ ] Validate WebSocket latency < 10ms

### Post-Launch Validation

- [ ] Run 48-hour live demo with full monitoring
- [ ] Validate all 6 optimization areas achieved expected improvements
- [ ] Document actual vs. expected performance gains
- [ ] Gather team feedback on implementation experience
- [ ] Plan Phase 4 (if needed) based on results

---

## 📊 Success Metrics & Validation

### Before & After Comparison

| Metric | Before (Current) | After (v2 Target) |
|--------|------------------|-------------------|
| Dashboard Response | 2–5 seconds | 200–500 ms |
| Overnight Backtest | 1–4 hours | 20–60 minutes |
| Analytics Calculation | 2–5 seconds | 100–500 ms |
| DB Query Time (indexed) | 100–500 ms | 5–10 ms |
| Signal Generation Latency | 50–100 ms | 30–40 ms |

### Testing & Validation Strategy

- **Performance baseline**: Capture before-state metrics
- **Load testing**: 10–50 concurrent dashboard users
- **Integration testing**: Verify backtest → dashboard → API chain
- **Stability testing**: 48-hour run with monitoring
- **Regression testing**: All 23 strategies backtest correctly

### Rollback Plan

- **Git tags**: Tag version `v1` (before) and `v2-optimization` (after)
- **Database**: Keep backup of pre-optimization schema + data
- **Cache strategy**: Can disable Redis cache (falls back to live calc)
- **Circuit breaker**: Can revert to sequential job execution

---

## 💬 Discussion Points for Finalization

### Decision 1: Parallel Backtest Resource Allocation

Should we use 2, 4, or 8 CPU cores for parallel backtesting?

- **Conservative (2 cores)**: Leaves system resources for other tasks
- **Balanced (4 cores)**: Recommended; 60s backtest + room for monitoring
- **Aggressive (8 cores)**: Fastest (30s) but may impact dashboard during runs

**Recommendation**: Start with 4 cores; adjust based on system load monitoring.

---

### Decision 2: Redis Deployment

Should Redis be in-process (Python) or separate Docker container?

- **In-process**: Faster, no network latency, memory overhead
- **Docker**: Separate container, easier to manage, persistence options

**Recommendation**: Docker container for production; in-process for dev.

---

### Decision 3: WFO Parameter Reduction Aggressiveness

How aggressive should we be in reducing parameter grids?

- **Conservative**: Keep 5–10 params per strategy (slower WFO)
- **Balanced**: 2–3 top params only (9.5h → 1–2h)
- **Aggressive**: 1–2 params + Bayesian search (1–2h → 20 min)

**Recommendation**: Start balanced; gather results after first run. Adjust based on strategy performance stability.

---

### Decision 4: Phase 4 (Polish) Timing

Should Phase 4 be included in initial Version 2 launch?

- **No**: Launch Phase 1–3 only; Phase 4 as post-launch refinement
- **Yes**: Include Phase 4 for maximum performance upfront

**Recommendation**: No. Launch Phase 1–3; gather results. Phase 4 can be executed based on observed bottlenecks.

---

### Risk Assessment

| Risk | Probability | Mitigation |
|------|-------------|-----------|
| Backtest accuracy regression | Low | Regression tests on all 23 strategies |
| Cache invalidation bugs | Medium | TTL monitoring; manual cache clear endpoint |
| Job scheduling overlap | Medium | Circuit breaker with hard timeouts |
| Connection pool exhaustion | Low | Monitoring + alert on pool usage > 80% |

---

### Team Alignment Questions

1. Are we committed to completing Phase 1 before moving to Phase 2?
2. Who owns monitoring/alerting during execution?
3. Do we have a performance regression test suite?
4. What's the approval process for database schema changes?
5. How do we validate that optimizations don't break trading logic?

---

## 📝 Next Steps

1. **Review** this plan with the team
2. **Discuss and finalize** the 4 decision points above
3. **Assign Phase 1 tasks** and establish a start date
4. **Create feature branch** and set up performance monitoring
5. **Execute Phase 1** in parallel; measure before/after metrics
6. **Review Phase 1 results**; plan Phase 2 timeline

---

**Document Version**: 1.0  
**Last Updated**: May 10, 2026  
**Owner**: TradePanel Development Team
