import json

def test_end_to_end_basic(client):
    with open("tests/simulation/scenario_inputs/hanoi_weekend.json") as f:
        scenario = json.load(f)

    # bắt buộc có province và days
    scenario.setdefault("province", "Hà Nội")
    scenario.setdefault("days", 2)

    # bắt buộc có preferences hợp lệ
    scenario.setdefault("preferences", {})
    prefs = scenario["preferences"]
    prefs.setdefault("interests", ["Văn hóa", "Ẩm thực"])
    prefs.setdefault("pace", "medium")
    prefs.setdefault("group_type", "family")
    prefs.setdefault("avoid_categories", [])
    prefs.setdefault("time_preferences", {"morning": [], "afternoon": [], "evening": []})

    response = client.post("/itinerary/generate", json=scenario)
    assert response.status_code == 200
    data = response.json()
    assert "itinerary" in data
