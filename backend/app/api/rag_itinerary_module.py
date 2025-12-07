# backend/app/api/rag_itinerary_module.py
from typing import List, Dict, Any, Optional, Union
from fastapi import HTTPException
import threading
import re

from app.db.session import engine
from app.rag_module.rag_pipeline import RAGPipeline
from app.api.llm_module import generate_itinerary_with_gemini
import asyncio

_PIPELINE = {"instance": None, "lock": threading.Lock()}


def get_pipeline(persist_path: str = "app/rag_store", rebuild: bool = False) -> RAGPipeline:
    if _PIPELINE["instance"] is None or rebuild:
        with _PIPELINE["lock"]:
            if _PIPELINE["instance"] is None or rebuild:
                pipeline = RAGPipeline(
                    engine=engine,
                    persist_path=persist_path,
                    rebuild=rebuild
                )

                if not getattr(pipeline, "is_built", False):
                    pipeline.build_from_postgres(["tourism_places"])

                _PIPELINE["instance"] = pipeline

    return _PIPELINE["instance"]


def generate_itinerary_for_request(
    province: str,
    categories: List[str],
    subcategories: List[str],
    places: List[Dict[str, Any]],
    days: int,
    audience: Optional[str],
    start_date: Optional[str],
    end_date: Optional[str],
    budget_per_person: Optional[Union[int, str]],
    top_k: int,
    activities: Optional[List[str]] = None,
    seasonal_event: Optional[str] = None,
    place_tags: Optional[List[str]] = None
):
    pipeline = get_pipeline()

    # Clean budget
    if isinstance(budget_per_person, str):
        cleaned = re.sub(r"[^0-9]", "", budget_per_person)
        budget_per_person = int(cleaned) if cleaned.isdigit() else None

    # MUST HAVE tags
    if not place_tags or len(place_tags) == 0:
        raise HTTPException(status_code=400, detail="Cần ít nhất 1 tag để tạo lịch trình.")

    # Build search query from tags
    search_query = " ".join(place_tags).lower()
    rag_results = pipeline.retrieve(search_query, top_k=top_k)

    # LLM Prompt
    prompt = f"""
Bạn là chuyên gia du lịch Việt Nam.

Người dùng muốn tạo lịch trình tại tỉnh **{province}** trong **{days} ngày**.

Danh sách địa điểm người dùng chọn:
{[p["name"] for p in places]}

Các tags cần ưu tiên:
{place_tags}

Hoạt động người dùng quan tâm:
{activities}

Sự kiện theo mùa:
{seasonal_event}

Gợi ý từ hệ thống (RAG):
{rag_results}

Yêu cầu:
- Tạo lịch trình chi tiết **theo từng ngày**
- Mỗi ngày gồm: sáng / trưa / chiều / tối
- Tối ưu hoá di chuyển gần nhau
- Dựa trên các tags ưu tiên để chọn điểm phù hợp
- Có thể thêm điểm mới nếu hợp lý
- Gợi ý thêm chi phí dự kiến nếu biết budget
"""

    try:
        itinerary_text = asyncio.run(generate_itinerary_with_gemini(prompt))

        return {
            "province": province,
            "days": days,
            "budget_per_person": budget_per_person,
            "itinerary_text": itinerary_text,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM Error: {str(e)}")
