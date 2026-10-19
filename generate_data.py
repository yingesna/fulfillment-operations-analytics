"""Generate reproducible, synthetic daily fulfillment operations data."""
import csv
import random
from datetime import date, timedelta
from pathlib import Path

OUTPUT = Path("data/fulfillment_operations.csv")
FIELDS = ["date","facility","scheduled_staff","actual_staff","scheduled_labor_hours","actual_labor_hours","forecast_orders","orders_received","orders_processed","on_time_orders","defect_count","backlog_orders"]

def generate(seed=42):
    rng = random.Random(seed)
    rows = []
    for facility, base_staff, baseline_volume in [("FC-01",35,4200),("FC-02",42,5100),("FC-03",29,3450)]:
        previous_backlog = 0
        for day in range(90):
            current = date(2026, 1, 1) + timedelta(days=day)
            weekend = current.weekday() >= 5
            scheduled = base_staff + rng.randint(-3, 4)
            actual = max(1, scheduled - rng.randint(0, 6))
            scheduled_hours = scheduled * 8
            actual_hours = actual * 8
            forecast = int(baseline_volume * (0.88 if weekend else 1.0) * rng.uniform(0.90, 1.10))
            received = max(0, int(forecast * rng.uniform(0.89, 1.16)))
            capacity = int(actual_hours * rng.uniform(13.5, 16.5))
            processed = min(previous_backlog + received, capacity)
            backlog = previous_backlog + received - processed
            late_share = min(0.22, 0.015 + 0.11 * (backlog / max(1, received)) + rng.uniform(0, 0.025))
            on_time = processed - int(processed * late_share)
            defects = min(processed, int(processed * rng.uniform(0.002, 0.011)))
            rows.append(dict(zip(FIELDS,[current.isoformat(),facility,scheduled,actual,scheduled_hours,actual_hours,forecast,received,processed,on_time,defects,backlog])))
            previous_backlog = backlog
    return rows

def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(generate())
    print(f"Wrote {len(generate())} synthetic records to {OUTPUT}")

if __name__ == "__main__":
    main()
