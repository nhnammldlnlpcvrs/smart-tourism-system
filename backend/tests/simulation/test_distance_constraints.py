def test_distance_constraints(client, base_payload):
    response = client.post("/itinerary/generate", json=base_payload)
    assert response.status_code == 200

    data = response.json()
    itinerary_text = data.get("itinerary", "")

    # Kiểm tra có ít nhất 2 ngày trong itinerary
    assert "🗓️ **Day 1**" in itinerary_text
    assert "🗓️ **Day 2**" in itinerary_text
