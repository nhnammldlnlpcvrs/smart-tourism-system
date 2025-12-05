# backend/app/rag_module/rag_pipeline.py
from typing import List, Dict, Any, Optional
import os

from .loader import load_from_postgres
from .embedder import Embedder
from .vector_store import VectorStore
from .retriever import Retriever
from .prompt_builder import build_itinerary_prompt
from .generator import LLMGenerator


class RAGPipeline:
    def __init__(self, engine=None, persist_path: Optional[str] = None, rebuild: bool = False):
        self.engine = engine
        self.persist_path = persist_path or "app/rag_store"
        self.rebuild = rebuild

        # Components
        self.embedder = Embedder()
        self.store: Optional[VectorStore] = None
        self.retriever: Optional[Retriever] = None
        self.generator = LLMGenerator()

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
                print("🔵 Loaded existing vector store from disk.")
            except Exception as e:
                print("⚠ Failed to load vector store, will rebuild.", e)
                self.store = None
                self.retriever = None

    # Build store from pre-loaded record objects
    def build_from_records(self, records: List[Dict[str, Any]]):
        """
        Build FAISS vectors from processed record list.
        """
        print(f"🔧 Building vector store from {len(records)} records…")

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

        self.store.save()  # 💾 Persist FAISS + metadata
        self.retriever = Retriever(self.embedder, self.store)
        self.is_built = True

        print("✅ Vector store built & saved.")
        return self

    # Build store directly from PostgreSQL
    def build_from_postgres(self, table_names: List[str]):
        if not self.engine:
            raise RuntimeError("engine required to load postgres tables")

        print(f"Loading data from Postgres: {table_names}")
        records = load_from_postgres(self.engine, table_names)

        return self.build_from_records(records)

    # Retrieval
    def retrieve(self, query: str, top_k: int = 5):
        if not self.retriever:
            raise RuntimeError("Retriever is not initialized")

        return self.retriever.retrieve(query, top_k=top_k)

    # Full RAG → Itinerary LLM
    def generate_itinerary(
        self,
        province: str,
        selected_categories: List[str],
        selected_subcategories: List[str],
        places: List[Dict[str, Any]],
        days: int = 2,
        audience: str = "general",
        start_date: str = None,
        end_date: str = None,
        budget_per_person: str = None,
        top_k: int = 5,
        activities: Optional[List[str]] = None,
        seasonal_event: Optional[str] = None,
    ):

        # Build the query from available filters
        search_terms = [
            province,
            *selected_categories,
            *selected_subcategories
        ]

        if activities:
            search_terms.extend(activities)

        if seasonal_event:
            search_terms.append(seasonal_event)

        query = " ".join([str(x).lower() for x in search_terms if x])

        contexts = self.retrieve(query, top_k=top_k)

        prompt = build_itinerary_prompt(
            province=province,
            selected_categories=selected_categories,
            selected_subcategories=selected_subcategories,
            places=places,
            retrieved_contexts=contexts,
            days=days,
            audience=audience,
            start_date=start_date,
            end_date=end_date,
            budget_per_person=budget_per_person,
            activities=activities,
            seasonal_event=seasonal_event
        )

        llm_out = self.generator.generate(prompt)

        return {
            "prompt": prompt,
            "llm_output": llm_out,
            "retrieved": contexts
        }