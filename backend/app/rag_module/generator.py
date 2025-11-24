from typing import List, Dict
from llm_module import ask_gemini
import json

"""
    Tạo prompt kết hợp giữa contexts (list record dicts) và câu hỏi.
    retrieved_contexts: list of dict (record).
    Mỗi record được serialize đầy đủ sang JSON để gửi cho LLM.
"""
def build_prompt(user_query: str, retrieved_contexts: List[Dict]) -> str:
    context_texts = []
    for r in retrieved_contexts:
        # Serialize toàn bộ record sang JSON, giữ UTF-8 và readable
        record_json = json.dumps(r, ensure_ascii=False, indent=2)
        context_texts.append(record_json)

    # Nối các record với separator để LLM phân biệt
    context_text = "\n\n---\n\n".join(context_texts)

    prompt = f"""
Dưới đây là các thông tin tham khảo (toàn bộ dữ liệu các record đã retrieve):

{context_text}

Câu hỏi của người dùng: {user_query}

→ Hãy trả lời BẰNG TIẾNG VIỆT, súc tích, thân thiện.
Nếu không đủ dữ liệu, hãy nói: "Xin lỗi, tôi chưa có thông tin về điều đó."
"""
    return prompt.strip()


def generate_answer(user_query: str, retrieved_contexts: List[Dict]) -> str:
    try:
        prompt = build_prompt(user_query, retrieved_contexts)
        answer = ask_gemini(prompt)
        return answer
    except Exception as e:
        return f"Lỗi trong generator: {e}"