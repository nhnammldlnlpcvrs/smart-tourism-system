# backend/tests/test_api/test_tourism_api.py
def test_tourism_api(client):
    response = client.get("/tourism/provinces")
    assert response.status_code == 200
    data = response.json()

    assert "provinces" in data
    assert isinstance(data["provinces"], list)
