import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "failure-case.schema.json"

CASE_PATHS = [
    ROOT / "corpus" / "authority" / "DTF-028.json",
    ROOT / "corpus" / "evidence" / "DTF-029.json",
    ROOT / "corpus" / "evidence" / "DTF-030.json",
    ROOT / "corpus" / "lifecycle" / "DTF-031.json",
]


class DecisionResolutionCorpusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.validator = Draft202012Validator(schema)
        cls.cases = {
            case["id"]: case
            for case in (
                json.loads(path.read_text(encoding="utf-8"))
                for path in CASE_PATHS
            )
        }

    def test_cases_are_reserved_028_through_031(self):
        self.assertEqual(
            sorted(self.cases),
            ["DTF-028", "DTF-029", "DTF-030", "DTF-031"],
        )

    def test_all_cases_validate_against_existing_schema(self):
        for case_id, case in self.cases.items():
            with self.subTest(case=case_id):
                self.assertEqual(list(self.validator.iter_errors(case)), [])

    def test_all_failure_cases_prohibit_pass(self):
        for case_id, case in self.cases.items():
            with self.subTest(case=case_id):
                self.assertEqual(
                    case["expected"]["dispositions"]["PASS"],
                    "prohibited",
                )

    def test_authority_laundering_is_broader_than_reputation_substitution(self):
        case = self.cases["DTF-028"]
        proposition = case["proposition"]["statement"].lower()
        for term in (
            "repetition",
            "consensus",
            "endorsement",
            "aggregation",
            "projection",
            "discovery",
            "reputation",
            "capability",
            "unrelated authority",
        ):
            self.assertIn(term, proposition)

    def test_decision_basis_case_separates_authority_from_other_causes(self):
        case = self.cases["DTF-029"]
        statement = case["proposition"]["statement"].lower()
        for term in (
            "evidence",
            "policy",
            "lifecycle",
            "correction",
            "evaluation context",
        ):
            self.assertIn(term, statement)
        self.assertIn("authority change", statement)

    def test_silent_resolution_rejects_workflow_progression_as_resolution(self):
        case = self.cases["DTF-030"]
        falsification = " ".join(
            item["condition"].lower() for item in case["falsification"]
        )
        self.assertIn("workflow progression", falsification)
        self.assertIn("peer pressure", falsification)
        self.assertIn("resolution basis", falsification)

    def test_false_persistence_requires_current_resolution_evidence(self):
        case = self.cases["DTF-031"]
        categories = {x["category"] for x in case["evidence_required"]}
        self.assertTrue({"freshness", "policy", "provenance", "lifecycle-state"} <= categories)
        statement = case["proposition"]["statement"].lower()
        self.assertIn("current admissible evidence", statement)

    def test_upstream_research_provenance_is_preserved_without_dependency_claim(self):
        for case_id, case in self.cases.items():
            with self.subTest(case=case_id):
                locators = {ref["locator"] for ref in case["references"]}
                self.assertIn(
                    "https://github.com/JessHines360/protocol-of-care-for-agents",
                    locators,
                )
                self.assertIn(
                    "https://github.com/JessHines360/protocol-of-care-for-agents/blob/main/experiments/SIMULATION_01_RUNBOOK.md",
                    locators,
                )
                notes = " ".join(ref.get("note", "") for ref in case["references"]).lower()
                self.assertIn("not a normative dependency", notes)


if __name__ == "__main__":
    unittest.main()
