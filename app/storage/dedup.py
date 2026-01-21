import hashlib
from app.storage.db import get_db_connection

class Deduplicator:
    def _compute_hash(self, pr_number: int, path : str, line : int, body: str) -> str:
        raw = f"{pr_number} : {path} : {line} : {body.strip()}"
        return hashlib.sha256(raw.encode()).hexdigest()
    
    def is_duplicate(self, pr_number : int, path : str, line: int, body : str) -> bool:
        comment_hash = self._compute_hash(pr_number, path, line, body)
        conn = get_db_connection()
        cursor = conn.execute(
            "SELECT 1 FROM posted_comments WHERE body_hash = ?",
            (comment_hash, )
            )   
        exists = cursor.fetchone() is not None
        conn.close()
        return exists
    
    def mark_as_posted(self, pr_number: int, path: str, line: int, body: str):
        """
        Saves the comment fingerprint to DB.
        """
        comment_hash = self._compute_hash(pr_number, path, line, body)
        conn = get_db_connection()
        try:
            conn.execute(
                "INSERT INTO posted_comments (pr_number, file_path, line, body_hash) VALUES (?, ?, ?, ?)",
                (pr_number, path, line, comment_hash)
            )
            conn.commit()
            print(f" DEBUG: Saved hash {comment_hash[:8]}... to DB") # <--- Added Debug
        except Exception as e:
            # Print the error so we know WHY it failed
            print(f" DB ERROR: Could not save comment! Reason: {e}") 
        finally:
            conn.close()