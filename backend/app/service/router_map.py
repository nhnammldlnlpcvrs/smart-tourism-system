from fastapi import APIRouter, Query
from app.service.map_module import get_nearby_places, get_distance, get_location

# Tạo router cho API Google Maps
router = APIRouter(prefix="/map", tags=["Google Map"])

# 🗺️ Endpoint: Tìm địa điểm gần vị trí chỉ định
@router.get("/nearby")
async def nearby_places(
    lat: float, 
    lng: float, 
    radius: int = Query(500, description="Bán kính tìm kiếm tính bằng mét (m)")
):
    """
    API Nearby Search:
    - Nhận toạ độ lat, lng
    - Trả về danh sách địa điểm gần đó (bán kính mặc định: 500m)
    
    Ví dụ call:
    /map/nearby?lat=21.0285&lng=105.8542&radius=1000
    """
    return await get_nearby_places(lat, lng, radius)


# 🚗 Endpoint: Tính khoảng cách & thời gian di chuyển
@router.get("/distance")
async def distance(
    origin: str = Query(..., description="Điểm bắt đầu (ví dụ: 'Hanoi')"),
    destination: str = Query(..., description="Điểm đến (ví dụ: 'Da Nang')")
):
    """
    API Directions:
    - Nhận chuỗi origin và destination
    - Trả về quãng đường và thời gian ước tính

    """
    return await get_distance(origin, destination)
