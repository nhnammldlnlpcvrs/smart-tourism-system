from sqlalchemy import Table, MetaData
from typing import List, Dict, Any

def load_postgres_data_dynamic(engine, table_names: List[str]) -> List[Dict[str, Any]]:
    metadata = MetaData()
    results = []

    with engine.begin() as conn:
        for tbl_name in table_names:
            table = Table(tbl_name, metadata, autoload_with=engine)

            rows = conn.execute(table.select()).fetchall()
            for r in rows:
                row_dict = dict(r._mapping)
                rid = row_dict.get("id", None)

                results.append({
                    "id": f"{tbl_name}:{rid}",
                    "record": row_dict
                })

    return results
