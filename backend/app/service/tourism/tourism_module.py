# backend/app/service/tourism/tourism_module.py
from app.db.session import SessionLocal
from app.db.models.tourism_model import TourismPlace as Tourism


def get_all_provinces():
    session = SessionLocal()
    try:
        rows = session.query(Tourism.province).distinct().all()
        provinces = sorted({p[0] for p in rows})
        return provinces
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
        print(f"\n=== DEBUG: get_places_by_subcategories ===")
        print(f"Province parameter: '{province}'")
        print(f"Type of province: {type(province)}")
        
        # In tất cả tỉnh trong DB để so sánh
        all_provinces_in_db = session.query(Tourism.province).distinct().all()
        db_provinces = [p[0] for p in all_provinces_in_db]
        print(f"All provinces in DB: {db_provinces}")
        
        # Kiểm tra xem province có tồn tại không
        if province not in db_provinces:
            print(f"WARNING: Province '{province}' NOT FOUND in database!")
            # Tìm tỉnh gần giống
            for db_prov in db_provinces:
                if province.lower() in db_prov.lower() or db_prov.lower() in province.lower():
                    print(f"  Similar found: '{db_prov}'")
        
        # Query dữ liệu
        print(f"\nQuerying for province: '{province}'")
        rows = session.query(Tourism).filter(
            Tourism.province == province
        ).all()
        
        print(f"Found {len(rows)} rows with exact match")
        
        # Nếu không tìm thấy, thử tìm không phân biệt hoa thường
        if len(rows) == 0:
            print("\nTrying case-insensitive search...")
            all_rows = session.query(Tourism).all()
            matches = []
            for r in all_rows:
                if r.province and province.lower() == r.province.lower():
                    matches.append(r)
            
            print(f"Found {len(matches)} rows with case-insensitive match")
            rows = matches

        # Nếu không có subcategory nào được chọn, trả về tất cả
        if not selected_subcats:
            matched_places = rows
            print(f"No subcategories selected, returning all {len(rows)} places")
        else:
            matched_places = []
            for place in rows:
                subcat_field = place.sub_category

                if isinstance(subcat_field, list):
                    if any(sc in subcat_field for sc in selected_subcats):
                        matched_places.append(place)
                elif isinstance(subcat_field, str):
                    if subcat_field in selected_subcats:
                        matched_places.append(place)
            
            print(f"With subcategories {selected_subcats}, matched {len(matched_places)} places")

        print(f"Total matched places to return: {len(matched_places)}")
        
        if matched_places:
            print("Sample place:", {
                "name": matched_places[0].name,
                "category": matched_places[0].category,
                "sub_category": matched_places[0].sub_category
            })

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
                "province": p.province,
                "type": p.type,
                "tags": p.tags,
                "review_count": p.review_count,
                "highlights": p.highlights,
                "food": p.food,
                "open_hours": p.open_hours
            }
            for p in matched_places
        ]

    finally:
        session.close()