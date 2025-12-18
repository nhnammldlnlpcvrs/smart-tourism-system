# backend/tests/test_service/test_map.py
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock, MagicMock
from app.api.main import app

client = TestClient(app)


# -------------------------
# HELPERS để tạo mock client
# -------------------------
def make_mock_async_client_for_post(fake_json):
    """
    Trả về một mock AsyncClient dùng được trong 'async with',
    .post(...) trả về response-like object whose .json() returns fake_json (synchronously).
    """
    # response object: .json() is synchronous in real httpx.Response
    mock_response = MagicMock()
    mock_response.json.return_value = fake_json

    # client instance used in context manager
    mock_client = AsyncMock()
    # ensure async context manager returns this instance
    mock_client.__aenter__.return_value = mock_client
    mock_client.__aexit__.return_value = None

    # client.post is awaitable and returns the mock_response
    mock_client.post = AsyncMock(return_value=mock_response)
    return mock_client


def make_mock_async_client_for_get(json_sequence):
    """
    Trả về mock AsyncClient cho các gọi .get(...) trong get_location.
    json_sequence: list of return values (for successive .json() calls).
    """
    mock_response = MagicMock()
    # .json() should be synchronous and produce values in sequence
    # we implement by popping from list each call
    seq = list(json_sequence)

    def json_side_effect():
        if not seq:
            return []
        return seq.pop(0)

    mock_response.json.side_effect = json_side_effect

    mock_client = AsyncMock()
    mock_client.__aenter__.return_value = mock_client
    mock_client.__aexit__.return_value = None

    mock_client.get = AsyncMock(return_value=mock_response)
    return mock_client


# ==================================================
# TEST /map/nearby
# ==================================================
def test_map_nearby_success():
    fake_osm_response = {
        "elements": [
            {
                "tags": {"name": "Hồ Tây"},
                "center": {"lat": 21.05, "lon": 105.82},
            }
        ]
    }

    mock_client = make_mock_async_client_for_post(fake_osm_response)

    # patch AsyncClient used inside app.service.map.map_module
    with patch("app.service.map.map_module.httpx.AsyncClient", return_value=mock_client):
        res = client.get("/map/nearby?lat=21.0&lng=105.8&radius=500")

    assert res.status_code == 200
    data = res.json()

    assert "results" in data
    assert len(data["results"]) == 1
    assert data["results"][0]["name"] == "Hồ Tây"
    # numeric values preserved from mock center
    assert data["results"][0]["latitude"] == 21.05
    assert data["results"][0]["longitude"] == 105.82


def test_map_nearby_empty_results():
    mock_client = make_mock_async_client_for_post({"elements": []})

    with patch("app.service.map.map_module.httpx.AsyncClient", return_value=mock_client):
        res = client.get("/map/nearby?lat=0&lng=0&radius=500")

    assert res.status_code == 200
    assert res.json() == {"results": []}


# ==================================================
# TEST /map/distance
# ==================================================
def test_map_distance_success():
    # Nominatim returns JSON arrays with dicts containing lat, lon, display_name
    fake_loc_hanoi = [{"lat": "21.0278", "lon": "105.8342", "display_name": "Hanoi"}]
    fake_loc_danang = [{"lat": "16.0544", "lon": "108.2022", "display_name": "Da Nang"}]

    mock_client = make_mock_async_client_for_get([fake_loc_hanoi, fake_loc_danang])

    with patch("app.service.map.map_module.httpx.AsyncClient", return_value=mock_client):
        res = client.get("/map/distance?origin=Hanoi&destination=Da Nang")

    assert res.status_code == 200
    data = res.json()

    assert "distance_text" in data
    assert data["origin"] == "Hanoi"
    assert data["destination"] == "Da Nang"


def test_map_distance_not_found():
    # Both calls return empty list -> error path
    mock_client = make_mock_async_client_for_get([[], []])

    with patch("app.service.map.map_module.httpx.AsyncClient", return_value=mock_client):
        res = client.get("/map/distance?origin=XXX&destination=YYY")

    assert res.status_code == 200
    data = res.json()
    assert "error" in data
    assert data["error"] == "Không tìm thấy tọa độ của địa điểm."
