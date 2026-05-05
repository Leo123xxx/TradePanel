-- =============================================================================
-- Migration: backtest_runs table
-- Run once against your trading_platform PostgreSQL database.
-- Stores every backtest run with full metrics + params for snapshot restore.
-- =============================================================================

-- Drop existing table if schema is stale (safe — no production data yet)
DROP TABLE IF EXISTS backtest_runs CASCADE;

CREATE TABLE backtest_runs (
    id              SERIAL PRIMARY KEY,
    run_id          TEXT NOT NULL UNIQUE,          -- e.g. BT-0042
    strategy_name   TEXT NOT NULL,
    run_date        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    period_start    DATE,
    period_end      DATE,

    -- Core performance metrics
    win_rate        NUMERIC(6, 4),                 -- 0.0 – 1.0
    sharpe_ratio    NUMERIC(8, 4),
    profit_factor   NUMERIC(8, 4),
    net_profit_zar  NUMERIC(14, 2),
    max_drawdown_pct NUMERIC(8, 4),                -- negative value, e.g. -0.062
    total_trades    INTEGER,
    winning_trades  INTEGER,
    losing_trades   INTEGER,
    roi_pct         NUMERIC(8, 4),
    risk_reward     NUMERIC(8, 4),
    recovery_factor NUMERIC(8, 4),

    -- Pass/Fail/Review based on go-live criteria:
    --   PASS  : win_rate >= 0.90 of backtest, sharpe >= 0.8, max_dd < 12%
    --   REVIEW: borderline on one metric
    --   FAIL  : fails hard criteria
    status          TEXT NOT NULL DEFAULT 'PENDING'
                    CHECK (status IN ('PASS', 'FAIL', 'REVIEW', 'PENDING')),

    -- Stored strategy parameters at time of run (for exact restore)
    params_json     JSONB,

    -- Full metrics blob for snapshot restore
    metrics_json    JSONB,

    -- Optional notes / trigger reason
    notes           TEXT,

    -- Walk-forward fold metadata if applicable
    wfo_fold        INTEGER,
    wfo_total_folds INTEGER,

    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes for common query patterns
CREATE INDEX IF NOT EXISTS idx_backtest_runs_strategy
    ON backtest_runs (strategy_name);

CREATE INDEX IF NOT EXISTS idx_backtest_runs_run_date
    ON backtest_runs (run_date DESC);

CREATE INDEX IF NOT EXISTS idx_backtest_runs_status
    ON backtest_runs (status);

-- Auto-update updated_at on row modification
CREATE OR REPLACE FUNCTION update_backtest_runs_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_backtest_runs_updated_at ON backtest_runs;
CREATE TRIGGER trg_backtest_runs_updated_at
    BEFORE UPDATE ON backtest_runs
    FOR EACH ROW EXECUTE FUNCTION update_backtest_runs_updated_at();

-- =============================================================================
-- Seed a few example runs so the UI renders immediately after migration
-- (safe to skip in production)
-- =============================================================================
INSERT INTO backtest_runs (
    run_id, strategy_name, run_date, period_start, period_end,
    win_rate, sharpe_ratio, profit_factor, net_profit_zar,
    max_drawdown_pct, total_trades, winning_trades, losing_trades,
    roi_pct, risk_reward, recovery_factor, status, notes,
    params_json, metrics_json
) VALUES
(
    'BT-0001', 'stat_arb_gold_silver',
    NOW() - INTERVAL '2 days',
    '2026-01-01', '2026-04-25',
    0.912, 4.66, 6.2, 28400.00, -0.031,
    48, 44, 4, 0.227, 4.1, 7.3, 'PASS',
    'Auto-run after WFO optimization',
    '{"bb_window": 20, "entry_zscore": 2.0, "exit_zscore": 0.5, "atr_multiplier": 1.5}',
    '{"equity_curve": [], "trade_log": []}'
),
(
    'BT-0002', 'cot_sentiment',
    NOW() - INTERVAL '7 days',
    '2026-01-01', '2026-03-31',
    0.885, 3.21, 5.1, 19200.00, -0.058,
    22, 19, 3, 0.154, 3.8, 2.7, 'PASS',
    'Q1 2026 validation run',
    '{"lookback_weeks": 26, "threshold": 0.6, "timeframe": "D1"}',
    '{"equity_curve": [], "trade_log": []}'
),
(
    'BT-0003', 'bb_mean_reversion',
    NOW() - INTERVAL '17 days',
    '2026-01-01', '2026-03-31',
    0.713, 1.44, 2.1, 4100.00, -0.098,
    29, 21, 8, 0.033, 2.2, 0.42, 'REVIEW',
    'Drawdown borderline — watch closely',
    '{"bb_period": 20, "bb_std": 3.0, "rsi_period": 14}',
    '{"equity_curve": [], "trade_log": []}'
),
(
    'BT-0004', 'fast_ma_scalper',
    NOW() - INTERVAL '30 days',
    '2026-01-01', '2026-03-28',
    0.521, 0.41, 0.88, -2800.00, -0.142,
    89, 46, 43, -0.022, 0.9, -0.15, 'FAIL',
    'Real-data failure — demoted from active',
    '{"fast_ma": 5, "slow_ma": 20, "timeframe": "M5"}',
    '{"equity_curve": [], "trade_log": []}'
)
ON CONFLICT (run_id) DO NOTHING;
