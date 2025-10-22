from app.services.nlp_preprocessing import preprocess_query
from app.services.decision_module import decide_workflow
from app.services.web_search import search_web
from app.services.llm_module import call_llm

def handle_chat(user_input: str):
    nlp_result = preprocess_query(user_input)
    action = decide_workflow(nlp_result)

    if action == "llm":
        answer = call_llm(user_input)
    elif action == "web_search":
        snippets = search_web(nlp_result)
        answer = call_llm(user_input, context=snippets)
    else:
        answer = "Xin lỗi, tôi chưa hiểu yêu cầu của bạn."

    return {"answer": answer}