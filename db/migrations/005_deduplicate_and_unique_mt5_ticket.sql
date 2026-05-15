-- Cleanup duplicates in trades table before adding unique constraint
-- Keep only the newest row (highest created_at) for each mt5_ticket
DELETE FROM trades
WHERE trade_id NOT IN (
    SELECT trade_id
    FROM (
        SELECT trade_id,
               ROW_NUMBER() OVER (PARTITION BY mt5_ticket ORDER BY created_at DESC) as rn
        FROM trades
        WHERE mt5_ticket IS NOT NULL
    ) t
    WHERE t.rn = 1
);

-- Now add the unique constraint
ALTER TABLE trades ADD CONSTRAINT trades_mt5_ticket_key UNIQUE (mt5_ticket);
