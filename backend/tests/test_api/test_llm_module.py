import pytest
import asyncio
from unittest.mock import patch, AsyncMock, MagicMock

from app.api.llm_module import (
    ask_gemini,
    generate_itinerary_with_gemini,
    generate_smart_comment,
)


# ---------------------------------------------------------
# 1) ask_gemini — SUCCESS
# ---------------------------------------------------------
@pytest.mark.asyncio
async def test_ask_gemini_success():

    # Fake Gemini response object
    fake_resp = MagicMock()
    fake_resp.text = "Kết quả du lịch mẫu."

    mock_session = AsyncMock()
    mock_session.send_message_async.return_value = fake_resp

    with patch("app.api.llm_module.chat_session", mock_session):
        res = await ask_gemini("Xin gợi ý")
        assert res == "Kết quả du lịch mẫu."


# ---------------------------------------------------------
# 2) ask_gemini — MODEL NOT INITIALIZED
# ---------------------------------------------------------
@pytest.mark.asyncio
async def test_ask_gemini_not_initialized():
    with patch("app.api.llm_module.chat_model", None), \
         patch("app.api.llm_module.chat_session", None):
        res = await ask_gemini("hello")
        assert res == "ERROR: ChatModel_Not_Initialized"


# ---------------------------------------------------------
# 3) ask_gemini — FAILURE ở send_message_async
# ---------------------------------------------------------
@pytest.mark.asyncio
async def test_ask_gemini_send_error():

    mock_session = AsyncMock()
    mock_session.send_message_async.side_effect = Exception("network")

    with patch("app.api.llm_module.chat_session", mock_session):
        res = await ask_gemini("hello")

    assert "[error]" in res


# ---------------------------------------------------------
# 4) generate_itinerary_with_gemini — SUCCESS
# ---------------------------------------------------------
@pytest.mark.asyncio
async def test_generate_itinerary_success():
    fake_resp = MagicMock()
    fake_resp.text = "Lịch trình 2 ngày tại Đà Nẵng."

    mock_model = AsyncMock()
    mock_model.generate_content_async.return_value = fake_resp

    with patch("app.api.llm_module.writer_model", mock_model):
        res = await generate_itinerary_with_gemini("Gợi ý lịch trình")
        assert res == "Lịch trình 2 ngày tại Đà Nẵng."


# ---------------------------------------------------------
# 5) generate_itinerary_with_gemini — MODEL NOT INIT
# ---------------------------------------------------------
@pytest.mark.asyncio
async def test_generate_itinerary_not_initialized():
    with patch("app.api.llm_module.writer_model", None):
        res = await generate_itinerary_with_gemini("test")
        assert res == "ERROR: WriterModel_Not_Initialized"


# ---------------------------------------------------------
# 6) generate_itinerary_with_gemini — EXCEPTION
# ---------------------------------------------------------
@pytest.mark.asyncio
async def test_generate_itinerary_gen_error():
    mock_model = AsyncMock()
    mock_model.generate_content_async.side_effect = Exception("api_fail")

    with patch("app.api.llm_module.writer_model", mock_model):
        res = await generate_itinerary_with_gemini("test")
    
    assert "GEN_ERROR" in res


# ---------------------------------------------------------
# 7) generate_smart_comment — SUCCESS
# ---------------------------------------------------------
@pytest.mark.asyncio
async def test_generate_smart_comment_success():

    fake_resp = MagicMock()
    fake_resp.text = "Khách sạn đa dạng, chất lượng tốt."

    mock_model = AsyncMock()
    mock_model.generate_content_async.return_value = fake_resp

    with patch("app.api.llm_module.writer_model", mock_model):
        res = await generate_smart_comment("Hà Nội", "hotel")
    
    assert "Khách sạn" in res


# ---------------------------------------------------------
# 8) generate_smart_comment — MODEL FAIL → STATUS: FAILED
# ---------------------------------------------------------
@pytest.mark.asyncio
async def test_generate_smart_comment_failed():

    # writer_model.generate_content_async trả về lỗi
    mock_model = AsyncMock()
    mock_model.generate_content_async.side_effect = Exception("boom")

    with patch("app.api.llm_module.writer_model", mock_model):
        res = await generate_smart_comment("Hà Nội", "hotel")

    assert "FAILED_TO_GENERATE_COMMENT" in res
