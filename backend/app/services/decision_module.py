def decide_workflow(nlp_result):
    """
    - Nếu intent thuộc loại đơn giản (ask_food, ask_place) -> LLM
    - Nếu intent cần dữ liệu cập nhật (weather, events) -> Web Search
    """
    if nlp_result["intent"] in ["ask_weather", "plan_trip"]:
        return "web_search"
    return "llm"