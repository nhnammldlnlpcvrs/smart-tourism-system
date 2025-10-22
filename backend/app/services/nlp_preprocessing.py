def preprocess_query(text: str):
    """
    - Chuẩn hóa văn bản (lowercase, bỏ ký tự đặc biệt)
    - Tách intent & entities
    """
    text = text.lower().strip()
    intent = None
    if "thời tiết" in text:
        intent = "ask_weather"
    elif "ăn" in text:
        intent = "ask_food"
    elif "đi đâu" in text:
        intent = "ask_place"

    return {"intent": intent, "entities": {}}