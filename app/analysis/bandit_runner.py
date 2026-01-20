import subprocess
import json
import os
import sys

class BanditRunner:
    def analyze(self, file_path: str):
        if not os.path.exists(file_path):
            return []
        cmd = [sys.executable, "-m", "bandit", "-f", "json", "-q", file_path]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if not result.stdout.strip():
                return []
                
            data = json.loads(result.stdout)
            findings = []
            for item in data.get("results", []):
                findings.append({
                    "tool": "bandit",
                    "severity": item["issue_severity"],
                    "message": item["issue_text"],
                    "line": item["line_number"],
                    "file": file_path
                })
            return findings
        except Exception as e:
            print(f"Bandit failed: {e}")
            return []