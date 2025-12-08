# backend/app/service/itinerary/itinerary_module.py
from fastapi import HTTPException
from datetime import datetime
from typing import List, Dict, Any

from app.api.rag_itinerary_module import generate_itinerary_for_request


def validate_date(date_str: str) -> datetime:
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Ngày '{date_str}' không hợp lệ, format phải là YYYY-MM-DD"
        )


def process_itinerary_request(
    places: List[Dict[str, Any]],
    start_date: str,
    end_date: str,
    top_k: int = 5
):
    # Validate dates
    start = validate_date(start_date)
    end = validate_date(end_date)

    if end < start:
        raise HTTPException(
            status_code=400,
            detail="end_date phải lớn hơn hoặc bằng start_date."
        )
    
    # Cải tiến: Thêm kiểm tra nếu danh sách địa điểm trống
    if not places:
        return {
            "days": 0,
            "itinerary": {
                "schedule": [],
                "text": "Không có địa điểm nào được chọn để tạo lịch trình."
            }
        }

    days = (end - start).days + 1

    # Call RAG
    rag_result = generate_itinerary_for_request(
    places=places,
    days=days,
    start_date=start_date,
    end_date=end_date,
    top_k=top_k
    )


    return {
        "days": days,
        "itinerary": rag_result
    }