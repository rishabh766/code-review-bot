import requests
import hmac 
import hashlib
import json

SECRET = "my_super_secret_token_123"
URL = "http://127.0.0.1:8000/webhook"

data = {"action" : "opened", "pull_request":{"title" : "Test PR"}}
payload = json.dumps(data).encode()

signature = "sha256=" + hmac.new(SECRET.encode(), payload, hashlib.sha256).hexdigest()

headers = {
    "X-Hub-Signature-256": signature,
    "X-GitHub-Event": "pull_request",
    "Content-Type": "application/json"
}

response = requests.post(URL, data=payload, headers=headers)
print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")