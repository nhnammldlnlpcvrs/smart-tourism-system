import os
from typing import List

from .loader import load_postgres_data_dynamic
from .splitter import split_documents
from .embedder import get_embeddings, _record_to_text
from .vectorstore import VectorStore
from .retriever import retrieve_relevant_docs
from .generator import generate_answer

class RAGPipelinePG:
    def __init__(
        self,
        tables: List[str],
        engine,
        persist_path=None,
        rebuild_on_init=False,
    ):
        self.tables = tables
        self.engine = engine
        self.persist_path = persist_path
        self.rebuild_on_init = rebuild_on_init

        self._store = None
        self.build_index()

    def build_index(self):
        idx = None if not self.persist_path else f"{self.persist_path}/faiss.index"

        if idx and os.path.exists(idx) and not self.rebuild_on_init:
            self._store = VectorStore.load(self.persist_path)
            return

        data = load_postgres_data_dynamic(self.engine, self.tables)
        chunks = split_documents(data)

        vectors = get_embeddings([{"record": c["record"]} for c in chunks])

        records = []
        for c in chunks:
            raw = c["record"]
            records.append({"raw": raw, "text": _record_to_text(raw)})

        self._store = VectorStore(vectors, records, persist_path=self.persist_path)

    def retrieve_context(self, query, top_k=3):
        return retrieve_relevant_docs(query, self._store, top_k)

    async def answer(self, question: str, top_k=3):
        ctx = self.retrieve_context(question, top_k)
        if not ctx:
            return {"answer": "Xin lỗi, tôi chưa có thông tin về điều đó.", "contexts": []}

        ans = await generate_answer(question, ctx)
        return {"answer": ans, "contexts": ctx}
