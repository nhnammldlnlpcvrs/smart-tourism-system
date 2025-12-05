# backend/app/service/weather/weather_router.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from .weather_module import get_current_weather

router = APIRouter(prefix="/weather", tags=["Weather"])

class WeatherQuery(BaseModel):
    city: str

@router.post("/current")
async def get_weather(q: WeatherQuery):
    if (data := await get_current_weather(q.city)) and "error" not in data:
        return data
    
    # Nếu không thỏa mãn điều kiện trên -> Báo lỗi 404
    raise HTTPException(status_code=404, detail="City not found")