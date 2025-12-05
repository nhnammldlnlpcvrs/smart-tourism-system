# backend/app/service/itinerary/itinerary_router.py
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List, Dict, Any
from sqlalchemy.orm import Session

from app.db.models.tourism_model import TourismPlace
from app.db.session import get_db
from app.api.rag_itinerary_module import generate_itinerary_for_request

router = APIRouter(prefix="/itinerary", tags=["Itinerary RAG"])


# API TRẢ VỀ TOÀN BỘ OPTIONS CHO FE
@router.get("/options")
def get_fixed_options(db: Session = Depends(get_db)):
    """
    Trả về toàn bộ lựa chọn cố định từ dữ liệu thực tế trong DB.
    Các trường được lấy từ model TourismPlace.
    """

    places = db.query(TourismPlace).all()

    # Các tập hợp để collect unique values
    special_for_set = set()
    activities_set = set()
    seasonal_event_set = set()
    budget_range_set = set()
    duration_set = set()

    for place in places:

        # special_for: ARRAY(Text)
        if place.special_for:
            for item in place.special_for:
                if item and item.strip():
                    special_for_set.add(item.strip())

        # activities: ARRAY(Text)
        if place.activities:
            for item in place.activities:
                if item and item.strip():
                    activities_set.add(item.strip())

        # seasonal_events: ARRAY(Text)
        if place.seasonal_events:
            for item in place.seasonal_events:
                if item and item.strip():
                    seasonal_event_set.add(item.strip())

        # price_range: Text
        if place.price_range:
            budget_range_set.add(place.price_range.strip())

        # duration_recommend: Text (VD: "2-3 giờ", "Nửa ngày")
        if place.duration_recommend:
            duration_set.add(place.duration_recommend.strip())

    return {
        "special_for": sorted(list(special_for_set)),
        "activities": sorted(list(activities_set)),
        "seasonal_events": sorted(list(seasonal_event_set)),
        "price_range": sorted(list(budget_range_set)),
        "duration_recommend": sorted(list(duration_set)),
    }


# REQUEST MODEL CHO API TẠO LỊCH TRÌNH
class ItineraryRequest(BaseModel):
    province: str
    categories: List[str]
    subcategories: List[str]
    places: List[Dict[str, Any]]

    start_date: str | None = None
    end_date: str | None = None
    days: int | None = None

    activities: List[str] = []
    special_for: str | None = None
    seasonal_event: str | None = None

    budget_per_person: str | None = None
    top_k: int = 5


# API CHÍNH: TẠO LỊCH TRÌNH
@router.post("/generate")
def generate_itinerary(req: ItineraryRequest):

    days = req.days or 2

    itinerary_text = generate_itinerary_for_request(
        province=req.province,
        categories=req.categories,
        subcategories=req.subcategories,
        places=req.places,
        days=days,
        audience=req.special_for,
        start_date=req.start_date,
        end_date=req.end_date,
        budget_per_person=req.budget_per_person,
        top_k=req.top_k,
        activities=req.activities,
        seasonal_events=req.seasonal_events,
    )

    return {
        "province": req.province,
        "days": days,
        "start_date": req.start_date,
        "end_date": req.end_date,
        "audience": req.special_for,
        "activities": req.activities,
        "seasonal_events": req.seasonal_events,
        "budget_per_person": req.budget_per_person,
        "itinerary": itinerary_text
    }
