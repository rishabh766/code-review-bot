import hmac
import hashlib
import os 
import logging
from fastapi import APIRouter, Request, HTTPException, Header

logging.basicConfig(level = logging.INFO)
logger = logging.getLogger("webhook")

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
    event_type = request.headers.get("X-GitHub-Event")
    if event_type != "pull_request":
        logger.info(f"ignoring event : {event_type}")
        return {"status" : "ignored", "reason" : "not_a_pull_request"}
    action = payload.get("action")
    if action not in ["opened", "synchronize", "reopened"]:
        logger.info(f"igonoring PR action : {action}")
        return {"status" : "ignored", "reason": "unsupported_action"}
    
    pr_data = payload.get("pull_request", {})
    repo_data = payload.get("repository", {})

    log_context = {
        "repo" : repo_data.get("full_name"),
        "pr" : pr_data.get("number"),
        "action" : action,
        "head_sha" : pr_data.get("head", {}).get("sha")
    }
    logger.info(f"Processing PR Event : {log_context}")

    #TODO: trigger the analysis pipeline here

    return {"status" : "accepted", "context" : log_context}



    
