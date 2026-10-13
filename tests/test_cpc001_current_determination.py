import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
DETERMINATION = ROOT / "research/consumer-protection/cpc-001-agent-delegation-revocation/evidence/current-determination.yaml"


class CPC001DeterminationBoundaryTests(unittest.TestCase):
    def _text(self) -> str:
        return DETERMINATION.read_text(encoding="utf-8")

    def test_no_claim_is_fully_supported_by_synthetic_fixture(self):
        text = self._text()
        self.assertNotRegex(text, r"assurance_determination:\s+SUPPORTED\b")

    def test_consumer_inspection_and_challenge_remain_unassessed(self):
        text = self._text()
        self.assertRegex(text, r"id:\s+C2[\s\S]+?assurance_determination:\s+NOT_ASSESSED")
        self.assertRegex(text, r"id:\s+C7[\s\S]+?assurance_determination:\s+NOT_ASSESSED")

    def test_stop_point_discloses_next_gate(self):
        text = self._text()
        self.assertIn("reached: true", text)
        self.assertIn("GitHub Actions", text)

    def test_non_claims_include_no_independent_reproduction(self):
        text = self._text()
        self.assertIn("No independent reproduction", text)
        self.assertIn("No ARPA conformance", text)


if __name__ == "__main__":
    unittest.main()
