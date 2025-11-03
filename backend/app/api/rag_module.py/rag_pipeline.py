# rag_pipeline.py
"""
RAGPipeline
- Orchestrator cho toàn bộ pipeline RAG: load -> split -> embed -> index -> retrieve -> generate
- Tuân thủ SRP: class này chỉ phối hợp (orchestrate). Các bước cụ thể được inject qua tham số (Dependency Injection).
- Hỗ trợ persist index để không phải embed lại mỗi lần khởi động.
"""

from typing import Callable, List, Optional, Any, Dict
from pathlib import Path
from loguru import logger
import numpy as np

# Các import mặc định (bạn có thể override khi khởi tạo RAGPipeline)
from .loader import load_json_data                # -> List[Dict]
from .splitter import split_documents              # -> List[str] hoặc List[Dict(chunks with meta)]
from .embedder import get_embeddings               # -> np.ndarray
from .vectorstore import VectorStore               # class with add/search/persist
from .retriever import retrieve_relevant_docs      # -> List[str]
from .generator import generate_answer             # -> str

class RAGPipeline:
    """
    RAGPipeline orchestrator.
    - json_path: đường dẫn file JSON gốc.
    - persist_path: thư mục lưu index + metadata (nếu muốn persist).
    - loader, splitter, embedder, vectorstore_cls, retriever_fn, generator_fn: dependencies (DI).
    """

    def __init__(
        self,
        json_path: str,
        persist_path: Optional[str] = None,
        loader_fn: Callable[[str], List[Dict]] = load_json_data,
        splitter_fn: Callable[[List[Dict]], List[Any]] = split_documents,
        embedder_fn: Callable[[List[str]], np.ndarray] = get_embeddings,
        vectorstore_cls: Callable[..., VectorStore] = VectorStore,
        retriever_fn: Callable[..., List[str]] = retrieve_relevant_docs,
        generator_fn: Callable[..., str] = generate_answer,
        faiss_dim: Optional[int] = None,
        rebuild_on_init: bool = True,
    ):
        self.json_path = Path(json_path)
        self.persist_path = Path(persist_path) if persist_path else None

        # Dependencies (DI)
        self.loader_fn = loader_fn
        self.splitter_fn = splitter_fn
        self.embedder_fn = embedder_fn
        self.vectorstore_cls = vectorstore_cls
        self.retriever_fn = retriever_fn
        self.generator_fn = generator_fn

        # Internal state
        self._store: Optional[VectorStore] = None
        self._chunks: List[Dict] = []      # metadata + text chunks
        self._vectors: Optional[np.ndarray] = None
        self._faiss_dim = faiss_dim        # optional; nếu None sẽ lấy từ embeddings shape

        if rebuild_on_init:
            try:
                # Nếu có persist path, cố load index trước khi build mới
                if self.persist_path and self._try_load_persisted():
                    logger.info("Loaded persisted index.")
                else:
                    logger.info("Không tìm thấy persisted index hoặc persist_path chưa cấu hình; sẽ build mới.")
                    self.build_index()
            except Exception as e:
                logger.exception(f"Lỗi khi khởi tạo RAGPipeline: {e}")
                # cố gắng build index từ JSON
                self.build_index()

    # ---------------------------
    # Public API
    # ---------------------------

    def build_index(self) -> None:
        """
        Build toàn bộ index từ file JSON:
        1) load raw data
        2) split thành chunks (mỗi chunk có metadata)
        3) embed chunks (trả về np.ndarray shape (n, d))
        4) tạo VectorStore từ vectors + metadata
        """
        logger.info("Bắt đầu build index từ JSON.")
        # 1) load
        raw = self.loader_fn(str(self.json_path))
        if not raw:
            raise ValueError(f"Không có dữ liệu trong {self.json_path}")

        # 2) split thành chunks
        # splitter_fn có thể trả list[str] hoặc list[dict] (khuyến nghị dict: {id, name, text})
        chunks = self.splitter_fn(raw)
        if not chunks:
            raise ValueError("Splitter trả về danh sách rỗng.")

        # Chuẩn hoá: nếu chunks là list[str], chuyển thành dict có text only
        normalized_chunks: List[Dict] = []
        for i, c in enumerate(chunks):
            if isinstance(c, str):
                normalized_chunks.append({"id": i, "text": c})
            elif isinstance(c, dict):
                # mong có keys: 'id' và 'text' (các field khác là metadata)
                normalized_chunks.append(c)
            else:
                raise TypeError("Invalid chunk type returned from splitter_fn; expected str or dict.")

        self._chunks = normalized_chunks
        texts = [c["text"] for c in self._chunks]

        # 3) embed
        logger.info(f"Calling embedder on {len(texts)} chunks.")
        vectors = self.embedder_fn(texts)  # expect np.ndarray (n, d) or list -> convert
        vectors = np.array(vectors, dtype="float32")
        if vectors.ndim != 2:
            raise ValueError("Embeddings must be 2D array (n_chunks, dim).")
        self._vectors = vectors
        self._faiss_dim = vectors.shape[1] if self._faiss_dim is None else self._faiss_dim

        # 4) create vectorstore
        logger.info("Tạo VectorStore từ embeddings.")
        self._store = self.vectorstore_cls(vectors=self._vectors, texts=[c["text"] for c in self._chunks], persist_path=(str(self.persist_path) if self.persist_path else None))
        logger.success("Build index hoàn tất.")

    def retrieve_context(self, query: str, top_k: int = 3) -> List[Dict]:
        """
        Lấy các đoạn văn bản liên quan nhất (cùng metadata) cho query.
        Trả về list các dict metadata: at minimum phải có key 'text'.
        """
        if self._store is None:
            raise RuntimeError("Vector store chưa được khởi tạo. Gọi build_index() trước.")
        # reuse retriever fn: may expect (query, store)
        try:
            docs = self.retriever_fn(query, self._store, top_k=top_k)
        except TypeError:
            # fallback: if retriever_fn(query) takes different signature
            docs = self.retriever_fn(query)
        # retriever_fn expected to return list[str] or list[dict]; normalize to list[dict]
        normalized = []
        for d in docs:
            if isinstance(d, str):
                normalized.append({"text": d})
            elif isinstance(d, dict):
                normalized.append(d)
            else:
                normalized.append({"text": str(d)})
        return normalized

    def generate_final_answer(self, question: str, contexts: List[Dict]) -> str:
        """
        Tạo prompt từ contexts + question, rồi gọi generator_fn.
        contexts: list of dicts with key 'text' and optional metadata.
        """
        # Tạo list text context
        context_texts = [c.get("text", "") for c in contexts if c.get("text", "").strip()]
        # Nếu không có context trả về fallback message
        if not context_texts:
            return "Xin lỗi, tôi chưa có thông tin về điều đó."
        # gọi generator (generator_fn nhận (question, contexts) hoặc (question, list_texts))
        try:
            # ưu tiên truyền cả contexts (list of dict) để generator có thể dùng metadata
            answer = self.generator_fn(question, context_texts)
        except TypeError:
            # fallback signature
            answer = self.generator_fn(context="\n\n".join(context_texts), question=question)
        return answer

    def answer(self, question: str, top_k: int = 3) -> Dict[str, Any]:
        """
        Full RAG: retrieve_context -> generate_final_answer
        Trả về dict: {question, answer, contexts}
        """
        question = question.strip()
        if not question:
            return {"question": question, "answer": "Câu hỏi rỗng.", "contexts": []}

        contexts = self.retrieve_context(question, top_k=top_k)
        answer = self.generate_final_answer(question, contexts)
        return {"question": question, "answer": answer, "contexts": contexts}

    # ---------------------------
    # Persist / reload
    # ---------------------------

    def _try_load_persisted(self) -> bool:
        """
        Thử load index + metadata từ persist_path (nếu có)
        Expect VectorStore to support loading when constructed with persist_path,
        or implement vectorstore_cls.load(...) method. Return True nếu success.
        """
        if not self.persist_path:
            return False
        # try to instantiate VectorStore with persist_path only
        try:
            # many VectorStore implementations support loading from persist_path automatically in __init__
            self._store = self.vectorstore_cls(vectors=np.zeros((1, self._faiss_dim), dtype="float32"), texts=[], persist_path=str(self.persist_path))
            # if vectorstore_cls writes/reads index in __init__, it should set internal index accordingly
            # Here we do a naive check: if index exists and has ntotal > 0
            try:
                ntotal = getattr(self._store.index, "ntotal", None)
                if ntotal and ntotal > 0:
                    logger.info(f"Loaded persisted index with {ntotal} vectors.")
                    return True
            except Exception:
                # If vectorstore does not expose index.ntotal, just return True (optimistic)
                return True
        except Exception as e:
            logger.warning(f"Không load được persisted index: {e}")
            self._store = None
            return False
        return False

    def persist(self) -> None:
        """
        Ghi index + metadata ra disk; yêu cầu VectorStore hỗ trợ persist (đã implement trong vectorstore.py).
        """
        if self._store is None:
            raise RuntimeError("Không có index để persist.")
        if not self.persist_path:
            raise RuntimeError("persist_path chưa được cấu hình.")
        # VectorStore constructor may have already saved index; here we call a method if available
        save_fn = getattr(self._store, "save", None)
        if callable(save_fn):
            save_fn()
            logger.info(f"VectorStore persisted to {self.persist_path}.")
        else:
            logger.info("VectorStore không có phương thức save(), nhưng index có thể đã được lưu trong __init__.")

    def reload_index(self) -> None:
        """
        Rebuild index từ JSON (useful for /reload endpoint).
        """
        logger.info("Reloading index from JSON...")
        self.build_index()

# End of file
