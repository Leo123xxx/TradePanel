from fastapi import APIRouter, HTTPException, Response
import os
import requests
import logging
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/whatsapp", tags=["whatsapp"])
logger = logging.getLogger("whatsapp_router")

WAHA_URL = os.getenv("WAHA_URL", "http://waha:3000").rstrip("/")
WAHA_API_KEY = os.getenv("WAHA_API_KEY", "")
SESSION_NAME = "default"

def _get_headers():
    headers = {"Content-Type": "application/json"}
    if WAHA_API_KEY:
        headers["X-Api-Key"] = WAHA_API_KEY
    return headers

@router.get("/status")
def get_whatsapp_status():
    try:
        url = f"{WAHA_URL}/api/sessions/{SESSION_NAME}"
        response = requests.get(url, headers=_get_headers(), timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            status = data.get("status", "UNKNOWN")
            return {
                "status": status, 
                "connected": status == "WORKING",
                "phone": os.getenv("WHATSAPP_PHONE", "Not configured"),
                "details": data
            }
        elif response.status_code == 404:
            return {"status": "NO_SESSION", "connected": False, "phone": os.getenv("WHATSAPP_PHONE", "Not configured")}
        else:
            return {"status": "ERROR", "connected": False, "details": response.text}
    except Exception as e:
        return {"status": "ERROR", "connected": False, "details": str(e)}

@router.post("/qr")
def get_whatsapp_qr():
    """Trigger QR code generation or return existing one. Auto-starts session if stopped."""
    try:
        # Check current status
        check_url = f"{WAHA_URL}/api/sessions/{SESSION_NAME}"
        check_resp = requests.get(check_url, headers=_get_headers(), timeout=5)
        
        if check_resp.status_code == 404:
            # Session doesn't exist, create it
            logger.info(f"Creating WhatsApp session: {SESSION_NAME}")
            create_url = f"{WAHA_URL}/api/sessions/"
            create_resp = requests.post(create_url, json={"name": SESSION_NAME}, headers=_get_headers(), timeout=10)
            if create_resp.status_code not in (200, 201):
                raise HTTPException(status_code=500, detail="Failed to create WAHA session")
        else:
            data = check_resp.json()
            status = data.get("status")
            if status == "STOPPED":
                logger.info(f"Starting stopped WhatsApp session: {SESSION_NAME}")
                start_url = f"{WAHA_URL}/api/sessions/{SESSION_NAME}/start"
                requests.post(start_url, headers=_get_headers(), timeout=10)
                
        # Return instructions for the frontend
        return {
            "status": "INITIATED",
            "qr_image_url": "/api/whatsapp/qr_image",
            "dashboard_url": f"{os.getenv('WAHA_EXTERNAL_URL', 'http://localhost:8025')}/dashboard"
        }
    except Exception as e:
        logger.error(f"Error in WhatsApp QR endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/qr_image")
def get_whatsapp_qr_image():
    """Proxies the QR image from WAHA to the frontend"""
    try:
        qr_url = f"{WAHA_URL}/api/sessions/{SESSION_NAME}/auth/qr?format=image"
        resp = requests.get(qr_url, headers=_get_headers(), timeout=10)
        
        if resp.status_code == 200:
            return Response(content=resp.content, media_type="image/png")
        elif resp.status_code == 404:
            # Maybe session isn't in SCAN_QR_CODE state
            raise HTTPException(status_code=404, detail="QR code not available. Is the session starting or already connected?")
        else:
            raise HTTPException(status_code=resp.status_code, detail=f"WAHA error: {resp.text}")
    except Exception as e:
        logger.error(f"Error fetching QR image: {e}")
        raise HTTPException(status_code=500, detail=str(e))

