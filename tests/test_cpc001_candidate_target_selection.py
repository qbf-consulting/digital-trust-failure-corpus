import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
REGISTER = ROOT / "research/consumer-protection/cpc-001-agent-delegation-revocation/evidence/candidate-target-selection-register.yaml"
GUIDE = ROOT / "research/consumer-protection/cpc-001-agent-delegation-revocation/evidence/candidate-target-selection-guide.md"


class CPC001CandidateTargetSelectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.register_text = REGISTER.read_text(encoding="utf-8")
        cls.guide_text = GUIDE.read_text(encoding="utf-8")

    def test_register_is_not_started_or_admitted(self):
        self.assertIn("status: CANDIDATE_SELECTION_NOT_STARTED", self.register_text)
        self.assertIn("candidate_target_selected: false", self.register_text)
        self.assertIn("candidate_target_admitted: false", self.register_text)
        self.assertIn("non_synthetic_evidence_present: false", self.register_text)
        self.assertIn("candidate_records: []", self.register_text)

    def test_register_preserves_current_evidence_boundary(self):
        self.assertIn("executed-synthetic-target", self.register_text)
        self.assertIn("ci-executed-synthetic-target", self.register_text)
        self.assertIn("non-synthetic-implementation", self.register_text)
        self.assertIn("completed-rahp-assessment", self.register_text)
        self.assertIn("consumer-usability-validation", self.register_text)

    def test_selection_principles_require_action_specific_authorization(self):
        self.assertIn("protected action boundary must be concrete", self.register_text)
        self.assertIn("authorization evaluation point", self.register_text)
        self.assertIn("revocation enforcement point", self.register_text)
        self.assertIn("registry or identity evidence is not sufficient", self.register_text)

    def test_allowed_recommendations_do_not_include_supported_or_pass(self):
        self.assertIn("ADMIT_FOR_EXPERIMENTAL_BINDING", self.register_text)
        self.assertNotIn("SUPPORTED", self.register_text)
        self.assertNotIn("PASS", self.register_text)

    def test_current_claims_remain_prohibited(self):
        self.assertIn("CPC-001 has selected a non-synthetic implementation target.", self.register_text)
        self.assertIn("CPC-001 has admitted a non-synthetic implementation target.", self.register_text)
        self.assertIn("CPC-001 establishes product or service safety.", self.register_text)
        self.assertIn("CPC-001 has completed RAHP assessment.", self.register_text)
        self.assertIn("CPC-001 has completed independent reproduction.", self.register_text)

    def test_guide_discloses_candidate_metadata_is_not_evidence(self):
        self.assertIn("candidate selection not started", self.guide_text.lower())
        self.assertIn("Candidate review metadata is not execution evidence", self.guide_text)
        self.assertIn("the target satisfies CPC-001", self.guide_text)
        self.assertIn("the target enforces revocation correctly", self.guide_text)


if __name__ == "__main__":
    unittest.main()
