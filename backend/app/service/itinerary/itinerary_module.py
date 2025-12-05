# backend/app/service/itinerary/itinerary_module.py
from fastapi import HTTPException
from datetime import datetime
from typing import List, Optional, Union

from app.api.rag_itinerary_module import generate_itinerary_for_request


def validate_date(date_str: str) -> datetime:
    """Validate YYYY-MM-DD date format."""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Ngày '{date_str}' không hợp lệ, format phải là YYYY-MM-DD"
        )


def validate_places(places: List[dict]):
    """Ensure all places contain minimal required fields."""
    required_keys = {"name", "latitude", "longitude"}

    for place in places:
        if not isinstance(place, dict):
            raise HTTPException(status_code=400, detail="Mỗi place phải là JSON object.")

        missing = required_keys - set(place.keys())
        if missing:
            raise HTTPException(
                status_code=400,
                detail=f"Thiếu field trong place: {', '.join(missing)}"
            )


def process_itinerary_request(
    province: str,
    categories: List[str],
    subcategories: List[str],
    places: List[dict],
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    days: Optional[int] = None,
    audience: Optional[str] = None,
    budget_per_person: Optional[Union[int, str]] = None,
    activities: Optional[List[str]] = None,
    seasonal_event: Optional[str] = None,
    top_k: int = 5
):
    """Validate + chuẩn hóa input + đẩy vào RAG để tạo timeline."""

    # --- Validate category ---
    if not categories:
        raise HTTPException(status_code=400, detail="Bạn phải chọn ít nhất 1 category.")

    # --- Validate places ---
    if not places:
        raise HTTPException(status_code=400, detail="Không có địa điểm du lịch nào được chọn.")
    validate_places(places)

    # --- Activities: convert None -> [] ---
    if activities is None:
        activities = []

    # --- Validate date logic ---
    if start_date and end_date:
        start = validate_date(start_date)
        end = validate_date(end_date)
        if end < start:
            raise HTTPException(status_code=400, detail="Ngày kết thúc phải sau ngày bắt đầu.")
        days = (end - start).days + 1

    elif days:  
        # Nếu người dùng chỉ chọn days
        start = None
        end = None

    else:
        raise HTTPException(
            status_code=400,
            detail="Bạn phải cung cấp start_date + end_date hoặc days."
        )

    # --- Call RAG ---
    try:
        response_text = generate_itinerary_for_request(
            province=province,
            categories=categories,
            subcategories=subcategories,
            places=places,
            days=days,
            audience=audience,
            start_date=start_date,
            end_date=end_date,
            budget_per_person=budget_per_person,
            top_k=top_k,
            activities=activities,
            seasonal_event=seasonal_event
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi RAG Pipeline: {str(e)}")

    return {
        "province": province,
        "days": days,
        "start_date": start_date,
        "end_date": end_date,
        "audience": audience,
        "activities": activities,
        "seasonal_event": seasonal_event,
        "budget_per_person": budget_per_person,
        "itinerary": response_text
    }