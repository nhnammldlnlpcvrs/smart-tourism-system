# backend/app/api/llm_module.py
import os
import asyncio
from dotenv import load_dotenv
import google.generativeai as genai
from typing import Any, Callable, List, Dict

from app.service.weather.weather_module import get_current_weather
from app.service.map.map_module import get_nearby_places, get_distance
from app.service.tourism.tourism_module import get_category_tree_by_province
from app.service.hotel.hotel_module import get_hotels_by_province_and_place_id
from app.service.foods.food_module import get_foods_by_province_and_tag

# --- Init environment ---
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    # Không raise khi import để không làm crash server lúc dev — chỉ in warning.
    print("[WARN] GEMINI_API_KEY not set. Gemini calls will fail until you set the key.")

genai.configure(api_key=API_KEY)


# --- Tools provided to Gemini for tool-calling ---
chat_tools = [
    get_current_weather,
    get_nearby_places,
    get_distance,
    get_category_tree_by_province,
    get_hotels_by_province_and_place_id,
    get_foods_by_province_and_tag,
]


# --- Helper: try multiple model names and return initialized GenerativeModel ---
def _init_model_with_fallback(
    candidate_models: List[str],
    tools: List[Callable] | None = None,
    system_instruction: str = "",
    generation_config: dict | None = None,
):
    """
    Try to create a genai.GenerativeModel with the candidate names in order.
    Returns (model_instance, used_model_name) or (None, None) on failure.
    This avoids import-time crashes if some model names are unsupported.
    """
    for m in candidate_models:
        try:
            kwargs: Dict[str, Any] = {"model_name": m}
            if tools:
                kwargs["tools"] = tools
            if system_instruction:
                kwargs["system_instruction"] = system_instruction
            if generation_config:
                kwargs["generation_config"] = generation_config

            model = genai.GenerativeModel(**kwargs)
            print(f"[INFO] Initialized Gemini model: {m}")
            return model, m
        except Exception as e:
            # don't crash import — try next
            print(f"[WARN] model init failed for {m}: {type(e).__name__}: {e}")
            continue

    print("[ERROR] No available Gemini model could be initialized from candidates.")
    return None, None


# --- Choose safe candidate model names (order matters: prefer newer then fallback) ---
CHAT_MODEL_CANDIDATES = [
    "models/gemini-2.5-flash",
    "models/gemini-1.5-flash",
    "models/gemini-1.5-flash-latest",
    "models/gemini-1.0"  # last resort
]

WRITER_MODEL_CANDIDATES = CHAT_MODEL_CANDIDATES[:]  # same list; can be separated if needed


# --- Initialize chat model (with tool-calling) and writer model (pure generation) ---
chat_model, chat_model_name = _init_model_with_fallback(
    CHAT_MODEL_CANDIDATES,
    tools=chat_tools,
    system_instruction="Bạn là Trợ lý Du lịch Việt Nam. Trả lời ngắn gọn, chính xác. Có thể gọi các tool nếu cần."
)

# CẬP NHẬT: Tối ưu hóa System Instruction cho giọng điệu hệ thống
writer_model, writer_model_name = _init_model_with_fallback(
    WRITER_MODEL_CANDIDATES,
    tools=None,
    system_instruction="Bạn là **Công cụ Tạo Dữ liệu Gợi ý** tự động (AI Suggestion Generator). Nhiệm vụ là tạo ra dữ liệu khách quan, có cấu trúc (ví dụ: Markdown, Bảng). Tuyệt đối **KHÔNG** sử dụng đại từ nhân xưng (tôi, bạn), lời chào, lời tạm biệt, hoặc bất kỳ ngôn ngữ nào mang tính đối thoại hay cảm xúc. Chỉ trả về đầu ra dữ liệu trực tiếp theo yêu cầu."
)

# If models not available, we still keep variables None — code handles it gracefully.
if chat_model is None:
    print("[WARN] chat_model uninitialized: tool-calling will not work until a valid model is available.")
if writer_model is None:
    print("[WARN] writer_model uninitialized: pure generation will not work until a valid model is available.")

# Start chat session only if chat_model exists
chat_session = None
if chat_model:
    try:
        chat_session = chat_model.start_chat(history=[])
    except Exception as e:
        print(f"[WARN] failed to start chat session: {type(e).__name__}: {e}")
        chat_session = None


# Utility: robust text extractor
def _extract_text_from_response(resp) -> str:
    """
    Try to extract textual content from various response shapes returned by google.generativeai.
    Fallbacks: resp.candidates -> parts -> p.text, resp.text, str(resp)
    """
    try:
        # preferred: candidates -> content.parts
        if hasattr(resp, "candidates") and resp.candidates:
            cand = resp.candidates[0]
            if getattr(cand, "content", None) and getattr(cand.content, "parts", None):
                parts = cand.content.parts
                texts = []
                for p in parts:
                    if hasattr(p, "text") and p.text:
                        texts.append(p.text)
                if texts:
                    return "".join(texts).strip()

        # fallback: resp.text (quick accessor)
        if hasattr(resp, "text") and resp.text:
            return resp.text.strip()

        # last resort: try str()
        return str(resp)[:4000]  # limit length
    except Exception as e:
        return f"[extract_error] {type(e).__name__}: {e}"


# Tool-calling handler
async def _run_tool(func: Callable, kwargs: dict):
    """Run a tool function (async or sync) and return result or error dict."""
    try:
        if asyncio.iscoroutinefunction(func):
            return await func(**kwargs)
        else:
            return await asyncio.to_thread(func, **kwargs)
    except Exception as e:
        return {"error": f"{type(e).__name__}: {e}"}


