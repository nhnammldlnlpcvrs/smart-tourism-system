# utils/create_tables.py
import json
import os
import re
from app.db.session import SessionLocal
from app.db.models.tourism_model import TourismPlace
from app.db.models.foods_model import VietnamFood
from app.db.models.hotel_model import VietnamHotel


def load_jsonl(file_path):
    """
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File không tồn tại: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    if not content:
        return

    if content.startswith("["):
        try:
            data = json.loads(content)
            for row in data:
                yield row
        except json.JSONDecodeError as e:
            raise ValueError(f"Không parse được JSON array trong {file_path}: {e}")
    else:
        pattern = r'\{.*?\}'
        for match in re.finditer(pattern, content):
            try:
                yield json.loads(match.group())
            except json.JSONDecodeError as e:
                print(f"Lỗi parse 1 object JSON trong {file_path}: {e}")


def load_tourism(file_path):
    db = SessionLocal()
    count = 0
    try:
        for row in load_jsonl(file_path):
            try:
                obj = TourismPlace(**row)
                db.add(obj)
                count += 1
            except Exception as e:
                print(f"Lỗi parse tourism row {row.get('id')}: {e}")
        db.commit()
        print(f"Đã load {count} tourism places từ {file_path}")
    finally:
        db.close()


def load_foods(file_path):
    db = SessionLocal()
    count = 0
    try:
        for row in load_jsonl(file_path):
            try:
                obj = VietnamFood(**row)
                db.add(obj)
                count += 1
            except Exception as e:
                print(f"Lỗi parse foods row ID {row.get('id')}: {e}")
        db.commit()
        print(f"Đã load {count} món ăn từ {file_path}")
    finally:
        db.close()


def load_hotels(file_path):
    db = SessionLocal()
    count = 0
    try:
        for row in load_jsonl(file_path):
            try:
                obj = VietnamHotel(**row)
                db.add(obj)
                count += 1
            except Exception as e:
                print(f"Lỗi parse hotels row locationId {row.get('locationId')}: {e}")
        db.commit()
        print(f"Đã load {count} khách sạn từ {file_path}")
    finally:
        db.close()


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_dir = os.path.join(base_dir, "data")

    load_tourism(os.path.join(data_dir, "vietnam_tourism.jsonl"))
    load_foods(os.path.join(data_dir, "vietnam_foods.jsonl"))
    load_hotels(os.path.join(data_dir, "vietnam_hotels.jsonl"))