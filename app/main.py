# app/main.py

import os
from fastapi import FastAPI
from app.routers import user  # or from .routers import user if relative
from config import DB_URL,SECRET_KEY

app = FastAPI()

# Include the user router
app.include_router(user.router)

@app.get("/health")
def health_check():
    # Example usage of env vars
    return {
        "status": "ok",
        "db_url": os.getenv("DB_URL"),  # Just for demonstration; remove in production
    }
