from fastapi import APIRouter, HTTPException, Depends
from app.service.weather_service import get_current_weather
from pydantic import BaseModel

# Định nghĩa APIRouter
router = APIRouter(
    prefix="/weather",
    tags=["Weather"],
    responses={404: {"description": "Not found"}},
)

# Pydantic model cho input của API
class WeatherQuery(BaseModel):
    city: str

@router.post("/current")
async def get_weather(query: WeatherQuery):
    """
    Lấy thông tin thời tiết hiện tại cho một thành phố cụ thể.
    Nếu thành công, trả về JSON object chứa thông tin thời tiết.
    """
    city = query.city
    try:
        weather_data = get_current_weather(city)
        if "error" in weather_data:
            # Nếu service trả về lỗi (ví dụ: thành phố không tồn tại)
            raise HTTPException(status_code=404, detail=weather_data["error"])
        
        return {
            "city": city,
            "weather": weather_data
        }
    except Exception as e:
        # Xử lý các lỗi khác có thể xảy ra trong quá trình gọi service
        print(f"Error fetching weather for {city}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while fetching weather data.")
