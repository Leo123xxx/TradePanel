-- db/init/003_add_timeframe_to_signals.sql

ALTER TABLE signals ADD COLUMN IF NOT EXISTS timeframe VARCHAR(10);
