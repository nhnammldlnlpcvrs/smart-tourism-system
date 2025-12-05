from app.db.session import SessionLocal
from app.db.models.tourism_model import TourismPlace as Tourism

<<<<<<< HEAD

def get_all_provinces():
    session = SessionLocal()
    try:
        rows = session.query(Tourism.province).distinct().all()
        provinces = sorted({p[0] for p in rows})
        return provinces
    finally:
        session.close()


=======
def get_provinces():
    session = SessionLocal()
    try:
        # Query lấy danh sách các tỉnh duy nhất (DISTINCT)
        # Kết quả trả về dạng list các tuple: [('Quảng Ngãi',), ('Đà Nẵng',), ...]
        rows = session.query(Tourism.province).distinct().all()
        
        # Chuyển đổi thành list string và sắp xếp
        # Lọc bỏ các giá trị None hoặc rỗng nếu có
        return sorted([row[0] for row in rows if row[0]])
    except Exception as e:
        print(f"Error getting provinces: {e}")
        return []
    finally:
        session.close()

>>>>>>> 726c261a4888baa19632f336fe1ddff549a38933
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

            # Sub-category dạng list
            if isinstance(subcats, list):
                for s in subcats:
                    if s:
                        category_map[category].add(s)

            # Sub-category dạng string
            elif isinstance(subcats, str) and subcats.strip():
                category_map[category].add(subcats.strip())

        # Convert set → list sorted
        return {
            category: sorted(list(subs))
            for category, subs in category_map.items()
        }

    finally:
        session.close()


def get_places_by_subcategories(province: str, selected_subcats: list[str]):
    session = SessionLocal()
    try:
        rows = session.query(Tourism).filter(
            Tourism.province == province
        ).all()

        matched_places = []

        for place in rows:
            subcat_field = place.sub_category

            if isinstance(subcat_field, list):
                if any(sc in subcat_field for sc in selected_subcats):
                    matched_places.append(place)

            elif isinstance(subcat_field, str):
                if subcat_field in selected_subcats:
                    matched_places.append(place)

        return [
            {
                "id": p.id,
                "name": p.name,
                "address": p.address,
                "category": p.category,
                "sub_category": p.sub_category,
                "description": p.description,
                "image_url": p.image_url,
                "rating": p.rating,
                "province": p.province
            }
            for p in matched_places
        ]

    finally:
        session.close()
