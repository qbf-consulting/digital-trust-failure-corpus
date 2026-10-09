"""Validate primary-source record dispositions and two case-specific reference bindings."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class InspectedRecordsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT / "research/external-sources/inspected-record-dispositions.json").read_text())

    def test_eight_records_across_three_families(self):
        records = self.data["records"]
        self.assertEqual(len(records), 8)
        self.assertEqual(len({r["family"] for r in records}), 3)
        self.assertEqual(len({(r["family"], r["id"]) for r in records}), 8)
        for record in records:
            self.assertTrue(record["url"].startswith("https://"))
            self.assertTrue(record["rights"])
            self.assertGreater(len(record["basis"]), 65)
            self.assertEqual(len(list((ROOT / "corpus").rglob(record["case_id"] + ".json"))), 1)

    def test_two_distinct_high_confidence_privacy_bindings(self):
        records = {r["id"]: r for r in self.data["records"]}
        self.assertEqual(records["T4"]["case_id"], "DTF-032")
        self.assertEqual(records["T18"]["case_id"], "DTF-035")
        for identifier in ("T4", "T18"):
            self.assertEqual(records[identifier]["disposition"], "direct-mechanism")
            self.assertIn("#t", records[identifier]["url"])

if __name__ == "__main__":
    unittest.main()
