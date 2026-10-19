-- Explore associations, not causal proof. Compare daily staffing coverage bands.
WITH daily AS (
  SELECT *,
         CASE WHEN 1.0 * actual_staff / NULLIF(scheduled_staff, 0) < 0.90
              THEN 'Below 90%' ELSE '90% or higher' END AS staffing_band
  FROM fulfillment_operations
)
SELECT staffing_band, COUNT(*) AS facility_days,
       ROUND(100.0 * SUM(on_time_orders) / NULLIF(SUM(orders_processed), 0), 2) AS on_time_pct,
       ROUND(1.0 * SUM(orders_processed) / NULLIF(SUM(actual_labor_hours), 0), 2) AS orders_per_labor_hour,
       ROUND(1.0 * SUM(backlog_orders) / NULLIF(SUM(orders_received), 0), 3) AS backlog_to_daily_intake_ratio
FROM daily
GROUP BY staffing_band;
