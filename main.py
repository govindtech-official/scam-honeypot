from fastapi import FastAPI, Header, HTTPException, Body
from pydantic import BaseModel
from typing import Optional
import re

app = FastAPI()

API_KEY = "Key-2607"


class ScamRequest(BaseModel):
    conversation_id: Optional[str] = None
    message: Optional[str] = None
    history: Optional[list] = None


def is_scam(message: str):
    keywords = ["bank", "upi", "account", "blocked", "otp", "click"]
    if not message:
        return False
    for word in keywords:
        if word in message.lower():
            return True
    return False


def extract_intelligence(text: str):
    if not text:
        return {
            "upi_ids": [],
            "bank_accounts": [],
            "phishing_links": []
        }

    return {
        "upi_ids": re.findall(r"[\\w.-]+@[\\w]+", text),
        "bank_accounts": re.findall(r"\\b\\d{9,18}\\b", text),
        "phishing_links": re.findall(r"https?://\\S+", text)
    }


@app.post("/scam")
def receive_message(
    x_api_key: str = Header(None),
    data: Optional[ScamRequest] = Body(default=None)
):
    # 🔐 API KEY CHECK
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    # 🧪 Handle tester empty request
    if data is None or data.message is None:
        return {
            "scam_detected": False,
            "agent_engaged": False,
            "agent_reply": None,
            "extracted_intelligence": {
                "upi_ids": [],
                "bank_accounts": [],
                "phishing_links": []
            }
        }

    scam = is_scam(data.message)
    intel = extract_intelligence(data.message)

    reply = None
    if scam:
        reply = "I am confused, which bank is this about?"

    return {
        "scam_detected": scam,
        "agent_engaged": scam,
        "agent_reply": reply,
        "extracted_intelligence": intel
    }
