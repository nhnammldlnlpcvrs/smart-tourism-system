from .embedder import get_embeddings

def retrieve_relevant_docs(query: str, store, top_k=3):
    q_vec = get_embeddings([{"record": query}])
    records = store.search(q_vec, top_k)

    return [{"title": f"Doc {i}", "body": r} for i, r in enumerate(records)]
