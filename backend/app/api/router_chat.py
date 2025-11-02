from fastapi import APIRouter, Query
from pydantic import BaseModel
from app.api.llm_module import ask_gemini

# Tạo router cho nhóm API Chat
router = APIRouter(prefix="/chat", tags=["Chat"])

# 📌 GET endpoint để gọi chatbot dùng query param
@router.get("/smart-find")
async def smart_find(query: str = Query(...)):
    """
    Nhận input từ người dùng thông qua query string:
    Ví dụ: /chat/smart-find?query=quán ăn gần đây
    """
    # ⛓️ Đợi kết quả từ hàm gọi Gemini (bắt buộc dùng await)
    response = await ask_gemini(query)
    return {"result": response}

# 🧩 Định nghĩa body request cho API POST
class ChatRequest(BaseModel):
    # message: nội dung người dùng nhắn tới chatbot
    message: str

# 💬 POST endpoint chat tổng quát
@router.post("/")
async def chat(request: ChatRequest):
    """
    API chính dành cho hội thoại chatbot du lịch.
    - Nhận câu hỏi từ user dưới dạng JSON body.
    - Gửi đến LLM (Gemini) để xử lý.
    - Có thể trigger function calling để lấy dữ liệu thật (bản đồ, thời tiết,...)
    """
    # ⛓️ BẮT BUỘC phải dùng await vì ask_gemini là async
    reply = await ask_gemini(request.message)

    # Trả về cả câu hỏi người dùng và phản hồi của bot
    return {
        "user_message": request.message,
        "bot_reply": reply
    }
