-- migrate_account_profiles.sql
-- Creates account_profiles table and seeds Demo / Live / Paper accounts.
-- Adds account_id FK column to trades (nullable -- existing rows keep NULL).

-- 1. Account profiles table
CREATE TABLE IF NOT EXISTS account_profiles (
    account_id   SERIAL PRIMARY KEY,
    account_name VARCHAR(80)  NOT NULL,
    account_type VARCHAR(20)  NOT NULL CHECK (account_type IN ('DEMO','LIVE','PAPER')),
    broker       VARCHAR(80)  DEFAULT 'MetaTrader 5',
    currency     VARCHAR(10)  DEFAULT 'USD',
    initial_balance NUMERIC(14,2) DEFAULT 10000.00,
    is_active    BOOLEAN      DEFAULT TRUE,
    notes        TEXT,
    created_at   TIMESTAMPTZ  DEFAULT NOW(),
    updated_at   TIMESTAMPTZ  DEFAULT NOW()
);

-- 2. Remove duplicate seed rows FIRST (keep lowest account_id per name)
DELETE FROM account_profiles
WHERE account_id NOT IN (
    SELECT MIN(account_id) FROM account_profiles GROUP BY account_name
);

-- Reset sequence to the current max so next INSERT gets a clean id
SELECT setval('account_profiles_account_id_seq', (SELECT MAX(account_id) FROM account_profiles));

-- 3. NOW add UNIQUE constraint (safe because duplicates are gone)
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'account_profiles_account_name_key'
          AND conrelid = 'account_profiles'::regclass
    ) THEN
        ALTER TABLE account_profiles ADD CONSTRAINT account_profiles_account_name_key UNIQUE (account_name);
    END IF;
END$$;

-- 4. Seed the three standard profiles (skip if already present)
INSERT INTO account_profiles (account_name, account_type, broker, currency, initial_balance, notes)
VALUES
    ('Demo Account',  'DEMO',  'MetaTrader 5', 'USD', 10000.00, 'Primary demo / simulation account'),
    ('Live Account',  'LIVE',  'MetaTrader 5', 'USD', 10000.00, 'Live funded account'),
    ('Paper Account', 'PAPER', 'MetaTrader 5', 'USD', 10000.00, 'Paper trading / forward test')
ON CONFLICT (account_name) DO NOTHING;

-- 5. Add account_id to trades (nullable to not break existing rows)
ALTER TABLE trades ADD COLUMN IF NOT EXISTS account_id INTEGER REFERENCES account_profiles(account_id);

-- Index for fast account-scoped queries
CREATE INDEX IF NOT EXISTS idx_trades_account_id ON trades(account_id);

-- 6. Auto-update trigger for account_profiles.updated_at
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

-- Verification
SELECT account_id, account_name, account_type, currency, initial_balance
FROM account_profiles
ORDER BY account_id;
