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
def api_recommend_hotels(place_id: int, radius: float = 50.0):
    """
    TÌM KHÁCH SẠN GẦN ĐỊA ĐIỂM VUI CHƠI
    
    API này hoạt động theo cơ chế "Du lịch thông minh":
    1. Frontend gửi ID của địa điểm khách đang xem (ví dụ: Hồ Gươm, Chùa Hương).
    2. Backend tự lấy tọa độ của địa điểm đó trong Database.
    3. Backend quét và trả về danh sách khách sạn xung quanh trong bán kính cho phép.
    
    Params:
    - place_id (int): ID của địa điểm tham quan (Bắt buộc).
    - radius (float): Bán kính tìm kiếm tính bằng km (Mặc định 10km).
    """
    return get_hotels_by_province_and_place_id(place_id, radius_km=radius)