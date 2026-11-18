"""Adversarial inventory validation, including omission and false-success guards."""
import copy
import json
import unittest
from tools.validate_trust_tasks_inventory import MANIFEST, PILOT, check


class TestTrustTasksInventory(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(MANIFEST.read_text())
        cls.pilot = json.loads(PILOT.read_text())

    def test_pinned_inventory_and_sample(self):
        counts = check(self.data, self.pilot)
        self.assertEqual(counts["sample-screened"], 12)
        self.assertEqual(counts["needs-review"], 1379)

    def test_missing_entry_fails(self):
        data = copy.deepcopy(self.data)
        data["records"].pop()
        with self.assertRaises(ValueError):
            check(data, self.pilot)

    def test_duplicate_entry_fails(self):
        data = copy.deepcopy(self.data)
        data["records"][1] = copy.deepcopy(data["records"][0])
        with self.assertRaises(ValueError):
            check(data, self.pilot)

    def test_unpinned_revision_fails(self):
        data = copy.deepcopy(self.data)
        data["source"]["commit"] = "main"
        with self.assertRaises(ValueError):
            check(data, self.pilot)

    def test_forged_provenance_fails(self):
        data = copy.deepcopy(self.data)
        data["records"][0]["spec_blob"] = "unverified"
        with self.assertRaises(ValueError):
            check(data, self.pilot)

    def test_false_review_promotion_fails(self):
        data = copy.deepcopy(self.data)
        data["records"][0]["review_state"] = "reviewed-mapped"
        with self.assertRaises(ValueError):
            check(data, self.pilot)

    def test_pilot_reconciliation_fails_closed(self):
        data = copy.deepcopy(self.data)
        row = next(x for x in data["records"] if x["review_state"] == "sample-screened")
        row["review_state"] = "needs-review"
        with self.assertRaises(ValueError):
            check(data, self.pilot)


if __name__ == "__main__":
    unittest.main()
