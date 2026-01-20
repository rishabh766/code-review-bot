import requests
import hmac
import hashlib
import json

SECRET = "my_super_secret_token_123"
URL = "http://127.0.0.1:8000/webhook"

def send_event(event_type, action):
    data = {"action": action, "pull_request": {"number": 101, "head": {"sha": "abc1234"}, "title": "Test"}}
    # If not PR, GitHub sends different structures, but for this test, the header matters most.
    
    payload = json.dumps(data).encode()
    signature = "sha256=" + hmac.new(SECRET.encode(), payload, hashlib.sha256).hexdigest()
    
    headers = {
        "X-Hub-Signature-256": signature,
        "X-GitHub-Event": event_type,
        "Content-Type": "application/json"
    }
    
    print(f"\n--- Sending {event_type} / {action} ---")
    resp = requests.post(URL, data=payload, headers=headers)
    print(f"Status: {resp.status_code} | Body: {resp.text}")

# Test 1: Valid PR Open
send_event("pull_request", "opened")

# Test 2: Invalid Action (e.g. closed)
send_event("pull_request", "closed")

# Test 3: Invalid Event (e.g. push)
send_event("push", "pushed")