import pytest
from unittest.mock import patch, MagicMock

from app.api.rag_itinerary_module import generate_itinerary_rag


@pytest.mark.asyncio
async def test_generate_itinerary_rag_basic():
    """
    Test cơ bản: mock pipeline và kiểm tra output format.
    """

    fake_contexts = [
        {"title": "Điểm A", "score": 0.88},
        {"title": "Điểm B", "score": 0.75},
    ]

    fake_places = [
        {"name": "Place 1", "activities": ["Ảnh đẹp"], "weather_notes": "Thoáng mát", "highlights": ["Check-in"], "duration_recommend": "2 giờ"},
        {"name": "Place 2", "activities": ["Đi dạo"], "weather_notes": "Nắng nhẹ", "highlights": ["Ẩm thực"], "duration_recommend": "1 giờ"},
        {"name": "Place 3", "activities": ["Ngắm cảnh"], "weather_notes": "Gió nhẹ", "highlights": ["Phong cảnh"], "duration_recommend": "3 giờ"},
        {"name": "Place 4", "activities": ["Chụp ảnh"], "weather_notes": "Mát mẻ", "highlights": ["Nổi bật"], "duration_recommend": "1.5 giờ"},
    ]

    # Mock pipeline
    mock_pipeline = MagicMock()
    mock_pipeline.search.return_value = fake_contexts

    with patch("app.api.rag_itinerary_module.get_pipeline", return_value=mock_pipeline):
        res = generate_itinerary_rag(
            province="Hà Nội",
            days=1,
            preferences={
                "interests": ["culture"],
                "pace": "relaxed",
                "group_type": "family",
                "avoid_categories": ["crowded"],
            },
            places=fake_places
        )

    # ---- Assertions ----
    assert res["province"] == "Hà Nội"
    assert res["days"] == 1
    assert "itinerary" in res
    assert "rag_contexts_used" in res

    # Itinerary phải chứa Day 1
    assert "Day 1" in res["itinerary"]

    # Kiểm tra 4 điểm trong 1 ngày
    assert "Place 1" in res["itinerary"]
    assert "Place 2" in res["itinerary"]
    assert "Place 3" in res["itinerary"]
    assert "Place 4" in res["itinerary"]

    # RAG contexts trả về đúng mock
    assert res["rag_contexts_used"] == fake_contexts


def test_generate_itinerary_with_less_places():
    """
    Test khi số lượng places < days * 4
    """

    fake_contexts = [{"title": "CTX", "score": 0.5}]
    fake_places = [
        {"name": "P1", "activities": [], "weather_notes": "", "highlights": [], "duration_recommend": ""},
        {"name": "P2", "activities": [], "weather_notes": "", "highlights": [], "duration_recommend": ""},
    ]

    mock_pipeline = MagicMock()
    mock_pipeline.search.return_value = fake_contexts

    with patch("app.api.rag_itinerary_module.get_pipeline", return_value=mock_pipeline):
        res = generate_itinerary_rag(
            province="Đồng Nai",
            days=1,
            preferences={},
            places=fake_places
        )

    assert "P1" in res["itinerary"]
    assert "P2" in res["itinerary"]
    # Không đủ 4 điểm → không crash
    assert "Day 1" in res["itinerary"]
    assert res["rag_contexts_used"] == fake_contexts
