import os
import json
import google.generativeai as genai
from app.storage.models import Finding
from app.llm.prompts import REVIEW_SYSTEM_PROMPT

class LLMReviewer:
    def __init__(self, api_key: str = None):
        # Load API Key
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            print(" WARNING: No GEMINI_API_KEY found. LLM will fail.")
            return

        # Configure Gemini
        genai.configure(api_key=self.api_key)
        try:
            self.model = genai.GenerativeModel('gemini-2.5-flash') 
        except:
            self.model = genai.GenerativeModel('gemini-pro')

    def review_diff(self, diff_text: str, allowed_files: list, context: str = "") -> dict:
        if not self.api_key:
            return {"summary": "LLM Disabled (No Key)", "comments": []}

        # 1. Construct the Prompt
        # We combine System Instructions + Context + The actual Diff
        full_prompt = f"""
        {REVIEW_SYSTEM_PROMPT}
        
        CONTEXT (Relevant Code Snippets):
        {context}
        
        GIT DIFF TO REVIEW:
        {diff_text}
        """
        try:
            response = self.model.generate_content(
                full_prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            
            # 3. Parse JSON
            # Gemini 1.5 Flash is good at following JSON mode
            response_text = response.text
            try:
                json_data = json.loads(response_text)
            except json.JSONDecodeError:
                # Fallback: sometimes LLM adds markdown backticks
                if "```json" in response_text:
                    clean_text = response_text.replace("```json", "").replace("```", "")
                    json_data = json.loads(clean_text)
                else:
                    raise
            
            return self._parse_response(json_data, allowed_files)

        except Exception as e:
            print(f"!!! LLM Call Failed: {e}")
            return {"summary": "LLM Analysis Failed", "comments": []}

    def _parse_response(self, response: dict, allowed_files: list) -> dict:
        summary = response.get("summary", "No summary provided.")
        raw_findings = response.get("findings", [])
        
        valid_findings = []
        for item in raw_findings:
            target_file = item.get("file")
            
            # Anti-Hallucination: Check if file exists in the PR
            if target_file not in allowed_files:
                continue
                
            try:
                finding = Finding(
                    tool="llm",
                    category=item.get("category", "maintainability"),
                    severity=item.get("severity", "low"),
                    file=target_file,
                    line=item.get("line", 0),
                    message=item.get("message", ""),
                    code_snippet=None 
                )
                valid_findings.append(finding)
            except Exception:
                continue
                
        return {
            "summary": summary,
            "comments": valid_findings 
        }