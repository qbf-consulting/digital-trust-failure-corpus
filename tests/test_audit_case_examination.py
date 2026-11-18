"""Test the exact source-bound audit Gate B research contract and false-success controls."""
import copy
import json
import unittest

from tools.validate_trust_tasks_inventory import MANIFEST
from tools.validate_audit_case_examination import PATH, check

class AuditCaseExaminationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(PATH.read_text())
        cls.inventory = json.loads(MANIFEST.read_text())

    def assert_invalid(self, data):
        with self.assertRaises(ValueError):
            check(data, self.inventory)

    def test_complete_case_matrix(self):
        result = check(self.data, self.inventory)
        self.assertEqual(result["case_comparisons"], 111)
        self.assertEqual(result["versions"], 3)
        self.assertEqual(result["independently_accepted"], 0)

    def test_missing_task_fails(self):
        data = copy.deepcopy(self.data)
        data["records"].pop()
        self.assert_invalid(data)

    def test_missing_case_fails(self):
        data = copy.deepcopy(self.data)
        data["records"][0]["decisions"].pop()
        self.assert_invalid(data)

    def test_duplicate_case_fails(self):
        data = copy.deepcopy(self.data)
        data["records"][0]["decisions"][1]["case_id"] = data["records"][0]["decisions"][0]["case_id"]
        self.assert_invalid(data)

    def test_wrong_source_blob_fails(self):
        data = copy.deepcopy(self.data)
        data["records"][1]["source_blob"] = "0"*40
        self.assert_invalid(data)

    def test_false_independent_acceptance_fails(self):
        data = copy.deepcopy(self.data)
        data["records"][0]["independent_acceptance"] = "completed"
        self.assert_invalid(data)

    def test_unsupported_no_match_fails(self):
        data = copy.deepcopy(self.data)
        data["records"][0]["decisions"][0]["disposition"] = "reviewed-no-match"
        self.assert_invalid(data)

    def test_candidate_without_test_fails(self):
        data = copy.deepcopy(self.data)
        next(x for x in data["records"][0]["decisions"] if x["disposition"] == "conditional-candidate")["test_hypothesis"] = ""
        self.assert_invalid(data)

    def test_historical_delta_removed_fails(self):
        data = copy.deepcopy(self.data)
        data["records"][1].pop("version_delta")
        self.assert_invalid(data)

    def test_upstream_pin_drift_fails(self):
        data = copy.deepcopy(self.data)
        data["upstream"]["commit"] = "0"*40
        self.assert_invalid(data)

if __name__ == "__main__":
    unittest.main()
