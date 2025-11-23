# rag_pipeline.py
from typing import Callable, List, Optional, Any, Dict
from pathlib import Path
from loguru import logger
import numpy as np

from .loader import load_json_data
from .splitter import split_documents
from .embedder import get_embeddings
from .vectorstore import VectorStore
from .retriever import retrieve_relevant_docs
from .generator import generate_answer

class RAGPipeline:
    

    def __init__(
        self,
        json_path: str,
        persist_path: Optional[str] = None,
        loader_fn: Callable[[str], List[Dict]] = load_json_data,
        splitter_fn: Callable[[List[Dict]], List[Dict]] = split_documents,
        embedder_fn: Callable[[List[Dict]], np.ndarray] = get_embeddings,
        vectorstore_cls = VectorStore,
        retriever_fn: Callable[..., List[Dict]] = retrieve_relevant_docs,
        generator_fn: Callable[..., str] = generate_answer,
        faiss_dim: Optional[int] = None,
        rebuild_on_init: bool = True,
    ):
        self.json_path = Path(json_path)
        self.persist_path = Path(persist_path) if persist_path else None

        self.loader_fn = loader_fn
        self.splitter_fn = splitter_fn
        self.embedder_fn = embedder_fn
        self.vectorstore_cls = vectorstore_cls
        self.retriever_fn = retriever_fn
        self.generator_fn = generator_fn

        self._store = None
        self._chunks: List[Dict] = []
        self._vectors = None
        self._faiss_dim = faiss_dim

        if rebuild_on_init:
            try:
                if self.persist_path and self._try_load_persisted():
                    logger.info("Loaded persisted index.")
                else:
                    logger.info("No persisted index found, building new index.")
                    self.build_index()
            except Exception as e:
                logger.exception(f"Init error: {e}")
                self.build_index()

    def build_index(self) -> None:
        logger.info("Building index from JSON...")
        raw = self.loader_fn(str(self.json_path))
        if not raw:
            raise ValueError(f"No data in {self.json_path}")

        chunks = self.splitter_fn(raw)
        if not chunks:
            raise ValueError("Splitter returned empty list")

        self._chunks = chunks
        # prepare records for embedding: embedder expects list of {"record": ...}
        records_for_embed = [{"record": c["record"]} for c in self._chunks]

        logger.info(f"Embedding {len(records_for_embed)} records...")
        vectors = self.embedder_fn(records_for_embed)
        vectors = np.array(vectors, dtype="float32")
        if vectors.ndim != 2:
            raise ValueError("Embeddings must be 2D array (n_chunks, dim).")
        self._vectors = vectors
        self._faiss_dim = vectors.shape[1] if self._faiss_dim is None else self._faiss_dim

        # create vectorstore
        records = [c["record"] for c in self._chunks]
        self._store = self.vectorstore_cls(vectors=self._vectors, records=records, persist_path=(str(self.persist_path) if self.persist_path else None))
        logger.success("Index built.")

    def retrieve_context(self, query: str, top_k: int = 3) -> List[Dict]:
        if self._store is None:
            raise RuntimeError("Vector store not initialized. Call build_index() first.")
        docs = None
        try:
            docs = self.retriever_fn(query, self._store, top_k=top_k)
        except TypeError:
            docs = self.retriever_fn(query)
        # ensure list[dict]
        normalized = []
        for d in docs:
            if isinstance(d, dict):
                normalized.append(d)
            else:
                # fallback: if string, wrap
                normalized.append({"text": str(d)})
        return normalized

    def generate_final_answer(self, question: str, contexts: List[Dict]) -> str:
        context_texts = [c for c in contexts if c]
        if not context_texts:
            return "Xin lỗi, tôi chưa có thông tin về điều đó."
        try:
            answer = self.generator_fn(question, context_texts)
            return answer
        except TypeError:
            # fallback: swap args
            return self.generator_fn(context_texts, question)

    def answer(self, question: str, top_k: int = 3) -> Dict[str, Any]:
        question = question.strip()
        if not question:
            return {"question": question, "answer": "Câu hỏi rỗng.", "contexts": []}
        contexts = self.retrieve_context(question, top_k=top_k)
        answer = self.generate_final_answer(question, contexts)
        return {"question": question, "answer": answer, "contexts": contexts}

    def _try_load_persisted(self) -> bool:
        if not self.persist_path:
            return False
        try:
            self._store = self.vectorstore_cls.load(str(self.persist_path))
            # optimistic check
            return True
        except Exception as e:
            logger.warning(f"Cannot load persisted store: {e}")
            self._store = None
            return False

    def persist(self) -> None:
        if self._store is None:
            raise RuntimeError("No store to persist.")
        save_fn = getattr(self._store, "save", None)
        if callable(save_fn):
            save_fn()
            logger.info(f"VectorStore persisted to {self.persist_path}")
        else:
            logger.info("VectorStore does not implement save(), but persisted files may exist.")
