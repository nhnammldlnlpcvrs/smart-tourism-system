import pytest
from fastapi.testclient import TestClient
from app.api.main import app

client = TestClient(app)

# Giả lập dữ liệu sample nếu cần
@pytest.fixture
def sample_food_data(monkeypatch):
    # Dữ liệu mẫu
    data = [
        {"id": 1, "food": "Phở Hà Nội", "province": "Hà Nội", "tags": ["nước", "truyền thống"], "description": "Món ăn truyền thống", "image_url": None},
        {"id": 2, "food": "Bánh mì", "province": "TP.HCM", "tags": ["ăn sáng"], "description": "Món ăn sáng phổ biến", "image_url": None},
        {"id": 3, "food": "Gỏi Cuốn", "province": "Hà Nội", "tags": ["ăn nhẹ"], "description": "Món ăn nhẹ", "image_url": None}
    ]
    # Patch FOODS trong food_module
    from app.service.foods import food_module
    monkeypatch.setattr(food_module, "FOODS", data)
    return data

def test_foods_provinces(client, sample_food_data):
    res = client.get("/foods/provinces")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert "An Giang" in data
    assert "Bình Dương" in data


def test_main_tags(client, sample_food_data):
    province = "Hà Nội"
    res = client.get(f"/foods/tags/main?province={province}")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    # Tags phải có ít nhất một trong các tag của Hà Nội
    tags_hn = [tag for item in sample_food_data if item["province"] == province for tag in item["tags"]]
    assert any(tag in data for tag in tags_hn)

def test_foods_by_province_and_tag(client, sample_food_data):
    province = "Hà Nội"
    tag = "truyền thống"
    res = client.get(f"/foods/?province={province}&tag={tag}")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    # Mỗi phần tử phải là dict có các key cơ bản
    for item in data:
        assert "id" in item
        assert "food" in item
        assert "description" in item
        assert tag in [t for f in sample_food_data if f["id"] == item["id"] for t in f["tags"]]
