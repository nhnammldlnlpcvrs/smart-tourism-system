import os
import requests
from dotenv import load_dotenv

# Load API key từ file .env
load_dotenv()
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_weather(city: str, lang: str = "vi"):
    """
    Gọi OpenWeatherMap API để lấy thông tin thời tiết theo tên thành phố.

    Parameters:
    - city (str): Tên thành phố (ví dụ: "Hanoi")
    - lang (str): Ngôn ngữ trả về mô tả thời tiết (mặc định: "vi" - Tiếng Việt)

    Returns:
    - dict: Dữ liệu thời tiết bao gồm:
        {
            "city": <Tên thành phố>,
            "country": <Mã quốc gia>,
            "weather": <Mô tả thời tiết>,
            "temperature": <Nhiệt độ độ C>,
            "humidity": <Độ ẩm %>,
            "wind_speed": <Tốc độ gió m/s>
        }
      Hoặc trả về lỗi:
        {"error": <Thông báo lỗi>}
    """

    # ✅ Kiểm tra key tồn tại
    if not OPENWEATHER_API_KEY:
        return {"error": "❌ Thiếu OPENWEATHER_API_KEY trong file .env"}

    # ✅ API Endpoint OpenWeatherMap
    url = "https://api.openweathermap.org/data/2.5/weather"

    # ✅ Tham số request
    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric",  # Đổi sang độ C
        "lang": lang        # Ngôn ngữ mô tả thời tiết (việt hoá)
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()
    except Exception as e:
        return {"error": f"❌ Không thể kết nối tới API: {str(e)}"}

    # ✅ Kiểm tra lỗi từ API (ví dụ: City sai → code 404)
    if response.status_code != 200 or "weather" not in data:
        return {"error": f"⛔ Lỗi API: {data.get('message', 'Không lấy được dữ liệu.')}"}

    # ✅ Parse dữ liệu
    weather = data["weather"][0]["description"].capitalize()
    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    wind = data["wind"]["speed"]
    country = data["sys"]["country"]
    city_name = data.get("name", city)

    # ✅ Chuẩn hoá dữ liệu trả về
    return {
        "city": city_name,
        "country": country,
        "weather": weather,
        "temperature": temp,
        "humidity": humidity,
        "wind_speed": wind,
    }