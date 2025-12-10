import pytest
from app.db.models.tourism_model import TourismPlace

def test_get_provinces(client, db_session):
    # Arrange
    p1 = TourismPlace(
        name="Điểm 1",
        province="Hà Nội",
        category="Văn hóa",
        sub_category=["Bảo tàng"],
        type="A",
        description="...",
        highlights=["..."],
        address="...",
        latitude=1.0,
        longitude=1.0,
        image_url="...",
        open_hours="8:00-18:00",
        duration_recommend="2h",
        activities=["..."],
        food=["..."],
        tags=["culture"],
        best_time_to_visit="...",
        seasonal_events=None,
        rating=4.0,
        review_count=10,
        popularity_score=90.0,
        special_for=None,
        weather_notes=None,
        nearby_places=None,
        price_range=None,
    )

    db_session.add(p1)
    db_session.commit()

    # Act
    res = client.get("/tourism/provinces")
    data = res.json()

    # Assert
    assert res.status_code == 200
    assert "provinces" in data
    assert "Hà Nội" in data["provinces"]
