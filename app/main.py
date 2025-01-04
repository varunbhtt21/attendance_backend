# app/main.py

import os
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env

app = FastAPI()

@app.get("/health")
def health_check():
    # Example usage of env vars
    return {
        "status": "ok",
        "db_url": os.getenv("DB_URL"),  # Just for demonstration; remove in production
    }
