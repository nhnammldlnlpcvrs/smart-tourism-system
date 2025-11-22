# retriever.py
from typing import List, Dict, Any
import numpy as np
from .embedder import get_embeddings
from .vectorstore import VectorStore

"""
    - query: str
    - store: VectorStore instance
    Trả về list[record dict] (top_k).
"""
def retrieve_relevant_docs(query: str, store: VectorStore, top_k: int = 3, embed_model: str = None) -> List[Dict[str, Any]]:
    # Embed the query as a small JSON payload {"query": query} or just the string.
    # Many embedding models expect text for queries; we pass string directly.
    q_vec = get_embeddings([{"record": {"query": query}}])  # Our get_embeddings expects list of dict with "record"
    # get_embeddings returns ndarray shape (1, d)
    return store.search(q_vec, top_k=top_k)
