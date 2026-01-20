import subprocess
import json
import os

class SemgrepRunner:
    def analyze(self, file_path: str):
        """
        Runs Semgrep on a file using the default security ruleset.
        """
        if not os.path.exists(file_path):
            return []

        # --config=p/python uses the standard Python security rules
        cmd = ["semgrep", "--config=p/python", "--json", file_path]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if not result.stdout.strip():
                return []
                
            data = json.loads(result.stdout)
            return data.get("results", [])
            
        except Exception as e:
            print(f"Semgrep failed: {e}")
            return []