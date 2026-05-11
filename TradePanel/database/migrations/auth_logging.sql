-- Authorization Logging Schema
-- Track all authorization attempts (authorized and unauthorized)
-- Created: May 10, 2026

CREATE TABLE IF NOT EXISTS telegram_auth_log (
    id SERIAL PRIMARY KEY,
    chat_id BIGINT NOT NULL,
    username VARCHAR(255),
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    status VARCHAR(20) NOT NULL,  -- 'authorized' or 'unauthorized'
    command_attempted VARCHAR(100),
    ip_address VARCHAR(45),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for fast lookups
CREATE INDEX IF NOT EXISTS idx_telegram_auth_log_chat_id ON telegram_auth_log(chat_id);
CREATE INDEX IF NOT EXISTS idx_telegram_auth_log_status ON telegram_auth_log(status);
CREATE INDEX IF NOT EXISTS idx_telegram_auth_log_timestamp ON telegram_auth_log(timestamp DESC);

-- View: Unauthorized access attempts (suspicious IPs)
CREATE OR REPLACE VIEW telegram_unauthorized_attempts AS
SELECT
    chat_id,
    username,
    first_name,
    last_name,
    command_attempted,
    COUNT(*) as attempt_count,
    MAX(timestamp) as last_attempt,
    MIN(timestamp) as first_attempt
FROM telegram_auth_log
WHERE status = 'unauthorized'
GROUP BY chat_id, username, first_name, last_name, command_attempted
ORDER BY last_attempt DESC;

-- View: Authorized users (access log)
CREATE OR REPLACE VIEW telegram_authorized_users AS
SELECT
    chat_id,
    username,
    first_name,
    last_name,
    COUNT(*) as command_count,
    MAX(timestamp) as last_access,
    MIN(timestamp) as first_access
FROM telegram_auth_log
WHERE status = 'authorized'
GROUP BY chat_id, username, first_name, last_name
ORDER BY last_access DESC;

-- View: Daily summary
CREATE OR REPLACE VIEW telegram_auth_daily_summary AS
SELECT
    DATE(timestamp) as date,
    status,
    COUNT(*) as attempt_count,
    COUNT(DISTINCT chat_id) as unique_users
FROM telegram_auth_log
GROUP BY DATE(timestamp), status
ORDER BY date DESC;
