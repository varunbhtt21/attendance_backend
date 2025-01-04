# app/main.py

from fastapi import FastAPI
from app.routers import user, attendance, face
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.include_router(user.router)
app.include_router(attendance.router)
app.include_router(face.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
