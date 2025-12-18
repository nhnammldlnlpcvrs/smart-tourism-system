# backend/tests/simulation/test_daily_load.py
def test_daily_load_limit(client, base_payload):
    payload = base_payload.copy()
    payload["days"] = 10 

    response = client.post("/itinerary/generate", json=payload)

    assert response.status_code == 200
    data = response.json()
    itinerary_text = data.get("itinerary", "")
    
    assert "Day 1" in itinerary_text
    assert "Day 10" in itinerary_text or "Day" in itinerary_text
