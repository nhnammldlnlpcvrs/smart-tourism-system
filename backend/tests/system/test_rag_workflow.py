def test_rag_pipeline_end_to_end(client):
    """
    Kiểm tra RAG pipeline load & search.
    Chấp nhận cả 2 schema trả về context: {'content': str, ...} hoặc {'raw': {...}}.
    """
    from app.api.rag_itinerary_module import get_pipeline

    pipeline = get_pipeline()
    assert pipeline is not None

    contexts = pipeline.search("địa điểm du lịch nổi tiếng Hà Nội", top_k=5)
    assert isinstance(contexts, list)
    assert len(contexts) > 0

    first = contexts[0]
    assert isinstance(first, dict)

    # Accept either schema:
    if "content" in first:
        assert isinstance(first["content"], str)
        assert first["content"].strip() != ""
    elif "raw" in first:
        # raw có thể là dict chứa các trường mô tả
        assert isinstance(first["raw"], dict)
        # At least one of the raw fields should contain text
        raw_text = ""
        for v in first["raw"].values():
            if isinstance(v, str) and v.strip():
                raw_text = v
                break
            if isinstance(v, (list, dict)) and v:
                raw_text = str(v)
                break
        assert raw_text != "", "RAG raw object không có nội dung đáng kể"
    else:
        raise AssertionError("RAG context không có 'content' hoặc 'raw' key")
