import subprocess
import json
import os
import sys
from app.storage.models import Finding

class BanditRunner:
    def analyze(self, file_path: str) -> list[Finding]:
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
                # Normalize severity
                raw_sev = item["issue_severity"].lower() # HIGH, MEDIUM, LOW
                
                findings.append(Finding(
                    tool="bandit",
                    category="security",
                    severity=raw_sev, # bandit already uses high/medium/low
                    file=file_path,
                    line=item["line_number"],
                    message=item["issue_text"],
                    code_snippet=item.get("code")
                ))
            return findings
            
        except Exception as e:
            print(f"Bandit failed: {e}")
            return []