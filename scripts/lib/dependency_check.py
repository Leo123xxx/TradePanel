import sys
import os
import importlib.metadata
from pathlib import Path
from dotenv import load_dotenv

def check_dependencies():
    """
    Verifies that all required packages and environment variables are present.
    Exits with code 1 if anything is missing.
    """
    project_root = Path(__file__).parent.parent.parent
    load_dotenv(project_root / ".env")
    
    # 1. Check Python Version
    if sys.version_info < (3, 10):
        print(f"Error: Python 3.10 or higher is required. Current: {sys.version}")
        sys.exit(1)
        
    # 2. Check Required Packages
    required = [
        'pandas', 'numpy', 'psycopg2', 'python-dotenv', 
        'pyarrow', 'yfinance'
    ]
    
    # MetaTrader5 is Windows-only
    if os.name == 'nt':
        required.append('MetaTrader5')
        
    missing = []
    for package in required:
        try:
            importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            # Some packages have different names in pip vs import
            if package == 'psycopg2':
                try:
                    importlib.metadata.version('psycopg2-binary')
                    continue
                except importlib.metadata.PackageNotFoundError:
                    pass
            elif package == 'python-dotenv':
                 try:
                    importlib.metadata.version('python-dotenv')
                    continue
                 except importlib.metadata.PackageNotFoundError:
                    pass
            missing.append(package)
            
    if missing:
        print(f"Error: Missing required packages: {', '.join(missing)}")
        print(f"Please run: pip install -r {project_root / 'requirements.txt'}")
        sys.exit(1)
        
    # 3. Check Environment Variables
    crucial_env = ['DB_HOST', 'DB_NAME', 'DB_USER', 'DB_PASSWORD']
    missing_env = [var for var in crucial_env if not os.getenv(var)]
    
    if missing_env:
        print(f"Error: Missing environment variables in .env: {', '.join(missing_env)}")
        sys.exit(1)
        
    return True

if __name__ == "__main__":
    if check_dependencies():
        print("All dependencies and environment variables are present.")
