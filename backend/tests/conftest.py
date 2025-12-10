# backend/tests/conftest.py
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from app.api.main import app  # Nếu main.py tạo FastAPI app
from app.db.models.tourism_model import TourismPlace


# ====== FIX IMPORT PATH ======
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from app.db.base import Base
from app.api.main import app
from app.db.session import SessionLocal

TEST_DB_URL = "postgresql://postgres:postgres@localhost:5432/smart_tourism_test"


@pytest.fixture(scope="session")
def test_engine():
    engine = create_engine(TEST_DB_URL)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def db_session(test_engine):
    """Transaction rollback để mỗi test có DB sạch"""
    connection = test_engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session, monkeypatch):
    """Override SessionLocal để API dùng DB test"""
    monkeypatch.setattr(SessionLocal, "__call__", lambda self=db_session: db_session)
    return TestClient(app)

# ----------------- Client Fixture -----------------
@pytest.fixture
def client():
    return TestClient(app)

# ----------------- Fake DB Fixture -----------------
@pytest.fixture
def db_tourism_place():
    # Fake object cho test hotels
    return TourismPlace(id=1, name="Điểm Test", province="Hà Nội")

# ----------------- Mock Weather API -----------------
@pytest.fixture
def mock_weather_api(monkeypatch):
    """Mock OpenWeather API cho get_current_weather"""
    monkeypatch.setattr("app.service.weather.weather_module.API_KEY", "fake_key")

    mock_data = {
        "name": "Hà Nội",
        "weather": [{"description": "nhiều mây", "icon": "04d"}],
        "main": {"temp": 25.6, "humidity": 80},
        "wind": {"speed": 3.5}
    }

    async_mock_response = AsyncMock()
    async_mock_response.status_code = 200
    async_mock_response.json.return_value = mock_data

    async_mock_client = AsyncMock()
    async_mock_client.get.return_value = async_mock_response
    async_mock_client.__aenter__.return_value = async_mock_client
    async_mock_client.__aexit__.return_value = None

    patcher = patch("app.service.weather.weather_module.httpx.AsyncClient", return_value=async_mock_client)
    patcher.start()
    yield
    patcher.stop()