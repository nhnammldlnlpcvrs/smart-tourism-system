import asyncio
from app.rag_module.rag_pipeline import RAGPipelinePG
from app.db.session import engine

async def main():
    print("=== TEST RAG PIPELINE ===")

    try:
        rag = RAGPipelinePG(
            tables=["tourism_places", "vietnam_hotels", "vietnam_foods"],
            engine=engine,
            persist_path="backend/app/rag_store",
            rebuild_on_init=False   # không rebuild lại index nếu đã tồn tại
        )
    except Exception as e:
        print("❌ Lỗi khởi tạo RAG Pipeline:", e)
        return

    print("→ RAG pipeline khởi tạo OK")

    query = "An Giang có rừng gì đẹp?"
    print(f"\n=== QUERY: {query} ===")

    try:
        result = await rag.answer(query, top_k=3)
    except Exception as e:
        print("❌ Lỗi khi chạy RAG:", e)
        return
    
    print("\n=== ANSWER ===")
    print(result.get("answer", ""))

    print("\n=== SOURCES ===")
    sources = result.get("documents", [])
    for i, doc in enumerate(sources, 1):
        print(f"\n--- Document {i} ---")
        print("Score:", doc.get("score"))
        print("Content:", doc.get("text")[:300], "...")  # in 300 ký tự đầu
        print("Metadata:", doc.get("metadata"))

    print("\n=== DONE ===")


if __name__ == "__main__":
    asyncio.run(main())
