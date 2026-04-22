# scripts/test_paper_iteration.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from forward_test.paper_engine import PaperEngine

if __name__ == "__main__":
    print("Starting Paper Engine dry-run iteration...")
    try:
        engine = PaperEngine()
        engine.run_once()
        print("Dry-run complete. Check logs for signals or risk blocks.")
    except Exception as e:
        print(f"Dry-run FAILED: {e}")
