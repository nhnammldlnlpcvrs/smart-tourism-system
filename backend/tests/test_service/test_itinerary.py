import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.api.main import app
from app.service.itinerary.itinerary_router import get_db

client = TestClient(app)


# ------------------------------------------------------------
# Utility: mock DB generator đúng chuẩn FastAPI
# ------------------------------------------------------------
def make_fake_db(places):
    """Tạo DB session mock trả về danh sách place (ORM Object)."""
    return MagicMock(
        query=lambda *args, **kwargs: MagicMock(
            filter=lambda *a, **k: MagicMock(all=lambda: places)
        )
    )


# ------------------------------------------------------------
# 1. SUCCESS
# ------------------------------------------------------------
def test_api_generate_itinerary_success():
    # Fake ORM instance
    fake_place = MagicMock()
    fake_place.id = 1
    fake_place.name = "Hồ Tây"
    fake_place.province = "Hà Nội"
    fake_place.category = "nature"
    fake_place.sub_category = ["lake"]
    fake_place.address = "abc"
    fake_place.latitude = 10.0
    fake_place.longitude = 20.0
    fake_place.highlights = []
    fake_place.activities = ["walking"]
    fake_place.special_for = ["family"]
    fake_place.duration_recommend = None
    fake_place.seasonal_events = []
    fake_place.best_time_to_visit = None
    fake_place.tags = ["relax"]
    fake_place.weather_notes = None
    fake_place.price_range = None
    fake_place.open_hours = None

    # override get_db
    def override_get_db():
        yield make_fake_db([fake_place])

    app.dependency_overrides[get_db] = override_get_db

    # mock RAG
    with patch(
        "app.service.itinerary.itinerary_module.generate_itinerary_rag",
        return_value={"itinerary": "OK"}
    ):
        payload = {
            "province": "Hà Nội",
            "days": 2,
            "preferences": {
                "interests": ["lake"],
                "pace": None,
                "group_type": "family",
                "avoid_categories": [],
                "time_preferences": {}
            }
        }

        res = client.post("/itinerary/generate", json=payload)

    assert res.status_code == 200
    assert res.json() == {"itinerary": "OK"}

    app.dependency_overrides.clear()


# ------------------------------------------------------------
# 2. INVALID DAYS
# ------------------------------------------------------------
def test_api_generate_itinerary_invalid_days():
    def override_get_db():
        yield MagicMock()  # không cần dùng DB
    app.dependency_overrides[get_db] = override_get_db

    payload = {
        "province": "Hà Nội",
        "days": 0,
        "preferences": {
            "interests": [],
            "pace": None,
            "group_type": None,
            "avoid_categories": [],
            "time_preferences": {}
        }
    }

    res = client.post("/itinerary/generate", json=payload)

    assert res.status_code == 400
    assert res.json()["detail"] == "Số ngày phải > 0"

    app.dependency_overrides.clear()


# ------------------------------------------------------------
# 3. PROVINCE NOT FOUND
# ------------------------------------------------------------
def test_api_generate_itinerary_province_not_found():

    # DB trả về rỗng
    def override_get_db():
        yield make_fake_db([])

    app.dependency_overrides[get_db] = override_get_db

    payload = {
        "province": "KhôngCó",
        "days": 2,
        "preferences": {
            "interests": [],
            "pace": None,
            "group_type": None,
            "avoid_categories": [],
            "time_preferences": {}
        }
    }

    res = client.post("/itinerary/generate", json=payload)

    assert res.status_code == 404
    assert res.json()["detail"] == "Không tìm thấy địa điểm nào theo tỉnh yêu cầu."

    app.dependency_overrides.clear()
