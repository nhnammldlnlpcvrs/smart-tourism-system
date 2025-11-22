from sqlalchemy import text
from .session import engine
from .base import Base

# Import models
from .models.tourism_model import (
    TourismPlace, TourismActivity, TourismFood, TourismTag
)
from .models.hotel_model import Hotel
from .models.foods_model import Food


def init_db():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created!")


def test_connection():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("PostgreSQL connected successfully!")
    except Exception as e:
        print("Connection failed:", e)


if __name__ == "__main__":
    test_connection()
    init_db()