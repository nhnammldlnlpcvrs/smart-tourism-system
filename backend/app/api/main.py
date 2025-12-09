# backend/app/api/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.service.map.map_router import router as map_router
from app.service.weather.weather_router import router as weather_router
from app.service.foods.food_router import router as food_router
from app.service.hotel.hotel_router import router as hotel_router
from app.service.tourism.tourism_router import router as tourism_router
from app.service.itinerary.itinerary_router import router as itinerary_router

app = FastAPI(
    title="Smart Tourism System",
    description="API Server for Smart Tourism System",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to frontend domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# System Routes
@app.get("/", tags=["System"])
def home():
    return {"message": "API Layer đang hoạt động!"}

@app.get("/health", tags=["System"])
def health():
    return {"status": "ok"}

# Business Routers
app.include_router(tourism_router, prefix="/tourism", tags=["Tourism"])
app.include_router(itinerary_router, prefix="/itinerary", tags=["Itinerary RAG"])
app.include_router(map_router, prefix="/map", tags=["Map"])
app.include_router(weather_router, prefix="/weather", tags=["Weather"])
app.include_router(food_router, prefix="/foods", tags=["Foods"])
app.include_router(hotel_router, prefix="/hotels", tags=["Hotels"])