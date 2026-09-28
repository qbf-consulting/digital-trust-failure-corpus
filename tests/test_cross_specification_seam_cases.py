import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PATHS = {
    "DTF-020": ROOT / "corpus" / "composition" / "DTF-020.json",
    "DTF-021": ROOT / "corpus" / "composition" / "DTF-021.json",
    "DTF-022": ROOT / "corpus" / "composition" / "DTF-022.json",
    "DTF-023": ROOT / "corpus" / "composition" / "DTF-023.json",
    "DTF-024": ROOT / "corpus" / "composition" / "DTF-024.json",
    "DTF-025": ROOT / "corpus" / "evidence" / "DTF-025.json",
    "DTF-026": ROOT / "corpus" / "evidence" / "DTF-026.json",
    "DTF-027": ROOT / "corpus" / "evidence" / "DTF-027.json",
}


class CrossSpecificationSeamTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = {
            case_id: json.loads(path.read_text(encoding="utf-8"))
            for case_id, path in PATHS.items()
        }

    def test_cross_specification_ids_are_complete(self):
        self.assertEqual(sorted(self.cases), [f"DTF-{n:03d}" for n in range(20, 28)])

    def test_all_cross_specification_failures_prohibit_pass(self):
        for case_id, case in self.cases.items():
            with self.subTest(case=case_id):
                self.assertEqual(case["expected"]["dispositions"]["PASS"], "prohibited")

    def test_semantic_ownership_requires_composition_policy_and_provenance(self):
        case = self.cases["DTF-020"]
        categories = {x["category"] for x in case["evidence_required"]}
        self.assertTrue({"composition", "policy", "provenance"} <= categories)

    def test_cross_stage_lifecycle_case_preserves_time_and_freshness(self):
        case = self.cases["DTF-021"]
        categories = {x["category"] for x in case["evidence_required"]}
        self.assertTrue({"lifecycle-state", "temporal", "freshness", "composition"} <= categories)

    def test_context_binding_does_not_establish_execution(self):
        case = self.cases["DTF-022"]
        statement = case["proposition"]["statement"].lower()
        self.assertIn("must not", statement)
        self.assertIn("execution", statement)
        self.assertIn("binding", statement)

    def test_component_pass_does_not_imply_composition_pass(self):
        case = self.cases["DTF-023"]
        statement = case["proposition"]["statement"].lower()
        self.assertIn("must not automatically imply pass", statement)

    def test_quorum_case_requires_independence_evidence(self):
        case = self.cases["DTF-024"]
        self.assertIn("false-independence", case["failure_classes"])
        categories = {x["category"] for x in case["evidence_required"]}
        self.assertTrue({"composition", "provenance", "relationship"} <= categories)

    def test_provenance_depth_is_not_assurance_depth(self):
        case = self.cases["DTF-025"]
        falsification = " ".join(x["condition"].lower() for x in case["falsification"])
        self.assertIn("longer", falsification)
        self.assertIn("independent corroboration", falsification)

    def test_valid_subset_is_not_automatically_complete(self):
        case = self.cases["DTF-026"]
        statement = case["proposition"]["statement"].lower()
        self.assertIn("individually valid", statement)
        self.assertIn("complete evidentiary basis", statement)

    def test_workflow_success_is_not_assurance_success(self):
        case = self.cases["DTF-027"]
        statement = case["proposition"]["statement"].lower()
        for term in ("workflow", "schema validation", "ci", "substantive trust"):
            self.assertIn(term, statement)


if __name__ == "__main__":
    unittest.main()
