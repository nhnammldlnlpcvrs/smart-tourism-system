# db/init_db.py
from app.db.session import engine
from app.db.base import Base
from app.db.models.tourism_model import TourismPlace
from app.db.models.foods_model import VietnamFood
from app.db.models.hotel_model import VietnamHotel

def init_tables():
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")

if __name__ == "__main__":
    init_tables()