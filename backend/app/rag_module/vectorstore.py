import faiss, os, pickle
import numpy as np
from typing import List, Dict, Optional, Any

class VectorStore:

    def __init__(self, vectors: np.ndarray, records: List[Dict[str, Any]], persist_path: Optional[str] = None):
        assert len(vectors) == len(records)

        self.records = records
        self.d = vectors.shape[1]
        self.index = faiss.IndexFlatL2(self.d)
        self.index.add(vectors.astype("float32"))

        self.persist_path = persist_path
        if persist_path:
            os.makedirs(persist_path, exist_ok=True)
            faiss.write_index(self.index, f"{persist_path}/faiss.index")
            with open(f"{persist_path}/records.pkl", "wb") as f:
                pickle.dump(self.records, f)

    @classmethod
    def load(cls, persist_path: str):
        idx = f"{persist_path}/faiss.index"
        rec = f"{persist_path}/records.pkl"

        if not os.path.exists(idx) or not os.path.exists(rec):
            raise FileNotFoundError("Index not found")

        index = faiss.read_index(idx)
        with open(rec, "rb") as f:
            records = pickle.load(f)

        inst = cls.__new__(cls)
        inst.index = index
        inst.records = records
        inst.d = index.d
        inst.persist_path = persist_path
        return inst

    def search(self, q_vec: np.ndarray, top_k=3):
        if q_vec.ndim == 1:
            q_vec = q_vec.reshape(1, -1)

        dist, idxs = self.index.search(q_vec, top_k)
        ids = idxs[0].tolist()

        return [self.records[i] for i in ids if 0 <= i < len(self.records)]
