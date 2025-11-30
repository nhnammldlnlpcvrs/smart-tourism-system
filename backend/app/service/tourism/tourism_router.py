from fastapi import APIRouter
from .tourism_module import get_category_tree_by_province

router = APIRouter(prefix="/tourism", tags=["Tourism"])

@router.get("/tags")
def api_get_tags_with_categories(province: str):
    return get_category_tree_by_province(province)