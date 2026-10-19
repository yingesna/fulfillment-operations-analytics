"""Create an operations KPI summary and dashboard from generated synthetic data."""
import csv
from collections import defaultdict
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DATA = Path("data/fulfillment_operations.csv")
OUT = Path("dashboards")

def summarize(rows):
    groups = defaultdict(lambda: defaultdict(int))
    for row in rows:
        g = groups[row["facility"]]
        for key in ("orders_received","orders_processed","on_time_orders","actual_labor_hours","actual_staff","scheduled_staff","defect_count"):
            g[key] += int(row[key])
    return {facility: {
        "on_time_pct": 100 * g["on_time_orders"] / g["orders_processed"],
        "orders_per_labor_hour": g["orders_processed"] / g["actual_labor_hours"],
        "staffing_coverage_pct": 100 * g["actual_staff"] / g["scheduled_staff"],
        "dpmo": 1_000_000 * g["defect_count"] / g["orders_processed"],
    } for facility, g in groups.items()}

def main():
    with DATA.open(newline="", encoding="utf-8") as handle:
        metrics = summarize(list(csv.DictReader(handle)))
    OUT.mkdir(exist_ok=True)
    names = sorted(metrics)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(names, [metrics[n]["on_time_pct"] for n in names])
    ax.set(title="On-time fulfillment by facility (synthetic)", ylabel="On-time (%)", ylim=(0, 100))
    fig.tight_layout()
    fig.savefig(OUT / "on_time_by_facility.png", dpi=160)
    plt.close(fig)
    for facility in names:
        print(f"{facility}: {metrics[facility]}")
    print("Saved dashboards/on_time_by_facility.png")

if __name__ == "__main__":
    main()
