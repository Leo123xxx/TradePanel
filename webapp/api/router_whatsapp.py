from fastapi import APIRouter, HTTPException
import os
import requests
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/whatsapp", tags=["whatsapp"])

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
            return {
                "status": data.get("status", "UNKNOWN"), 
                "connected": data.get("status") == "WORKING",
                "phone": os.getenv("WHATSAPP_PHONE", "Not configured")
            }
        elif response.status_code == 404:
            return {"status": "NO_SESSION", "connected": False, "phone": os.getenv("WHATSAPP_PHONE", "Not configured")}
        else:
            return {"status": "ERROR", "connected": False, "details": response.text}
    except Exception as e:
        return {"status": "ERROR", "connected": False, "details": str(e)}

@router.post("/qr")
def get_whatsapp_qr():
    """Trigger QR code generation or return existing one"""
    try:
        # First check if session exists
        check_url = f"{WAHA_URL}/api/sessions/{SESSION_NAME}"
        check_resp = requests.get(check_url, headers=_get_headers(), timeout=5)
        
        if check_resp.status_code == 404:
            # Session doesn't exist, create it
            create_url = f"{WAHA_URL}/api/sessions/"
            create_resp = requests.post(create_url, json={"name": SESSION_NAME}, headers=_get_headers(), timeout=10)
            if create_resp.status_code not in (200, 201):
                raise HTTPException(status_code=500, detail="Failed to create WAHA session")
                
        # Get QR code
        qr_url = f"{WAHA_URL}/api/sessions/{SESSION_NAME}/auth/qr"
        qr_resp = requests.get(qr_url, headers=_get_headers(), timeout=10)
        
        if qr_resp.status_code == 200:
            # Returning the raw image data is complex, let's just instruct the frontend to use the URL directly
            # or return the URL if the backend is exposed. But wait, WAHA handles QR via its own UI too.
            # We will just return the URL to the QR code
            return {"qr_url": f"{WAHA_URL}/dashboard"}
            
        raise HTTPException(status_code=500, detail="Failed to fetch QR code")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
