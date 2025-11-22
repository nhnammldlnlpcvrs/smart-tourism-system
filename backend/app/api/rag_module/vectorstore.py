import faiss
import numpy as np
import os
import pickle
from typing import List, Dict, Optional, Any

"""
    VectorStore dùng FAISS IndexFlatL2 (mặc định). Lưu embeddings + records (metadata).
    - vectors: np.ndarray shape (n, d)
    - records: list[dict] tương ứng
    - persist_path: nếu truyền sẽ ghi faiss.index và records.pkl
"""
class VectorStore:

    def __init__(self, vectors: np.ndarray, records: List[Dict[str, Any]], persist_path: Optional[str] = None):
        assert len(vectors) == len(records), "vectors and records must have same length"
        self.records = records
        self.d = vectors.shape[1]

        self.index = faiss.IndexFlatL2(self.d)
        self.index.add(vectors.astype("float32"))

        self.persist_path = persist_path
        if persist_path:
            os.makedirs(persist_path, exist_ok=True)
            faiss.write_index(self.index, os.path.join(persist_path, "faiss.index"))
            with open(os.path.join(persist_path, "records.pkl"), "wb") as f:
                pickle.dump(self.records, f)


    @classmethod
    def load(cls, persist_path: str) -> "VectorStore":
        """
        Tạo VectorStore từ persist_path (faiss.index + records.pkl).
        """
        idx_path = os.path.join(persist_path, "faiss.index")
        rec_path = os.path.join(persist_path, "records.pkl")
        if not os.path.exists(idx_path) or not os.path.exists(rec_path):
            raise FileNotFoundError("Persist files not found in persist_path")

        index = faiss.read_index(idx_path)
        with open(rec_path, "rb") as f:
            records = pickle.load(f)

        d = index.d
        placeholder = np.zeros((0, d), dtype="float32")
        inst = cls.__new__(cls)
        inst.records = records
        inst.d = d
        inst.index = index
        inst.persist_path = persist_path
        return inst
    

    def search(self, query_vector: np.ndarray, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Tìm top_k nearest records theo L2. 
        - query_vector shape: (1, d) hoặc (n, d) nhưng we assume (1, d) here.
        Trả về list các record dict theo thứ tự gần nhất -> xa.
        """
        if query_vector.ndim == 1:
            query_vector = query_vector.reshape(1, -1)
        distances, indices = self.index.search(query_vector.astype("float32"), top_k)
        inds = indices[0].tolist()
        result = []
        for i in inds:
            # in case index returns -1 for padding
            if i < 0 or i >= len(self.records):
                continue
            result.append(self.records[i])
        return result

    def save(self) -> None:
        """
        Explicit persist nếu muốn.
        """
        if not self.persist_path:
            raise RuntimeError("persist_path not configured")
        faiss.write_index(self.index, os.path.join(self.persist_path, "faiss.index"))
        with open(os.path.join(self.persist_path, "records.pkl"), "wb") as f:
            pickle.dump(self.records, f)
