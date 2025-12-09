import json
import os
import math
import urllib.parse
from app.db.session import SessionLocal
from app.db.models.tourism_model import TourismPlace

# 1. Cấu hình đường dẫn
DATA_PATH = os.path.join(
    os.path.dirname(__file__),
    "..", "..", "..", "data", "vietnam_hotels.jsonl"
)
DATA_PATH = os.path.abspath(DATA_PATH)

# 2. Load dữ liệu
def load_hotels():
    hotels = []
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    raw = json.loads(line)
                    lat = raw.get("latitude")
                    lon = raw.get("longitude")
                    
                    # Chỉ lấy những khách sạn CÓ TỌA ĐỘ (vì logic mới dựa hoàn toàn vào map)
                    if not lat or not lon:
                        continue

                    map_link = f"https://www.google.com/maps?q={lat},{lon}"

                    hotels.append({
                        "id": raw.get("locationId"),
                        "hotel": raw["name"],           
                        "address": raw.get("address", raw.get("parentGeo", "")),
                        "latitude": float(lat),
                        "longitude": float(lon),
                        "link": map_link
                    })
                except: continue
    return hotels

HOTELS = load_hotels()

# 3. Haversine (Tính khoảng cách)
def haversine(lat1, lon1, lat2, lon2):
    try:
        R = 6371
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c
    except: return float('inf')

# 4. HÀM CHÍNH: TÌM QUANH ĐỊA ĐIỂM (BẮT BUỘC CÓ ID)
def get_hotels_by_province_and_place_id(place_id: int, radius_km: float = 50.0):
    session = SessionLocal()
    target_lat = None
    target_lon = None
    place_name = ""

    try:
        # Lấy toạ độ điểm vui chơi
        place = session.query(TourismPlace).filter(TourismPlace.id == place_id).first()
        if place and place.latitude and place.longitude:
            target_lat = place.latitude
            target_lon = place.longitude
            place_name = place.name
    except Exception as e:
        print(f"Lỗi DB: {e}")
        return []
    finally:
        session.close()

    # Nếu không tìm thấy địa điểm hoặc địa điểm không có toạ độ -> Trả về rỗng luôn
    if not target_lat:
        return []

    results = []

    # Quét toàn bộ khách sạn (Vì máy tính tính toán rất nhanh, quét 5000 cái mất chưa tới 0.01s)
    for item in HOTELS:
        dist = haversine(item["latitude"], item["longitude"], target_lat, target_lon)
        
        if dist <= radius_km:
            data = item.copy()
            data["description"] = f"Cách {place_name} {dist:.1f}km"
            data["distance"] = dist
            results.append(data)

    # Sắp xếp gần nhất lên đầu
    results.sort(key=lambda x: x["distance"])

    return results[:6]