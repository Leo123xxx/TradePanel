import sys
import os
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from notifications.router import CommandRouter
import MetaTrader5 as mt5

def test_commands():
    print("Testing New Bot Commands...")
    router = CommandRouter()
    
    print("\n--- Testing /mode ---")
    print(router.get_mode().encode('ascii', 'ignore').decode())
    
    print("\n--- Testing /signals ---")
    print(router.get_signals().encode('ascii', 'ignore').decode())
    
    print("\n--- Testing /analysis ---")
    print(router.get_analysis().encode('ascii', 'ignore').decode())
    
    print("\n--- Testing /risk ---")
    print(router.get_risk().encode('ascii', 'ignore').decode())
    
    print("\n--- Testing /active ---")
    print(router.get_active().encode('ascii', 'ignore').decode())

if __name__ == "__main__":
    test_commands()
