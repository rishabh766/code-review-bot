import json
from app.storage.models import Finding
# Ensure app/llm/prompts.py exists (Milestone 4, Step 4)
from app.llm.prompts import REVIEW_SYSTEM_PROMPT 

class LLMReviewer:
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.mock_mode = True if not api_key else False

    def review_diff(self, diff_text: str, allowed_files: list) -> dict:
        """
        Analyzes the diff and returns structured findings.
        allowed_files: A list of filenames that actually exist (to prevent hallucinations).
        """
        # 1. Get the Raw Response (Mock or Real)
        if self.mock_mode:
            json_response = self._get_mock_response()
        else:
            # TODO: Call real Gemini API here
            json_response = {}

        # 2. Validate and Parse into 'comments'
        return self._parse_response(json_response, allowed_files)

    def _parse_response(self, response: dict, allowed_files: list) -> dict:
        """
        Converts raw JSON into a structured dict with Finding objects.
        Filters out hallucinations (files not in the PR).
        """
        summary = response.get("summary", "No summary provided.")
        raw_findings = response.get("findings", [])
        
        valid_findings = []
        for item in raw_findings:
            # 1. Anti-Hallucination Check
            # We use .get("file") because our prompt asks for "file" key
            target_file = item.get("file")
            
            if target_file not in allowed_files:
                print(f"⚠️ [LLM] Filtered hallucinated file: {target_file}")
                continue
                
            # 2. Convert to Standard Model
            try:
                finding = Finding(
                    tool="llm",  # Explicitly set the tool name
                    category=item.get("category", "maintainability"),
                    severity=item.get("severity", "low"),
                    file=target_file,
                    line=item.get("line", 0),
                    message=item.get("message", ""),
                    code_snippet=None 
                )
                valid_findings.append(finding)
            except Exception as e:
                print(f"⚠️ [LLM] Failed to parse finding: {e}")
                # We print the item to debug what went wrong
                print(f"   Item data: {item}")
                continue
                
        return {
            "summary": summary,
            "comments": valid_findings 
        }

    def _get_mock_response(self):
        # The keys here (file, line, category...) MUST match _parse_response calls above
        return {
            "summary": "This PR introduces some unused variables and potential security risks.",
            "findings": [
                {
                    "file": "bad_code.py", 
                    "line": 13,
                    "category": "security",
                    "severity": "high",
                    "message": "The use of `eval()` is extremely dangerous.",
                    "suggestion": "Remove immediately."
                },
                {
                    "file": "non_existent_file.py", 
                    "line": 99,
                    "category": "bug",
                    "severity": "medium",
                    "message": "This file doesn't exist but LLM hallucinated it."
                }
            ]
        }