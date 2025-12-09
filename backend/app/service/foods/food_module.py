import os
import json

DATA_PATH = os.path.join(
    os.path.dirname(__file__),
    "..", "..", "..", "data", "vietnam_foods.jsonl"
)

DATA_PATH = os.path.abspath(DATA_PATH)

def load_foods():
    foods = []
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        for line in f:
            foods.append(json.loads(line))
    return foods

FOODS = load_foods()

def get_main_tags(province: str):
    tags_counter = {}

    for item in FOODS:
        if item["province"] != province:
            continue
        for tag in item["tags"]:
            tags_counter[tag] = tags_counter.get(tag, 0) + 1

    sorted_tags = sorted(tags_counter.items(), key=lambda x: x[1], reverse=True)
    return [tag for tag, _ in sorted_tags[:6]]


def get_foods_by_province_and_tag(province: str, tag: str):
    return [
        {
            "id": item["id"],
            "food": item["food"],
            "image_url": item.get("image_url", None),
            "description": item["description"],
        }
        for item in FOODS
        if item["province"] == province and tag in item["tags"]
    ]

