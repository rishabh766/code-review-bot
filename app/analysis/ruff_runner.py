import subprocess
import json
import os
from app.storage.models import Finding

class RuffRunner: 
    def analyze(self, file_path : str) -> list[Finding]:
        if not os.path.exists(file_path):
            return []
        
        cmd = ["ruff", "check", file_path, "--select=E,F", "--output-format=json"]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if not result.stdout.strip():
                return []
            
            raw_issues = json.loads(result.stdout)
            findings = []

            for i in raw_issues:
                code = i.get("code", "")
                category = "style"
                severity = "low"

                if code.startswith("F"):
                    category = "bug"
                    severity = "medium"

                elif code == "E501": 
                    continue

                findings.append(Finding(
                    tool="ruff",
                    category=category,
                    severity=severity,
                    file = file_path,
                    line = i["location"]["row"],
                    message=i["message"],
                    code_snippet=None
                ))

            return findings
        
        except Exception as e:
            print("Ruff failed: ",e)
            return []