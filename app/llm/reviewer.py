import json

class LLMReviewer: 
    def __init__(self, api_key : str = None):
        self.api_key = api_key
        self.mock_mode = True if not api_key else False

    def review_diff(self, diff_text : str) -> dict:
        if self.mock_mode:
            return self._get_mock_response()
        
        #TODO: Implement real gemini call here later
        return {}
    
    def _get_mock_response(self):
        print("Generating a mock response...")
        mock_output = {
            "summary": "This PR introduces some unused variables and potential security risks.",
            "comments": [
                {
                    "file": "bad_code.py",
                    "line": 13,
                    "text": "CRITICAL: The use of `eval()` is extremely dangerous and allows arbitrary code execution. Remove this immediately."
                },
                {
                    "file": "bad_code.py",
                    "line": 8,
                    "text": "SECURITY: Hardcoded passwords should never be committed. Use environment variables."
                },
                {
                    "file": "bad_code.py",
                    "line": 1,
                    "text": "NIT: You imported `os` but never used it. Consider removing to keep the namespace clean."
                }
            ]
        }
        return mock_output