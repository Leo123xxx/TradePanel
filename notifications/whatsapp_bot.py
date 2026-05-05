import os
import re
import requests
import json
import logging
from dotenv import load_dotenv

load_dotenv()

class WhatsAppBot:
    def __init__(self):
        self.waha_url = os.getenv("WAHA_URL", "http://waha:3000").rstrip("/")
        self.api_key = os.getenv("WAHA_API_KEY", "")
        self.default_phone = os.getenv("WHATSAPP_PHONE", "")
        self.session_name = "default"
        self.logger = logging.getLogger("WhatsAppBot")

    def _get_headers(self):
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["X-Api-Key"] = self.api_key
        return headers

    @staticmethod
    def _html_to_whatsapp(text: str) -> str:
        """Convert Telegram HTML formatting to WhatsApp-compatible text.

        Converts:
          <b>text</b>  →  *text*
          <i>text</i>  →  _text_
          <code>text</code>  →  `text`
          <a href='url'>text</a>  →  text (url)
          &amp; → &, &lt; → <, &gt; → >
          Strips all remaining HTML tags.
        """
        t = text
        # Bold
        t = re.sub(r"<b>(.*?)</b>", r"*\1*", t, flags=re.DOTALL)
        # Italic
        t = re.sub(r"<i>(.*?)</i>", r"_\1_", t, flags=re.DOTALL)
        # Code
        t = re.sub(r"<code>(.*?)</code>", r"`\1`", t, flags=re.DOTALL)
        # Links
        t = re.sub(r"<a\s+href=['\"]([^'\"]+)['\"]>(.*?)</a>", r"\2 (\1)", t, flags=re.DOTALL)
        # HTML entities
        t = t.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
        # Strip remaining HTML tags
        t = re.sub(r"<[^>]+>", "", t)
        return t

    def send_message(self, phone: str, text: str) -> bool:
        """Send a WhatsApp message via WAHA."""
        if not phone:
            self.logger.error("No phone number provided for WhatsApp message.")
            return False

        # Convert HTML formatting to WhatsApp-native formatting
        clean_text = self._html_to_whatsapp(text)

        # WAHA expects the phone number with @c.us suffix
        chat_id = f"{phone}@c.us" if not phone.endswith("@c.us") else phone

        payload = {
            "session": self.session_name,
            "chatId": chat_id,
            "text": clean_text
        }

        try:
            url = f"{self.waha_url}/api/sendText"
            response = requests.post(url, json=payload, headers=self._get_headers(), timeout=10)
            if response.status_code in (200, 201):
                self.logger.info(f"WhatsApp message sent to {phone}")
                return True
            else:
                self.logger.error(f"Failed to send WhatsApp message: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            self.logger.error(f"Error sending WhatsApp message: {e}")
            return False

    def send_alert(self, text: str) -> bool:
        """Send an alert to the default configured phone number."""
        if not self.default_phone:
            self.logger.warning("WHATSAPP_PHONE not set in .env. Skipping WhatsApp alert.")
            return False
        return self.send_message(self.default_phone, text)

    def get_status(self) -> dict:
        """Get the WAHA session status."""
        try:
            url = f"{self.waha_url}/api/sessions/{self.session_name}"
            response = requests.get(url, headers=self._get_headers(), timeout=5)
            if response.status_code == 200:
                data = response.json()
                return {"status": data.get("status", "UNKNOWN"), "connected": data.get("status") == "WORKING"}
            return {"status": "DISCONNECTED", "connected": False}
        except Exception as e:
            self.logger.error(f"Error getting WAHA status: {e}")
            return {"status": "ERROR", "connected": False}

