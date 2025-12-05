# backend/app/api/llm_module.py
import os
import asyncio
from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai.types import Part

# Import tools
from app.service.weather.weather_module import get_current_weather
from app.service.map.map_module import get_nearby_places, get_distance
from app.service.tourism.tourism_module import get_category_tree_by_province
from app.service.hotel.hotel_module import get_hotels_by_province_and_place_id
from app.service.foods.food_module import get_foods_by_province_and_tag

# INIT
os.environ["GRPC_VERBOSITY"] = "NONE"
os.environ["GRPC_TRACE"] = ""
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Liệt kê tools cho model
chat_tools = [
    get_current_weather,
    get_nearby_places,
    get_distance,
    get_category_tree_by_province,
    get_hotels_by_province_and_place_id,
    get_foods_by_province_and_tag
]

# Model chính (hỗ trợ tool calling)
chat_model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    tools=chat_tools,
    system_instruction=(
        "Bạn là Trợ lý Du lịch Việt Nam. "
        "Khi cần thiết, hãy tự động gọi các công cụ để lấy dữ liệu thực tế. "
        "Luôn trả lời ngắn gọn, vui vẻ, ưu tiên dữ liệu chính xác."
    )
)

# Chat session giữ lịch sử
chat_session = chat_model.start_chat(history=[])

# Writer model — chuyên viết câu giới thiệu
writer_model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    generation_config={"temperature": 0.8, "max_output_tokens": 200},
    system_instruction="Bạn là một hướng dẫn viên du lịch vui tính của Việt Nam."
)

# WRITER COMMENT
async def generate_smart_comment(city: str, service_type: str) -> str:
    prompt = ""

    if service_type == "hotel":
        prompt = (
            f"Viết 1–2 câu chào khách đang tìm khách sạn tại {city}. "
            f"Gợi ý nhẹ về phong cảnh đẹp và mời họ xem danh sách khách sạn."
        )
    elif service_type == "food":
        prompt = (
            f"Viết 1–2 câu giới thiệu món ăn nổi tiếng tại {city} "
            f"và mời người dùng xem danh sách quán ngon."
        )
    elif service_type == "place":
        prompt = (
            f"Viết 1–2 câu rủ rê người dùng khám phá các địa điểm đẹp tại {city}."
        )
    else:
        prompt = f"Viết câu chào mừng người dùng đến {city}."

    try:
        response = await writer_model.generate_content_async(prompt)
        return response.text.strip()
    except Exception:
        return f"Chào bạn! Đây là danh sách {service_type} tại {city} nha"


# TOOL CALLING HANDLER
async def handle_tool_calls(response):
    """Xử lý tool calling từ Gemini."""
    tool_results = []

    for call in response.function_calls:
        tool_name = call.name
        args = dict(call.args)

        tool_func = globals().get(tool_name)

        if not tool_func:
            print(f"[WARN] Tool không tồn tại: {tool_name}")
            continue

        try:
            # Chạy tool async hoặc sync
            if asyncio.iscoroutinefunction(tool_func):
                result = await tool_func(**args)
            else:
                result = await asyncio.to_thread(tool_func, **args)

            tool_results.append(
                Part.from_function_response(name=tool_name, response=result)
            )

        except Exception as e:
            tool_results.append(
                Part.from_function_response(
                    name=tool_name,
                    response={"error": str(e)}
                )
            )

    # Gửi lại tool result để model tổng hợp trả lời
    return await chat_session.send_message_async(tool_results)


# MAIN CHAT HANDLER
async def ask_gemini(user_prompt: str):
    """
    Hàm chính để chatbot trả lời message của user (có tool calling).
    """

    # Nếu history quá dài → reset để tiết kiệm token
    if len(chat_session.history) > 40:
        chat_session.history = chat_session.history[-20:]

    response = await chat_session.send_message_async(user_prompt)

    # Model muốn gọi tool?
    if response.function_calls:
        response = await handle_tool_calls(response)

    return response.text.strip()