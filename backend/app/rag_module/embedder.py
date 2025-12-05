# backend/app/rag_module/embedder.py
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any
from .loader import record_to_text

class Embedder:
    def __init__(self, model_name="intfloat/multilingual-e5-small"):
        self.model = SentenceTransformer(model_name)

    def encode(self, texts: List[str]):
        return self.model.encode(texts, convert_to_numpy=True)

    # NEW — encode records
    def encode_records(self, records: List[Dict[str, Any]]):
        texts = [record_to_text(r["record"]) for r in records]
        return self.encode(texts)

    # NEW — convert a single record
    def record_to_text(self, record: Dict[str, Any]) -> str:
        return record_to_text(record)