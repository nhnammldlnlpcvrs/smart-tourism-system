# backend/app/service/hotel/hotel_router.py
from fastapi import APIRouter
from typing import Optional
from app.service.tourism.tourism_module import get_all_provinces

from .hotel_module import get_hotels_by_province_and_place_id

router = APIRouter(prefix="/hotels", tags=["Hotels"])

@router.get("/provinces")
def api_get_provinces():
    return get_all_provinces()

@router.get("/")
def api_hotels(province: str, place_id: Optional[int] = None):
    """
    - province: Tên tỉnh (Bắt buộc).
    - place_id: ID địa điểm tham quan (Optional).
      + Có ID: Gợi ý khách sạn gần đó 10km.
      + Không ID: Liệt kê khách sạn theo tỉnh.
    """
    return get_hotels_by_province_and_place_id(province, place_id)