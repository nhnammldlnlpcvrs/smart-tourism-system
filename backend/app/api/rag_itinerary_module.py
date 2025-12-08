# backend/app/api/rag_itinerary_module.py
from typing import List, Dict, Any, Optional, Union
from fastapi import HTTPException
import threading
import re
import math
from collections import Counter

from app.db.session import engine
from app.rag_module.rag_pipeline import RAGPipeline

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


def _normalize_budget(budget_per_person: Optional[Union[int, str]]):
    if isinstance(budget_per_person, str):
        cleaned = re.sub(r"[^0-9]", "", budget_per_person)
        return int(cleaned) if cleaned.isdigit() else None
    return budget_per_person


def _choose_most_common(field_values: List[Any]) -> Optional[Any]:
    if not field_values:
        return None
    cnt = Counter(field_values)
    return cnt.most_common(1)[0][0]


def _enrich_places_with_contexts(selected_places: List[Dict[str, Any]], contexts: List[Dict[str, Any]]):
    """
    Try to match retrieved contexts to selected places by id or name and attach metadata:
    highlights, duration_recommend, price_range, seasonal_events, special_for, popularity_score, nearby_places, activities.
    """
    # Build lookup by id and by normalized name
    by_id = {}
    by_name = {}
    for item in contexts:
        raw = item.get("raw", {})
        if not isinstance(raw, dict):
            continue
        rid = raw.get("id")
        name = raw.get("name")
        if rid is not None:
            by_id[int(rid)] = raw
        if isinstance(name, str):
            by_name[name.strip().lower()] = raw

    enriched = []
    for p in selected_places:
        meta = {
            "id": p.get("id"),
            "name": p.get("name"),
            "address": p.get("address"),
            "latitude": p.get("latitude"),
            "longitude": p.get("longitude"),
            "category": p.get("category"),
            "sub_category": p.get("sub_category"),
            # defaults
            "highlights": [],
            "duration_recommend": None,
            "price_range": None,
            "seasonal_events": [],
            "special_for": [],
            "nearby_places": [],
            "activities": [],
            "popularity_score": 0.0
        }

        matched = None
        try:
            if meta["id"] is not None and int(meta["id"]) in by_id:
                matched = by_id[int(meta["id"])]
            else:
                n = meta["name"]
                if isinstance(n, str) and n.strip().lower() in by_name:
                    matched = by_name[n.strip().lower()]
        except Exception:
            matched = None

        if matched:
            # copy known fields if present
            if matched.get("highlights"):
                meta["highlights"] = matched.get("highlights") if isinstance(matched.get("highlights"), list) else [matched.get("highlights")]
            if matched.get("duration_recommend"):
                meta["duration_recommend"] = matched.get("duration_recommend")
            if matched.get("price_range"):
                meta["price_range"] = matched.get("price_range")
            if matched.get("seasonal_events"):
                meta["seasonal_events"] = matched.get("seasonal_events") if isinstance(matched.get("seasonal_events"), list) else [matched.get("seasonal_events")]
            if matched.get("special_for"):
                meta["special_for"] = matched.get("special_for") if isinstance(matched.get("special_for"), list) else [matched.get("special_for")]
            if matched.get("nearby_places"):
                meta["nearby_places"] = matched.get("nearby_places") if isinstance(matched.get("nearby_places"), list) else [matched.get("nearby_places")]
            if matched.get("activities"):
                meta["activities"] = matched.get("activities") if isinstance(matched.get("activities"), list) else [matched.get("activities")]
            if matched.get("popularity_score") is not None:
                try:
                    meta["popularity_score"] = float(matched.get("popularity_score"))
                except Exception:
                    pass

        enriched.append(meta)
    return enriched


def _assign_places_to_days(enriched_places: List[Dict[str, Any]], days: int):
    """
    Simple assignment strategy:
    - sort places by popularity_score desc (so best / most relevant first)
    - try to keep nearby places together by naive sequential grouping using nearby_places lists
    - assign roughly ceil(n / days) places per day
    """
    if days <= 0:
        raise HTTPException(status_code=400, detail="Số ngày phải lớn hơn 0.")

    n = len(enriched_places)
    per_day = max(1, math.ceil(n / days))

    # sort by popularity_score desc
    enriched_places = sorted(enriched_places, key=lambda x: x.get("popularity_score", 0.0), reverse=True)

    # naive grouping: keep the sorted order, then chunk
    schedule = []
    idx = 0
    for d in range(1, days + 1):
        chunk = enriched_places[idx: idx + per_day]
        if not chunk and idx < n:
            chunk = [enriched_places[idx]]
        idx += per_day
        schedule.append({
            "day": d,
            "places": chunk
        })
        if idx >= n:
            # fill remaining days with empty lists if any
            for dd in range(d + 1, days + 1):
                schedule.append({"day": dd, "places": []})
            break

    return schedule


def _format_text_from_schedule(province: str, start_date: Optional[str], schedule: List[Dict[str, Any]]):
    """
    Build a readable itinerary_text from schedule.
    Each day: list places with highlights, activities, duration.
    """
    lines = []
    header = f"Lịch trình tại {province}"
    if start_date:
        header += f" - bắt đầu {start_date}"
    lines.append(header)
    lines.append("")

    for day_block in schedule:
        day = day_block["day"]
        lines.append(f"Ngày {day}:")
        if not day_block["places"]:
            lines.append("  - (Không có địa điểm được phân bổ)")
            lines.append("")
            continue

        for p in day_block["places"]:
            lines.append(f"{p.get('name')}")
            if p.get("activities"):
                lines.append(f"- Hoạt động: {', '.join(p.get('activities'))}")
            if p.get("duration_recommend"):
                lines.append(f"- Thời lượng gợi ý: {p.get('duration_recommend')}")
            if p.get("highlights"):
                hl = p.get("highlights")
                lines.append(f"- Highlights: {', '.join(hl)}")
            if p.get("price_range"):
                lines.append(f"- Giá tham khảo: {p.get('price_range')}")
            if p.get("seasonal_events"):
                lines.append(f"- Sự kiện/năm: {', '.join(p.get('seasonal_events'))}")
            if p.get("special_for"):
                lines.append(f"- Phù hợp cho: {', '.join(p.get('special_for'))}")
            lines.append("")  # blank line between places

    return "\n".join(lines)


def generate_itinerary_for_request(
    places: List[Dict[str, Any]],
    days: int,
    start_date: Optional[str],
    end_date: Optional[str],
    top_k: int
):
    pipeline = get_pipeline()

    # RAG search – chỉ lấy context liên quan
    contexts = pipeline.search(
        query=" ".join([p["name"] for p in places]),
        top_k=top_k
    )

    # enrich metadata
    enriched = _enrich_places_with_contexts(places, contexts)

    # phân lịch
    schedule = _assign_places_to_days(enriched, days)

    # format text output
    text = _format_text_from_schedule(
        province="",
        start_date=start_date,
        schedule=schedule
    )

    return {
        "schedule": schedule,
        "text": text
    }