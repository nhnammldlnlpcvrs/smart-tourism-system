import os
import json
from collections import defaultdict

# --- Đường dẫn đến file chứa dữ liệu đặc sản Việt Nam ---
DATA_PATH = os.path.join(os.path.dirname(__file__), "../../data/vietnam_foods.jsonl")

def get_recommend_foods(province: str):
    """
    🔍 Trả về danh sách đặc sản của một tỉnh/thành phố Việt Nam
    (tương thích với JSONL kiểu mỗi dòng = 1 món ăn).

    Ví dụ:
        {"id": 180, "province": "Quảng Trị", "food": "Cá lóc kho tộ", "description": "..."}
    """
    try:
        if not os.path.exists(DATA_PATH):
            return {"error": f"Không tìm thấy file dữ liệu: {DATA_PATH}"}

        foods = []
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                item = json.loads(line)
                if item.get("province", "").strip().lower() == province.strip().lower():
                    foods.append({
                        "name": item.get("food"),
                        "description": item.get("description", "")
                    })

        if not foods:
            return {"error": f"Không có dữ liệu cho tỉnh '{province}'."}

        return {
            "province": province.strip(),
            "specialties": foods
        }

    except json.JSONDecodeError:
        return {"error": "Lỗi định dạng JSON trong file dữ liệu."}
    except Exception as e:
        return {"error": f"Lỗi: {str(e)}"}