# backend/app/service/itinerary/itinerary_router.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session

from app.db.models.tourism_model import TourismPlace
from app.db.session import get_db
from app.api.rag_itinerary_module import generate_itinerary_for_request

router = APIRouter(prefix="/itinerary", tags=["Itinerary RAG"])


# 1. API: Extract tags từ danh sách địa điểm
class ExtractTagsRequest(BaseModel):
    place_ids: List[int]


@router.post("/extract-tags")
def extract_tags(req: ExtractTagsRequest, db: Session = Depends(get_db)):
    places = db.query(TourismPlace).filter(
        TourismPlace.id.in_(req.place_ids)
    ).all()

    if not places:
        return {
            "activities": [],
            "special_for": [],
            "seasonal_events": [],
            "highlights": [],
            "price_range": [],
            "duration_recommend": [],
            "best_time_to_visit": [],
            "nearby_places": []
        }

    activities = set()
    special_for = set()
    seasonal_events = set()
    highlights = set()
    price_range = set()
    duration_recommend = set()
    best_time_to_visit = set()
    nearby_places = set()

    for p in places:
        if p.activities:
            activities.update([a for a in p.activities if a])
        if p.special_for:
            special_for.update([s for s in p.special_for if s])
        if p.seasonal_events:
            seasonal_events.update([ev for ev in p.seasonal_events if ev])
        if p.highlights:
            if isinstance(p.highlights, list):
                highlights.update([h for h in p.highlights if h])
            else:
                highlights.add(p.highlights)
        if p.price_range:
            price_range.add(p.price_range)

        if p.duration_recommend:
            duration_recommend.add(str(p.duration_recommend))

        if p.best_time_to_visit:
            best_time_to_visit.add(p.best_time_to_visit)

        if p.nearby_places:
            if isinstance(p.nearby_places, list):
                nearby_places.update([nb for nb in p.nearby_places if nb])
            else:
                nearby_places.add(p.nearby_places)

    return {
        "activities": sorted(list(activities)),
        "special_for": sorted(list(special_for)),
        "seasonal_events": sorted(list(seasonal_events)),
        "highlights": sorted(list(highlights)),
        "price_range": sorted(list(price_range)),
        "duration_recommend": sorted(list(duration_recommend)),
        "best_time_to_visit": sorted(list(best_time_to_visit)),
        "nearby_places": sorted(list(nearby_places))
    }


# 2. API Generate
class GenerateRequest(BaseModel):
    place_ids: List[int]
    place_tags: List[str]
    days: int
    audience: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    budget_per_person: int | str | None = None
    top_k: int = 5


@router.post("/generate")
def generate_itinerary(req: GenerateRequest, db: Session = Depends(get_db)):

    place_objs = db.query(TourismPlace).filter(
        TourismPlace.id.in_(req.place_ids)
    ).all()

    if not place_objs:
        raise HTTPException(status_code=400, detail="Không tìm thấy địa điểm phù hợp.")

    # Format JSON chuẩn để truyền vào RAG
    places = [
        {
            "id": p.id,
            "name": p.name,
            "address": p.address,
            "latitude": p.latitude,
            "longitude": p.longitude,
            "category": p.category,
            "sub_category": p.sub_category,
            "rating": p.rating
        }
        for p in place_objs
    ]

    province = place_objs[0].province

    result = generate_itinerary_for_request(
        province=province,
        categories=[],
        subcategories=[],
        places=places,
        days=req.days,
        audience=req.audience,
        start_date=req.start_date,
        end_date=req.end_date,
        budget_per_person=req.budget_per_person,
        top_k=req.top_k,
        place_tags=req.place_tags,
        activities=[],
        seasonal_event=None,
    )

    return {
        "province": province,
        "days": req.days,
        "audience": req.audience,
        "start_date": req.start_date,
        "end_date": req.end_date,
        "budget_per_person": req.budget_per_person,
        "itinerary": result
    }