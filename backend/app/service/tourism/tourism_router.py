from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.db.models.tourism_model import TourismPlace
from .tourism_module import get_category_tree_by_province

router = APIRouter(prefix="/tourism", tags=["Tourism"])


# ----------------------
# Tạo DB Session
# ----------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ----------------------
# 1) API trả về tags + category
# ----------------------
@router.get("/tags")
def api_get_tags_with_categories(province: str):
    return get_category_tree_by_province(province)


# ----------------------
# 2) API lấy địa điểm theo tên tỉnh (ĐƠN GIẢN)
# ----------------------
@router.get("/by-province/{province}")
def get_places_by_province(province: str, db: Session = Depends(get_db)):
    """
    Lấy địa điểm theo tỉnh - đơn giản, tìm chính xác hoặc gần đúng
    """
    # Thử tìm chính xác trước
    exact_results = db.query(TourismPlace).filter(
        TourismPlace.province == province
    ).all()
    
    if exact_results:
        print(f"[API] Found {len(exact_results)} exact matches for '{province}'")
        return exact_results
    
    # Nếu không tìm thấy chính xác, tìm gần đúng
    print(f"[API] No exact matches for '{province}', trying ilike search...")
    results = db.query(TourismPlace).filter(
        TourismPlace.province.ilike(f"%{province}%")
    ).all()
    
    print(f"[API] Found {len(results)} partial matches")
    return results


# ----------------------
# 3) API lấy chi tiết 1 địa điểm theo ID
# ----------------------
@router.get("/{place_id}")
def get_place_detail(place_id: int, db: Session = Depends(get_db)):
    result = (
        db.query(TourismPlace)
        .filter(TourismPlace.id == place_id)
        .first()
    )
    
    if not result:
        raise HTTPException(status_code=404, detail="Place not found")
    
    return result