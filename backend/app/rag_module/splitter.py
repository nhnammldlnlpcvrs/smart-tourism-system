def split_documents(data):
    chunks = []
    for item in data:
        chunks.append({
            "id": item["id"],
            "record": item["record"]
        })
    return chunks
