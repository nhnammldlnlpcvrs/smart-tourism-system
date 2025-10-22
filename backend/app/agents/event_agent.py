"""
Event Agent
------------
Mục đích:
- Lấy thông tin sự kiện, lễ hội, triển lãm hoặc hoạt động du lịch mới nhất.

TODO:
- Gọi API hoặc crawl dữ liệu từ các nguồn du lịch (TripAdvisor, Tourism.com.vn, v.v.)
- Có thể kết hợp với web_search_agent để truy xuất event theo địa điểm.
"""

def get_local_events(location: str):
    """
    Trả về danh sách sự kiện ở địa điểm du lịch.
    """
    print(f"[EventAgent] Fetching events in {location}")

    # TODO: Replace mock with real event data
    mock_events = [
        {"name": "Lễ hội Hoa Đà Lạt", "date": "2025-12-01", "description": "Sự kiện hoa lớn nhất Việt Nam."},
        {"name": "Festival Huế", "date": "2025-04-15", "description": "Lễ hội văn hóa truyền thống của cố đô Huế."},
    ]
    return mock_events