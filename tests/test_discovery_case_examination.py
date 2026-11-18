"""Negative controls for all-case discovery author research and changed versions."""
import copy
import json
import unittest
from tools.validate_trust_tasks_inventory import MANIFEST
from tools.validate_discovery_case_examination import PATH, check

class DiscoveryCaseExaminationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(PATH.read_text())
        cls.inventory = json.loads(MANIFEST.read_text())
    def reject(self, data):
        with self.assertRaises(ValueError):
            check(data, self.inventory)
    def test_reconciled_case_matrix(self):
        s = check(self.data, self.inventory)
        self.assertEqual((s["versions"], s["comparisons"], s["independently_accepted"]), (4, 148, 0))
    def test_missing_version(self):
        x = copy.deepcopy(self.data); x["records"].pop(); self.reject(x)
    def test_missing_case(self):
        x = copy.deepcopy(self.data); x["records"][0]["decisions"].pop(); self.reject(x)
    def test_duplicate_case(self):
        x = copy.deepcopy(self.data); x["records"][0]["decisions"][0]["case_id"] = x["records"][0]["decisions"][1]["case_id"]; self.reject(x)
    def test_wrong_source_sha(self):
        x = copy.deepcopy(self.data); x["records"][1]["source_blob"] = "0"*40; self.reject(x)
    def test_wrong_schema_sha(self):
        x = copy.deepcopy(self.data); x["records"][1]["schema_blob"] = "0"*40; self.reject(x)
    def test_false_reviewed_no_match(self):
        x = copy.deepcopy(self.data); x["records"][0]["decisions"][0]["disposition"] = "reviewed-no-match"; self.reject(x)
    def test_fabricated_independent_acceptance(self):
        x = copy.deepcopy(self.data); x["records"][0]["independent_acceptance"] = "completed"; self.reject(x)
    def test_fabricated_target_execution(self):
        x = copy.deepcopy(self.data); x["records"][2]["target_execution"] = "independent-target"; self.reject(x)
    def test_candidate_without_boundary(self):
        x = copy.deepcopy(self.data)
        next(d for d in x["records"][0]["decisions"] if d["disposition"] == "conditional-candidate")["authority_boundary"] = ""
        self.reject(x)
    def test_framework_version_is_not_policy_mismatch(self):
        for record in self.data["records"][:2]:
            case = next(x for x in record["decisions"] if x["case_id"] == "DTF-012")
            self.assertEqual(case["disposition"], "not-established-from-task")

    def test_first_time_required_ext_is_not_secondary_use(self):
        for record in self.data["records"]:
            case = next(x for x in record["decisions"] if x["case_id"] == "DTF-034")
            self.assertEqual(case["disposition"], "not-established-from-task")

    def test_temporal_version_specificity(self):
        for record in self.data["records"][2:]:
            case = next(x for x in record["decisions"] if x["case_id"] == "DTF-021")
            self.assertEqual(case["disposition"], "conditional-candidate")
            self.assertIn("window", case["authority_boundary"].lower())

    def test_missing_v04_delta(self):
        x = copy.deepcopy(self.data); x["records"][3].pop("version_delta"); self.reject(x)
    def test_wrong_expiry_version_delta(self):
        x = copy.deepcopy(self.data); x["records"][3]["version_delta"]["claim"] = "No temporal change."; self.reject(x)

if __name__ == "__main__":
    unittest.main()
