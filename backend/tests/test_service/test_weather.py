import pytest
from unittest.mock import AsyncMock, Mock, patch
import app.service.weather.weather_module as weather_module
from app.service.weather.weather_module import get_current_weather

@pytest.mark.asyncio
async def test_get_weather_success():
    weather_module.API_KEY = "fake_key"

    mock_data = {
        "name": "Hà Nội",
        "weather": [{"description": "nhiều mây", "icon": "04d"}],
        "main": {"temp": 25.6, "humidity": 80},
        "wind": {"speed": 3.5}
    }

    async_mock_client = AsyncMock()
    async_mock_response = AsyncMock()
    async_mock_response.status_code = 200

    # FIX QUAN TRỌNG: response.json là hàm đồng bộ
    async_mock_response.json = Mock(return_value=mock_data)

    async_mock_client.get.return_value = async_mock_response
    async_mock_client.__aenter__.return_value = async_mock_client
    async_mock_client.__aexit__.return_value = None

    with patch("app.service.weather.weather_module.httpx.AsyncClient", return_value=async_mock_client):
        res = await get_current_weather("Hà Nội")

    assert res is not None
    assert res["city"] == "Hà Nội"
    assert res["temp"] == 26
