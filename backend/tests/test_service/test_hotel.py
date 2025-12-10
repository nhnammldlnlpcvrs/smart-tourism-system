# tests/test_service/test_hotel.py
import pytest
from fastapi.testclient import TestClient
from app.api.main import app
from app.db.models.tourism_model import TourismPlace

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def db_tourism_place(db_session):
    """
    Tạo tạm một TourismPlace để test tìm khách sạn theo place_id.
    """
    place = TourismPlace(
        name="Điểm Test",
        province="Hà Nội",
        category="Văn hóa",
        sub_category=["Bảo tàng"],
        type="A",
        description="Mô tả test",
        highlights=["Highlight test"],
        address="Địa chỉ test",
        latitude=21.0285,
        longitude=105.8542,
        image_url="http://example.com/img.png",
        price_range="100-200",
        open_hours="8:00-17:00",
        duration_recommend="2h",
        activities=["Tham quan"],
        food=["Ăn uống"],
        best_time_to_visit="Mùa xuân",
        seasonal_events=["Event test"],
        tags=["culture"],
        rating=4.5,
        review_count=100,
        popularity_score=90.0,
        special_for=["Family"],
        weather_notes="Nắng nhẹ",
        nearby_places=None
    )
    db_session.add(place)
    db_session.commit()
    yield place
    # Cleanup
    db_session.delete(place)
    db_session.commit()


def test_hotels_provinces(client):
    res = client.get("/hotels/provinces")
    assert res.status_code == 200
    # HOTELS được load từ file JSONL, trả về danh sách tỉnh
    provinces = res.json()
    assert isinstance(provinces, list)
    assert len(provinces) > 0
    # Kiểm tra 1 tỉnh phổ biến có trong danh sách
    assert "Hà Nội" in provinces


def test_hotels_by_province_only(client):
    province = "Hà Nội"
    res = client.get(f"/hotels/?province={province}")
    assert res.status_code == 200
    hotels = res.json()
    assert isinstance(hotels, list)
    # Kiểm tra có ít nhất 1 khách sạn trong tỉnh
    assert len(hotels) > 0
    for h in hotels:
        assert "province" in h
        assert h["province"].strip().lower() == province.lower()


def test_hotels_by_province_and_place_id(client, db_tourism_place):
    province = db_tourism_place.province
    place_id = db_tourism_place.id
    res = client.get(f"/hotels/?province={province}&place_id={place_id}")
    assert res.status_code == 200
    hotels = res.json()
    assert isinstance(hotels, list)
    # Kiểm tra khách sạn có description chứa khoảng cách
    for h in hotels:
        assert "description" in h
        assert db_tourism_place.name in h["description"] or "Địa chỉ" in h["description"]
