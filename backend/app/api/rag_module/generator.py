from llm_module import ask_gemini
from typing import List

"""
    Tạo prompt hoàn chỉnh cho LLM, kết hợp giữa ngữ cảnh (retrieved_contexts)
    và câu hỏi của người dùng (user_query).
"""
def build_prompt(user_query : str, retrieved_contexts : List[str]) -> str:
    context_text = "\n\n".join(retrieved_contexts)
    prompt = f"""
Dưới đây là các thông tin du lịch có thể liên quan:

{context_text}

Câu hỏi của người dùng: {user_query}

→ Dựa trên thông tin trên, hãy trả lời bằng tiếng Việt, súc tích, và thân thiện.
Nếu không đủ dữ liệu, hãy nói: "Xin lỗi, tôi chưa có thông tin về điều đó."
"""
    return prompt.strip()


def generate_answer(user_query : str, retrieved_contexts : List[str]) -> str:
    try:
        prompt = build_prompt(user_query, retrieved_contexts)
        answer = ask_gemini(prompt)
        return answer
    except Exception as e:
        return f"Lỗi trong generator: {e}"