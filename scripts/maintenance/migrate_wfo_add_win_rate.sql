-- Migration: add oos_win_rate column to walk_forward_results
-- Run once via Adminer or psql before the next WFO run.
--
--   psql -U postgres -d tradepanel -f scripts/migrate_wfo_add_win_rate.sql
--   OR paste into Adminer → SQL → Execute
--
-- Safe to run multiple times (IF NOT EXISTS guard).

ALTER TABLE walk_forward_results
    ADD COLUMN IF NOT EXISTS oos_win_rate double precision DEFAULT 0.0;

-- Verify
SELECT column_name, data_type, column_default
FROM information_schema.columns
WHERE table_name = 'walk_forward_results'
  AND column_name = 'oos_win_rate';
