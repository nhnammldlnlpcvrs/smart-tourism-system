def call_llm(prompt, context=None):
    """
    Placeholder gọi LLM (OpenAI, HuggingFace, LangChain)
    """
    if context:
        prompt += f"\nDữ liệu hỗ trợ: {context}"
    return f"Trả lời giả lập cho: {prompt}"