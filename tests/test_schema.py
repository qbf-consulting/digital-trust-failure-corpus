import copy
import json
import pathlib
import unittest

from jsonschema import Draft202012Validator, ValidationError

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "failure-case.schema.json"
FIXTURE_PATH = ROOT / "tests" / "fixtures" / "valid" / "DTF-000.json"


class FailureCaseSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(cls.schema)
        cls.validator = Draft202012Validator(cls.schema)

    def test_canonical_fixture_validates(self):
        self.validator.validate(self.fixture)

    def test_missing_evidence_requirement_is_rejected(self):
        case = copy.deepcopy(self.fixture)
        case["evidence_required"] = []
        with self.assertRaises(ValidationError):
            self.validator.validate(case)

    def test_missing_falsification_condition_is_rejected(self):
        case = copy.deepcopy(self.fixture)
        case["falsification"] = []
        with self.assertRaises(ValidationError):
            self.validator.validate(case)

    def test_unknown_domain_is_rejected(self):
        case = copy.deepcopy(self.fixture)
        case["domains"] = ["invented-domain"]
        with self.assertRaises(ValidationError):
            self.validator.validate(case)

    def test_pass_cannot_be_only_safe_failure_disposition(self):
        case = copy.deepcopy(self.fixture)
        case["expected"]["dispositions"] = {
            "PASS": "allowed",
            "DENY": "prohibited",
            "INDETERMINATE": "prohibited",
        }
        with self.assertRaises(ValidationError):
            self.validator.validate(case)

    def test_disposition_cannot_be_simultaneously_allowed_and_prohibited(self):
        # The map representation gives every disposition exactly one state.
        # A list/object trying to express contradictory states is structurally invalid.
        case = copy.deepcopy(self.fixture)
        case["expected"]["dispositions"]["PASS"] = ["allowed", "prohibited"]
        with self.assertRaises(ValidationError):
            self.validator.validate(case)


if __name__ == "__main__":
    unittest.main()
