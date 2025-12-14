# backend/tests/test_api/test_llm_module.py
import pytest
import asyncio
from unittest.mock import patch, AsyncMock, MagicMock

from app.api.llm_module import (
    ask_gemini,
    generate_itinerary_with_gemini,
    generate_smart_comment,
)


@pytest.mark.asyncio
async def test_ask_gemini_success():

    fake_resp = MagicMock()
    fake_resp.text = "Kết quả du lịch mẫu."

    mock_session = AsyncMock()
    mock_session.send_message_async.return_value = fake_resp

    with patch("app.api.llm_module.chat_session", mock_session):
        res = await ask_gemini("Xin gợi ý")
        assert res == "Kết quả du lịch mẫu."


@pytest.mark.asyncio
async def test_ask_gemini_not_initialized():
    with patch("app.api.llm_module.chat_model", None), \
         patch("app.api.llm_module.chat_session", None):
        res = await ask_gemini("hello")
        assert res == "ERROR: ChatModel_Not_Initialized"


@pytest.mark.asyncio
async def test_ask_gemini_send_error():

    mock_session = AsyncMock()
    mock_session.send_message_async.side_effect = Exception("network")

    with patch("app.api.llm_module.chat_session", mock_session):
        res = await ask_gemini("hello")

    assert "[error]" in res


@pytest.mark.asyncio
async def test_generate_itinerary_success():
    fake_resp = MagicMock()
    fake_resp.text = "Lịch trình 2 ngày tại Đà Nẵng."

    mock_model = AsyncMock()
    mock_model.generate_content_async.return_value = fake_resp

    with patch("app.api.llm_module.writer_model", mock_model):
        res = await generate_itinerary_with_gemini("Gợi ý lịch trình")
        assert res == "Lịch trình 2 ngày tại Đà Nẵng."


@pytest.mark.asyncio
async def test_generate_itinerary_not_initialized():
    with patch("app.api.llm_module.writer_model", None):
        res = await generate_itinerary_with_gemini("test")
        assert res == "ERROR: WriterModel_Not_Initialized"


@pytest.mark.asyncio
async def test_generate_itinerary_gen_error():
    mock_model = AsyncMock()
    mock_model.generate_content_async.side_effect = Exception("api_fail")

    with patch("app.api.llm_module.writer_model", mock_model):
        res = await generate_itinerary_with_gemini("test")
    
    assert "GEN_ERROR" in res


@pytest.mark.asyncio
async def test_generate_smart_comment_success():

    fake_resp = MagicMock()
    fake_resp.text = "Khách sạn đa dạng, chất lượng tốt."

    mock_model = AsyncMock()
    mock_model.generate_content_async.return_value = fake_resp

    with patch("app.api.llm_module.writer_model", mock_model):
        res = await generate_smart_comment("Hà Nội", "hotel")
    
    assert "Khách sạn" in res


@pytest.mark.asyncio
async def test_generate_smart_comment_failed():

    # writer_model.generate_content_async trả về lỗi
    mock_model = AsyncMock()
    mock_model.generate_content_async.side_effect = Exception("boom")

    with patch("app.api.llm_module.writer_model", mock_model):
        res = await generate_smart_comment("Hà Nội", "hotel")

    assert "FAILED_TO_GENERATE_COMMENT" in res
