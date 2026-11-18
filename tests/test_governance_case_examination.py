"""Adversarial assertions for complete governance-capability case accounting."""
import copy
import json
import unittest
from tools.validate_trust_tasks_inventory import MANIFEST
from tools.validate_governance_case_examination import PATH, check

class GovernanceCaseExaminationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(PATH.read_text())
        cls.inventory = json.loads(MANIFEST.read_text())
    def reject(self, data):
        with self.assertRaises(ValueError):
            check(data, self.inventory)
    def test_full_matrix(self):
        x = check(self.data, self.inventory)
        self.assertEqual((x["versions"], x["comparisons"], x["independently_accepted"]), (3, 111, 0))
    def test_missing_case_fails(self):
        x = copy.deepcopy(self.data); x["records"][0]["decisions"].pop(); self.reject(x)
    def test_duplicate_case_fails(self):
        x = copy.deepcopy(self.data); x["records"][0]["decisions"][0]["case_id"] = x["records"][0]["decisions"][1]["case_id"]; self.reject(x)
    def test_missing_version_fails(self):
        x = copy.deepcopy(self.data); x["records"].pop(); self.reject(x)
    def test_source_drift_fails(self):
        x = copy.deepcopy(self.data); x["records"][1]["schema_blob"] = "0"*40; self.reject(x)
    def test_false_no_match_fails(self):
        x = copy.deepcopy(self.data); x["records"][0]["decisions"][0]["disposition"] = "reviewed-no-match"; self.reject(x)
    def test_false_independent_acceptance_fails(self):
        x = copy.deepcopy(self.data); x["records"][0]["independent_acceptance"] = "completed"; self.reject(x)
    def test_missing_boundary_fails(self):
        x = copy.deepcopy(self.data)
        next(d for d in x["records"][1]["decisions"] if d["disposition"] == "conditional-candidate")["authority_boundary"] = ""
        self.reject(x)
    def test_wrong_source_pin_fails(self):
        x = copy.deepcopy(self.data); x["upstream"]["commit"] = "0"*40; self.reject(x)

if __name__ == "__main__":
    unittest.main()
