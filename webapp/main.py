import asyncio
import sys
import os

try:
    import MetaTrader5 as mt5
except ImportError:
    from mt5_bridge.docker_mock import setup_mock
    setup_mock()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from webapp.api.router_logs import router as logs_router
from webapp.api.router_data import router as data_router
from webapp.api.router_analytics import router as analytics_router
from webapp.api.router_backtests import router as backtests_router
from webapp.api.router_accounts import router as accounts_router
from webapp.api.router_telegram import router as telegram_router
from webapp.api.router_whatsapp import router as whatsapp_router
from webapp.api.router_papertrades import router as papertrades_router
from webapp.api.router_health import router as health_router
from webapp.api.router_wfo import router as wfo_router
from webapp.api.router_intelligence import router as intelligence_router
from webapp.api.router_metrics import router as metrics_router

from webapp.bus import bus
import os

app = FastAPI(title="TradePanel Publication Hub")

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(logs_router, prefix="/api")
app.include_router(data_router, prefix="/api")
app.include_router(analytics_router, prefix="/api")
app.include_router(backtests_router, prefix="/api")
app.include_router(accounts_router, prefix="/api")
app.include_router(telegram_router, prefix="/api")
app.include_router(whatsapp_router, prefix="/api")
app.include_router(papertrades_router, prefix="/api")
app.include_router(health_router, prefix="/api")
app.include_router(wfo_router, prefix="/api")
app.include_router(intelligence_router, prefix="/api")
app.include_router(metrics_router, prefix="/api")


# Mount Static Files (Production Build)
frontend_dist = os.path.join("webapp", "frontend", "dist")
if os.path.exists(frontend_dist):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")

@app.on_event("startup")
async def startup_event():
    # Start the Postgres LISTEN loop in the background
    asyncio.create_task(bus.start_listening())
    print("EventBus listener started.")

@app.on_event("shutdown")
def shutdown_event():
    bus.stop()
    print("EventBus listener stopped.")

@app.get("/")
async def root():
    """Serve the visual glassmorphic dashboard."""
    index_path = os.path.join(frontend_dist, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"status": "TradePanel API is running", "message": "Frontend build missing. Run npm run build."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
