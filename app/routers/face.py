# app/routers/face.py
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
import face_recognition
import numpy as np
import json

from app.database import SessionLocal
from app.models import User
from app.dependencies import get_current_user

router = APIRouter(prefix="/face", tags=["Face"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/enroll")
async def enroll_face(
    file: UploadFile = File(...),
    current_user: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    1. Upload a single image file.
    2. Extract the first face encoding.
    3. Store encoding in user's record.
    """
    # Read file contents
    file_bytes = await file.read()

    # Convert to numpy array (face_recognition can handle raw bytes if using load_image_file in memory)
    # We'll do a small trick: write the bytes to a temp or pass directly to face_recognition
    # face_recognition.load_image_file normally expects a filepath, but there's a workaround:
    import io
    import PIL.Image

    image = face_recognition.load_image_file(io.BytesIO(file_bytes))

    # Detect face encodings
    encodings = face_recognition.face_encodings(image)
    if len(encodings) == 0:
        raise HTTPException(status_code=400, detail="No face detected in the image.")
    # We'll take the first face found
    first_encoding = encodings[0]

    # Convert the numpy array to a list for JSON serialization
    encoding_list = first_encoding.tolist()

    # Update user in DB
    user_record = db.query(User).filter(User.id == current_user).first()
    if not user_record:
        raise HTTPException(status_code=404, detail="User not found.")

    # Store as JSON string
    user_record.face_encoding = json.dumps(encoding_list)
    db.commit()
    db.refresh(user_record)

    return {"message": "Face enrolled successfully!", "user_id": user_record.id}
