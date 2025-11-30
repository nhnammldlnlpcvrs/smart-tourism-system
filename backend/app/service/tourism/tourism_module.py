from app.db.session import SessionLocal
from app.db.models.tourism_model import TourismPlace as Tourism

def get_category_tree_by_province(province: str):
    session = SessionLocal()
    try:
        rows = session.query(
            Tourism.category,
            Tourism.sub_category
        ).filter(
            Tourism.province == province
        ).all()

        category_map = {}

        for category, subcats in rows:
            if category not in category_map:
                category_map[category] = set()

            # Nếu subcats = None → bỏ qua
            if isinstance(subcats, list):
                for s in subcats:
                    if s:  # tránh string rỗng
                        category_map[category].add(s)

        # Trả về sorted
        return {
            category: sorted(list(subs))
            for category, subs in category_map.items()
        }

    finally:
        session.close()