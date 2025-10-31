
'''
import requests
import json

def get_city_coordinates(city_name: str):
    """Tìm toạ độ (lat, lon) của thành phố bằng Open-Meteo Geocoding API"""
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": city_name, "count": 1, "language": "vi", "format": "json"}

    response = requests.get(url, params=params)
    data = response.json()

    if "results" not in data:
        return None

    city = data["results"][0]
    return {
        "name": city["name"],
        "country": city.get("country", ""),
        "latitude": city["latitude"],
        "longitude": city["longitude"]
    }

def get_weather(city_name: str):
    """Lấy thời tiết hiện tại cho 1 thành phố từ Open-Meteo"""
    coords = get_city_coordinates(city_name)
    if not coords:
        return {"status": "error", "message": f"Không tìm thấy thành phố: {city_name}"}

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": coords["latitude"],
        "longitude": coords["longitude"],
        "current_weather": True,
        "timezone": "auto"
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "current_weather" not in data:
        return {"status": "error", "message": "Không lấy được dữ liệu thời tiết."}

    weather = data["current_weather"]

    # Mã thời tiết (weathercode) -> mô tả tiếng Việt
    weather_codes = {
        0: "Trời quang đãng",
        1: "Trời hầu như quang",
        2: "Có mây nhẹ",
        3: "Nhiều mây",
        45: "Sương mù",
        48: "Sương mù có sương giá",
        51: "Mưa phùn nhẹ",
        53: "Mưa phùn vừa",
        55: "Mưa phùn dày",
        61: "Mưa nhẹ",
        63: "Mưa vừa",
        65: "Mưa to",
        71: "Tuyết rơi nhẹ",
        73: "Tuyết vừa",
        75: "Tuyết dày",
        95: "Có dông",
        99: "Dông mạnh kèm mưa đá"
    }

    code = weather.get("weathercode", -1)
    description = weather_codes.get(code, "Không xác định")

    result = {
        "status": "success",
        "city": coords["name"],
        "country": coords["country"],
        "temperature": weather["temperature"],
        "windspeed": weather["windspeed"],
        "weather_description": description,
        "time": weather["time"],
        "source": "Open-Meteo"
    }

    return result


# 🌤️ Demo: chạy trực tiếp
if __name__ == "__main__":
    city = input("Nhập tên thành phố: ")
    info = get_weather(city)
    print(json.dumps(info, ensure_ascii=False, indent=2))

    


import requests

class WeatherAPI:
    BASE_URL = "https://api.open-meteo.com/v1/forecast"

    def get_weather(self, latitude: float, longitude: float):
        """Lấy thông tin thời tiết hiện tại từ Open-Meteo."""
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current_weather": True
        }
        response = requests.get(self.BASE_URL, params=params)
        data = response.json()

        if "current_weather" in data:
            cw = data["current_weather"]
            return {
                "temperature": cw["temperature"],
                "windspeed": cw["windspeed"],
                "weathercode": cw["weathercode"],
                "time": cw["time"]
            }
        else:
            return {"error": "Không lấy được dữ liệu thời tiết."}



import requests

class WeatherAPI:
    BASE_URL = "https://api.open-meteo.com/v1/forecast"

    def get_weather(self, latitude: float, longitude: float):
        """Gọi API Open-Meteo để lấy thời tiết hiện tại"""
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current_weather": True
        }
        response = requests.get(self.BASE_URL, params=params)
        data = response.json()

        if "current_weather" in data:
            cw = data["current_weather"]
            return {
                "temperature": cw["temperature"],
                "windspeed": cw["windspeed"],
                "weathercode": cw["weathercode"],
                "time": cw["time"]
            }
        else:
            return {"error": "Không lấy được dữ liệu thời tiết."}
'''


import requests

class WeatherAPI:
    BASE_URL = "https://api.open-meteo.com/v1/forecast"

    def get_weather(self, latitude: float, longitude: float):
        """Gọi Open-Meteo API để lấy dữ liệu thời tiết hiện tại"""
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current_weather": True
        }
        response = requests.get(self.BASE_URL, params=params)
        data = response.json()

        if "current_weather" in data:
            cw = data["current_weather"]
            return {
                "temperature": cw["temperature"],
                "windspeed": cw["windspeed"],
                "weathercode": cw["weathercode"],
                "time": cw["time"]
            }
        else:
            return {"error": "Không lấy được dữ liệu thời tiết."}
