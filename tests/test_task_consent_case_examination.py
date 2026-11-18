"""Task-consent full 37-case comparison negative and falsification controls."""
import copy
import json
import unittest
from tools.validate_trust_tasks_inventory import MANIFEST
from tools.validate_task_consent_case_examination import PATH, check

class TaskConsentCaseExaminationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(PATH.read_text())
        cls.inventory = json.loads(MANIFEST.read_text())
    def invalid(self, data):
        with self.assertRaises(ValueError):
            check(data, self.inventory)
    def test_complete_family(self):
        summary = check(self.data, self.inventory)
        self.assertEqual(summary["versions"], 4)
        self.assertEqual(summary["comparisons"], 148)
        self.assertEqual(summary["independently_accepted"], 0)
    def test_case_missing(self):
        x = copy.deepcopy(self.data); x["records"][0]["decisions"].pop(); self.invalid(x)
    def test_case_duplicated(self):
        x = copy.deepcopy(self.data); x["records"][0]["decisions"][0]["case_id"] = x["records"][0]["decisions"][1]["case_id"]; self.invalid(x)
    def test_version_missing(self):
        x = copy.deepcopy(self.data); x["records"].pop(); self.invalid(x)
    def test_source_drift(self):
        x = copy.deepcopy(self.data); x["records"][1]["source_blob"] = "0"*40; self.invalid(x)
    def test_wrong_case_baseline(self):
        x = copy.deepcopy(self.data); x["dtfc_case_revision"] = "not-a-commit"; self.invalid(x)
    def test_false_independent_review(self):
        x = copy.deepcopy(self.data); x["records"][0]["independent_acceptance"] = "completed"; self.invalid(x)
    def test_false_no_match(self):
        x = copy.deepcopy(self.data); x["records"][0]["decisions"][0]["disposition"] = "reviewed-no-match"; self.invalid(x)
    def test_candidate_without_test(self):
        x = copy.deepcopy(self.data)
        next(d for d in x["records"][0]["decisions"] if d["disposition"] == "conditional-candidate")["test_hypothesis"] = ""
        self.invalid(x)
    def test_missing_version_delta(self):
        x = copy.deepcopy(self.data); x["records"][1].pop("version_delta"); self.invalid(x)
    def test_no_automatic_minor_equivalence(self):
        x = copy.deepcopy(self.data); x["records"][1]["version_delta"]["claim"] = "0.2 is unchanged."; self.invalid(x)
    def test_claimed_target_execution(self):
        x = copy.deepcopy(self.data); x["records"][2]["target_execution"] = "independent-target"; self.invalid(x)

if __name__ == "__main__":
    unittest.main()
