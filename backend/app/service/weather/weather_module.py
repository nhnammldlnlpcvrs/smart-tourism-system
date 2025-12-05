# backend/app/service/weather/weather_module.py
import os
import httpx
from dotenv import load_dotenv

# Load key một lần duy nhất khi khởi động
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

async def get_current_weather(city: str):
    if not API_KEY:
        return {"error": "Chưa cấu hình API Key"}

    async with httpx.AsyncClient() as client:
        try:
            # Gọi API bất đồng bộ
            response = await client.get(
                BASE_URL,
                params={"q": city, "appid": API_KEY, "units": "metric", "lang": "vi"},
                timeout=5.0 # Timeout 5s để không treo
            )
            
            if response.status_code != 200:
                return None # Không tìm thấy thành phố hoặc lỗi API

            data = response.json()
            
            # Trả về dữ liệu đã lọc gọn
            return {
                "city": data.get("name", city),
                "weather": data["weather"][0]["description"].capitalize(),
                "temp": round(data["main"]["temp"]), # Làm tròn nhiệt độ (25.6 -> 26)
                "humidity": f"{data['main']['humidity']}%",
                "wind": f"{data['wind']['speed']} m/s",
                "icon": f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png" # Link ảnh icon thời tiết
            }
        except Exception as e:
            print(f"Weather Error: {e}")
            return None