# db/init_db.py
from session import engine
from base import Base
from models.tourism_model import TourismPlace
from models.foods_model import VietnamFood
from models.hotel_model import VietnamHotel

def init_tables():
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")

if __name__ == "__main__":
    init_tables()