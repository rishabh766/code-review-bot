from fastapi import FastAPI
from dotenv import load_dotenv
from app.github.webhook import router as webhook_router
from app.storage.db import init_db

load_dotenv()
init_db()

app = FastAPI(titel = "Code Review Bot", version = "1.0.0")

app.include_router(webhook_router)

@app.get("/")
def read_root():
    return {"status" : "okay", "message" : "Code review bot is active"}

