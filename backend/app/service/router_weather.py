from fastapi import APIRouter, Query
from app.service.weather_module import get_weather

# 🌤️ Tạo router cho API thời tiết
router = APIRouter(prefix="/weather", tags=["Weather"])

@router.get("/")
def weather(
    city: str = Query(
        ..., 
        description="Tên thành phố muốn xem thời tiết (ví dụ: 'Hanoi')"
    )
):
    """
    API lấy thông tin thời tiết hiện tại theo thành phố.
    - Tham số:
        city: tên thành phố (bắt buộc)
    - Kết quả trả về bao gồm:
        - Mô tả thời tiết
        - Nhiệt độ (°C)
        - Độ ẩm (%)
        - Tốc độ gió (m/s)

    """
    # Gọi service xử lý dữ liệu thời tiết
    return get_weather(city)
