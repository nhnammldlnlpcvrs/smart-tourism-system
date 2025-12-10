# backend/app/service/itinerary/itinerary_router.py

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from app.db.models.tourism_model import TourismPlace
from app.db.session import get_db
from app.service.itinerary.itinerary_module import process_itinerary_request

router = APIRouter(tags=["Itinerary RAG"])


# ---- INPUT MODEL (Trip Profile) ----
class ItineraryPreferences(BaseModel):
    interests: List[str] = []                # match: category, sub_category, activities
    pace: Optional[str] = None               # slow/medium/fast
    group_type: Optional[str] = None         # family/couple/adventure
    avoid_categories: List[str] = []         # match: tags/category
    time_preferences: Dict[str, List[str]] = {}   # morning/afternoon/evening → activities


class ItineraryRequest(BaseModel):
    province: str
    days: int
    preferences: ItineraryPreferences


# ---- API: /itinerary/generate ----
@router.post("/generate")
def generate_itinerary(req: ItineraryRequest, db: Session = Depends(get_db)):

    if req.days <= 0:
        raise HTTPException(status_code=400, detail="Số ngày phải > 0")

    # Lấy địa điểm theo province
    place_objs = db.query(TourismPlace).filter(
        TourismPlace.province.ilike(f"%{req.province}%")
    ).all()

    if not place_objs:
        raise HTTPException(status_code=404, detail="Không tìm thấy địa điểm nào theo tỉnh yêu cầu.")

    # Convert ORM → dict
    place_dicts = []
    for p in place_objs:
        place_dicts.append({
            "id": p.id,
            "name": p.name,
            "province": p.province,
            "category": p.category,
            "sub_category": p.sub_category or [],
            "address": p.address,
            "latitude": p.latitude,
            "longitude": p.longitude,
            "highlights": p.highlights or [],
            "activities": p.activities or [],
            "special_for": p.special_for or [],
            "duration_recommend": p.duration_recommend,
            "seasonal_events": p.seasonal_events or [],
            "best_time_to_visit": p.best_time_to_visit,
            "tags": p.tags or [],
            "weather_notes": p.weather_notes,
            "price_range": p.price_range,
            "open_hours": p.open_hours
        })

    return process_itinerary_request(
        province=req.province,
        days=req.days,
        preferences=req.preferences.dict(),
        places=place_dicts
    )