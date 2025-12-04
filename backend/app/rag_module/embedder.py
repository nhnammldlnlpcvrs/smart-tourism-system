from sentence_transformers import SentenceTransformer
import numpy as np

_e5_model = SentenceTransformer("intfloat/multilingual-e5-small")

def _record_to_text(record):
    if isinstance(record, dict):
        return " ".join(f"{k}: {v}" for k, v in record.items() if v)
    elif isinstance(record, str):
        return record
    raise TypeError(f"Unsupported record type: {type(record)}")

def get_embeddings(records):
    texts = [_record_to_text(r["record"]) for r in records]
    emb = _e5_model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
    return emb.astype("float32")
