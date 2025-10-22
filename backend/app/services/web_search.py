def search_web(nlp_result):
    """
    Giả lập gọi API search layer (sau này dùng SerpAPI, Bing, hoặc LangChain Tool)
    """
    query = nlp_result.get("entities", {}).get("location", "") or "du lịch"
    return [f"Thông tin mới nhất về {query}..."]