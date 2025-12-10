# tests/test_main.py
import pytest
from fastapi.testclient import TestClient
from app.api.main import app

client = TestClient(app)


# -------------------------
# 1) Test root & health
# -------------------------

def test_home():
    res = client.get("/")
    assert res.status_code == 200
    assert res.json() == {"message": "API Layer đang hoạt động!"}


def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}


# -------------------------
# 2) Test routers (smoke)
# -------------------------

@pytest.mark.parametrize(
    "path, method, payload",
    [
        ("/tourism/provinces", "GET", None),
        ("/map/nearby?lat=0&lng=0&radius=100", "GET", None),
        ("/weather/current", "POST", {"city": "Hanoi"}),
        ("/foods/provinces", "GET", None),
        ("/hotels/provinces", "GET", None),
    ]
)
def test_router_endpoint_exists(client, path, method, payload):
    """
    Smoke test: endpoint hoạt động (không 404).
    """
    if method == "GET":
        res = client.get(path)
    else:
        res = client.post(path, json=payload)

    assert res.status_code != 404, f"{path} bị 404 — kiểm tra router"
