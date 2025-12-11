def test_tag_matching(client, base_payload):
    response = client.post("/itinerary/generate", json=base_payload)
    assert response.status_code == 200
    data = response.json()
    itinerary_text = data.get("itinerary", "")

    # Kiểm tra ít nhất có một hoạt động gợi ý
    assert "- Hoạt động:" in itinerary_text
    # Kiểm tra ít nhất có một highlight
    assert "- Nổi bật:" in itinerary_text
