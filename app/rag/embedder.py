import os
import google.generativeai as genai

class GeminiEmbeddings:
    def __init__(self, api_key : str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)

    def embed_text(self, text : str) -> list:
        if not self.api_key or not text:
            return []
        
        try:
            result = genai.embed_content(
                model="models/text-embedding-004",
                content=text,
                task_type="retrieval_document"
            )
            return result['embedding']
        except Exception as e:
            print(f"Embedding failed : {e}")
            return []
        
    
        