from fastapi import FastAPI, Header, HTTPException, Body
from typing import Any
import re

app = FastAPI()

API_KEY = "Key-2607"


def is_scam(message: str):
    if not message:
        return False
    keywords = ["bank", "upi", "account", "blocked", "otp", "click"]
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
    body: Any = Body(default={})
):
    # 🔐 API KEY CHECK
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    # 🧪 Handle tester ping (empty or invalid body)
    if not isinstance(body, dict):
        body = {}

    message = body.get("message")

    scam = is_scam(message)
    intel = extract_intelligence(message)

    reply = None
    if scam:
        reply = "I am confused, which bank is this about?"

    return {
        "scam_detected": scam,
        "agent_engaged": scam,
        "agent_reply": reply,
        "extracted_intelligence": intel
    }
