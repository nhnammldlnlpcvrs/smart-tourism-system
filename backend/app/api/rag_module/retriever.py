from typing import List
import numpy as np
from .embedder import get_embedding
from .vectorstore import VectorStore

"""
    - chuyển query thành vector
    - gọi store.search để lấy top_k docs
"""
def retrieve_relevant_docs(query : str, store : VectorStore, top_k: int = 3) -> List[str]:
    q_vec = get_embedding([query])
    results = store.search(q_vec, top_k = top_k)
    return results