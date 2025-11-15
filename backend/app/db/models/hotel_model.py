from sqlalchemy import Column, Integer, Text, Float
from app.db.base import Base

class Hotel(Base):
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True, autoincrement=True)  # locationId
    name = Column(Text, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    parent_geo = Column(Text)       # parentGeo
    parent_geo_id = Column(Integer) # parentGeoId