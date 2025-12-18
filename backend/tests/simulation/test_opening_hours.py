# backend/tests/simulation/test_opening_hours.py
def test_opening_hours(client, base_payload):
    response = client.post("/itinerary/generate", json=base_payload)
    assert response.status_code == 200
    data = response.json()
    itinerary_text = data.get("itinerary", "")

    assert "**Sáng:**" in itinerary_text or "**Trưa:**" in itinerary_text or "**Chiều:**" in itinerary_text or "**Tối:**" in itinerary_text
