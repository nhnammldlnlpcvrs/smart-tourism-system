# backend/app/service/hotel/hotel_module.py
import json
import os
import math
import urllib.parse
from app.db.session import SessionLocal
from app.db.models.tourism_model import TourismPlace

DATA_PATH = os.path.join(
    os.path.dirname(__file__),
    "..", "..", "..", "data", "vietnam_hotels.jsonl"
)
DATA_PATH = os.path.abspath(DATA_PATH)

def load_hotels():
    hotels = []
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    raw = json.loads(line)
                    lat = raw.get("latitude")
                    lon = raw.get("longitude")
                    
                    map_link = ""
                    if lat and lon:
                        map_link = f"https://www.google.com/maps?q={lat},{lon}"
                    else:
                        query_str = f"{raw['name']} {raw.get('parentGeo', '')}"
                        encoded_query = urllib.parse.quote(query_str)
                        map_link = f"https://www.google.com/maps/search/?api=1&query={encoded_query}"

                    hotels.append({
                        "id": raw.get("locationId"),
                        "hotel": raw["name"],           
                        "province": raw.get("parentGeo", ""),   
                        "address": raw.get("address", raw.get("parentGeo", "")),
                        "latitude": float(lat) if lat else None,
                        "longitude": float(lon) if lon else None,
                        "link": map_link
                    })
                except: continue
    return hotels

HOTELS = load_hotels()

def haversine(lat1, lon1, lat2, lon2):
    if not lat1 or not lon1 or not lat2 or not lon2:
        return float('inf')
    try:
        R = 6371
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) \
            * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c
    except:
        return float('inf')

def get_hotels_by_province_and_place_id(province: str, place_id: int):
    """
    - province: Tên tỉnh (để lọc sơ bộ).
    - place_id: ID địa điểm du lịch (để lấy toạ độ tâm).
    """
    
    # Kết nối DB lấy tọa độ điểm du lịch
    session = SessionLocal()
    target_lat = None
    target_lon = None
    place_name = ""

    try:
        if place_id:
            place = session.query(TourismPlace).filter(TourismPlace.id == place_id).first()
            if place and place.latitude and place.longitude:
                target_lat = place.latitude
                target_lon = place.longitude
                place_name = place.name
    except Exception as e:
        print(f"Lỗi DB: {e}")
    finally:
        session.close()

    results = []
    prov_norm = province.strip().lower()

    for item in HOTELS:
        # Lọc theo tỉnh trước
        if not item["province"] or item["province"].strip().lower() != prov_norm:
            continue

        if target_lat and target_lon and item["latitude"] and item["longitude"]:
            dist = haversine(item["latitude"], item["longitude"], target_lat, target_lon)
            
            # Lấy khách sạn trong bán kính 10km
            if dist <= 10.0:
                data = item.copy()
                data["description"] = f"Cách {place_name} {dist:.1f}km"
                data["distance"] = dist
                results.append(data)
        
        elif not place_id:
            data = item.copy()
            data["description"] = f"Địa chỉ: {item['address']}"
            data["distance"] = 0
            results.append(data)

    # Sắp xếp gần nhất lên đầu (chỉ khi tìm theo địa điểm)
    if place_id and target_lat:
        results.sort(key=lambda x: x["distance"])

    return results[:5]