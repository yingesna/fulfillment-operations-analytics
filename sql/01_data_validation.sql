-- SQLite: run after importing data/fulfillment_operations.csv as fulfillment_operations
SELECT COUNT(*) AS records, COUNT(DISTINCT facility) AS facilities,
       MIN(date) AS first_day, MAX(date) AS last_day
FROM fulfillment_operations;

-- Expect zero invalid records
SELECT *
FROM fulfillment_operations
WHERE actual_staff < 0 OR scheduled_staff <= 0
   OR orders_received < 0 OR orders_processed < 0
   OR on_time_orders > orders_processed
   OR defect_count > orders_processed OR backlog_orders < 0;
