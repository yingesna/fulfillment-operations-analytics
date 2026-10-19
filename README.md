# Fulfillment Operations & Workforce Analytics

**Portfolio case study | Synthetic data | SQL (SQLite) | Python | Operational KPIs**

## Business problem
How do staffing coverage, daily order volume, and capacity constraints relate to fulfillment productivity, order backlogs, quality, and on-time processing across three simulated facilities?

This is an independent learning project inspired by common fulfillment operations workflows. **All data is artificially generated. It is not Amazon data and does not represent actual company performance.**

## Dataset
Run `python generate_data.py` to generate 270 facility-day observations (90 days × 3 facilities) with a fixed random seed.

Fields: `date`, `facility`, `scheduled_staff`, `actual_staff`, `scheduled_labor_hours`, `actual_labor_hours`, `forecast_orders`, `orders_received`, `orders_processed`, `on_time_orders`, `defect_count`, `backlog_orders`.

Backlog is carried forward per facility: **ending backlog = previous ending backlog + orders received − orders processed**. Processing cannot exceed simulated daily capacity or available work.

## KPIs
- **Orders per labor hour:** processed orders / actual labor hours.
- **On-time fulfillment rate:** on-time orders / processed orders.
- **Staffing coverage:** actual staff / scheduled staff.
- **DPMO proxy:** defect count / processed orders × 1,000,000. This uses one opportunity per processed order, and is not an Amazon-defined metric.
- **Backlog to intake ratio:** sum of daily ending backlog / sum of daily orders received. This is a diagnostic ratio, not a unique-order backlog rate.
- **Forecast error:** (orders received − forecast orders) / forecast orders.

## Run locally
```bash
python -m pip install -r requirements.txt
python generate_data.py
python analyze.py
python -m unittest discover -s tests
```

The chart will be written to `dashboards/on_time_by_facility.png`. The Python analysis prints weighted facility-level KPIs.

## SQL analysis
Import `data/fulfillment_operations.csv` into a SQLite table named `fulfillment_operations` (for example using DB Browser for SQLite or a Python import script), then execute:
1. `sql/01_data_validation.sql` — completeness and logical constraints.
2. `sql/02_kpi_analysis.sql` — facility-level KPI comparisons.
3. `sql/03_root_cause_analysis.sql` — exploratory staffing coverage segmentation.

## Limitations
Synthetic relationships are programmed assumptions, not empirical findings. Comparing staffing bands is descriptive and **does not establish causation**. Findings should be computed from generated data before writing any conclusions or recommendations. No actual productivity gains, financial savings, or business outcomes are claimed.

## Next steps
Add an executable notebook, richer dashboard, SQL import automation, time-series diagnostics, and a documented executive summary based on validated outputs.


## Automated GitHub Actions pipeline
The [analytics workflow](.github/workflows/analytics.yml) runs on pushes, pull requests, and manual dispatch. It generates the synthetic dataset, runs unit tests, executes SQL checks via `validate_sql.py`, produces the on-time performance chart, and uploads both the CSV and PNG as a downloadable workflow artifact.

To run it manually, open **Actions → Validate and build analytics artifacts → Run workflow**. When the run finishes, download **fulfillment-analytics-results** from the run's Artifacts section. Workflow artifacts are generated outputs; they are not committed to the repository.

To run SQL validation locally:
```bash
python generate_data.py
python validate_sql.py
```
