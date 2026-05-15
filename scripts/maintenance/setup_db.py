import os
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
import psycopg2
from dotenv import load_dotenv

def setup_database():
    load_dotenv()
    
    # Connection details
    conn_params = {
        "host": os.getenv("DB_HOST", "127.0.0.1"),
        "port": os.getenv("DB_PORT", "5432"),
        "database": os.getenv("DB_NAME", "trading_platform"),
        "user": os.getenv("DB_USER", "postgres"),
        "password": os.getenv("DB_PASSWORD", "postgres")
    }
    
    try:
        conn = psycopg2.connect(**conn_params)
        conn.autocommit = True
        cur = conn.cursor()
        
        print("Creating tables...")
        
        # 1. strategies
        cur.execute("""
            CREATE TABLE IF NOT EXISTS strategies (
                strategy_id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                category VARCHAR(50),
                status VARCHAR(20) DEFAULT 'ACTIVE',
                parameters JSONB,
                version INT DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # 2. backtest_runs
        cur.execute("""
            CREATE TABLE IF NOT EXISTS backtest_runs (
                run_id SERIAL PRIMARY KEY,
                strategy_id INT REFERENCES strategies(strategy_id),
                pair VARCHAR(20),
                timeframe VARCHAR(10),
                start_date TIMESTAMP,
                end_date TIMESTAMP,
                metrics JSONB,
                scorecard JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # 3. signals
        cur.execute("""
            CREATE TABLE IF NOT EXISTS signals (
                signal_id SERIAL PRIMARY KEY,
                strategy_id INT REFERENCES strategies(strategy_id),
                timestamp TIMESTAMP NOT NULL,
                pair VARCHAR(20),
                direction VARCHAR(10),
                indicator_values JSONB,
                triggered_trade_id UUID
            );
        """)
        
        # 4. trades (Detailed in Master Plan Section 5.2)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS trades (
                trade_id UUID PRIMARY KEY,
                strategy_id INT REFERENCES strategies(strategy_id),
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
        """)
        
        # 5. positions
        cur.execute("""
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
        """)
        
        # 6. bot_health
        cur.execute("""
            CREATE TABLE IF NOT EXISTS bot_health (
                health_id SERIAL PRIMARY KEY,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                event_type VARCHAR(50), -- HEARTBEAT | CONNECTION_LOST | ERROR
                status VARCHAR(20),
                message TEXT,
                meta_data JSONB
            );
        """)
        
        # 7. daily_summary
        cur.execute("""
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
        """)
        
        # 8. commands
        cur.execute("""
            CREATE TABLE IF NOT EXISTS commands (
                command_id SERIAL PRIMARY KEY,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                command_text TEXT NOT NULL,
                status VARCHAR(20) DEFAULT 'PENDING', -- PENDING | PROCESSED | FAILED
                response_text TEXT
            );
        """)
        
        # 9. market_data
        cur.execute("""
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
        """)
        
        # 10. regime_log
        cur.execute("""
            CREATE TABLE IF NOT EXISTS regime_log (
                regime_id SERIAL PRIMARY KEY,
                pair VARCHAR(20) NOT NULL,
                timestamp TIMESTAMP NOT NULL,
                regime VARCHAR(50), -- TRENDING | RANGING | HIGH_VOL | LOW_VOL
                adx_value NUMERIC,
                atr_value NUMERIC
            );
        """)
        
        # 11. cot_data — CFTC Commitments of Traders weekly data
        cur.execute("""
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
        """)

        print("SUCCESS: All 11 tables created successfully.")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"ERROR setting up database: {e}")

if __name__ == "__main__":
    setup_database()
