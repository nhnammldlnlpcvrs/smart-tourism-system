from app.db.session import SessionLocal
from app.db.models.tourism_model import TourismPlace as Tourism

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