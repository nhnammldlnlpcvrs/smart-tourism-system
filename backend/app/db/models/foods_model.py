# models/foods_model.py
from sqlalchemy import Column, Integer, Text, ARRAY
from app.db.base import Base

class VietnamFood(Base):
    __tablename__ = "vietnam_foods"

    id = Column(Integer, primary_key=True)
    province = Column(Text)
    food = Column(Text)
    description = Column(Text)
    tags = Column(ARRAY(Text))
