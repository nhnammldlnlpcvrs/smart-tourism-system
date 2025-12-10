from fastapi import APIRouter
from app.service.tourism.tourism_module import get_all_provinces
from .food_module import (
    get_main_tags,
    get_foods_by_province_and_tag
)

router = APIRouter(tags=["Foods"])

@router.get("/provinces")
def api_get_provinces():
    return get_all_provinces()

@router.get("/tags/main")
def api_main_tags(province: str):
    return get_main_tags(province)

@router.get("/")
def api_foods(province: str, tag: str):
    return get_foods_by_province_and_tag(province, tag)