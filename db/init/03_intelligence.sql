-- Strategy Intelligence Table
CREATE TABLE IF NOT EXISTS strategy_intelligence (
    intel_id SERIAL PRIMARY KEY,
    strategy_name VARCHAR(100) NOT NULL,
    pair VARCHAR(20) NOT NULL,
    timeframe VARCHAR(10) NOT NULL,
    maturity_score INTEGER DEFAULT 0, -- Count of successful WFO windows
    latest_sharpe NUMERIC(10,4),
    latest_win_rate NUMERIC(10,2),
    recommended_tweaks JSONB, -- History of parameter changes
    findings TEXT,
    status VARCHAR(20) DEFAULT 'ACTIVE', -- ACTIVE, ARCHIVED, REMOVED
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Strategy Intelligence Archive (Long-term storage)
CREATE TABLE IF NOT EXISTS intelligence_archive (
    archive_id SERIAL PRIMARY KEY,
    original_intel_id INTEGER,
    strategy_name VARCHAR(100),
    pair VARCHAR(20),
    timeframe VARCHAR(10),
    summary_report JSONB, -- Aggregated results for AI training
    archived_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for performance
CREATE INDEX IF NOT EXISTS idx_strat_intel_name ON strategy_intelligence(strategy_name);
