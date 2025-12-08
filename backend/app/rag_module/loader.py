# backend/app/rag_module/loader.py
from typing import List, Dict, Any
from sqlalchemy import MetaData, Table
from sqlalchemy.engine import Engine


# Load all rows from a Postgres table list
def load_from_postgres(engine: Engine, table_names: List[str]) -> List[Dict[str, Any]]:
    metadata = MetaData()
    results = []

    with engine.begin() as conn:
        for tbl in table_names:
            table = Table(tbl, metadata, autoload_with=engine)
            rows = conn.execute(table.select()).fetchall()

            for r in rows:
                row_dict = dict(r._mapping)
                rid = row_dict.get("id")
                results.append({
                    "id": f"{tbl}:{rid}",
                    "record": row_dict
                })

    return results


# For loading from any in-memory list
def load_from_list(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out = []
    for it in items:
        rid = it.get("id")
        out.append({"id": f"list:{rid}", "record": it})
    return out


# Convert PostgreSQL row → clean embedding text
def record_to_text(record: Dict[str, Any]) -> str:
    fields = []

    def add(label: str, value: Any):
        """Safely append text field."""
        if not value:
            return
        if isinstance(value, list):
            if len(value) > 0:
                cleaned = ", ".join([str(v) for v in value if v])
                if cleaned.strip():
                    fields.append(f"{label}: {cleaned}")
        else:
            fields.append(f"{label}: {value}")

    add("Name", record.get("name"))
    add("Province", record.get("province"))
    add("Category", record.get("category"))
    add("Subcategories", record.get("sub_category"))
    add("Type", record.get("type"))
    add("Address", record.get("address"))
    add("Description", record.get("description"))
    add("Highlights", record.get("highlights"))
    add("Tags", record.get("tags"))
    add("Activities", record.get("activities"))
    add("Food", record.get("food"))
    add("Seasonal Events", record.get("seasonal_events"))
    add("Best Time To Visit", record.get("best_time_to_visit"))
    add("Weather Notes", record.get("weather_notes"))
    add("Special For", record.get("special_for"))
    add("Price Range", record.get("price_range"))
    add("Duration", record.get("duration_recommend"))
    add("Open Hours", record.get("open_hours"))
    add("Rating", record.get("rating"))
    add("Reviews", record.get("review_count"))

    return " | ".join(fields)