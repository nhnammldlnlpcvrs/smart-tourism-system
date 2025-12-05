# models/hotel_model.py
from sqlalchemy import Column, BigInteger, Float, Text
from app.db.base import Base

class VietnamHotel(Base):
    __tablename__ = "vietnam_hotels"

    locationId = Column(BigInteger, primary_key=True)
    name = Column(Text)
    latitude = Column(Float)
    longitude = Column(Float)
    parentGeo = Column(Text)
    parentGeoId = Column(BigInteger)
