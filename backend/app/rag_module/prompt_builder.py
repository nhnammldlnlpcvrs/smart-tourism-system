# backend/app/rag_module/prompt_builder.py
from typing import List, Dict, Any

def _short_place_line(place: Dict[str, Any]) -> str:
    name = place.get("name", "")
    cat = place.get("category", "")
    subs = ", ".join(place.get("sub_category", [])) if place.get("sub_category") else ""
    dur = place.get("duration_recommend", "")
    price = place.get("price_range", "")
    popular = place.get("popularity_score", "")
    return f"- {name} | {cat} | {subs} | duration: {dur} | price: {price} | popularity: {popular}"

def build_itinerary_prompt(
    province: str,
    selected_categories: List[str],
    selected_subcategories: List[str],
    places: List[Dict[str, Any]],
    retrieved_contexts: List[Dict[str, Any]],
    days: int = 2,
    audience: str = "general",
    start_date: str = None,
    end_date: str = None,
    budget_per_person: str = None
) -> str:
    header = [
        "SYSTEM: You are a travel assistant. Use ONLY data provided in 'RAG DATA'. Do NOT hallucinate.",
        f"Province: {province}",
        f"Audience: {audience}",
        f"Days: {days}"
    ]
    if start_date and end_date:
        header.append(f"Dates: {start_date} -> {end_date}")
    if budget_per_person:
        header.append(f"Budget per person: {budget_per_person}")

    places_block = "\n".join([_short_place_line(p) for p in places])
    context_texts = []
    for i, c in enumerate(retrieved_contexts, 1):
        # each c likely has 'raw' or 'record'
        rec = c.get("raw") if isinstance(c, dict) and "raw" in c else c.get("record", c)
        summary = []
        if isinstance(rec, dict):
            if rec.get("name"): summary.append(f"Name: {rec.get('name')}")
            if rec.get("description"): summary.append(f"Desc: {rec.get('description')[:300]}")
            if rec.get("highlights"): summary.append("Highlights: " + ", ".join(rec.get("highlights", [])))
            if rec.get("duration_recommend"): summary.append(f"Duration: {rec.get('duration_recommend')}")
            if rec.get("price_range"): summary.append(f"Price: {rec.get('price_range')}")
            if rec.get("best_time_to_visit"): summary.append(f"BestTime: {rec.get('best_time_to_visit')}")
            if rec.get("special_for"): summary.append("SpecialFor: " + ", ".join(rec.get("special_for", [])))
            if rec.get("nearby_places"): summary.append("Nearby: " + ", ".join(map(str, rec.get("nearby_places"))))
        context_texts.append(f"---\nDoc {i}:\n" + "\n".join(summary))

    prompt = "\n".join(header) + "\n\n"
    prompt += "USER SELECTED PLACES:\n" + places_block + "\n\n"
    prompt += "RAG DATA (use this only):\n" + "\n\n".join(context_texts) + "\n\n"
    prompt += (
        "TASK: Produce a JSON itinerary according to the schema below. Use ONLY the information in RAG DATA. "
        "Group nearby places together using 'nearby' information. Prioritize high popularity_score. "
        "Estimate cost using price_range fields. If any field missing for a place, state 'Không có dữ liệu'.\n\n"
        "OUTPUT JSON schema:\n"
        '{ "summary": str, "estimated_cost": str, "days": [ { "day": int, "plan": [ { "place": str, "why_visit": str, "recommended_duration": str, "best_time": str, "activities": [], "food": [], "nearby_suggestions": [] } ] } ] , "travel_tips": [] }\n\n'
    )
    return prompt