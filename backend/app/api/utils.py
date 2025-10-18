import os
import json
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

# Load OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Load landmarks data
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "landmarks.json")
with open(DATA_PATH, "r", encoding="utf-8") as f:
    LANDMARKS = json.load(f)

# Khởi tạo LLM từ LangChain
llm = ChatOpenAI(
    openai_api_key=OPENAI_API_KEY,
    model_name="gpt-3.5-turbo",
    temperature=0.7
)


def search_landmark_in_data(query: str):
    """
    Tìm địa điểm trong file landmarks.json theo tên.
    So khớp linh hoạt theo từ khóa người dùng nhập.
    """
    query_lower = query.lower()

    for name, info in LANDMARKS.items():
        # So khớp tên địa điểm
        if name.lower() in query_lower or query_lower in name.lower():
            return {name: info}

        # So khớp theo keywords
        for kw in info.get("keywords", []):
            if kw.lower() in query_lower:
                return {name: info}

    return None


def generate_ai_response(question: str, fallback_data=None):
    """
    Nếu tìm thấy dữ liệu trong JSON -> Tạo câu trả lời từ dữ liệu đó
    Nếu không -> Fallback dùng GPT trả lời chung
    """
    system_prompt = "Bạn là trợ lý du lịch thông minh chuyên tư vấn về du lịch tại Việt Nam."

    if fallback_data:
        # Trả lời dựa trên thông tin JSON
        landmark_name = list(fallback_data.keys())[0]
        info = fallback_data[landmark_name]

        content = (
            f"Người dùng hỏi về địa điểm du lịch: {landmark_name}.\n"
            f"Mô tả: {info.get('description', 'Chưa có mô tả')}.\n"
            f"Món ăn đặc sản: {', '.join(info.get('foods', []))}.\n"
            f"Các địa điểm liên quan gần đó: {', '.join(info.get('related_places', []))}.\n"
            f"Hãy trả lời thân thiện và tự nhiên như người thật."
        )
    else:
        # GPT tự trả lời chung chung
        content = f"Hãy trả lời câu hỏi sau về du lịch Việt Nam: {question}"

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=content)
    ]
    response = llm(messages)
    return response.content


def chatbot_reply(question: str):
    """
    Hàm chính để chatbot trả lời.
    """
    # 1. Thử tìm trong JSON trước
    data_match = search_landmark_in_data(question)

    # 2. Nếu có -> tạo câu trả lời từ JSON + GPT hỗ trợ diễn đạt
    if data_match:
        return generate_ai_response(question, fallback_data=data_match)

    # 3. Nếu không có -> fallback GPT trả lời chung
    return generate_ai_response(question, fallback_data=None)