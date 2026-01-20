import subprocess
import json
import os

class RuffRunner: 
    def analyze(self, file_path : str):
        if not os.path.exists(file_path):
            return []
        
        cmd = ["ruff", "check", file_path, "--select=E,F", "--output-format=json"]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if not result.stdout.strip():
                return []
            return json.loads(result.stdout)
        
        except Exception as e:
            print("Ruff failed: ",e)
            return []