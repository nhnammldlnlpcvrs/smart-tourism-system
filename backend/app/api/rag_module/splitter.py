from typing import List, Dict, Any

"""
    Trả về list các dict có tối thiểu: { "id": int, "record": Dict }
 """
def split_documents(data: List[Dict]) -> List[Dict[str, Any]]:
    chunks = []
    for i, item in enumerate(data):
        chunks.append({
            "id": i,
            "record": item
        })
    return chunks