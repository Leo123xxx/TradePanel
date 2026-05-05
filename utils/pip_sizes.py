"""
utils/pip_sizes.py — Shared PIP_SIZES configuration.
"""

PIP_SIZES = {
    # ── Original pairs ──────────────────────────────────────────────────────
    "EURUSD": 0.0001,
    "GBPUSD": 0.0001,
    "USDJPY": 0.01,     # JPY pairs: price in XX.YY, 1 pip = 0.01
    "XAUUSD": 0.10,     # Gold: price in XXXX.X, 1 pip = $0.10/oz
    "XAGUSD": 0.001,    # Silver: price in XX.XXX, 1 pip = $0.001/oz
    "BTCUSD": 1.0,      # Bitcoin: 1 pip = $1
    "ETHUSD": 1.0,      # Ethereum: 1 pip = $1
    # ── New pairs added 2026-04-30 ───────────────────────────────────────────
    # pip_size must be consistent with pip_value_per_lot in config.yaml
    # gross_usd = (price_diff / pip_size) * pip_value_per_lot * lot_size
    "GBPJPY":  0.01,    # JPY cross: 1 pip = 0.01 JPY; pip_val=6.7 USD/pip/lot
    "AUDUSD":  0.0001,  # FX major: standard 4-decimal; pip_val=10.0 USD/pip/lot
    "USDCAD":  0.0001,  # FX major: standard 4-decimal; pip_val=7.5 USD/pip/lot
    "USDZAR":  0.0001,  # Exotic FX: standard 4-decimal; pip_val=10.0 ZAR/pip/lot
    "USOIL":   0.01,    # Crude WTI: price in XX.XXX, 1 pip=$0.01; pip_val=10.0 USD/pip/lot
    "US500":   1.0,     # S&P 500 index: 1 pip = 1 index point; pip_val=1.0 USD/pip/lot
    "USTEC":   1.0,     # Nasdaq 100 index: 1 pip = 1 index point; pip_val=1.0 USD/pip/lot
    "NVDA":    0.01,    # Stock CFD: price in XXX.XX, 1 pip=$0.01; pip_val=1.0 USD/pip/lot
    "AMD":     0.01,    # Stock CFD: 1 pip=$0.01; pip_val=1.0 USD/pip/lot
    "MSFT":    0.01,    # Stock CFD: 1 pip=$0.01; pip_val=1.0 USD/pip/lot
    "AAPL":    0.01,    # Stock CFD: 1 pip=$0.01; pip_val=1.0 USD/pip/lot
}

DEFAULT_PIP_SIZE = 0.0001

def get_pip_size(symbol):
    return PIP_SIZES.get(symbol, DEFAULT_PIP_SIZE)
