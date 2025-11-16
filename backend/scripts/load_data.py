from app.db.base import Base
from app.db.session import engine, SessionLocal
from app.db.models.tourism_model import TourismPlace, TourismActivity, TourismTag
from app.db.models.hotel_model import Hotel
from app.db.models.foods_model import Food

import json
from pathlib import Path

Base.metadata.create_all(bind=engine)

DATA_DIR = Path(__file__).parent.parent / "data"

def load_tourism():
    db = SessionLocal()
    print("=== Start loading tourism data into PostgreSQL ===")
    file_path = DATA_DIR / "vietnam_tourism.jsonl"

    # Xóa dữ liệu cũ
    db.query(TourismActivity).delete()
    db.query(TourismTag).delete()
    db.query(TourismPlace).delete()
    db.commit()

    places_to_add = []
    activities_to_add = []
    tags_to_add = []

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            item = json.loads(line)
            place = TourismPlace(
                name=item.get("name"),
                type=item.get("type"),
                province=item.get("province"),
                description=item.get("description"),
                best_time_to_visit=item.get("best_time_to_visit")
            )
            db.add(place)
            db.flush()  # tạo id tạm để dùng cho child records

            for act in item.get("activities", []):
                activities_to_add.append(TourismActivity(tourism_id=place.id, activity=act))

            for tag in item.get("tags", []):
                tags_to_add.append(TourismTag(tourism_id=place.id, tag=tag))

    db.bulk_save_objects(activities_to_add)
    db.bulk_save_objects(tags_to_add)
    db.commit()
    db.close()
    print("Tourism data loaded.")


def load_hotels():
    db = SessionLocal()
    print("=== Start loading hotels data into PostgreSQL ===")
    file_path = DATA_DIR / "vietnam_hotel.jsonl"

    db.query(Hotel).delete()
    db.commit()

    hotels_to_add = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            item = json.loads(line)

            latitude = float(item.get("latitude")) if item.get("latitude") not in (None, "") else None
            longitude = float(item.get("longitude")) if item.get("longitude") not in (None, "") else None
            parent_geo_id = int(item.get("parentGeoId")) if item.get("parentGeoId") not in (None, "") else None

            hotel = Hotel(
                name=item.get("name"),
                latitude=latitude,
                longitude=longitude,
                parent_geo=item.get("parentGeo"),
                parent_geo_id=parent_geo_id
            )
            hotels_to_add.append(hotel)

    db.bulk_save_objects(hotels_to_add)
    db.commit()
    db.close()
    print("Hotels data loaded.")


def load_foods():
    db = SessionLocal()
    print("=== Start loading foods data into PostgreSQL ===")
    file_path = DATA_DIR / "vietnam_foods.jsonl"

    db.query(Food).delete()
    db.commit()

    foods_to_add = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            item = json.loads(line)
            food = Food(
                province=item.get("province"),
                name=item.get("food"),
                description=item.get("description")
            )
            foods_to_add.append(food)

    db.bulk_save_objects(foods_to_add)
    db.commit()
    db.close()
    print("Foods data loaded.")


if __name__ == "__main__":
    print("=== Start loading data into PostgreSQL ===")
    load_tourism()
    load_hotels()
    load_foods()
    print("All data loaded successfully!")
