# backend/app/service/itinerary/itinerary_router.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session

from app.db.models.tourism_model import TourismPlace
from app.db.session import get_db
from app.service.itinerary.itinerary_module import process_itinerary_request

router = APIRouter(prefix="/itinerary", tags=["Itinerary RAG"])


class ExtractNamesRequest(BaseModel):
    place_ids: List[int]


@router.post("/extract-names")
def extract_names(req: ExtractNamesRequest, db: Session = Depends(get_db)):
    places = db.query(TourismPlace).filter(
        TourismPlace.id.in_(req.place_ids)
    ).all()

    return {"places": [{"id": p.id, "name": p.name} for p in places]}


class GenerateRequest(BaseModel):
    place_ids: List[int]
    start_date: str
    end_date: str
    top_k: int = 5


@router.post("/generate")
def generate_itinerary(req: GenerateRequest, db: Session = Depends(get_db)):

    place_objs = db.query(TourismPlace).filter(
        TourismPlace.id.in_(req.place_ids)
    ).all()

    if not place_objs:
        raise HTTPException(status_code=400, detail="Không tìm thấy địa điểm phù hợp.")

    # Build place dict list: Trích xuất an toàn hơn cho các trường có thể là None hoặc List
    places = [
        {
            "id": p.id,
            "name": p.name,
            "address": p.address,
            # Sử dụng getattr() với giá trị mặc định an toàn
            "open_hours": getattr(p, 'open_hours', None),
            "price_range": getattr(p, 'price_range', None),
            "highlights": getattr(p, 'highlights', []), # Mặc định là list rỗng
            "activities": getattr(p, 'activities', []), # Mặc định là list rỗng
            "duration_recommend": getattr(p, 'duration_recommend', None),
            "seasonal_events": getattr(p, 'seasonal_events', []), # Mặc định là list rỗng
            "special_for": getattr(p, 'special_for', []), # Mặc định là list rỗng
        }
        for p in place_objs
    ]

    result = process_itinerary_request(
        places=places,
        start_date=req.start_date,
        end_date=req.end_date,
        top_k=req.top_k
    )

    return result