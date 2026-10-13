import json
import pathlib
import unittest

try:
    import yaml
except ModuleNotFoundError:  # pragma: no cover
    yaml = None

ROOT = pathlib.Path(__file__).resolve().parents[1]
DETERMINATION = ROOT / "research/consumer-protection/cpc-001-agent-delegation-revocation/evidence/current-determination.yaml"


class CPC001DeterminationBoundaryTests(unittest.TestCase):
    def _load(self):
        self.assertIsNotNone(yaml, "PyYAML is required by repository validation")
        with DETERMINATION.open("r", encoding="utf-8") as handle:
            return yaml.safe_load(handle)

    def test_no_claim_is_fully_supported_by_synthetic_fixture(self):
        data = self._load()
        determinations = {claim["id"]: claim["assurance_determination"] for claim in data["claims"]}
        self.assertNotIn("SUPPORTED", determinations.values())

    def test_consumer_inspection_and_challenge_remain_unassessed(self):
        data = self._load()
        determinations = {claim["id"]: claim["assurance_determination"] for claim in data["claims"]}
        self.assertEqual(determinations["C2"], "NOT_ASSESSED")
        self.assertEqual(determinations["C7"], "NOT_ASSESSED")

    def test_stop_point_discloses_next_gate(self):
        data = self._load()
        self.assertTrue(data["current_stop_point"]["reached"])
        self.assertIn("GitHub Actions", data["current_stop_point"]["next_required_evidence_gate"])

    def test_non_claims_include_no_independent_reproduction(self):
        data = self._load()
        non_claims = "\n".join(data["explicit_non_claims"])
        self.assertIn("No independent reproduction", non_claims)
        self.assertIn("No ARPA conformance", non_claims)


if __name__ == "__main__":
    unittest.main()
