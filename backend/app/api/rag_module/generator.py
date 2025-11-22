# generator.py
from typing import List, Dict
from llm_module import ask_gemini

"""
    Tạo prompt kết hợp giữa contexts (list record dicts) và câu hỏi.
    retrieved_contexts: list of dict (record).
"""
def build_prompt(user_query: str, retrieved_contexts: List[Dict]) -> str:
    # Chuyển mỗi record thành block text ngắn để prompt rõ ràng.
    context_texts = []
    for r in retrieved_contexts:
        # Lấy một số field hay có: name, province, description — fallback stringify
        name = r.get("name") or r.get("title") or ""
        province = r.get("province", "")
        desc = r.get("description", "") or r.get("desc", "")
        # Nếu record có cấu trúc khác, stringify một đoạn gọn
        if not (name or province or desc):
            # stringify top-level keys (ngắn)
            items = []
            for k, v in r.items():
                items.append(f"{k}: {v}")
            desc = "; ".join(items)
        block = f"Tên: {name}\nTỉnh: {province}\nMô tả: {desc}"
        context_texts.append(block)

    context_text = "\n\n---\n\n".join(context_texts)

    prompt = f"""
Dưới đây là các thông tin tham khảo (đã trích xuất):

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
