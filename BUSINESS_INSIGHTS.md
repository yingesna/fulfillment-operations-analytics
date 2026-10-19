# Executive insights | Synthetic fulfillment operations

**Scope:** 270 facility-day observations across FC-01, FC-02, and FC-03, January 1–March 31, 2026. The dataset is simulated using a fixed random seed. No Amazon or Apple internal data is used.

## Executive snapshot

| KPI | Simulated result |
|---|---:|
| Orders received | 1,141,648 |
| Orders processed | 1,058,478 |
| On-time fulfillment | 81.26% |
| Orders per actual labor hour | 14.97 |
| Staffing coverage | 91.23% |
| Defects per million processed orders | 6,394 |

All rates are **weighted by their appropriate denominators** rather than averages of daily percentages. DPMO here assumes one defect opportunity per processed order.

## Three observations and recommendations

### 1. FC-02 has the lowest on-time rate and highest ending backlog
FC-02 processed **419,484** orders, with **80.73%** on-time fulfillment and an ending backlog of **40,476** orders. FC-01 recorded **82.31%** on-time fulfillment and an ending backlog of **23,143**. These results suggest prioritizing capacity and queue management at FC-02 in this simulation.

**Recommendation:** Review daily incoming volume against available labor-hour capacity, then model whether a targeted shift reallocation or staggered coverage could reduce end-of-day backlog. Evaluate impacts on on-time rate and productivity together.

### 2. Low staffing-coverage days coincide with weaker service
Across **123 facility-days** with staffing coverage below 90%, the weighted on-time rate was **80.66%**, compared with **81.69%** across **147 facility-days** at 90% coverage or higher: a **1.03 percentage-point** difference.

**Recommendation:** Create a daily staffing coverage threshold alert and investigate volume, backlog, and service-level movements before deciding on labor changes. This is an association in simulated data, not evidence that staffing alone caused the difference.

### 3. Productivity is similar across facilities, but customer outcomes differ
Processed orders per actual labor hour ranged from **14.90** at FC-02 to **15.02** at FC-03, while on-time fulfillment ranged from **80.73%** to **82.31%**.

**Recommendation:** Use a balanced scorecard rather than optimizing throughput alone. Track productivity alongside on-time performance, defects, and end-of-day backlog to avoid trading service quality for speed.

## Caveats and definitions

- All observations, business scenarios, and relationships are **synthetic**; findings describe this simulation only.
- **On-time %** = sum(on-time orders) / sum(processed orders).
- **Productivity** = sum(processed orders) / sum(actual labor hours).
- **Staffing coverage** = sum(actual staff) / sum(scheduled staff).
- **DPMO proxy** = sum(defects) × 1,000,000 / sum(processed orders); assumes one opportunity per processed order.
- **Ending backlog** = the final day's backlog at each facility, not a sum across days.
- The generator creates service outcomes partly as a function of backlog, so correlations are not independent causal discoveries.
- Findings were computed from the reproducible generator using seed 42. Re-run `python generate_data.py` and `python validate_sql.py` to verify.

## What this demonstrates

A complete analytics workflow: define business questions, construct a consistent dataset, validate inputs, calculate weighted KPIs, segment performance, communicate limitations, and translate patterns into testable operational recommendations.
