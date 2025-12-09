from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router_chat import router as chat_router
from app.service.router_map import router as map_router
from app.service.router_weather import router as weather_router

app = FastAPI(
    title="Tourist Guide Backend",
    description="Backend cho ứng dụng hướng dẫn du lịch tích hợp Google Maps và Thời tiết."
)

origins = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
app.include_router(map_router)
app.include_router(weather_router)

@app.get("/")
def home():
    return {"message": "🎉 Vietnam Smart Tourism API đang hoạt động!"}

@app.get("/test-cors")
def test_cors():
    return {"message": "CORS is working!", "status": "success"}
