# backend/app/db/init_db.py
from backend.app.db.session import engine
from backend.app.db.base import Base
from backend.app.db.models.tourism_model import TourismPlace
from backend.app.db.models.foods_model import VietnamFood
from backend.app.db.models.hotel_model import VietnamHotel

def init_tables():
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")

if __name__ == "__main__":
    init_tables()