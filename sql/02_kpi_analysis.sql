-- Weighted KPIs by facility (SQLite)
SELECT facility,
       SUM(orders_received) AS orders_received,
       SUM(orders_processed) AS orders_processed,
       ROUND(1.0 * SUM(orders_processed) / NULLIF(SUM(actual_labor_hours), 0), 2) AS orders_per_labor_hour,
       ROUND(100.0 * SUM(on_time_orders) / NULLIF(SUM(orders_processed), 0), 2) AS on_time_pct,
       ROUND(100.0 * SUM(actual_staff) / NULLIF(SUM(scheduled_staff), 0), 2) AS staffing_coverage_pct,
       ROUND(1000000.0 * SUM(defect_count) / NULLIF(SUM(orders_processed), 0), 1) AS defects_per_million_processed
FROM fulfillment_operations
GROUP BY facility
ORDER BY on_time_pct DESC;
