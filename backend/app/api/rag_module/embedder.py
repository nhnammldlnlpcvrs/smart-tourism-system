import google.generativeai as genai
from typing import List
import numpy as np

"""
    Trả về mảng numpy shape (n_texts, dim).
    - texts: danh sách các đoạn văn
    - model_name: tên model embedding (có thể đổi)
"""
def get_embedding(texts : List[str], model_name : str = "model/embedding-001") -> np.ndarray:
    vectors = []
    for t in texts:
        # gọi gemini
        respond = genai.embed_content(model = model_name, content = t)

        # sau khi gemini trả lời bằng file json , lấy chỉ số embed
        vectors.append(respond["embedding"])
    
    return np.array(vectors, dtype = "float32")

