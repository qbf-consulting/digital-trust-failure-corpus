import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "failure-case.schema.json"
LIFECYCLE_DIR = ROOT / "corpus" / "lifecycle"


class LifecycleCorpusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.validator = Draft202012Validator(schema)
        cls.case_paths = sorted(LIFECYCLE_DIR.glob("DTF-*.json"))
        cls.cases = [json.loads(path.read_text(encoding="utf-8")) for path in cls.case_paths]

    def test_lifecycle_tranche_contains_expected_cases(self):
        self.assertEqual([case["id"] for case in self.cases], ["DTF-004", "DTF-005", "DTF-006"])

    def test_all_lifecycle_cases_validate(self):
        for path, case in zip(self.case_paths, self.cases):
            with self.subTest(case=case["id"]):
                errors = list(self.validator.iter_errors(case))
                self.assertEqual(errors, [], f"{path} failed schema validation: {errors}")

    def test_lifecycle_failures_prohibit_pass(self):
        for case in self.cases:
            with self.subTest(case=case["id"]):
                self.assertEqual(case["expected"]["dispositions"]["PASS"], "prohibited")

    def test_lifecycle_cases_require_temporal_and_lifecycle_evidence(self):
        for case in self.cases:
            categories = {item["category"] for item in case["evidence_required"]}
            with self.subTest(case=case["id"]):
                self.assertIn("lifecycle-state", categories)
                self.assertIn("temporal", categories)

    def test_historical_validity_case_is_explicit(self):
        case = next(case for case in self.cases if case["id"] == "DTF-006")
        self.assertIn("historical-validity", case["failure_classes"])
        self.assertIn("historical", case["proposition"]["statement"].lower())


if __name__ == "__main__":
    unittest.main()
