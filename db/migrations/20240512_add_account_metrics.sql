-- Migration: Create account_metrics table for snapshots
-- Date: 2024-05-12

CREATE TABLE IF NOT EXISTS public.account_metrics (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    equity DECIMAL(15, 2) NOT NULL,
    balance DECIMAL(15, 2) NOT NULL,
    margin_level DECIMAL(10, 2),
    floating_pnl DECIMAL(15, 2) NOT NULL,
    realized_pnl_today DECIMAL(15, 2) NOT NULL,
    drawdown_pct DECIMAL(5, 2),
    active_positions INTEGER DEFAULT 0
);

-- Index for faster time-series queries
CREATE INDEX IF NOT EXISTS idx_account_metrics_timestamp ON public.account_metrics (timestamp DESC);

COMMENT ON TABLE public.account_metrics IS 'Stores periodic snapshots of account state for analytics and Grafana.';
