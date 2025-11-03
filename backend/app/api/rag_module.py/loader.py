import json
from typing import List, Dict


"""Đọc data từ file json"""
def load_json_data(filePath : str) -> List[Dict]:
    with open(filePath, "r", encoding = "utf-8") as input:
        data = json.load(input)
        return data