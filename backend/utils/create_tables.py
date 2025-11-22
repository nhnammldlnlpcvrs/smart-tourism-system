from app.db.base import Base
from app.db.session import engine

from app.db.models.tourism_model import TourismPlace, TourismActivity, TourismTag
from app.db.models.hotel_model import Hotel
from app.db.models.foods_model import Food

Base.metadata.create_all(bind=engine)

print("All tables have been created successfully!")