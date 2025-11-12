from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List, Dict


"""Chuyển 1 record dict thành một chuỗi văn bản chuẩn để tokenize/embed."""
def _record_to_text(item: Dict) -> str:
    return (
        f"Tên: {item.get('name','')}\n"
        f"Loại: {item.get('type','')}\n"
        f"Tỉnh: {item.get('province','')}\n"
        f"Mô tả: {item.get('description','')}\n"
        f"Hoạt động: {', '.join(item.get('activities', []))}\n"
        f"Ẩm thực: {', '.join(item.get('food', []))}\n"
        f"Thời gian lý tưởng: {item.get('best_time_to_visit','')}\n"
        f"Tags: {', '.join(item.get('tags', []))}"
    )


"""
    Chia các record thành các chunk văn bản.
    - data: List[Dict] từ loader
    - chunk_size, chunk_overlap: tham số cho text splitter
"""
def split_documents(data : List[Dict], chunk_size: int = 500, chunk_overlap: int = 100) -> List[str]:
    splitter = RecursiveCharacterTextSplitter(chunk_size, chunk_overlap)
    texts = []
    for item in data:
        line = _record_to_text(item)        # từ json -> str
        chunk = splitter.split_text(line)   # str -> chunks
        texts.extend(chunk)                 # lưu các chunks vào 1 List
    return texts



