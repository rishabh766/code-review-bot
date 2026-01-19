import hmac
import hashlib
import os 
from fastapi import APIRouter, Request, HTTPException, Header

router = APIRouter()

WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET", "my_super_secret_token_123")

def verify_signature(payload:bytes, signature:str):
    if not signature:
        raise HTTPException(status_code=403, detail = "Missing Signature header")
    
    if not signature.startswith("sha256="):
        raise HTTPException(status_code=403, detail="Invalid signature format")
    
    expected_signature = "sha256=" + hmac.new(
        key = WEBHOOK_SECRET.encode(),
        msg = payload,
        digestmod=hashlib.sha256
        ).hexdigest()
    
    if not hmac.compare_digest(expected_signature, signature):
        return HTTPException(status_code=403, detail="Invalid signature")
    

@router.post("/webhook")
async def handle_webhook(request: Request, x_hub_signature_256 : str = Header(None)):
    payload_bytes = await request.body()

    verify_signature(payload_bytes, x_hub_signature_256)
    payload = await request.json()
    event_type = request.headers.get("X-GitHub-Event", "unknown")
    print(f"Recieved a valid webhook. Event : {event_type}")
    return {"status" : "recieved"}


    
