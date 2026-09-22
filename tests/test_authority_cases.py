import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "failure-case.schema.json"
AUTHORITY_DIR = ROOT / "corpus" / "authority"
LICENSE_POLICY_PATH = ROOT / "licensing" / "artifact-license-policy.json"


class AuthorityCorpusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.validator = Draft202012Validator(cls.schema)
        cls.case_paths = sorted(AUTHORITY_DIR.glob("DTF-*.json"))
        cls.cases = [json.loads(path.read_text(encoding="utf-8")) for path in cls.case_paths]

    def test_authority_family_contains_expected_cases(self):
        self.assertEqual(
            [case["id"] for case in self.cases],
            [
                "DTF-001", "DTF-002", "DTF-003",
                "DTF-013", "DTF-014", "DTF-015", "DTF-016",
                "DTF-017", "DTF-018", "DTF-019",
            ],
        )

    def test_all_authority_cases_validate(self):
        for path, case in zip(self.case_paths, self.cases):
            with self.subTest(case=case["id"]):
                errors = list(self.validator.iter_errors(case))
                self.assertEqual(errors, [], f"{path} failed schema validation: {errors}")

    def test_failure_cases_never_allow_pass(self):
        for case in self.cases:
            with self.subTest(case=case["id"]):
                self.assertEqual(case["expected"]["dispositions"]["PASS"], "prohibited")

    def test_cases_keep_falsification_and_evidence_explicit(self):
        for case in self.cases:
            with self.subTest(case=case["id"]):
                self.assertGreaterEqual(len(case["evidence_required"]), 1)
                self.assertGreaterEqual(len(case["falsification"]), 1)

    def test_machine_readable_corpus_is_apache_licensed(self):
        policy = json.loads(LICENSE_POLICY_PATH.read_text(encoding="utf-8"))
        guidance = policy["path_guidance"]
        apache_paths = {
            path
            for rule in guidance
            if rule["license"] == "Apache-2.0"
            for path in rule["paths"]
        }
        self.assertIn("corpus/**", apache_paths)


if __name__ == "__main__":
    unittest.main()
