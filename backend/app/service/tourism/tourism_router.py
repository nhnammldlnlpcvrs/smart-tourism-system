# backend/app/service/tourism/tourism_router.py
from fastapi import APIRouter, Query
from fastapi import Body
from .tourism_module import (
    get_all_provinces,
    get_category_tree_by_province,
    get_places_by_subcategories
)

router = APIRouter(prefix="/tourism", tags=["Tourism"])


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
    subcategories: list[str] = Query(...)
):
    """
    Ví dụ gọi API:
    /tourism/places?province=An%20Giang&subcategories=Chùa&subcategories=Di%20tích
    """
    return {
        "province": province,
        "selected_subcategories": subcategories,
        "results": get_places_by_subcategories(province, subcategories)
    }