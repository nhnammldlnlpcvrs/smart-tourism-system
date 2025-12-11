# tests/simulation/end_to_end.py

from fastapi.testclient import TestClient
from app.api.main import app

client = TestClient(app)

def run_simulation(
    province: str = "Hà Nội",
    tags: list[str] = None,
    start_time: str = "08:00",
    end_time: str = "20:00",
    max_distance_km: float = 10,
):
    """
    Hàm mô phỏng end-to-end để các test khác import.
    Tương thích với việc test gọi run_simulation() không có tham số.
    """
    payload = {
        "province": province,
        "tags": tags or [],
        "start_time": start_time,
        "end_time": end_time,
        "max_distance_km": max_distance_km,
    }

    response = client.post("/simulation/run", json=payload)
    assert response.status_code == 200, response.text
    return response.json()
