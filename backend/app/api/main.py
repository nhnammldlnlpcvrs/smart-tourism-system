from fastapi import FastAPI
<<<<<<< Updated upstream
from fastapi.middleware.cors import CORSMiddleware
=======
from fastapi.middleware.cors import CORSMiddleware  # ← THÊM DÒNG NÀY
>>>>>>> Stashed changes
from app.api.router_chat import router as chat_router
from app.service.router_map import router as map_router
from app.service.router_weather import router as weather_router

app = FastAPI(
    title="Tourist Guide Backend",
    description="Backend cho ứng dụng hướng dẫn du lịch tích hợp Google Maps và Thời tiết."
)

<<<<<<< Updated upstream
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
=======
# ======================
# 🚨 THÊM CORS MIDDLEWARE
# ======================
origins = [
    "http://localhost:5500",      # Frontend dev server của bạn
    "http://127.0.0.1:5500",      # Frontend dev server
    "http://localhost:5173",      # Vite default port
    "http://127.0.0.1:5173",      # Vite default port
    "http://localhost:3000",      # React default
    "http://127.0.0.1:3000",      # React default
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # Cho phép các domain này
    allow_credentials=True,       # Cho phép gửi cookies
    allow_methods=["*"],          # Cho phép tất cả HTTP methods
    allow_headers=["*"],          # Cho phép tất cả headers
)

@app.get("/")
def home():
    return {"message": "🎉 Vietnam Smart Tourism API đang hoạt động!"}

# Include routers
app.include_router(tourism_router)
app.include_router(chat_router)
app.include_router(map_router)
app.include_router(weather_router)
app.include_router(food_router)
app.include_router(hotel_router)

# Thêm để test CORS
@app.get("/test-cors")
def test_cors():
    return {"message": "CORS is working!", "status": "success"}
>>>>>>> Stashed changes
