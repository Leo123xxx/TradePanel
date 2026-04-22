import http.server
import socketserver
import os
import json
import glob
from pathlib import Path

PORT = 5000
DASHBOARD_DIR = Path("dashboard")
DATA_DIR = Path("results/daily_validation")

class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Serve static files from the dashboard directory
        super().__init__(*args, directory=str(DASHBOARD_DIR), **kwargs)

    def do_GET(self):
        if self.path == '/api/data':
            self.serve_latest_data()
        else:
            super().do_GET()

    def serve_latest_data(self):
        """Finds the most recent dashboard_*.json file and serves its content."""
        try:
            files = list(DATA_DIR.glob("dashboard_*.json"))
            if not files:
                self.send_error(404, "No dashboard data found. Run validation suite first.")
                return

            # Sort by modification time to get the newest
            latest_file = max(files, key=os.path.getmtime)
            
            with open(latest_file, 'r') as f:
                data = json.load(f)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode('utf-8'))
        except Exception as e:
            self.send_error(500, f"Error serving data: {str(e)}")

if __name__ == "__main__":
    # Ensure directories exist
    if not DASHBOARD_DIR.exists():
        print(f"Error: Dashboard directory {DASHBOARD_DIR} not found.")
        exit(1)
        
    print(f"==================================================")
    print(f"  TRADEPANEL PRO DASHBOARD SERVER")
    print(f"  URL: http://localhost:{PORT}")
    print(f"  Data Source: {DATA_DIR}")
    print(f"==================================================")
    
    with socketserver.TCPServer(("", PORT), DashboardHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")
            httpd.shutdown()
