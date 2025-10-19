import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# Load environment variables
load_dotenv()

# Load JSON landmarks data
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "landmarks.json")
try:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        LANDMARKS = json.load(f)
except Exception as e:
    raise RuntimeError(f"Failed to load landmarks.json: {e}")

# Initialize LLM
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7,
    max_tokens=300,
    api_key=os.getenv("OPENAI_API_KEY"),
)

def search_landmark(query: str):
    """Search for a landmark using keywords."""
    query_lower = query.lower()
    for name, info in LANDMARKS.items():
        if name.lower() in query_lower or query_lower in name.lower():
            return name, info
        for keyword in info.get("keywords", []):
            if keyword.lower() in query_lower:
                return name, info
    return None, None

def build_answer_from_data(name, info):
    """Build a natural Vietnamese travel description based on JSON data."""
    description = " ".join(info.get("description", []))
    foods = ", ".join(info.get("foods", []))
    nearby = ", ".join(info.get("related_places", []))
    return (
        f"**{name}** là một địa điểm du lịch nổi tiếng tại Việt Nam. "
        f"{description} "
        f"Những món ăn đặc sản bạn nên thử khi đến đây gồm: {foods}. "
        f"Các địa điểm lân cận có thể tham khảo: {nearby}."
    )

def ask_gpt(question):
    """Ask GPT if not found in local data."""
    try:
        messages = [
            SystemMessage(content="Bạn là chuyên gia du lịch Việt Nam. Trả lời thân thiện, tự nhiên."),
            HumanMessage(content=question),
        ]
        response = llm(messages)
        return response.content
    except Exception as e:
        return f"Xin lỗi, tôi đang gặp lỗi khi xử lý yêu cầu: {e}"

def chatbot_reply(question: str):
    """Main chatbot response handler."""
    if any(word in question.lower() for word in ["thời tiết", "nhiệt độ", "mưa", "nắng", "trời"]):
        return ask_gpt(question)
    
    name, info = search_landmark(question)
    if name:
        return build_answer_from_data(name, info)
    return ask_gpt(question)