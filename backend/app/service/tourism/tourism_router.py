# backend/app/service/tourism/tourism_router.py
from fastapi import APIRouter, Query
from typing import Optional
from .tourism_module import (
    get_all_provinces,
    get_category_tree_by_province,
    get_places_by_subcategories
)

router = APIRouter()


@router.get("/provinces")
def api_get_provinces():
    return {
        "provinces": get_all_provinces()
    }


@router.get("/categories")
def api_get_categories(province: str):
    return {
        "province": province,
        "categories": get_category_tree_by_province(province)
    }


@router.get("/places")
def api_get_places(
    province: str,
    subcategories: Optional[list[str]] = Query(None)  
):
    """
    Ví dụ gọi API:
    /tourism/places?province=An%20Giang&subcategories=Chùa&subcategories=Di%20tích
    """
    if not subcategories:
        # Nếu không có subcategories, lấy tất cả địa điểm
        results = get_places_by_subcategories(province, [])
    else:
        results = get_places_by_subcategories(province, subcategories)
    
    return {
        "province": province,
        "selected_subcategories": subcategories or [],
        "results": results
    }