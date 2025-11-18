from fastapi import APIRouter, Query
from app.service.food_module import get_recommend_foods

# 🔌 Tạo router riêng cho module "Đặc sản Việt Nam"
router = APIRouter(prefix="/food", tags=["Vietnam Foods"])

@router.get("/recommend")
async def recommend_foods(
    province: str = Query(..., description="Tên tỉnh/thành phố, ví dụ: Hà Nội, Quảng Nam, Cần Thơ")
):
    """
    🍽️ API gợi ý đặc sản Việt Nam theo tỉnh/thành phố.
    Ví dụ:
        GET /food/recommend?province=Hà Nội
    """
    result = get_recommend_foods(province)
    return result


@router.get("/list")
async def list_all_foods():
    """
    📋 API liệt kê toàn bộ danh sách đặc sản (từ file JSONL).
    """
    import os, json
    from app.service.food_module import DATA_PATH

    if not os.path.exists(DATA_PATH):
        return {"error": f"Không tìm thấy dữ liệu: {DATA_PATH}"}

    data = []
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                data.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    return {"total_provinces": len(data), "data": data}