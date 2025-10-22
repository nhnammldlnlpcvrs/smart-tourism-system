"""
Weather Agent
--------------
Mục đích:
- Lấy thông tin thời tiết hiện tại hoặc dự báo ở một địa điểm du lịch cụ thể.

TODO:
- Tích hợp API như OpenWeatherMap, WeatherAPI hoặc Meteostat.
- Chuẩn hóa đầu ra thành dict JSON với: {location, temperature, condition, humidity, wind_speed}.
"""

import os
import requests

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "dummy-key")

def get_weather(location: str):
    """
    Lấy thông tin thời tiết hiện tại cho địa điểm cụ thể.
    """
    print(f"[WeatherAgent] Getting weather for: {location}")

    # TODO: Replace with real API call
    mock_weather = {
        "location": location,
        "temperature": "28°C",
        "condition": "Sunny",
        "humidity": "65%",
        "wind_speed": "10 km/h",
    }
    return mock_weather