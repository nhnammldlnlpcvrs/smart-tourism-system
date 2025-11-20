from fastapi import APIRouter
from app.service.hotel_module import recommend_hotels

router = APIRouter(prefix="/hotels", tags=["Hotel"])

@router.get("/recommend")
def get_recommended_hotels(lat: float, lon: float, limit: int = 5):
    results = recommend_hotels(lat, lon, limit)
    return {"hotels": results}
