# models/tourism_model.py
from sqlalchemy import Column, Integer, Float, Text, ARRAY
from ..base import Base

class TourismPlace(Base):
    __tablename__ = "tourism_places"

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    province = Column(Text)
    category = Column(Text)
    sub_category = Column(ARRAY(Text))
    type = Column(Text)
    description = Column(Text)
    highlights = Column(ARRAY(Text))
    address = Column(Text)
    latitude = Column(Float)
    longitude = Column(Float)
    image_url = Column(Text)
    price_range = Column(Text)
    open_hours = Column(Text)
    duration_recommend = Column(Text)
    activities = Column(ARRAY(Text))
    food = Column(ARRAY(Text))
    best_time_to_visit = Column(Text)
    seasonal_events = Column(ARRAY(Text))
    tags = Column(ARRAY(Text))
    rating = Column(Float)
    review_count = Column(Integer)
    popularity_score = Column(Float)
    special_for = Column(ARRAY(Text))
    weather_notes = Column(Text)
    nearby_places = Column(ARRAY(Integer))
