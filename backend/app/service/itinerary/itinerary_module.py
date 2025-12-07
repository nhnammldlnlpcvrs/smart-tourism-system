# backend/app/service/itinerary/itinerary_module.py
from fastapi import HTTPException
from datetime import datetime
from typing import List, Optional, Union

from app.api.rag_itinerary_module import generate_itinerary_for_request


def validate_date(date_str: str) -> datetime:
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Ngày '{date_str}' không hợp lệ, format phải là YYYY-MM-DD"
        )


def validate_places(places: List[dict]):
    required_keys = {"name", "latitude", "longitude"}

    for place in places:
        missing = required_keys - set(place.keys())
        if missing:
            raise HTTPException(
                status_code=400,
                detail=f"Thiếu trường: {', '.join(missing)}"
            )


def process_itinerary_request(
    province: str,
    places: List[dict],
    place_tags: List[str],
    start_date: Optional[str],
    end_date: Optional[str],
    days: Optional[int],
    audience: Optional[str],
    budget_per_person: Optional[Union[int, str]],
    top_k: int = 5
):

    if not places:
        raise HTTPException(status_code=400, detail="Bạn chưa chọn địa điểm.")
    validate_places(places)

    if start_date and end_date:
        start = validate_date(start_date)
        end = validate_date(end_date)
        days = (end - start).days + 1
    elif not days:
        raise HTTPException(
            status_code=400,
            detail="Cần cung cấp days hoặc start_date + end_date."
        )

    return generate_itinerary_for_request(
        province=province,
        categories=[],              # bỏ – không dùng
        subcategories=[],           # bỏ – không dùng
        places=places,
        days=days,
        audience=audience,
        start_date=start_date,
        end_date=end_date,
        budget_per_person=budget_per_person,
        top_k=top_k,
        place_tags=place_tags,      # ***QUAN TRỌNG***
        activities=[],              # bỏ – FE không dùng nữa
        seasonal_event=None
    )