async def handle_tool_calls(response):
    """
    Given a Gemini response that requests tool calls (function_calls),
    execute the tools and return a follow-up message (by sending tool outputs back into the chat.
    Must have a valid chat_session initialized.
    """
    if chat_session is None:
        return {"error": "chat_session not initialized (no chat model available)."}

    tool_results = []
    # function_calls may be list of objects; handle robustly
    calls = getattr(response, "function_calls", None) or []
    for call in calls:
        try:
            name = getattr(call, "name", None) or call.get("name")
            args = getattr(call, "args", None) or call.get("args", {}) or {}
        except Exception:
            name = None
            args = {}

        if not name:
            tool_results.append({"function_response": {"name": None, "response": {"error": "malformed function call"}}})
            continue

        tool_func = globals().get(name)
        if not callable(tool_func):
            # Also try imported tool list by checking chat_tools
            tool_func = next((t for t in chat_tools if getattr(t, "__name__", None) == name), None)

        if not tool_func:
            tool_results.append({"function_response": {"name": name, "response": {"error": "Tool not found"}}})
            continue

        result = await _run_tool(tool_func, args)
        tool_results.append({"function_response": {"name": name, "response": result}})

    # send tool results back to the model to let it synthesize final answer
    try:
        followup = await chat_session.send_message_async(content=tool_results)
        return followup
    except Exception as e:
        return {"error": f"failed to send tool results back to model: {type(e).__name__}: {e}"}


# Public API functions

# 1) Main chatbot with tool-calling
async def ask_gemini(user_prompt: str) -> str:
    """
    Send a user prompt to Gemini (with tool-calling support).
    Returns text response or an error string.
    """
    if chat_model is None or chat_session is None:
        # Trả về thông báo lỗi cấu trúc, không phải câu văn dài
        return "ERROR: ChatModel_Not_Initialized"

    # keep history manageable
    try:
        if len(chat_session.history) > 40:
            chat_session.history = chat_session.history[-20:]
    except Exception:
        pass

    try:
        response = await chat_session.send_message_async(user_prompt)
    except Exception as e:
        return f"[error] failed to send_message_async: {type(e).__name__}: {e}"

    # if model requested tool calls
    try:
        if getattr(response, "function_calls", None):
            response = await handle_tool_calls(response)
            # handle_tool_calls returns a response-like object or dict
            if isinstance(response, dict) and "error" in response:
                return f"TOOL_ERROR: {response['error']}"
    except Exception as e:
        return f"TOOL_CALL_FAILED: {type(e).__name__}: {e}"

    # extract text safely
    return _extract_text_from_response(response)


# 2) Pure generation: create itinerary text (no tool-calling)
async def generate_itinerary_with_gemini(prompt: str) -> str:
    """
    Use writer_model (pure generation) to produce itinerary text from prompt.
    Returns generated text or error message.
    """
    if writer_model is None:
        # Trả về thông báo lỗi cấu trúc
        return "ERROR: WriterModel_Not_Initialized"

    try:
        # Use generate_content_async which returns candidate(s) or text
        response = await writer_model.generate_content_async(prompt)
    except Exception as e:
        return f"GEN_ERROR: generate_content_async failed: {type(e).__name__}: {e}"

    return _extract_text_from_response(response)


# 3) Short smart comment generator (1-2 sentences)
async def generate_smart_comment(city: str, service_type: str) -> str:
    # CẬP NHẬT: Yêu cầu mô hình tạo đầu ra ngắn gọn, không đối thoại.
    prompts = {
        "hotel": f"Tạo một câu tóm tắt, khách quan về dịch vụ khách sạn tại {city}. Ngắn gọn, tối đa 1 câu.",
        "food": f"Tạo một câu tóm tắt, khách quan về các lựa chọn ẩm thực nổi bật tại {city}. Ngắn gọn, tối đa 1 câu.",
        "place": f"Tạo một câu tóm tắt, khách quan giới thiệu các địa điểm du lịch tại {city}. Ngắn gọn, tối đa 1 câu.",
    }
    prompt = prompts.get(service_type, f"Tạo một câu tóm tắt cho điểm đến {city}.")

    return await generate_smart_comment_safe(prompt)


async def generate_smart_comment_safe(prompt: str) -> str:
    txt = await generate_itinerary_with_gemini(prompt)
    
    # CẬP NHẬT: Xử lý lỗi/đầu ra trống bằng thông báo lỗi hệ thống
    if txt.startswith("ERROR:") or txt.startswith("GEN_ERROR:") or txt.strip() == "":
        return f"STATUS: FAILED_TO_GENERATE_COMMENT ({txt.split(': ')[0]})"
    
    # Giữ lại tối đa 2 câu (hoặc phần đầu) để đảm bảo ngắn gọn
    sentences = txt.strip().split(".")
    
    if len(sentences) <= 2:
        return txt.strip()
    
    # Ghép tối đa 2 câu đầu
    return ". ".join(s.strip() for s in sentences[:2]).strip() + "."


# Expose module-level convenience sync wrappers if needed by sync code
def ask_gemini_sync(user_prompt: str, timeout: float = 60.0) -> str:
    """Sync wrapper for ask_gemini (for synchronous endpoints)."""
    return asyncio.run(asyncio.wait_for(ask_gemini(user_prompt), timeout=timeout))


def generate_itinerary_sync(prompt: str, timeout: float = 120.0) -> str:
    """Sync wrapper for generate_itinerary_with_gemini."""
    return asyncio.run(asyncio.wait_for(generate_itinerary_with_gemini(prompt), timeout=timeout))