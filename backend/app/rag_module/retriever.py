# backend/app/rag_module/retriever.py
from typing import List, Dict, Any
import numpy as np
from .embedder import Embedder
from .vector_store import VectorStore

class Retriever:
    def __init__(self, embedder: Embedder, store: VectorStore):
        self.embedder = embedder
        self.store = store

    def retrieve(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        q_vec = self.embedder.model.encode([query], convert_to_numpy=True).astype("float32")
        return self.store.search(q_vec, top_k=top_k)