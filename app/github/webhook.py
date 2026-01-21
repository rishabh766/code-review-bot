import hmac
import hashlib
import os
import logging
from fastapi import APIRouter, Request, HTTPException, Header, BackgroundTasks

from app.github.client import GitHubClient
from app.github.diff_parser import DiffParser
from app.analysis.aggregator import Aggregator
from app.storage.dedup import Deduplicator # <--- Import

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("webhook")

router = APIRouter()
WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET", "my_super_secret_token_123")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def verify_signature(payload: bytes, signature: str):
    if not signature:
        raise HTTPException(status_code=403, detail="Missing signature")
    expected_signature = "sha256=" + hmac.new(
        key=WEBHOOK_SECRET.encode(), 
        msg=payload, 
        digestmod=hashlib.sha256
    ).hexdigest()
    if not hmac.compare_digest(expected_signature, signature):
        raise HTTPException(status_code=403, detail="Invalid signature")

def process_pr(event_data: dict):
    repo_full_name = event_data["repository"]["full_name"]
    owner, repo = repo_full_name.split("/")
    pr_number = event_data["pull_request"]["number"]
    head_sha = event_data["pull_request"]["head"]["sha"]
    
    logger.info(f" Processing PR #{pr_number}...")

    # 1. Initialize Tools
    client = GitHubClient(token=GITHUB_TOKEN)
    parser = DiffParser()
    aggregator = Aggregator()
    deduplicator = Deduplicator() # <--- Init

    # 2. Fetch Files
    files_json = client.get_pr_files(owner, repo, pr_number)
    
    if not files_json:
        logger.warning(" Could not fetch files. Using Mock Data.")
        # FIX: Add '+' to simulate a real Git Diff
        files_json = [
            {
                "filename": "bad_code.py", 
                "status": "modified", 
                "patch": """@@ -1,2 +1,3 @@
                +x = 1
                +password = '123'
                +eval("print('hacking system')")
                """
            }
        ]

    # 3. Filter & Analyze
    valid_files = parser.filter_files(files_json)
    result = aggregator.analyze_pr(valid_files)

    # 4. Deduplicate Inline Comments
    raw_comments = result["inline_comments"]
    new_comments = []
    
    for c in raw_comments:
        if not deduplicator.is_duplicate(pr_number, c['path'], c['line'], c['body']):
            new_comments.append(c)
            # Mark as posted immediately (Optimistic)
            deduplicator.mark_as_posted(pr_number, c['path'], c['line'], c['body'])
        else:
            logger.info(f" Skipping duplicate comment on {c['path']}:{c['line']}")

    # 5. Post Inline Comments (Only new ones)
    if new_comments:
        client.post_batch_review(owner, repo, pr_number, head_sha, new_comments)
    else:
        logger.info(" No new inline comments to post.")

    # 6. Post Summary (Always post summary for now)
    client.post_comment(owner, repo, pr_number, result["summary_text"])

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
    
    if event_type == "pull_request" and payload.get("action") in ["opened", "synchronize", "reopened"]:
        background_tasks.add_task(process_pr, payload)
        return {"status": "processing"}
        
    return {"status": "ignored"}