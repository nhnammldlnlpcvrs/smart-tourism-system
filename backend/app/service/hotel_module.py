import json
import math
import os

DATA_PATH = os.path.join(
    os.path.dirname(__file__),
    "..", "..", "data", "vietnam_hotels.jsonl"
)
DATA_PATH = os.path.abspath(DATA_PATH)

hotels = []

def load_hotels():
    loaded = []
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            try:
                h = json.loads(line.strip())

                # Chuẩn hoá dữ liệu
                h["address"] = h.get("address", h.get("parentGeo", "Việt Nam"))
                h["rating"] = h.get("rating", "Chưa có đánh giá")

                loaded.append(h)
            except json.JSONDecodeError:
                print(f"⚠ Bỏ qua dòng lỗi: {i}")
    return loaded

hotels = load_hotels()

# Tính khoảng cách Haversine
def distance(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return 2 * R * math.asin(math.sqrt(a))

async def recommend_hotels(latitude, longitude, city: str = "", limit=5):
    city = city.lower().strip()

    scored = []
    for h in hotels:
        if city and city not in h.get("parentGeo", "").lower():
            continue

        dist = distance(latitude, longitude, float(h["latitude"]), float(h["longitude"]))
        h["distance"] = round(dist, 1)
        scored.append((dist, h))

    scored.sort(key=lambda x: x[0])
    return [x[1] for x in scored[:limit]]