# backend/app/api/rag_itinerary_module.py
from typing import List, Dict, Any, Optional, Union
from fastapi import HTTPException
import threading
import re

from app.db.session import engine, SessionLocal
from app.rag_module.rag_pipeline import RAGPipeline

# Thread-safe singleton
_PIPELINE = {"instance": None, "lock": threading.Lock()}


def get_pipeline(persist_path: str = "app/rag_store", rebuild: bool = False) -> RAGPipeline:
    """Create/get RAGPipeline singleton."""
    if _PIPELINE["instance"] is None or rebuild:
        with _PIPELINE["lock"]:
            if _PIPELINE["instance"] is None or rebuild:

                pipeline = RAGPipeline(
                    engine=engine,
                    persist_path=persist_path,
                    rebuild=rebuild
                )

                # Build vector database if not ready
                if getattr(pipeline, "store", None) is None or not getattr(pipeline, "is_built", False):
                    pipeline.build_from_postgres(table_names=["tourism_places"])

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
    seasonal_event: Optional[str] = None
):
    """Clean user inputs + call RAG Pipeline safely."""

    pipeline = get_pipeline()

    if activities is None:
        activities = []

    # Normalize budget
    if isinstance(budget_per_person, str):
        cleaned = re.sub(r"[^0-9]", "", budget_per_person)
        budget_per_person = int(cleaned) if cleaned.isdigit() else None

    if days <= 0:
        raise HTTPException(status_code=400, detail="Số ngày phải lớn hơn 0.")

    input_payload = {
        "province": province,
        "selected_categories": categories,
        "selected_subcategories": subcategories,
        "places": places,
        "days": days,
        "audience": audience,
        "activities": activities,
        "seasonal_event": seasonal_event,
        "start_date": start_date,
        "end_date": end_date,
        "budget_per_person": budget_per_person,
        "top_k": top_k,
    }

    try:
        return pipeline.generate_itinerary(**input_payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RAG Pipeline Error: {str(e)}")