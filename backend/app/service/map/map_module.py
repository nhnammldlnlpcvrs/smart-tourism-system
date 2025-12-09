# backend/app/service/map/map_module.py
import httpx
import asyncio

#  Hàm lấy tọa độ từ tên địa điểm (Geocoding)
async def get_location(query: str):
    """
    Lấy tọa độ (lat, lng) từ tên địa điểm bằng Nominatim (OpenStreetMap).
    - query: chuỗi tên địa điểm (VD: 'Ninh Thuận', 'Hà Nội', 'Đà Nẵng')
    - Không cần API key, giới hạn nhẹ (1 request/s).
    """
    try:
        url = f"https://nominatim.openstreetmap.org/search"
        params = {"q": query, "format": "json", "limit": 1}
        headers = {"User-Agent": "TourismAssistant/1.0 (contact@example.com)"}

        async with httpx.AsyncClient() as client:
            res = await client.get(url, params=params, headers=headers)
            data = res.json()

            if not data:
                return None

            return {
                "lat": float(data[0]["lat"]),
                "lng": float(data[0]["lon"]),
                "address": data[0].get("display_name", query)
            }

    except Exception as e:
        print("Lỗi lấy tọa độ (Nominatim):", e)
        return None


# Hàm tạo liên kết mở Google Maps từ lat/lng
def create_map_link(lat: float, lng: float) -> str:
    """
    Tạo link Google Maps từ tọa độ.
    Dù dữ liệu lấy từ OpenStreetMap, vẫn mở trên Google Maps cho dễ xem.
    """
    return f"https://www.google.com/maps?q={lat},{lng}"


#  Hàm tìm địa điểm gần đó (chuyển từ Google sang Overpass API)
async def get_nearby_places(lat: float, lng: float, radius: int = 1000, type: str = "tourism"):
    """
    Tìm các điểm du lịch gần tọa độ sử dụng Overpass API (nguồn dữ liệu OpenStreetMap).
    - lat, lng: tọa độ trung tâm
    - radius: bán kính tìm kiếm (m)
    - type: loại địa điểm (vd: tourism, restaurant, hotel, ...)
    """
    try:
        overpass_url = "https://overpass-api.de/api/interpreter"
        query = f"""
        [out:json];
        (
          node["{type}"](around:{radius},{lat},{lng});
          way["{type}"](around:{radius},{lat},{lng});
          relation["{type}"](around:{radius},{lat},{lng});
        );
        out center;
        """

        async with httpx.AsyncClient() as client:
            res = await client.post(overpass_url, data=query)
            data = res.json()

            places = []
            for el in data.get("elements", []):
                name = el.get("tags", {}).get("name")
                if not name:
                    continue
                center = el.get("center", el)
                lat_p, lon_p = center["lat"], center["lon"]
                places.append({
                    "name": name,
                    "latitude": lat_p,
                    "longitude": lon_p,
                    "address": el.get("tags", {}).get("addr:full", "Không rõ địa chỉ"),
                    "google_maps_link": create_map_link(lat_p, lon_p)
                })

            return {"results": places}

    except Exception as e:
        print(" Lỗi lấy địa điểm gần đó (Overpass):", e)
        return {"results": []}


# Hàm tính khoảng cách (sử dụng Haversine formula)
from math import radians, sin, cos, sqrt, atan2

async def get_distance(origin: str, destination: str):
    """
    Tính khoảng cách giữa 2 địa điểm bằng công thức Haversine.
    Không cần API, chỉ dựa trên lat/lng từ Nominatim.
    """
    try:
        loc1 = await get_location(origin)
        loc2 = await get_location(destination)

        if not loc1 or not loc2:
            return {"error": "Không tìm thấy tọa độ của địa điểm."}

        R = 6371.0  # bán kính Trái Đất (km)

        lat1, lon1 = radians(loc1["lat"]), radians(loc1["lng"])
        lat2, lon2 = radians(loc2["lat"]), radians(loc2["lng"])

        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance_km = R * c

        return {
            "distance_text": f"{distance_km:.2f} km",
            "origin": loc1["address"],
            "destination": loc2["address"]
        }

    except Exception as e:
        print("Lỗi tính khoảng cách:", e)
        return {"error": str(e)}

