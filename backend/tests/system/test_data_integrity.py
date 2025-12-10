import json

def test_data_integrity_tourism_matches_api(client):
    """
    Kiểm tra JSONL ↔ API: API phải chứa tất cả province xuất hiện trong JSONL.
    (API thực tế trả {"provinces": [...]})
    """
    jsonl_path = "data/vietnam_tourism.jsonl"

    provinces_jsonl = set()
    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            obj = json.loads(line)
            provinces_jsonl.add(obj["province"])

    res = client.get("/tourism/provinces")
    assert res.status_code == 200

    data = res.json()
    assert isinstance(data, dict), f"/tourism/provinces expected dict but got {type(data)}"
    assert "provinces" in data, "/tourism/provinces missing key 'provinces'"

    provinces_api = set(data["provinces"])
    missing = provinces_jsonl - provinces_api
    assert not missing, f"API thiếu các provinces sau: {sorted(missing)}"
