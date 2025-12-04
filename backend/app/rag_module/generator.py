import json
from app.api.llm_module import ask_gemini

def build_prompt(user_query: str, retrieved_contexts):
    parts = []
    for r in retrieved_contexts:
        parts.append(json.dumps(r, ensure_ascii=False, indent=2))

    context_text = "\n\n---\n\n".join(parts)

    return f"""
    Dưới đây là các thông tin tham khảo:
        
        {context_text}
        
        ---
        
        Câu hỏi của người dùng: {user_query}
        
        Hướng dẫn cho hệ thống:
        Bạn là một hướng dẫn viên du lịch chuyên nghiệp, trả lời bằng tiếng Việt, với phong cách thân thiện – gãy gọn – dễ hiểu – giàu cảm xúc như khi đang trò chuyện với du khách.
        YÊU CẦU BẮT BUỘC KHI TRẢ LỜI:
        Phân tích và tổng hợp đầy đủ tất cả thông tin xuất hiện trong phần tham khảo (context).
        Không được bỏ sót bất kỳ chi tiết nào.
        Nếu có nhiều nguồn cung cấp thông tin về cùng một chủ đề, phải gom lại và viết thành một đoạn liền mạch.
        Câu trả lời phải mượt mà, tự nhiên như người thật nói chuyện.
        Tuyệt đối không được nhắc đến “tài liệu”, “doc”, “nguồn số X”, “ngữ cảnh số Y”…
        Chỉ viết nội dung đã tổng hợp, trình bày liền mạch trong một đoạn hoặc nhiều đoạn.
        Không tự bịa thêm thông tin ngoài context.
        Nếu tổng hợp xong mà vẫn không đủ dữ liệu để trả lời câu hỏi, phải trả lời:
        “Xin lỗi, tôi chưa có thông tin về điều đó.”
        Giọng văn phải mang sắc thái của một hướng dẫn viên du lịch:
        nhiệt tình
        am hiểu
        gợi ý thêm hoạt động phù hợp
        đưa lời khuyên hữu ích
        Định dạng trả lời:
        → Trả lời bằng một đoạn văn mô tả tự nhiên (có thể chia đoạn), thân thiện, liền mạch, đầy đủ thông tin đã tổng hợp từ context.”
    """

async def generate_answer(user_query: str, contexts):
    try:
        prompt = build_prompt(user_query, contexts)
        return await ask_gemini(prompt)
    except Exception as e:
        return "Lỗi trong generator: {e}"


