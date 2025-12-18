import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.api.main import app

fake_hotels = [
    {"hotel": "Khách sạn A", "latitude": 10.0, "longitude": 20.0, "description": "fake desc", "distance": 1.0},
    {"hotel": "Khách sạn B", "latitude": 11.0, "longitude": 21.0, "description": "fake desc", "distance": 2.0}
]

@pytest.fixture
def client():
    return TestClient(app)

# -------------------------
# TEST 1: province + place_id
# -------------------------
def test_hotels_by_province_and_place_id(client):
    # Patch đúng hàm API đang gọi
    with patch(
        "app.service.hotel.hotel_router.get_hotels_by_province_and_place_id",
        return_value=fake_hotels
    ):
        res = client.get("/hotels/", params={"place_id": 1})

    assert res.status_code == 200
    data = res.json()

    assert isinstance(data, list)
    assert len(data) == 2

    for h in data:
        assert "hotel" in h
        assert "description" in h
        assert "distance" in h
