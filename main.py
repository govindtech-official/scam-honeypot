from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import re

app = FastAPI()

API_KEY = "Key-2607"


class ScamRequest(BaseModel):
    conversation_id: str
    message: str
    history: list


def is_scam(message: str):
    keywords = ["bank", "upi", "account", "blocked", "otp", "click"]
    for word in keywords:
        if word in message.lower():
            return True
    return False


def extract_intelligence(text: str):
    upi_ids = re.findall(r"[\\w.-]+@[\\w]+", text)
    bank_accounts = re.findall(r"\\b\\d{9,18}\\b", text)
    phishing_links = re.findall(r"https?://\\S+", text)

    return {
        "upi_ids": upi_ids,
        "bank_accounts": bank_accounts,
        "phishing_links": phishing_links
    }


@app.post("/scam")
def receive_message(
    data: ScamRequest,
    x_api_key: str = Header(None)
):
    # 🔐 API KEY CHECK
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

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

