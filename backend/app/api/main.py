from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router_chat import router as chat_router
from app.service.router_map import router as map_router
from app.service.router_weather import router as weather_router

app = FastAPI(
    title="Tourist Guide Backend",
    description="Backend cho ứng dụng hướng dẫn du lịch tích hợp Google Maps và Thời tiết."
)

# --- CORS ---
origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],   # GET, POST, OPTIONS, PUT, DELETE
    allow_headers=["*"]
)

# --- Routers ---
app.include_router(chat_router)
app.include_router(map_router)
app.include_router(weather_router)
