def _extract_places(payload):
    """
    Như trên: chấp nhận list hoặc dict{'results': [...]}.
    """
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict) and "results" in payload:
        return payload["results"]
    if isinstance(payload, dict) and "places" in payload:
        return payload["places"]
    raise AssertionError(f"Không thể extract places từ payload shape {type(payload)}")

def test_generate_itinerary_full_flow(client):
    """
    Test luồng tạo itinerary từ API thật.
    Thích ứng với backend trả 'itinerary' có thể là list hoặc string.
    """
    places_payload = client.get("/tourism/places?province=Hà Nội").json()
    places = _extract_places(places_payload)
    assert isinstance(places, list) and len(places) > 0

    payload = {
        "province": "Hà Nội",
        "days": 2,
        "preferences": {
            "interests": ["cultural", "nature"],
            "pace": "medium",
            "group_type": "friends",
            "avoid_categories": ["crowded"]
        }
    }

    res = client.post("/itinerary/generate", json=payload)
    assert res.status_code == 200, f"itinerary/generate failed: {res.text}"

    data = res.json()
    assert isinstance(data, dict)
    assert "itinerary" in data
    assert "rag_contexts_used" in data

    itinerary = data["itinerary"]
    # itinerary có thể là list (đã parse) hoặc string (markdown)
    if isinstance(itinerary, list):
        assert len(itinerary) > 0
    elif isinstance(itinerary, str):
        assert itinerary.strip() != "", "Itinerary string rỗng"
    else:
        raise AssertionError(f"Unknown itinerary type: {type(itinerary)}")

    assert isinstance(data["rag_contexts_used"], list)
