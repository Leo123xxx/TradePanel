import os
import sys

# Add the project root to the Python path to ensure module imports work
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from data.ingestion import run_full_ingestion

if __name__ == "__main__":
    try:
        run_full_ingestion()
    except KeyboardInterrupt:
        print("\nIngestion cancelled by user.")
    except Exception as e:
        print(f"\nFATAL ERROR: {e}")
        sys.exit(1)
