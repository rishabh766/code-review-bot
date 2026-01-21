import hmac
import hashlib
import os 
import logging
from fastapi import APIRouter, Request, HTTPException, Header, BackgroundTasks

from app.github.client import GitHubClient
from app.github.diff_parser import DiffParser
from app.analysis.aggregator import Aggregator

logging.basicConfig(level = logging.INFO)
logger = logging.getLogger("webhook")

router = APIRouter()

WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET", "my_super_secret_token_123")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

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

def process_pr(event_data : dict):
    repo_full_name = event_data['repository']['full_name']
    owner, repo = repo_full_name.split("/")
    pr_number = event_data["pull_request"]["number"]

    logger.info(f"Processing PR#{pr_number} in {repo_full_name}...")
    client = GitHubClient(token = GITHUB_TOKEN)
    parser = DiffParser()
    aggregator = Aggregator()
    
    files_json = client.get_pr_files(owner, repo, pr_number)

    if not files_json:
        logger.warning("Could not fetch files (Invalid Token?). Using Mock Data.")
        files_json = [
            {"filename": "bad_code.py", "status": "modified", "patch": "x=1\npassword='123'"}
        ]

    valid_files = parser.filter_files(files_json)
    logger.info(f"Found {len(valid_files)} valid files to scan.")
    report = aggregator.analyze_pr(valid_files)
    client.post_comment(owner, repo, pr_number, report)

@router.post("/webhook")
async def handle_webhook(
    request: Request, 
    background_tasks: BackgroundTasks,
    x_hub_signature_256: str = Header(None)
):
    payload_bytes = await request.body()
    verify_signature(payload_bytes, x_hub_signature_256)
    
    payload = await request.json()
    event_type = request.headers.get("X-GitHub-Event")
    
    # Filter for PR events
    if event_type == "pull_request" and payload.get("action") in ["opened", "synchronize", "reopened"]:
        # Run processing in background
        background_tasks.add_task(process_pr, payload)
        return {"status": "processing", "message": "Analysis started"}
        
    return {"status": "ignored"}


    
