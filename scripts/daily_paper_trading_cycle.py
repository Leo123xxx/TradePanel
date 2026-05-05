"""
scripts/daily_paper_trading_cycle.py
TradePanel — Daily paper trading cycle wrapper.

Called by main.py --mode paper-trade (and the overnight scheduler).
Runs one full detect+execute pass of the PaperEngine, then exits cleanly.

This module is intentionally thin — all strategy logic lives in
forward_test/paper_engine.py. This wrapper exists so that
main.py can import it without depending on the scheduler internals.
"""

import logging
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

logger = logging.getLogger(__name__)


def run_cycle(config_path: str = "config/config.yaml") -> bool:
    """
    Execute one detect + execute pass of the PaperEngine.

    Returns True on success, False if the engine could not connect
    or encountered a fatal error.
    """
    try:
        from forward_test.paper_engine import PaperEngine
        logger.info("Initialising PaperEngine...")
        engine = PaperEngine(config_path=config_path)

        logger.info("Running signal detection pass...")
        engine.run_detect()

        logger.info("Running trade execution pass...")
        engine.run_execute()

        logger.info("Paper trading cycle complete.")
        return True

    except ImportError as e:
        logger.error(
            f"Could not import PaperEngine — check MT5 bridge or docker mock: {e}"
        )
        return False
    except Exception as e:
        logger.error(f"Paper trading cycle failed: {e}", exc_info=True)
        return False


if __name__ == "__main__":
    # Allow running directly: python scripts/daily_paper_trading_cycle.py
    import argparse
    from dotenv import load_dotenv

    load_dotenv()
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(name)s — %(levelname)s — %(message)s",
    )

    parser = argparse.ArgumentParser(description="Run one paper trading cycle")
    parser.add_argument(
        "--config",
        default="config/config.yaml",
        help="Path to config.yaml (default: config/config.yaml)",
    )
    args = parser.parse_args()

    success = run_cycle(config_path=args.config)
    sys.exit(0 if success else 1)
