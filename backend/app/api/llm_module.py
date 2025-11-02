import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

from app.service.map_module import get_nearby_places, get_distance  #map
from app.service.weather_module import get_weather  # weather

# 🔇 Tắt log gRPC để tránh spam console
os.environ["GRPC_VERBOSITY"] = "NONE"
os.environ["GRPC_TRACE"] = ""

# 📌 Load biến môi trường từ file .env
load_dotenv()

# 🔑 Lấy GEMINI_API_KEY từ .env để cấu hình cho Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ⚙️ Cấu hình sinh văn bản của model
generation_config = {
    "temperature": 0.3,  # kiểm soát độ sáng tạo (thấp -> chính xác hơn)
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 2048,
    "response_mime_type": "text/plain",
}

# 🛡️ Cấu hình an toàn nội dung
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

# 🤖 Tạo model Gemini kèm system prompt hướng dẫn nhiệm vụ
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=generation_config,
    safety_settings=safety_settings,
    system_instruction="""
Bạn là trợ lý du lịch Việt Nam.
Trả lời bằng tiếng Việt thân thiện, tự nhiên.

Các công cụ bạn có thể sử dụng:
1️⃣ get_nearby_places(location, type, radius) → lấy địa điểm du lịch gần đó
2️⃣ get_distance(origin, destination) → tính khoảng cách giữa hai điểm
3️⃣ get_weather(city) → lấy thông tin thời tiết hiện tại của một thành phố

Khi trả lời:
- Chỉ dùng dữ liệu từ công cụ
- Format kết quả:
    ⭐ <Tên địa điểm>
    📍 Địa chỉ: <địa chỉ>
    🔗 [Xem trên Google Maps](<link>)
    
Hoặc nếu là thời tiết:
    🌤️ Thời tiết tại <city>, <country>:
    - Mô tả: <weather>
    - Nhiệt độ: <temperature>°C
    - Độ ẩm: <humidity>%
    - Gió: <wind_speed> m/s
"""
)

# ✅ Mở phiên làm việc chat để duy trì ngữ cảnh cuộc hội thoại
chat_session = model.start_chat(history=[])

# 🧩 Hàm chính dùng để hỏi Gemini và xử lý kết quả từ tool
async def ask_gemini(prompt: str) -> str:
    try:
        # Gửi tin nhắn người dùng lên Gemini
        response = await chat_session.send_message_async(prompt)
        candidates = response.candidates

        # 🔍 Nếu Gemini yêu cầu gọi công cụ API
        if candidates and hasattr(candidates[0], "tool_calls"):
            tool_calls = candidates[0].tool_calls
            formatted_list = ""

            # Xử lý từng lời gọi công cụ
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)

                # 🗺️ Nếu gọi API Nearby Places
                if function_name == "get_nearby_places":
                    raw_places = await get_nearby_places(**args)
                    items = raw_places.get("results", [])[:5]  # lấy tối đa 5 địa điểm
                    for place in items:
                        name = place.get("name", "Không tên")
                        address = place.get("vicinity", "Không rõ địa chỉ")
                        link = place.get("google_maps_link", "")
                        formatted_list += f"⭐ {name}\n📍 Địa chỉ: {address}\n🔗 [Xem trên Google Maps]({link})\n\n"
                    return formatted_list.strip()

                # 📏 Nếu gọi API Distance Matrix
                elif function_name == "get_distance":
                    result = await get_distance(**args)
                    dist_text = result["routes"][0]["legs"][0]["distance"]["text"]
                    dur_text = result["routes"][0]["legs"][0]["duration"]["text"]
                    return f"📏 Quãng đường: {dist_text}\n⏱️ Thời gian di chuyển ước tính: {dur_text}"

                # 🌤️ Nếu gọi API Weather
                elif function_name == "get_weather":
                    weather = get_weather(**args)
                    if "error" in weather:
                        return "❌ " + weather["error"]
                    return (
                        f"🌤️ Thời tiết tại {weather['city']}, {weather['country']}:\n"
                        f"- Mô tả: {weather['weather']}\n"
                        f"- Nhiệt độ: {weather['temperature']}°C\n"
                        f"- Độ ẩm: {weather['humidity']}%\n"
                        f"- Gió: {weather['wind_speed']} m/s"
                    )

            # 🔁 Khi không có dữ liệu hợp lệ
            return "Xin lỗi, dữ liệu bạn cần chưa sẵn sàng."

        else:
            # Nếu Gemini trả lời không gọi tool (văn bản bình thường)
            return response.text

    except Exception as e:
        # Bắt lỗi chung để debug dễ hơn
        return f"Lỗi: {e.__class__.__name__} - {e}"
