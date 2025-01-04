from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
import os
from dotenv import load_dotenv

from app.database import SessionLocal
from app.models import Attendance
from app.dependencies import get_current_user
from app.utils.location import haversine_distance

router = APIRouter(prefix="/attendance", tags=["Attendance"])

load_dotenv()

CLASSROOM_LAT = float(os.getenv("CLASSROOM_LAT", 0))
CLASSROOM_LONG = float(os.getenv("CLASSROOM_LONG", 0))
CLASSROOM_RADIUS = float(os.getenv("CLASSROOM_RADIUS", 50))  # default 50m if not set

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
    if latitude is None or longitude is None:
        raise HTTPException(status_code=400, detail="Latitude and longitude are required")

    # Calculate distance from the classroom
    distance = haversine_distance(latitude, longitude, CLASSROOM_LAT, CLASSROOM_LONG)

    # Check if within the allowed radius
    is_in_classroom = distance <= CLASSROOM_RADIUS

    attendance_record = Attendance(
        user_id=current_user,
        latitude=latitude,
        longitude=longitude,
        # For now, we set is_valid based purely on geofence
        # Face recognition checks could be added here later
        is_valid=is_in_classroom
    )

    db.add(attendance_record)
    db.commit()
    db.refresh(attendance_record)

    return {
        "message": "Attendance marked",
        "attendance_id": attendance_record.id,
        "distance_from_classroom_m": distance,
        "is_valid": attendance_record.is_valid
    }
