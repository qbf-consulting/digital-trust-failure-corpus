import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
ADMISSION = ROOT / "research/consumer-protection/cpc-001-agent-delegation-revocation/evidence/non-synthetic-implementation-admission.yaml"
GUIDE = ROOT / "research/consumer-protection/cpc-001-agent-delegation-revocation/evidence/non-synthetic-implementation-admission-guide.md"


class CPC001NonSyntheticAdmissionTests(unittest.TestCase):
    def _text(self):
        return ADMISSION.read_text(encoding="utf-8")

    def test_admission_is_not_started_and_no_target_is_selected(self):
        text = self._text()
        self.assertIn('status: "ADMISSION_NOT_STARTED"', text)
        self.assertIn("non_synthetic_implementation_selected: false", text)
        self.assertIn("non_synthetic_implementation_evidence_present: false", text)
        self.assertIn('current_value: "NOT_ADMITTED"', text)

    def test_mandatory_admission_requirements_are_present(self):
        text = self._text()
        for requirement_id in [
            "NSI-001",
            "NSI-002",
            "NSI-003",
            "NSI-004",
            "NSI-005",
            "NSI-006",
            "NSI-007",
            "NSI-008",
        ]:
            self.assertIn(requirement_id, text)

    def test_prohibited_claims_prevent_premature_assurance(self):
        text = self._text()
        for phrase in [
            "product or service safety",
            "consumer usability",
            "ARPA conformance",
            "RAHP assessment completion",
            "independent reproduction",
            "non-synthetic implementation has passed CPC-001",
        ]:
            self.assertIn(phrase, text)

    def test_next_gate_requires_completed_binding_record(self):
        text = self._text()
        self.assertIn('required_artifact: "completed non-synthetic implementation binding record"', text)
        self.assertIn("non_synthetic_implementation_selected: true", text)
        self.assertIn("non_synthetic_implementation_evidence_present: true", text)
        self.assertIn('minimum_admission_result: "ADMITTED_FOR_NON_SYNTHETIC_TESTING"', text)

    def test_guide_keeps_synthetic_fixture_out_of_non_synthetic_evidence(self):
        text = GUIDE.read_text(encoding="utf-8")
        self.assertIn("repository-owned safe fixture", text)
        self.assertIn("repository-owned deliberately defective fixture", text)
        self.assertIn("not non-synthetic implementation evidence", text)
        self.assertIn("NOT_ADMITTED", text)


if __name__ == "__main__":
    unittest.main()
