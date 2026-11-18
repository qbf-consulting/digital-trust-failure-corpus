"""Prevent invented ACL review completeness and mapping evidence."""
import copy
import json
import unittest
from tools.validate_acl_review import PATH, MANIFEST, check


class ACLReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(PATH.read_text())
        cls.inventory = json.loads(MANIFEST.read_text())

    def test_acl_review_scope(self):
        self.assertEqual(check(self.data, self.inventory)["history_source_delta_screened"], 13)

    def test_missing_current_mapping(self):
        data = copy.deepcopy(self.data)
        data["current"].pop()
        with self.assertRaises(ValueError):
            check(data, self.inventory)

    def test_historical_promotion(self):
        data = copy.deepcopy(self.data)
        data["historical"][0]["review_state"] = "reviewed-mapped"
        with self.assertRaises(ValueError):
            check(data, self.inventory)

    def test_forged_source_blob(self):
        data = copy.deepcopy(self.data)
        data["current"][0]["source_blob"] = "0" * 40
        with self.assertRaises(ValueError):
            check(data, self.inventory)

    def test_forged_independent_execution(self):
        data = copy.deepcopy(self.data)
        data["current"][0]["execution_evidence"] = "verified"
        with self.assertRaises(ValueError):
            check(data, self.inventory)

    def test_missing_historical_version(self):
        data = copy.deepcopy(self.data)
        data["historical"].pop()
        with self.assertRaises(ValueError):
            check(data, self.inventory)

    def test_unknown_case(self):
        data = copy.deepcopy(self.data)
        data["current"][0]["case_id"] = "DTF-999"
        with self.assertRaises(ValueError):
            check(data, self.inventory)


if __name__ == "__main__":
    unittest.main()
