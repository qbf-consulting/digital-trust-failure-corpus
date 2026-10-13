import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
EVIDENCE_DIR = ROOT / "research/consumer-protection/cpc-001-agent-delegation-revocation/evidence"
TEMPLATE = EVIDENCE_DIR / "independent-reproduction-record-template.yaml"
GUIDE = EVIDENCE_DIR / "independent-reproduction-guide.md"


class CPC001IndependentReproductionTemplateTests(unittest.TestCase):
    def test_template_exists_and_is_not_marked_executed(self):
        text = TEMPLATE.read_text(encoding="utf-8")
        self.assertIn('record_type: "cpc-001-independent-reproduction-record"', text)
        self.assertIn('status: "TEMPLATE_NOT_EXECUTED"', text)
        self.assertIn("independent_reproduction_completed: false", text)

    def test_template_requires_reviewer_independence_statement(self):
        text = TEMPLATE.read_text(encoding="utf-8")
        self.assertIn("relationship_to_author", text)
        self.assertIn("independence_statement", text)
        self.assertIn("independent | same-organization | original-author | unknown", text)

    def test_template_preserves_assurance_boundary(self):
        text = TEMPLATE.read_text(encoding="utf-8")
        for prohibited in [
            "Production product or service safety",
            "Consumer usability validation",
            "ARPA conformance",
            "RAHP assessment",
            "Non-synthetic implementation evidence",
        ]:
            self.assertIn(prohibited, text)

    def test_guide_states_self_run_is_not_independent(self):
        text = GUIDE.read_text(encoding="utf-8")
        self.assertIn("A self-run by the original authoring path", text)
        self.assertIn("is not independent reproduction", text)

    def test_guide_requires_failed_reproduction_to_be_retained(self):
        text = GUIDE.read_text(encoding="utf-8")
        self.assertIn("If reproduction fails, the result should not be discarded", text)
        self.assertIn("A failed reproduction is evidence", text)


if __name__ == "__main__":
    unittest.main()
