# backend/tests/simulation/conftest.py
import pytest
from fastapi.testclient import TestClient
from app.api.main import app

@pytest.fixture(scope="module")
def client():
    return TestClient(app)

@pytest.fixture
def base_payload():
    return {
        "province": "Hà Nội",
        "days": 2,
        "preferences": {
            "interests": ["Văn hóa", "Ẩm thực"],
            "pace": "medium",
            "group_type": "family",
            "avoid_categories": [],
            "time_preferences": {"morning": [], "afternoon": [], "evening": []}
        }
    }
