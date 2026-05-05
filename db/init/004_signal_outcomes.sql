-- db/init/004_signal_outcomes.sql

CREATE TABLE IF NOT EXISTS signal_outcomes (
    signal_id INTEGER PRIMARY KEY REFERENCES signals(signal_id),
    outcome VARCHAR(20) NOT NULL, -- 'TP1', 'TP2', 'TP3', 'SL', 'EXPIRED'
    bars_to_close INTEGER,
    pnl_pips NUMERIC(10, 2),
    checked_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Index for performance queries
CREATE INDEX IF NOT EXISTS idx_signal_outcomes_outcome ON signal_outcomes(outcome);
