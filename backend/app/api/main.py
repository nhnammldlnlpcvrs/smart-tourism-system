from fastapi import FastAPI
from app.api.router_chat import router as chat_router
from app.service.router_map import router as map_router
from app.service.router_weather import router as weather_router
from app.service.food_router import router as food_router
from app.service.hotel_router import router as hotel_router
app = FastAPI(
    title="Tourist Guide Backend",
    description="Backend cho ứng dụng hướng dẫn du lịch tích hợp Google Maps và Thời tiết."
)

@app.get("/")
def home():
    return {"message": "🎉 Vietnam Smart Tourism API đang hoạt động!"}

app.include_router(chat_router)
app.include_router(map_router)
app.include_router(weather_router)
app.include_router(food_router)
app.include_router(hotel_router)