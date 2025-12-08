# backend/app/rag_module/rag_pipeline.py
from typing import List, Dict, Any, Optional
import os

from .loader import load_from_postgres
from .embedder import Embedder
from .vector_store import VectorStore
from .retriever import Retriever

class RAGPipeline:
    """
    Pipeline chỉ thực hiện chức năng RAG: Xây dựng Vector Store, Embedding và Truy xuất dữ liệu (Retrieval).
    """
    def __init__(self, engine=None, persist_path: Optional[str] = None, rebuild: bool = False):
        self.engine = engine
        self.persist_path = persist_path or "app/rag_store"
        self.rebuild = rebuild

        # Components
        self.embedder = Embedder()
        self.store: Optional[VectorStore] = None
        self.retriever: Optional[Retriever] = None
        # Loại bỏ: self.generator = LLMGenerator()

        # status flag
        self.is_built = False

        # Load existing FAISS store (lazy)
        index_path = os.path.join(self.persist_path, "faiss.index")
        meta_path = os.path.join(self.persist_path, "records.pkl")

        if os.path.exists(index_path) and os.path.exists(meta_path) and not rebuild:
            try:
                self.store = VectorStore.load(self.persist_path)
                self.retriever = Retriever(self.embedder, self.store)
                self.is_built = True
                print("Loaded existing vector store from disk.")
            except Exception as e:
                print("Failed to load vector store, will rebuild.", e)
                self.store = None
                self.retriever = None

    # Build store from pre-loaded record objects
    def build_from_records(self, records: List[Dict[str, Any]]):
        """
        Build FAISS vectors from processed record list.
        """
        if self.is_built and not self.rebuild:
             print("Vector store already built. Set rebuild=True to force rebuild.")
             return self
             
        print(f"Building vector store from {len(records)} records…")

        vectors = self.embedder.encode_records(records)

        doc_items = [
            {
                "raw": r["record"],
                "text": self.embedder.record_to_text(r["record"])
            }
            for r in records
        ]

        self.store = VectorStore(
            vectors=vectors,
            records=doc_items,
            persist_path=self.persist_path
        )

        self.store.save()  # Persist FAISS + metadata
        self.retriever = Retriever(self.embedder, self.store)
        self.is_built = True

        print("Vector store built & saved.")
        return self

    # Build store directly from PostgreSQL
    def build_from_postgres(self, table_names: List[str]):
        if not self.engine:
            raise RuntimeError("engine required to load postgres tables")

        print(f"Loading data from Postgres: {table_names}")
        records = load_from_postgres(self.engine, table_names)

        return self.build_from_records(records)

    # Retrieval: Đổi tên từ 'retrieve' thành 'search' để phù hợp với module gọi
    def search(self, query: str, top_k: int = 5):
        """
        Truy xuất các context liên quan nhất từ Vector Store.
        """
        if not self.retriever:
            raise RuntimeError("Retriever is not initialized or RAG store not built.")

        # Gọi phương thức retrieve thực tế của Retriever component
        return self.retriever.retrieve(query, top_k=top_k)
