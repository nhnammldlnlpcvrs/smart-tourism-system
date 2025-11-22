import google.generativeai as genai
from typing import List, Dict, Any, Optional    
import numpy as np


DEFAULT_EMBED_MODEL = "models/embedding-001"

"""
    Nhận list các record (dict) và trả về numpy.ndarray shape (n, d).
    - Nếu batch=False: gọi embed cho từng record.
    - Nếu batch=True: cố gắng gọi batch (tuỳ driver embed có hỗ trợ hay không).
    Lưu ý: content có thể là dict — Gemini hỗ trợ embedding structured JSON.
"""
def get_embeddings(records: List[Dict[str, Any]], model_name: str = DEFAULT_EMBED_MODEL, batch: bool = False) -> np.ndarray:
    
    vectors = []

    if batch:
        try:
            contents = [r["record"] for r in records]
            resp = genai.embed_content(model=model_name, content=contents)
            if isinstance(resp, list):
                for item in resp:
                    vectors.append(item["embedding"])
            else:
                data = resp.get("data") or resp.get("embeddings") or []
                for it in data:
                    vectors.append(it["embedding"])
        except Exception:
            for r in records:
                resp = genai.embed_content(model=model_name, content=r["record"])
                vectors.append(resp["embedding"])
    else:
        for r in records:
            resp = genai.embed_content(model=model_name, content=r["record"])
            vectors.append(resp["embedding"])

    return np.array(vectors, dtype="float32")

