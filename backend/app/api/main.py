import os
import google.generativeai as genai
from dotenv import load_dotenv

# Suppress gRPC logs
os.environ["GRPC_VERBOSITY"] = "NONE"
os.environ["GRPC_TRACE"] = ""

load_dotenv()

# Configure API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Generation configuration
generation_config = {
    "temperature": 0,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Safety settings
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

# Create the travel assistant model
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

# Start chat session
chat_session = model.start_chat(history=[])

print("Bot: Xin chào! Tôi có thể giúp gì cho bạn về du lịch Việt Nam?")

while True:
    user_input = input("You: ")
    print()

    response = chat_session.send_message(user_input)
    model_response = response.text

    print(f"Bot: {model_response}")
    print()
    
    # Append to chat history
    chat_session.history.append({"role": "user", "parts": [user_input]})
    chat_session.history.append({"role": "model", "parts": [model_response]})
    
    if user_input.lower() in ["thoát", "kết thúc", "exit", "quit", "bye", "cảm ơn"]:
        break