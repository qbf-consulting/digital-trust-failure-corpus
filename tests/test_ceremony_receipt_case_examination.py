"""Adversarial case-accounting and evidentiary controls for ceremony receipts."""
import copy
import json
import unittest
from tools.validate_trust_tasks_inventory import MANIFEST
from tools.validate_ceremony_receipt_case_examination import PATH, check

class CeremonyReceiptExaminationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(PATH.read_text())
        cls.inventory = json.loads(MANIFEST.read_text())

    def invalid(self, data):
        with self.assertRaises(ValueError):
            check(data, self.inventory)

    def test_complete_source_case_matrix(self):
        x = check(self.data, self.inventory)
        self.assertEqual((x["versions"], x["comparisons"]), (1, 37))
        self.assertEqual((x["conditional_candidates"], x["not_established_from_task"]), (17, 20))
        self.assertEqual(x["independently_accepted"], 0)

    def test_no_completion_from_recorder_echo(self):
        for case in ("DTF-010", "DTF-026", "DTF-027", "DTF-030"):
            with self.subTest(case=case):
                d = next(x for x in self.data["records"][0]["decisions"] if x["case_id"] == case)
                self.assertEqual(d["disposition"], "conditional-candidate")

    def test_threshold_requires_actual_approval_case(self):
        d = next(x for x in self.data["records"][0]["decisions"] if x["case_id"] == "DTF-024")
        self.assertIn("approval steps", d["rationale"])

    def test_invalid_case_version_rejected(self):
        d = copy.deepcopy(self.data)
        d["records"][0]["decisions"][0]["case_version"] = "0.2.0"
        self.invalid(d)

    def test_missing_case_rejected(self):
        d = copy.deepcopy(self.data)
        d["records"][0]["decisions"].pop()
        self.invalid(d)

    def test_duplicate_case_rejected(self):
        d = copy.deepcopy(self.data)
        d["records"][0]["decisions"][0]["case_id"] = d["records"][0]["decisions"][1]["case_id"]
        self.invalid(d)

    def test_wrong_source_blob_rejected(self):
        d = copy.deepcopy(self.data)
        d["records"][0]["source_blob"] = "0"*40
        self.invalid(d)

    def test_unjustified_review_promotion_rejected(self):
        d = copy.deepcopy(self.data)
        d["records"][0]["independent_acceptance"] = "completed"
        self.invalid(d)

    def test_missing_candidate_boundary_rejected(self):
        d = copy.deepcopy(self.data)
        next(x for x in d["records"][0]["decisions"] if x["disposition"] == "conditional-candidate")["authority_boundary"] = ""
        self.invalid(d)

    def test_unjustified_no_match_rejected(self):
        d = copy.deepcopy(self.data)
        d["records"][0]["decisions"][0]["disposition"] = "reviewed-no-match"
        self.invalid(d)

if __name__ == "__main__":
    unittest.main()
