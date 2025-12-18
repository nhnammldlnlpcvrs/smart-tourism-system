# backend/tests/simulation/test_distance_constraints.py
def test_tag_matching(client, base_payload):
    response = client.post("/itinerary/generate", json=base_payload)
    assert response.status_code == 200
    data = response.json()
    itinerary_text = data.get("itinerary", "")

    assert "- Hoạt động:" in itinerary_text
    assert "- Nổi bật:" in itinerary_text
