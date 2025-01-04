from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app.database import SessionLocal
from app.models import Attendance
from app.dependencies import get_current_user

router = APIRouter(prefix="/attendance", tags=["Attendance"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/mark")
def mark_attendance(
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    current_user: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    1. In real scenario, we'd do:
       - Face recognition check
       - Location check
         if is_in_classroom(latitude, longitude) and face_matched:
             is_valid=True
         else:
             is_valid=False
    2. For now, we just create a record and mark is_valid=True.
    """
    attendance_record = Attendance(
        user_id=current_user,
        latitude=latitude,
        longitude=longitude,
        is_valid=True  # placeholder logic
    )

    db.add(attendance_record)
    db.commit()
    db.refresh(attendance_record)

    return {
        "message": "Attendance marked successfully!",
        "attendance_id": attendance_record.id,
        "is_valid": attendance_record.is_valid
    }
