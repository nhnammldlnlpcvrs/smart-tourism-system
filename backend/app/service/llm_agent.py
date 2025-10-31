'''
from openai import OpenAI
from weather_api import WeatherAPI

# Tạo client (nhớ set môi trường: setx OPENAI_API_KEY "key_của_bạn")
client = OpenAI()
weather_api = WeatherAPI()

class LLMAgent:
    def __init__(self):
        self.locations = {
            "hanoi": (21.0285, 105.8542),
            "hochiminh": (10.7626, 106.6602),
            "danang": (16.0544, 108.2022)
        }

    def handle_query(self, query: str):
        """Xử lý truy vấn của người dùng."""
        query_lower = query.lower()
        for city in self.locations:
            if city in query_lower:
                lat, lon = self.locations[city]
                weather = weather_api.get_weather(lat, lon)
                if "error" in weather:
                    return "Xin lỗi, tôi không thể lấy dữ liệu thời tiết."
                return f"🌤 Thời tiết ở {city.title()} hiện tại: {weather['temperature']}°C, gió {weather['windspeed']} km/h, lúc {weather['time']}."
        
        # Nếu không có thành phố trong câu hỏi → chuyển qua LLM để trả lời bình thường
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": query}]
        )
        return response.choices[0].message.content

        

from openai import OpenAI
from weather_api import WeatherAPI

# Tạo client OpenAI (nhớ set biến môi trường OPENAI_API_KEY)
client = OpenAI()
weather_api = WeatherAPI()

class LLMAgent:
    def __init__(self):
        self.locations = {
            "hanoi": (21.0285, 105.8542),
            "hochiminh": (10.7626, 106.6602),
            "danang": (16.0544, 108.2022)
        }

    def handle_query(self, query: str):
        query_lower = query.lower()
        for city in self.locations:
            if city in query_lower:
                lat, lon = self.locations[city]
                weather = weather_api.get_weather(lat, lon)
                if "error" in weather:
                    return "Xin lỗi, tôi không thể lấy dữ liệu thời tiết."
                return f"🌤 Thời tiết ở {city.title()} hiện tại: {weather['temperature']}°C, gió {weather['windspeed']} km/h, lúc {weather['time']}."
        
        # Nếu không phải câu hỏi thời tiết, gọi LLM trả lời
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": query}]
        )
        return response.choices[0].message.content

        
        '''

from openai import OpenAI
from .weather_api import WeatherAPI  # <- chú ý import tương đối

# Khởi tạo client OpenAI
client = OpenAI()
weather_api = WeatherAPI()

class LLMAgent:
    def __init__(self):
        # Toạ độ 3 thành phố chính
        self.locations = {
            "hanoi": (21.0285, 105.8542),
            "hochiminh": (10.7626, 106.6602),
            "danang": (16.0544, 108.2022)
        }

    def handle_query(self, query: str):
        """Xử lý truy vấn người dùng (thời tiết hoặc hỏi LLM)"""
        query_lower = query.lower()
        for city in self.locations:
            if city in query_lower:
                lat, lon = self.locations[city]
                weather = weather_api.get_weather(lat, lon)
                if "error" in weather:
                    return "Xin lỗi, tôi không thể lấy dữ liệu thời tiết."
                return f"🌤 Thời tiết ở {city.title()} hiện tại: {weather['temperature']}°C, gió {weather['windspeed']} km/h, lúc {weather['time']}."
        
        # Nếu không phải câu hỏi thời tiết → gửi qua LLM
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": query}]
        )
        return response.choices[0].message.content
