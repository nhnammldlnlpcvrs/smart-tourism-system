import faiss
import numpy as np
from typing import List, Optional
import os
import pickle


class VectorStore:
    """
        - vectors: np.ndarray (n, d)
        - texts: list of original chunk texts (n items)
        - persist_path: nếu truyền, lưu index + metadata vào thư mục này
    """
    def __init__(self, vectors : np.ndarray, texts : List[str], persist_path: Optional[str] = None):
        assert len(vectors) == len(texts)       # 2 cái này phải có len bằng nhau, nếu ko là đã có lỗi
        self.texts = texts
        self.d = vectors.shape[1]

        #   Sử dụng IndexFlatL2
        self.index = faiss.IndexFlatL2(self.d)
        self.index.add(vectors)
        self.persist_path = persist_path

        #
        if persist_path:
            os.makedirs(persist_path, exist_ok = True)
            faiss.write_index(self.index, os.path.join(persist_path, "faiss.index"))
            with open(os.path.join(persist_path, "texts.pkl"), "wb") as f:
                pickle.dump(self.texts, f)


    """
        Tìm top_k vectors theo L2, trả về list các đoạn text tương ứng.
        - query_vector: np.ndarray shape (1, d)
    """
    def search(self, query_vector : np.ndarray, top_k : int = 3):
        distances, indices = self.index.search(query_vector, top_k)
        indices_array = indices[0].tolist()
        
        result = []
        for i in indices_array:
            result.append(self.texts[i])
        return result