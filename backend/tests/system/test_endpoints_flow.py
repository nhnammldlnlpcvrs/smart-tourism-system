# backend/tests/system/test_endpoints_flow.py
def _extract_places(payload):
    """
    Hỗ trợ: backend có thể trả list trực tiếp hoặc dict chứa 'results'.
    Trả về list places.
    """
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        # common shapes:
        # {"province": "Hà Nội", "results": [...], "selected_subcategories": []}
        if "results" in payload and isinstance(payload["results"], list):
            return payload["results"]
        # fallback: maybe single place dict
        if "place" in payload and isinstance(payload["place"], list):
            return payload["place"]
    raise AssertionError(f"Không thể extract places từ payload có shape {type(payload)}: {payload}")

def test_full_tourism_flow(client):
    """
    Test hệ thống: provinces → places → foods → hotels → map/nearby
    Các assert linh hoạt để phù hợp với backend hiện tại.
    """

    res = client.get("/tourism/provinces")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, dict), "Expected dict with key 'provinces'"
    assert "provinces" in data
    provinces = set(data["provinces"])
    assert "Hà Nội" in provinces, "Dữ liệu test yêu cầu có 'Hà Nội' trong provinces"

    res = client.get("/tourism/places?province=Hà Nội")
    assert res.status_code == 200
    places_payload = res.json()
    places = _extract_places(places_payload)
    assert isinstance(places, list)
    assert len(places) > 0, "Expected >0 places for Hà Nội"

    res = client.get("/foods/provinces")
    assert res.status_code == 200
    food_provs = res.json()
    assert isinstance(food_provs, list)
    assert "Hà Nội" in food_provs

    res = client.get("/hotels/provinces")
    assert res.status_code == 200
    hotel_provs = res.json()
    assert isinstance(hotel_provs, list)
    assert "Hà Nội" in hotel_provs

    first = places[0]
    lat = first.get("lat") or first.get("latitude")
    lng = first.get("lng") or first.get("longitude")

    if lat is None or lng is None:
        return
    res = client.get(f"/map/nearby?lat={lat}&lng={lng}&radius=2000")
    assert res.status_code == 200
    assert isinstance(res.json(), list)
