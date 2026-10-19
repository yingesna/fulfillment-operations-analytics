import unittest
from generate_data import generate

class SyntheticDataTests(unittest.TestCase):
    def test_reproducible(self):
        self.assertEqual(generate(), generate())

    def test_rows_and_facilities(self):
        rows = generate()
        self.assertEqual(len(rows), 270)
        self.assertEqual(len({r["facility"] for r in rows}), 3)

    def test_invariants_and_backlog_accounting(self):
        rows = generate()
        previous = {}
        for row in rows:
            facility = row["facility"]
            self.assertGreater(row["scheduled_staff"], 0)
            self.assertLessEqual(row["on_time_orders"], row["orders_processed"])
            self.assertLessEqual(row["defect_count"], row["orders_processed"])
            self.assertEqual(row["backlog_orders"], previous.get(facility, 0) + row["orders_received"] - row["orders_processed"])
            previous[facility] = row["backlog_orders"]

if __name__ == "__main__":
    unittest.main()
