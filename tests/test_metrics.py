"""Regression checks for the published fixed-seed executive summary."""
import unittest
from generate_data import generate
from analyze import summarize

class PublishedMetricsTests(unittest.TestCase):
    def test_fixed_seed_summary(self):
        rows = generate()
        total = lambda field: sum(r[field] for r in rows)
        self.assertEqual(total("orders_received"), 1141648)
        self.assertEqual(total("orders_processed"), 1058478)
        self.assertAlmostEqual(100 * total("on_time_orders") / total("orders_processed"), 81.26, delta=0.005)
        summary = summarize(rows)
        self.assertAlmostEqual(summary["FC-01"]["on_time_pct"], 82.31, delta=0.005)
        self.assertAlmostEqual(summary["FC-02"]["on_time_pct"], 80.73, delta=0.005)
        self.assertEqual([r for r in rows if r["facility"] == "FC-02"][-1]["backlog_orders"], 40476)

if __name__ == "__main__":
    unittest.main()
