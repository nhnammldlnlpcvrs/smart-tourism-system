import requests
from datetime import datetime
from typing import Dict

# --- CẤU HÌNH API OPENWEATHERMAP ---
# CẦN THAY THẾ KHÓA API THẬT CỦA BẠN OpenWeatherMap TẠI ĐÂY
# Khóa hiện tại (8179f97f3b1841c12de75ca17ca8acb4) là khóa giả lập hoặc đã hết hạn.
# Vui lòng thay thế bằng khóa API thực của bạn để tránh lỗi HTTP 401/403.  AIzaSyAKq9wSevTQfJda8F7ne__GfIsGYjdUUUo
OPENWEATHER_API_KEY = "8179f97f3b1841c12de75ca17ca8acb4" 
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_current_weather(city: str, unit: str = "C") -> Dict:
    """
    Lấy thông tin thời tiết hiện tại cho một thành phố cụ thể bằng OpenWeatherMap API.

    Args:
        city (str): Tên thành phố (ví dụ: 'Hanoi', 'Tokyo').
        unit (str): Đơn vị nhiệt độ, 'C' (metric) hoặc 'F' (imperial).

    Returns:
        Dict: Dữ liệu thời tiết, bao gồm nhiệt độ và điều kiện. 
              Trả về dictionary chứa 'error' nếu gặp lỗi.
    """
    # OpenWeatherMap sử dụng "metric" cho độ C và "imperial" cho độ F
    units = "metric" if unit.upper() == "C" else "imperial"

    params = {
        'q': city,
        'appid': OPENWEATHER_API_KEY,
        'units': units,
        'lang': 'vi' # Thêm ngôn ngữ tiếng Việt
    }

    try:
        response = requests.get(BASE_URL, params=params)
        
        # --- BẮT LỖI TỪ PHẢN HỒI HTTP ---
        if response.status_code == 401:
            return {
                "error": "Lỗi xác thực (401)",
                "message": "API Key của OpenWeatherMap không hợp lệ hoặc chưa được kích hoạt.",
                "status": "error",
                "timestamp": datetime.now().isoformat()
            }
        
        if response.status_code == 404:
            return {
                "error": "Không tìm thấy thành phố (404)",
                "message": f"Không tìm thấy dữ liệu thời tiết cho thành phố '{city}'. Vui lòng kiểm tra lại tên thành phố.",
                "status": "error",
                "timestamp": datetime.now().isoformat()
            }
        
        response.raise_for_status() # Bắt các lỗi HTTP khác (5xx, 4xx)

        data = response.json()
        
        # Kiểm tra xem dữ liệu có hợp lệ không
        if not data or 'main' not in data:
            return {
                "error": "Dữ liệu không đầy đủ",
                "message": "Dữ liệu thời tiết trả về không chứa thông tin nhiệt độ chính.",
                "status": "error",
                "timestamp": datetime.now().isoformat()
            }

        # Trích xuất dữ liệu cần thiết
        weather_info = {
            "city": data.get('name', city),
            "temp": f"{data['main']['temp']} °{unit.upper()}",
            "feels_like": f"{data['main']['feels_like']} °{unit.upper()}",
            "description": data['weather'][0]['description'].capitalize() if data.get('weather') else "Không rõ",
            "humidity": f"{data['main']['humidity']}%",
            "wind_speed": f"{data['wind']['speed']} m/s", # Tốc độ gió
            "status": "success",
            "timestamp": datetime.now().isoformat()
        }
        return weather_info

    except requests.exceptions.RequestException as e:
        # Xử lý lỗi kết nối mạng, timeout, DNS, v.v.
        print(f"Lỗi kết nối API OpenWeatherMap: {e}")
        return {
            "error": "Lỗi kết nối",
            "message": f"Lỗi HTTP: Không thể kết nối hoặc API Key có vấn đề.",
            "status": "error",
            "detail": str(e),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        # Xử lý các lỗi Python không mong muốn khác
        print(f"Lỗi không xác định trong weather_service: {e}")
        return {
            "error": "Lỗi nội bộ không xác định",
            "message": "Đã xảy ra lỗi không xác định trong dịch vụ thời tiết.",
            "status": "error",
            "detail": str(e),
            "timestamp": datetime.now().isoformat()
        }
