import os
from dotenv import load_dotenv
import google.generativeai as genai

# Ẩn log gRPC
os.environ["GRPC_VERBOSITY"] = "NONE"
os.environ["GRPC_TRACE"] = ""

# Load file .env
load_dotenv()

# Cấu hình API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Cấu hình sinh văn bản
generation_config = {
    "temperature": 0.3,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 2048,
    "response_mime_type": "text/plain",
}

# Cấu hình an toàn
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

# Tạo model Gemini
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    safety_settings=safety_settings,
    generation_config=generation_config,
    system_instruction="""
Bạn là trợ lý du lịch AI chuyên về Việt Nam.
Nhiệm vụ:
- Gợi ý các địa điểm nổi tiếng ở Việt Nam (Hạ Long, Đà Nẵng, Hội An, Sapa…)
- Giới thiệu món ăn và nhà hàng địa phương
- Gợi ý lịch trình theo vùng miền (Bắc, Trung, Nam)
- Cung cấp thông tin văn hóa, phong tục, lưu ý cho khách du lịch

Luôn trả lời bằng tiếng Việt, tự nhiên như hướng dẫn viên địa phương thân thiện.
Nếu không có thông tin, hãy trả lời lịch sự: "Xin lỗi, tôi chưa có thông tin về điều đó."
"""
)

# Tạo phiên chat (duy trì trong suốt runtime)
chat_session = model.start_chat(history=[])

def ask_gemini(prompt: str) -> str:
    """
    Hàm gửi câu hỏi đến Gemini và trả về câu trả lời bằng tiếng Việt.
    """
    try:
        response = chat_session.send_message(prompt)
        answer = response.text
        # Cập nhật lịch sử
        chat_session.history.append({"role": "user", "parts": [prompt]})
        chat_session.history.append({"role": "model", "parts": [answer]})
        return answer
    except Exception as e:
        return f"Lỗi khi gọi API: {e}"