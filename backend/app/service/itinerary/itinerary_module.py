# backend/app/service/itinerary/itinerary_module.py

from fastapi import HTTPException
from typing import List, Dict, Any
from app.api.rag_itinerary_module import generate_itinerary_rag


def process_itinerary_request(
    province: str,
    days: int,
    preferences: Dict,
    places: List[Dict[str, Any]]
):

    if days <= 0:
        raise HTTPException(status_code=400, detail="Số ngày phải > 0")

    # --- FILTERING LAYER ---
    filtered = [p for p in places if p["province"] == province]

    # 1. Sở thích (interests → match: category/sub_category/activities)
    interests = preferences.get("interests", [])
    if interests:
        filtered = [
            p for p in filtered
            if any(interest.lower() in (
                p["category"] + " " +
                " ".join(p.get("sub_category") or []) + " " +
                " ".join(p.get("activities") or [])
            ).lower()
            for interest in interests)
        ]

    # 2. Phù hợp group_type
    group = preferences.get("group_type")
    if group:
        filtered = [
            p for p in filtered
            if group.lower() in [x.lower() for x in p.get("special_for", [])]
        ]

    # 3. Tránh category/tags
    avoid = preferences.get("avoid_categories", [])
    if avoid:
        filtered = [
            p for p in filtered
            if not any(a.lower() in [t.lower() for t in p.get("tags", [])] for a in avoid)
        ]

    if not filtered:
        filtered = places  # fallback

    # RAG + Itinerary formatter
    return generate_itinerary_rag(
        province=province,
        days=days,
        preferences=preferences,
        places=filtered
    )