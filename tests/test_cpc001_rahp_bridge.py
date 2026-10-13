import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
BRIDGE = ROOT / "research/consumer-protection/cpc-001-agent-delegation-revocation/evidence/rahp-assessment-bridge.yaml"
GUIDE = ROOT / "research/consumer-protection/cpc-001-agent-delegation-revocation/evidence/rahp-assessment-guide.md"


class CPC001RahpBridgeTests(unittest.TestCase):
    def test_bridge_exists_and_is_not_executed(self):
        text = BRIDGE.read_text(encoding="utf-8")
        self.assertIn('status: BRIDGE_NOT_EXECUTED', text)
        self.assertIn('rahp_assessment_completed: false', text)

    def test_bridge_preserves_current_evidence_limits(self):
        text = BRIDGE.read_text(encoding="utf-8")
        self.assertIn('executed-synthetic-target', text)
        self.assertIn('ci-executed-synthetic-target', text)
        self.assertIn('independent-reproduction', text)
        self.assertIn('non-synthetic-implementation', text)
        self.assertIn('consumer-usability-validation', text)

    def test_bridge_disallows_overclaim_dispositions(self):
        text = BRIDGE.read_text(encoding="utf-8")
        for prohibited in [
            'PRODUCTION_SAFE',
            'INDEPENDENTLY_REPRODUCED',
            'ARPA_CONFORMANT',
            'RAHP_ASSESSED',
            'CONSUMER_USABILITY_VALIDATED',
        ]:
            self.assertIn(prohibited, text)

    def test_consumer_inspection_and_challenge_remain_not_assessed(self):
        text = BRIDGE.read_text(encoding="utf-8")
        self.assertIn('claim_id: C2', text)
        self.assertIn('claim_id: C7', text)
        self.assertIn('current_assessment_state: NOT_ASSESSED', text)

    def test_guide_states_that_it_is_not_an_assessment_result(self):
        text = GUIDE.read_text(encoding="utf-8")
        self.assertIn('assessment bridge, not an assessment result', text)
        self.assertIn('It does not claim that RAHP has executed', text)


if __name__ == "__main__":
    unittest.main()
