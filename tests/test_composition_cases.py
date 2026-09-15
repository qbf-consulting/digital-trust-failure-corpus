import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "failure-case.schema.json"
COMPOSITION_DIR = ROOT / "corpus" / "composition"


class CompositionCorpusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.validator = Draft202012Validator(schema)
        cls.case_paths = sorted(COMPOSITION_DIR.glob("DTF-*.json"))
        cls.cases = [json.loads(path.read_text(encoding="utf-8")) for path in cls.case_paths]

    def test_composition_tranche_contains_expected_cases(self):
        self.assertEqual([case["id"] for case in self.cases], ["DTF-007", "DTF-008", "DTF-009"])

    def test_all_composition_cases_validate(self):
        for path, case in zip(self.case_paths, self.cases):
            with self.subTest(case=case["id"]):
                self.assertEqual(list(self.validator.iter_errors(case)), [], f"{path} failed schema validation")

    def test_composition_failures_prohibit_pass(self):
        for case in self.cases:
            with self.subTest(case=case["id"]):
                self.assertEqual(case["expected"]["dispositions"]["PASS"], "prohibited")

    def test_false_independence_requires_composition_and_provenance(self):
        case = next(case for case in self.cases if case["id"] == "DTF-007")
        categories = {item["category"] for item in case["evidence_required"]}
        self.assertTrue({"composition", "provenance"}.issubset(categories))

    def test_conflict_case_is_explicitly_non_pass(self):
        case = next(case for case in self.cases if case["id"] == "DTF-008")
        self.assertIn("conflicting-evidence", case["failure_classes"])
        self.assertEqual(case["expected"]["dispositions"]["PASS"], "prohibited")

    def test_transitivity_case_requires_policy_and_relationship_evidence(self):
        case = next(case for case in self.cases if case["id"] == "DTF-009")
        categories = {item["category"] for item in case["evidence_required"]}
        self.assertTrue({"policy", "relationship", "composition"}.issubset(categories))


if __name__ == "__main__":
    unittest.main()
