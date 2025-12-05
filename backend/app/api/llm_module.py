import os
import asyncio
from dotenv import load_dotenv
import google.generativeai as genai

from app.service.weather.weather_module import get_current_weather
from app.service.map.map_module import get_nearby_places, get_distance
from app.service.tourism.tourism_module import get_category_tree_by_province
from app.service.hotel.hotel_module import get_hotels_by_province_and_place_id
from app.service.foods.food_module import get_foods_by_province_and_tag

# CẤU HÌNH VÀ KHỞI TẠO MODEL
# Tắt logging GRPC (Để terminal sạch sẽ hơn)
os.environ["GRPC_VERBOSITY"] = "NONE"
os.environ["GRPC_TRACE"] = ""

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Tổng hợp tất cả các tools mà Chatbot có thể sử dụng
chat_tools = [
    get_current_weather,
    get_nearby_places,
    get_distance,
    get_category_tree_by_province, # Để lấy cấu trúc du lịch
    get_hotels_by_province_and_place_id, # Gợi ý khách sạn
    get_foods_by_province_and_tag    # Gợi ý món ăn
]

chat_model = genai.GenerativeModel(
    model_name="gemini-2.5-flash", # Dùng model 2.5 flash cho tốc độ
    tools=chat_tools,
    system_instruction="Bạn là Trợ lý Du lịch Việt Nam, chuyên cung cấp thông tin thời tiết, địa điểm, món ăn và chỗ ở. Trả lời ngắn gọn, thân thiện và sử dụng các công cụ khi cần thiết."
)
# Khởi tạo session chat để giữ lịch sử hội thoại
chat_session = chat_model.start_chat(history=[])

# MODEL CHUYÊN DỤNG: WRITER (Viết lời bình)
writer_model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    generation_config={"temperature": 0.8, "max_output_tokens": 200},
    system_instruction="Bạn là một hướng dẫn viên du lịch vui tính, am hiểu văn hóa Việt Nam."
)

# CHUYÊN TẠO LỜI BÌNH LUẬN CHO APP (Sử dụng writer_model)
async def generate_smart_comment(city: str, service_type: str) -> str:
    """
    Sinh ra một câu bình luận ngắn gọn, thú vị dựa trên địa điểm và dịch vụ người dùng đang xem.
    """
    prompt = ""
    
    if service_type == "hotel":
        prompt = f"Người dùng đang tìm khách sạn tại {city}. Hãy viết một câu (1-2 câu) khen ngợi {city} và mời họ xem danh sách khách sạn bên dưới. Ví dụ: 'Woa, {city} mùa này đẹp lắm! Dưới đây là mấy khách sạn view xịn mình tìm được nè 👇'"
    elif service_type == "food":
        prompt = f"Người dùng đang tìm món ăn tại {city}. Hãy viết một câu (1-2 câu) nhắc đến một đặc sản nổi tiếng của {city} và mời họ xem danh sách. Ví dụ: 'Đến {city} mà không ăn [đặc sản] là phí lắm nha! Xem ngay list quán ngon này 👇'"
    elif service_type == "place":
        prompt = f"Người dùng đang xem địa điểm tham quan tại {city}. Hãy viết một câu hào hứng rủ họ xách ba lô lên và đi."
    else:
        prompt = f"Chào mừng bạn đến với {city}. Dưới đây là thông tin bạn cần."

    try:
        # Gọi model sinh text thuần túy -> Nhanh & Rẻ
        response = await writer_model.generate_content_async(prompt)
        return response.text.strip()
    except Exception:
        return f"Chào bạn! Dưới đây là danh sách {service_type} tại {city} mình tìm được nha! 👇"

# HÀM CHÍNH: XỬ LÝ CHATBOT TỰ DO (Sử dụng chat_session)
async def ask_gemini(user_prompt: str):
    """
    Xử lý yêu cầu của người dùng, gọi các công cụ (tools) nếu cần thiết.
    """
    response = await chat_session.send_message_async(user_prompt)

    if response.function_calls:
        print(f" DEBUG: Model quyết định gọi {len(response.function_calls)} tool.")
        
        # Tạo list các task (công việc) bất đồng bộ để gọi các tool
        tool_results = []
        for call in response.function_calls:
            # Lấy hàm cần gọi từ global scope
            tool_func = globals().get(call.name)
            if tool_func:
                # Thực hiện gọi hàm với các đối số mà model cung cấp
                # Dùng asyncio.to_thread nếu hàm là blocking (như các hàm DB/requests không phải async)
                # Hoặc gọi trực tiếp nếu hàm là async (như httpx/asyncpg)
                if asyncio.iscoroutinefunction(tool_func):
                    result = await tool_func(**dict(call.args))
                else:
                    result = await asyncio.to_thread(tool_func, **dict(call.args))
                
                tool_results.append(
                    genai.types.Part.from_function_response(name=call.name, response=result)
                )
            else:
                 print(f"Tool {call.name} not found.")
        
        # Gửi kết quả của tool trở lại cho Model để nó tổng hợp câu trả lời
        response = await chat_session.send_message_async(tool_results)

    return response.text.strip()