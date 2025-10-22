"""
Recommendation Agent
---------------------
Mục đích:
- Đưa ra gợi ý địa điểm, món ăn, hoạt động hoặc lịch trình theo sở thích người dùng.

TODO:
- Tích hợp model gợi ý (collaborative filtering hoặc rule-based)
- Hoặc dùng LLM (LangChain Tool) để generate recommendation tự nhiên hơn.
"""

def recommend_food(preferences: dict):
    """
    Gợi ý món ăn dựa trên sở thích người dùng.

    Args:
        preferences (dict): { "cuisine": "...", "diet": "...", "spice_level": "..." }

    Returns:
        list[dict]: Danh sách gợi ý món ăn
    """
    print(f"[RecommendationAgent] Generating food recommendations for: {preferences}")
    
    # TODO: Replace mock with ML or LLM-based recommendations
    mock_recommendations = [
        {"dish": "Phở Bò", "reason": "Món ăn truyền thống, phù hợp với mọi khẩu vị."},
        {"dish": "Gỏi Cuốn", "reason": "Món ăn nhẹ, tươi mát, tốt cho sức khỏe."},
    ]

def recommend_places(preferences: dict):
    """
    Gợi ý địa điểm dựa trên sở thích người dùng.

    Args:
        preferences (dict): { "type": "beach/mountain/culture", "budget": "...", "duration": "..." }

    Returns:
        list[dict]: Danh sách gợi ý địa điểm
    """
    print(f"[RecommendationAgent] Generating recommendations for: {preferences}")

    # TODO: Replace mock with ML or LLM-based recommendations
    mock_recommendations = [
        {"place": "Đà Nẵng", "reason": "Thành phố biển hiện đại, nhiều hoạt động giải trí."},
        {"place": "Sapa", "reason": "Phong cảnh núi đẹp, văn hóa dân tộc đặc sắc."},
    ]
    return mock_recommendations