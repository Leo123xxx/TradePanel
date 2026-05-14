# scripts/check_dependencies.py
import sys

def check():
    packages = [
        "MetaTrader5",
        "psycopg2",
        "pandas",
        "numpy",
        "yaml",
        "apscheduler",
        "dotenv"
    ]
    
    missing = []
    print("Checking dependencies...")
    for pkg in packages:
        try:
            if pkg == "yaml":
                import yaml
            elif pkg == "dotenv":
                import dotenv
            else:
                __import__(pkg)
            print(f"  [OK] {pkg}")
        except ImportError:
            print(f"  [!!] {pkg} is NOT installed.")
            missing.append(pkg)
            
    if missing:
        print("\nFATAL: Missing dependencies. Run:")
        print(f"pip install {' '.join(missing)}")
        if "yaml" in missing: print("pip install pyyaml")
        if "dotenv" in missing: print("pip install python-dotenv")
        sys.exit(1)
    else:
        print("\nAll dependencies found.")
        sys.exit(0)

if __name__ == "__main__":
    check()
