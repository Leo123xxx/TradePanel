import sys
import os
import time
import zlib
from datetime import datetime, timedelta
import json

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

try:
    import MetaTrader5 as mt5
except ImportError:
    print("MetaTrader5 package not found. Please install it with 'pip install MetaTrader5'")
    sys.exit(1)

from data.db_client import DBClient

def sync_mt5_account():
    """
    Syncs history and open positions from the current MT5 account to the database.
    Distinguishes between Manual trades (magic=0) and Bot trades (magic!=0).
    """
    print("\n" + "="*60)
    print("  TradePanel — MT5 Account History Synchronizer")
    print("="*60)

    # 1. Connect to MT5
    login = int(os.getenv("MT5_LOGIN", 0))
    password = os.getenv("MT5_PASSWORD", "")
    server = os.getenv("MT5_SERVER", "")

    if not mt5.initialize(login=login, password=password, server=server):
        print(f"FAILED to initialize MT5: {mt5.last_error()}")
        return

    account_info = mt5.account_info()
    if not account_info:
        print("FAILED to get account info.")
        mt5.shutdown()
        return

    print(f"Connected to Account: {account_info.login} ({account_info.company})")
    print(f"Balance: {account_info.balance} {account_info.currency}")
    print(f"Equity:  {account_info.equity}")

    db = DBClient()

    # 2. Map Account to DB account_id
    # We use account_type from .env or just map to account_id=1 for Demo
    account_id = 1 # Default Demo
    if os.getenv("TRADING_MODE") == "live":
        account_id = 2 # Live
    
    # Check if this account exists or update it
    db.execute_query(
        "UPDATE account_profiles SET initial_balance = %s, currency = %s, notes = %s, updated_at = NOW() WHERE account_id = %s",
        (account_info.balance, account_info.currency, f"Live Sync: {account_info.login} / {account_info.server}", account_id)
    )

    # 3. Fetch History (Deals)
    # Fetch from Jan 2024 to get full account history
    from_date = datetime(2024, 1, 1)
    to_date = datetime.now() + timedelta(days=1)
    
    deals = mt5.history_deals_get(from_date, to_date)
    if deals is None:
        print("No history deals found or error occurred.")
    else:
        print(f"Found {len(deals)} history deals. Syncing...")
        sync_deals(db, deals, account_id, from_date, to_date)

    # 4. Fetch Open Positions
    positions = mt5.positions_get()
    if positions is None:
        print("No open positions found.")
    else:
        print(f"Found {len(positions)} open positions. Syncing...")
        sync_positions(db, positions, account_id)

    print("\nSync completed successfully.")
    mt5.shutdown()

def sync_deals(db, deals, account_id, from_date, to_date):
    """
    MT5 Deals represent executions. We want to reconstruct 'Trades' (Entry to Exit).
    Simplification: We look for Out-deals and find their corresponding In-deal or just log them.
    Actually, let's just log every 'Out' deal as a closed trade if it has a profit.
    """
    inserted = 0
    updated = 0
    
    # Get strategy mapping
    strategy_rows = db.execute_query("SELECT strategy_id, name FROM strategies")
    name_to_id = {r[1]: r[0] for r in strategy_rows}
    
    # Magic Number Map (from zlib.adler32 logic in PaperEngine)
    # We don't have the registry here easily, but we can reverse it from the DB
    magic_to_id = {}
    for name, s_id in name_to_id.items():
        magic = zlib.adler32(name.encode()) % 1000000
        magic_to_id[magic] = s_id

    for d in deals:
        # We only care about DEAL_ENTRY_OUT (closing a position) to record a full trade
        # entry=1 is OUT, entry=0 is IN
        if d.entry != 1: 
            continue
            
        # Check if already exists by position_id (stored in mt5_ticket)
        exists = db.execute_query("SELECT trade_id FROM trades WHERE mt5_ticket = %s", (d.position_id,))
        if exists:
            continue

        # Map magic to strategy
        strategy_id = magic_to_id.get(d.magic)
        
        # Calculate P&L (gross_pnl is d.profit)
        # Exness Demo is ZAR, but d.profit is in account currency.
        pnl = d.profit + d.swap + d.commission
        
        # Direction from d.type (DEAL_TYPE_BUY = 0, DEAL_TYPE_SELL = 1)
        # Note: An OUT deal of type BUY means it was closing a SELL position.
        # So we need to find the IN deal to get the original direction.
        # For now, we'll simplify: if profit > 0 and type=BUY, it was probably a sell close.
        # Better: get the position ID.
        
        # Look for the IN deal for this position
        # We search the whole history range to find the entry deal
        pos_deals = mt5.history_deals_get(from_date, to_date, position=d.position_id)
        if pos_deals:
            in_deal = next((x for x in pos_deals if x.entry == 0), None)
            if in_deal:
                direction = "BUY" if in_deal.type == 0 else "SELL"
                entry_price = in_deal.price
                open_time = datetime.fromtimestamp(in_deal.time)
            else:
                # If we can't find the entry deal, we skip this to avoid partial trades
                continue
        else:
            continue

        query = """
            INSERT INTO trades 
            (trade_id, strategy_id, account_id, pair, direction, lot_size, 
             entry_price, exit_price, open_time, close_time, net_pnl, 
             status, mt5_ticket, mode)
            VALUES (gen_random_uuid(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        db.execute_query(query, (
            strategy_id, account_id, d.symbol, direction, d.volume,
            entry_price, d.price, open_time, datetime.fromtimestamp(d.time),
            pnl, 'CLOSED', d.position_id, 'LIVE' if account_id == 2 else 'DEMO'
        ))
        inserted += 1

    print(f"  Deals: {inserted} new trades synced.")

def sync_positions(db, positions, account_id):
    """Syncs currently open positions to the trades table."""
    # Get strategy mapping
    strategy_rows = db.execute_query("SELECT strategy_id, name FROM strategies")
    name_to_id = {r[1]: r[0] for r in strategy_rows}
    magic_to_id = {zlib.adler32(name.encode()) % 1000000: s_id for name, s_id in name_to_id.items()}

    synced = 0
    for p in positions:
        # Check if already exists
        exists = db.execute_query("SELECT trade_id FROM trades WHERE mt5_ticket = %s AND status = 'OPENED'", (p.ticket,))
        if exists:
            continue

        strategy_id = magic_to_id.get(p.magic)
        direction = "BUY" if p.type == 0 else "SELL"
        
        query = """
            INSERT INTO trades 
            (trade_id, strategy_id, account_id, pair, direction, lot_size, 
             entry_price, open_time, status, mt5_ticket, mode)
            VALUES (gen_random_uuid(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (mt5_ticket) DO UPDATE SET status = 'OPENED'
        """
        db.execute_query(query, (
            strategy_id, account_id, p.symbol, direction, p.volume,
            p.price_open, datetime.fromtimestamp(p.time), 'OPENED', p.ticket,
            'LIVE' if account_id == 2 else 'DEMO'
        ))
        synced += 1
    
    print(f"  Positions: {synced} open positions synced/updated.")

if __name__ == "__main__":
    sync_mt5_account()
