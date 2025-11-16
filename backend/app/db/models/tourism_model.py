from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class TourismPlace(Base):
    __tablename__ = "tourism_places"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    type = Column(Text)
    province = Column(Text)
    description = Column(Text)
    best_time_to_visit = Column(Text)

    # Relationships
    activities = relationship(
        "TourismActivity", back_populates="tourism", cascade="all, delete-orphan"
    )
    foods = relationship(
        "TourismFood", back_populates="tourism", cascade="all, delete-orphan"
    )
    tags = relationship(
        "TourismTag", back_populates="tourism", cascade="all, delete-orphan"
    )


class TourismActivity(Base):
    __tablename__ = "tourism_activities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tourism_id = Column(Integer, ForeignKey("tourism_places.id"), nullable=False)
    activity = Column(Text, nullable=False)

    tourism = relationship("TourismPlace", back_populates="activities")


class TourismFood(Base):
    __tablename__ = "tourism_foods"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tourism_id = Column(Integer, ForeignKey("tourism_places.id"), nullable=False)
    food = Column(Text, nullable=False)

    tourism = relationship("TourismPlace", back_populates="foods")


class TourismTag(Base):
    __tablename__ = "tourism_tags"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tourism_id = Column(Integer, ForeignKey("tourism_places.id"), nullable=False)
    tag = Column(Text, nullable=False)

    tourism = relationship("TourismPlace", back_populates="tags")