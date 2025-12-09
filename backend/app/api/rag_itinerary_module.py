# backend/app/api/rag_itinerary_module.py

from typing import List, Dict, Any
from app.rag_module.rag_pipeline import RAGPipeline
from app.db.session import engine
import threading

_PIPELINE = {"instance": None, "lock": threading.Lock()}


def get_pipeline():
    if _PIPELINE["instance"] is None:
        with _PIPELINE["lock"]:
            _PIPELINE["instance"] = RAGPipeline(
                engine=engine,
                persist_path="app/rag_store"
            )
            if not _PIPELINE["instance"].is_built:
                _PIPELINE["instance"].build_from_postgres(["tourism_places"])
    return _PIPELINE["instance"]


def generate_itinerary_rag(
    province: str,
    days: int,
    preferences: Dict,
    places: List[Dict[str, Any]]
):

    pipeline = get_pipeline()

    # --- Query RAG ---
    query = f"""
    Tạo lịch trình du lịch {days} ngày tại {province}.
    Ưu tiên loại hình: {preferences.get('interests')}.
    Nhịp độ: {preferences.get('pace')}.
    Nhóm khách: {preferences.get('group_type')}.
    Tránh: {preferences.get('avoid_categories')}.
    """

    contexts = pipeline.search(query=query, top_k=10)

    # Lấy khoảng 4 điểm/ngày
    selected = places[: days * 4]

    itinerary_lines = []

    for d in range(1, days + 1):
        itinerary_lines.append(f"🗓️ **Day {d}**")

        idx = (d - 1) * 4

        # Morning
        if idx < len(selected):
            p = selected[idx]
            itinerary_lines.append(f"**Sáng:** {p['name']}")
            itinerary_lines.append(f"- Hoạt động: {', '.join(p.get('activities', []))}")
            itinerary_lines.append(f"- Gợi ý: {p.get('weather_notes')}\n")

        # Noon
        if idx + 1 < len(selected):
            p = selected[idx + 1]
            itinerary_lines.append(f"**Trưa:** {p['name']}")
            itinerary_lines.append(f"- Nổi bật: {', '.join(p.get('highlights', []))}\n")

        # Afternoon
        if idx + 2 < len(selected):
            p = selected[idx + 2]
            itinerary_lines.append(f"**Chiều:** {p['name']}")
            itinerary_lines.append(f"- Thời gian gợi ý: {p.get('duration_recommend')}\n")

        # Evening
        if idx + 3 < len(selected):
            p = selected[idx + 3]
            itinerary_lines.append(f"**Tối:** {p['name']}\n")

        itinerary_lines.append("")

    return {
        "province": province,
        "days": days,
        "itinerary": "\n".join(itinerary_lines),
        "rag_contexts_used": contexts
    }