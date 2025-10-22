import requests
import os

SERPAPI_KEY = os.getenv("SERPAPI_KEY", "dummy-key")

def search_serpapi(query: str, num_results: int = 3):
    """
    Tác nhân web search:
    - Gửi request tới SerpAPI (hoặc API tương tự)
    - Trả về danh sách các snippet (tiêu đề, mô tả, URL)
    """
    print(f"[WebSearchAgent] Searching for: {query}")

    # Giả lập khi chưa có API thật
    mock_results = [
        {"title": f"Kết quả 1 cho {query}", "snippet": "Thông tin giả lập 1...", "url": "https://example.com/1"},
        {"title": f"Kết quả 2 cho {query}", "snippet": "Thông tin giả lập 2...", "url": "https://example.com/2"},
    ]
    return mock_results


def extract_snippets(results):
    """Trích xuất nội dung text từ kết quả search"""
    return [r["snippet"] for r in results]


""" 
    TODO:
    - Tích hợp SerpAPI, Bing API hoặc Google Custom Search API.
    - Tối ưu hóa query dựa trên intent và entities.
    
Cái này dùng trong services/web_search.py thay cho bản giả lập cũ:

from app.agents.web_search_agent import search_serpapi, extract_snippets

def search_web(nlp_result):
    query = nlp_result.get("entities", {}).get("location", "") or "du lịch Việt Nam"
    results = search_serpapi(query)
    snippets = extract_snippets(results)
    return snippets
"""