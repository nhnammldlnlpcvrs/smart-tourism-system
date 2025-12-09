# backend/app/rag_module/vector_store.py
import faiss
import os
import pickle
from typing import List, Dict, Any, Optional
import numpy as np

class VectorStore:
    def __init__(self, vectors: np.ndarray, records: List[Dict[str, Any]], persist_path: Optional[str] = None):
        assert vectors.shape[0] == len(records)
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
        idx_path = os.path.join(persist_path, "faiss.index")
        rec_path = os.path.join(persist_path, "records.pkl")
        if not os.path.exists(idx_path) or not os.path.exists(rec_path):
            raise FileNotFoundError("Persist files not found")
        index = faiss.read_index(idx_path)
        with open(rec_path, "rb") as f:
            records = pickle.load(f)
        d = index.d
        inst = cls.__new__(cls)
        inst.records = records
        inst.d = d
        inst.index = index
        inst.persist_path = persist_path
        return inst

    def search(self, q_vec: np.ndarray, top_k: int = 5):
        if q_vec.ndim == 1:
            q_vec = q_vec.reshape(1, -1)
        D, I = self.index.search(q_vec.astype("float32"), top_k)
        out = []
        for idx in I[0]:
            if 0 <= idx < len(self.records):
                out.append(self.records[idx])
        return out

    def save(self):
        if not self.persist_path:
            raise RuntimeError("persist_path not set")
        faiss.write_index(self.index, os.path.join(self.persist_path, "faiss.index"))
        with open(os.path.join(self.persist_path, "records.pkl"), "wb") as f:
            pickle.dump(self.records, f)