import sqlite3
import os

DB_PATH = "bot_memory.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute("""
    CREATE TABLE IF NOT EXISTS posted_comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
                 pr_number INTEGER,
                 file_path TEXT,
                 line INTEGER,
                 body_hash TEXT UNIQUE
            )
""")
    conn.commit()
    conn.close()

