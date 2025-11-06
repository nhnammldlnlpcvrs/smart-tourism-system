import httpx
import os

# 🔑 Lấy key Google Maps từ biến môi trường
GOOGLE_MAPS_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

def create_map_link(place_id: str, place_name: str) -> str:
    """
    Tạo liên kết Google Maps từ place_id.
    Google khuyến nghị dùng place_id vì chính xác và luôn đúng vị trí.
    
    encoded_name -> giúp hiển thị tiêu đề địa điểm khi mở Maps
    query_place_id -> xác định chính xác địa điểm
    """
    encoded_name = place_name.replace(" ", "+")  # mã hóa ký tự khoảng trắng thành '+'
    return f"https://www.google.com/maps/search/?api=1&query={encoded_name}&query_place_id={place_id}"

# 🗺️ API lấy danh sách địa điểm gần đó
async def get_nearby_places(lat: float, lng: float, radius: int):
    """
    Gọi Google Places API Nearby Search.
    - lat,lng: tọa độ trung tâm tìm kiếm
    - radius: bán kính tìm kiếm (m)
    - language: 'vi' -> trả về dữ liệu tiếng Việt
    
    Sau khi lấy dữ liệu, thêm trường google_maps_link dùng để hiển thị cho người dùng.
    """
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "key": GOOGLE_MAPS_KEY,
        "location": f"{lat},{lng}",
        "radius": radius,
        "language": "vi"
    }

    async with httpx.AsyncClient() as client:
        res = await client.get(url, params=params)
        data = res.json()

        # ✅ Kiểm tra và chèn link Google Maps vào mỗi địa điểm
        if 'results' in data:
            for place in data['results']:
                place_id = place.get('place_id')
                place_name = place.get('name', 'Địa điểm')  # fallback nếu không có name
                if place_id:
                    place['google_maps_link'] = create_map_link(place_id, place_name)

        return data


# 🚗 API tính khoảng cách và thời gian di chuyển
async def get_distance(origin: str, destination: str):
    """
    Gọi Google Directions API.
    - origin: điểm bắt đầu (VD: 'Hanoi')
    - destination: điểm đến (VD: 'Da Nang')
    
    Trả về JSON chứa:
        distance -> quãng đường
        duration -> thời gian di chuyển
    """
    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "key": GOOGLE_MAPS_KEY,
        "origin": origin,
        "destination": destination,
        "language": "vi"
    }

    async with httpx.AsyncClient() as client:
        res = await client.get(url, params=params)
        return res.json()
