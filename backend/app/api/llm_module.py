import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

# Import các module API con
from app.service.map_module import get_nearby_places, get_distance, get_location  #map
from app.service.weather_module import get_weather  # weather
from app.service.hotel_module import recommend_hotels
from app.service.food_module import get_recommend_foods

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

# Khởi tạo mô hình Gemini với hướng dẫn hệ thống (system instruction)
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=generation_config,
    safety_settings=safety_settings,
    system_instruction="""
Bạn là **trợ lý du lịch thông minh tại Việt Nam**, giúp người dùng tra cứu **khách sạn, địa điểm, món ăn và thời tiết**.
Trả lời bằng tiếng Việt thân thiện, tự nhiên.

---

###  Quy tắc hoạt động
1️⃣ Khi người dùng hỏi, hãy tự động xác định nhu cầu (ví dụ: khách sạn, quán ăn, món ăn, thời tiết, khoảng cách...).
2️⃣ Nếu cần thông tin từ công cụ, hãy gọi **các hàm Python có sẵn** để lấy dữ liệu (chẳng hạn `get_weather`, `recommend_hotels`, `get_nearby_places`, `get_distance`...).
3️⃣ **Không bao giờ hiển thị hoặc in mã lệnh, code, hay tool_code.**
4️⃣ Sau khi lấy dữ liệu, **tự tổng hợp lại và trả lời bằng tiếng Việt tự nhiên, thân thiện, ngắn gọn.**
5️⃣ **Không trả lời bằng tiếng Anh trừ khi người dùng yêu cầu rõ.**
6️⃣ Nếu không có dữ liệu, hãy trả lời lịch sự, ví dụ: “Xin lỗi, mình chưa có thông tin chính xác về khu vực này.”

---

###  Các công cụ bạn có thể gọi
- `recommend_hotels(city)` → Gợi ý khách sạn từ cơ sở dữ liệu nội bộ. 
- `get_recommend_foods(province)` → Gợi ý món ăn đặc sản từ cơ sở dữ liệu nội bộ. 
- `get_nearby_places(location, type, radius)` → Tìm địa điểm du lịch, nhà hàng, quán cà phê quanh vị trí.  
- `get_distance(origin, destination)` → Tính khoảng cách giữa hai địa điểm.  
- `get_weather(city)` → Lấy thông tin thời tiết hiện tại của một thành phố.  

---

### 🗂️ Cấu trúc câu trả lời
Tùy theo mục đích, hãy định dạng như sau:

📌 Format khách sạn:
🏨 <Tên>
⭐ Đánh giá: <rating>
📍 <Địa chỉ>
🔗 <Google Map>

📌 Format địa điểm:
⭐ <Tên điểm đến>
📍 <Địa chỉ>
🔗 <Google Map>

📌 Format thời tiết:
🌤️ Thời tiết tại <city>:
- Mô tả: <weather>
- Nhiệt độ: <temp>°C
- Độ ẩm: <humidity>%
- Gió: <wind_speed> m/s

📌 Format món ăn:
🍽️ <Tên món>
📝 Mô tả: <description>
---

### 💬 Cách trình bày
- Luôn viết giọng thân thiện, ngắn gọn, tự nhiên (giống như một người Việt Nam đang trò chuyện).  
- Có thể thêm emoji phù hợp: ☀️🌧️☕🏝️📍  
- **Không bao giờ in đoạn mã hoặc ký hiệu ```tool_code``` hay ```python```** trong phản hồi.  

---
Ví dụ:  
> ☁️ Thời tiết hôm nay ở quận Tân Phú, TP.HCM: 31°C, độ ẩm 70%, trời nhiều mây.  
> Dưới đây là vài quán cà phê gần bạn có thể ghé thử:
> ☕ Runam Bistro – [Xem bản đồ](https://maps.app.goo.gl/...)  
> ☕ The Coffee House – [Xem bản đồ](https://maps.app.goo.gl/...)  

"""
)

# Tạo session chat
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
            result_text = ""

            # Xử lý từng lời gọi công cụ
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)

               # 1️⃣ Gợi ý khách sạn
                if function_name == "recommend_hotels":
                    if "latitude" not in args or "longitude" not in args:
                        loc = await get_location(args.get("query", prompt))
                        if not loc:
                            return "❌ Không tìm thấy địa điểm để gợi ý khách sạn."
                        args.update({"latitude": loc["lat"], "longitude": loc["lng"]})

                    hotels = await recommend_hotels(**args)
                    if not hotels:
                        return "❌ Không có khách sạn phù hợp gần đây."

                    for h in hotels[:5]:
                        result_text += (
                            f"🏨 {h['name']}\n"
                            f"⭐ Đánh giá: {h.get('rating', 'Chưa có')}\n"
                            f"📍 {h['address']}\n"
                            f"🔗 https://www.google.com/maps?q={h['latitude']},{h['longitude']}\n\n"
                        )
                    return result_text.strip()

                # 2️⃣ Địa điểm gần đó
                elif function_name == "get_nearby_places":
                    data = await get_nearby_places(**args)
                    items = data.get("results", [])[:5]
                    for p in items:
                        result_text += (
                            f"⭐ {p.get('name')}\n"
                            f"📍 {p.get('vicinity')}\n"
                            f"🔗 {p.get('google_maps_link', '')}\n\n"
                        )
                    return result_text.strip()

                # 3️⃣ Khoảng cách
                elif function_name == "get_distance":
                    data = await get_distance(**args)
                    leg = data["routes"][0]["legs"][0]
                    return f"📏 {leg['distance']['text']} — ⏱ {leg['duration']['text']}"

                # 4️⃣ Thời tiết
                elif function_name == "get_weather":
                    w = await get_weather(**args)
                    return (
                        f"🌤️ Thời tiết tại {w['city']}:\n"
                        f"- Mô tả: {w['weather']}\n"
                        f"- 🌡 {w['temperature']}°C\n"
                        f"- 💧 {w['humidity']}%\n"
                        f"- 💨 {w['wind_speed']} m/s"
                    )

                # 5️⃣ Món ăn đặc sản
                elif function_name == "get_recommend_foods":
                    foods = await get_recommend_foods(**args)
                    if not foods:
                        return "🍽️ Không tìm thấy đặc sản phù hợp."
                    for f in foods[:5]:
                        result_text += (
                            f"🍽️ {f['food']}\n"
                            f"📍 {f['province']}\n"
                            f"📝 {f['description']}\n\n"
                        )
                    return result_text.strip() 

            # 🔁 Khi không có dữ liệu hợp lệ
            return "Xin lỗi, dữ liệu bạn cần chưa sẵn sàng."

        else:
            # Nếu Gemini trả lời không gọi tool (văn bản bình thường)
            return response.text

    except Exception as e:
        # Bắt lỗi chung để debug dễ hơn
        return f"Lỗi: {e.__class__.__name__} - {e}"
