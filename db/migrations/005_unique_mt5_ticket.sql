-- Add unique constraint to mt5_ticket in trades table
ALTER TABLE trades ADD CONSTRAINT trades_mt5_ticket_key UNIQUE (mt5_ticket);
