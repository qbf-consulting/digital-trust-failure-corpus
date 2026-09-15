import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "failure-case.schema.json"
EVIDENCE_DIR = ROOT / "corpus" / "evidence"


class EvidenceCorpusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.validator = Draft202012Validator(schema)
        cls.case_paths = sorted(EVIDENCE_DIR.glob("DTF-*.json"))
        cls.cases = [json.loads(path.read_text(encoding="utf-8")) for path in cls.case_paths]

    def test_evidence_tranche_contains_expected_cases(self):
        self.assertEqual([case["id"] for case in self.cases], ["DTF-010", "DTF-011", "DTF-012"])

    def test_all_evidence_cases_validate(self):
        for path, case in zip(self.case_paths, self.cases):
            with self.subTest(case=case["id"]):
                self.assertEqual(list(self.validator.iter_errors(case)), [], f"{path} failed schema validation")

    def test_evidence_failures_prohibit_pass(self):
        for case in self.cases:
            with self.subTest(case=case["id"]):
                self.assertEqual(case["expected"]["dispositions"]["PASS"], "prohibited")

    def test_missing_evidence_case_is_explicit(self):
        case = next(case for case in self.cases if case["id"] == "DTF-010")
        self.assertIn("missing-evidence", case["failure_classes"])
        self.assertIn("absence", case["proposition"]["statement"].lower())

    def test_freshness_case_requires_freshness_and_temporal_evidence(self):
        case = next(case for case in self.cases if case["id"] == "DTF-011")
        categories = {item["category"] for item in case["evidence_required"]}
        self.assertTrue({"freshness", "temporal"}.issubset(categories))

    def test_policy_mismatch_case_requires_policy_and_provenance(self):
        case = next(case for case in self.cases if case["id"] == "DTF-012")
        categories = {item["category"] for item in case["evidence_required"]}
        self.assertIn("policy-mismatch", case["failure_classes"])
        self.assertTrue({"policy", "provenance"}.issubset(categories))


if __name__ == "__main__":
    unittest.main()
