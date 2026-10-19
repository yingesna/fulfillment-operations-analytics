"""Import generated CSV into SQLite and execute project SQL scripts."""
import csv
import sqlite3
from pathlib import Path

CSV = Path("data/fulfillment_operations.csv")
SCHEMA = """
CREATE TABLE fulfillment_operations (
    date TEXT NOT NULL,
    facility TEXT NOT NULL,
    scheduled_staff INTEGER NOT NULL,
    actual_staff INTEGER NOT NULL,
    scheduled_labor_hours INTEGER NOT NULL,
    actual_labor_hours INTEGER NOT NULL,
    forecast_orders INTEGER NOT NULL,
    orders_received INTEGER NOT NULL,
    orders_processed INTEGER NOT NULL,
    on_time_orders INTEGER NOT NULL,
    defect_count INTEGER NOT NULL,
    backlog_orders INTEGER NOT NULL
);
"""

def main():
    if not CSV.exists():
        raise SystemExit("Missing dataset: run python generate_data.py first")
    with CSV.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        fields = reader.fieldnames
        assert fields is not None
        rows = list(reader)
    conn = sqlite3.connect(":memory:")
    conn.executescript(SCHEMA)
    placeholders = ", ".join("?" for _ in fields)
    columns = ", ".join(fields)
    conn.executemany(
        f"INSERT INTO fulfillment_operations ({columns}) VALUES ({placeholders})",
        [[row[key] for key in fields] for row in rows],
    )
    for path in sorted(Path("sql").glob("*.sql")):
        print(f"Executing {path}")
        for statement in path.read_text(encoding="utf-8").split(";"):
            statement = statement.strip()
            if not statement:
                continue
            result = conn.execute(statement)
            results = result.fetchall()
            if path.name == "01_data_validation.sql" and "WHERE actual_staff < 0" in statement:
                if results:
                    raise AssertionError(f"Invalid data rows: {results[:5]}")
            print(f"  {len(results)} result rows")
            if results:
                print(" ", results[:4])
    conn.close()
    print("SQL validation complete.")

if __name__ == "__main__":
    main()
