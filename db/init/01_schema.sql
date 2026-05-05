-- =============================================================================
-- TradePanel Database Schema (Consolidated for Docker Init)
-- =============================================================================

-- 1. strategies
CREATE TABLE IF NOT EXISTS strategies (
    strategy_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    status VARCHAR(20) DEFAULT 'ACTIVE',
    parameters JSONB,
    version INT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. backtest_runs (from migrate_backtest_runs.sql)
CREATE TABLE IF NOT EXISTS backtest_runs (
    id              SERIAL PRIMARY KEY,
    run_id          TEXT NOT NULL UNIQUE,
    strategy_name   TEXT NOT NULL,
    run_date        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    period_start    DATE,
    period_end      DATE,
    win_rate        NUMERIC(6, 4),
    sharpe_ratio    NUMERIC(8, 4),
    profit_factor   NUMERIC(8, 4),
    net_profit_zar  NUMERIC(14, 2),
    max_drawdown_pct NUMERIC(8, 4),
    total_trades    INTEGER,
    winning_trades  INTEGER,
    losing_trades   INTEGER,
    roi_pct         NUMERIC(8, 4),
    risk_reward     NUMERIC(8, 4),
    recovery_factor NUMERIC(8, 4),
    status          TEXT NOT NULL DEFAULT 'PENDING'
                    CHECK (status IN ('PASS', 'FAIL', 'REVIEW', 'PENDING')),
    params_json     JSONB,
    metrics_json    JSONB,
    notes           TEXT,
    wfo_fold        INTEGER,
    wfo_total_folds INTEGER,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_backtest_runs_strategy ON backtest_runs (strategy_name);
CREATE INDEX IF NOT EXISTS idx_backtest_runs_run_date ON backtest_runs (run_date DESC);
CREATE INDEX IF NOT EXISTS idx_backtest_runs_status ON backtest_runs (status);

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

-- 3. account_profiles
CREATE TABLE IF NOT EXISTS account_profiles (
    account_id   SERIAL PRIMARY KEY,
    account_name VARCHAR(80)  NOT NULL UNIQUE,
    account_type VARCHAR(20)  NOT NULL CHECK (account_type IN ('DEMO','LIVE','PAPER')),
    broker       VARCHAR(80)  DEFAULT 'MetaTrader 5',
    currency     VARCHAR(10)  DEFAULT 'USD',
    initial_balance NUMERIC(14,2) DEFAULT 10000.00,
    is_active    BOOLEAN      DEFAULT TRUE,
    notes        TEXT,
    created_at   TIMESTAMPTZ  DEFAULT NOW(),
    updated_at   TIMESTAMPTZ  DEFAULT NOW()
);

CREATE OR REPLACE FUNCTION set_account_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_account_profiles_updated ON account_profiles;
CREATE TRIGGER trg_account_profiles_updated
BEFORE UPDATE ON account_profiles
FOR EACH ROW EXECUTE FUNCTION set_account_updated_at();

-- 4. signals
CREATE TABLE IF NOT EXISTS signals (
    signal_id SERIAL PRIMARY KEY,
    strategy_id INT REFERENCES strategies(strategy_id),
    timestamp TIMESTAMP NOT NULL,
    pair VARCHAR(20),
    direction VARCHAR(10),
    indicator_values JSONB,
    triggered_trade_id UUID
);

-- 5. trades
CREATE TABLE IF NOT EXISTS trades (
    trade_id UUID PRIMARY KEY,
    strategy_id INT REFERENCES strategies(strategy_id),
    account_id INTEGER REFERENCES account_profiles(account_id),
    mode VARCHAR(20), -- BACKTEST | PAPER | LIVE
    pair VARCHAR(20),
    direction VARCHAR(10), -- BUY | SELL
    lot_size NUMERIC,
    entry_price NUMERIC,
    exit_price NUMERIC,
    expected_entry NUMERIC,
    slippage_pips NUMERIC,
    tp_price NUMERIC,
    sl_price NUMERIC,
    open_time TIMESTAMP,
    close_time TIMESTAMP,
    duration_seconds INT,
    gross_pnl NUMERIC,
    net_pnl NUMERIC,
    spread_cost NUMERIC,
    swap_cost NUMERIC,
    commission_cost NUMERIC,
    status VARCHAR(20), -- OPENED | CLOSED
    close_reason VARCHAR(50), -- TP_HIT | SL_HIT | SIGNAL_REVERSAL | MANUAL | DRAWDOWN_PAUSE
    mt5_ticket BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_trades_account_id ON trades(account_id);

-- 6. positions
CREATE TABLE IF NOT EXISTS positions (
    position_id SERIAL PRIMARY KEY,
    mt5_ticket BIGINT UNIQUE,
    strategy_id INT REFERENCES strategies(strategy_id),
    pair VARCHAR(20),
    volume NUMERIC,
    direction VARCHAR(10),
    entry_price NUMERIC,
    time_synced TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 7. bot_health
CREATE TABLE IF NOT EXISTS bot_health (
    health_id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    event_type VARCHAR(50), -- HEARTBEAT | CONNECTION_LOST | ERROR
    status VARCHAR(20),
    message TEXT,
    meta_data JSONB
);

-- 8. daily_summary
CREATE TABLE IF NOT EXISTS daily_summary (
    summary_id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    total_pnl NUMERIC,
    win_rate NUMERIC,
    max_drawdown NUMERIC,
    trade_count INT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(date)
);

-- 9. commands
CREATE TABLE IF NOT EXISTS commands (
    command_id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    command_text TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'PENDING', -- PENDING | PROCESSED | FAILED
    response_text TEXT
);

-- 10. market_data
CREATE TABLE IF NOT EXISTS market_data (
    data_id SERIAL PRIMARY KEY,
    pair VARCHAR(20) NOT NULL,
    timeframe VARCHAR(10) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    open NUMERIC NOT NULL,
    high NUMERIC NOT NULL,
    low NUMERIC NOT NULL,
    close NUMERIC NOT NULL,
    tick_volume BIGINT,
    spread INT,
    UNIQUE(pair, timeframe, timestamp)
);

-- 11. regime_log
CREATE TABLE IF NOT EXISTS regime_log (
    regime_id SERIAL PRIMARY KEY,
    pair VARCHAR(20) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    regime VARCHAR(50), -- TRENDING | RANGING | HIGH_VOL | LOW_VOL
    adx_value NUMERIC,
    atr_value NUMERIC
);

-- 12. cot_data
CREATE TABLE IF NOT EXISTS cot_data (
    cot_id          SERIAL PRIMARY KEY,
    pair            VARCHAR(10)  NOT NULL,
    report_date     DATE         NOT NULL,
    cftc_code       VARCHAR(10)  NOT NULL,
    comm_long       BIGINT,
    comm_short      BIGINT,
    noncomm_long    BIGINT,
    noncomm_short   BIGINT,
    net_commercial  BIGINT,
    net_noncomm     BIGINT,
    cot_index       NUMERIC(6,2),
    open_interest   BIGINT,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (pair, report_date)
);

-- 13. wfo_runs
CREATE TABLE IF NOT EXISTS wfo_runs (
    wfo_id SERIAL PRIMARY KEY,
    strategy_id INT REFERENCES strategies(strategy_id),
    run_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    parameters JSONB,
    metrics JSONB,
    status VARCHAR(20) DEFAULT 'COMPLETED'
);

-- Seed Account Profiles
INSERT INTO account_profiles (account_name, account_type, broker, currency, initial_balance, notes)
VALUES
    ('Demo Account',  'DEMO',  'MetaTrader 5', 'USD', 10000.00, 'Primary demo / simulation account'),
    ('Live Account',  'LIVE',  'MetaTrader 5', 'USD', 10000.00, 'Live funded account'),
    ('Paper Account', 'PAPER', 'MetaTrader 5', 'USD', 10000.00, 'Paper trading / forward test')
ON CONFLICT (account_name) DO NOTHING;
