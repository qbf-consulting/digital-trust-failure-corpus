import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PATHS = {
    f"DTF-{n:03d}": ROOT / "corpus" / "privacy" / f"DTF-{n:03d}.json"
    for n in range(32, 38)
}


class PrivacyCorrelationCaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = {
            case_id: json.loads(path.read_text(encoding="utf-8"))
            for case_id, path in PATHS.items()
        }

    def test_privacy_tranche_ids_are_complete(self):
        self.assertEqual(sorted(self.cases), [f"DTF-{n:03d}" for n in range(32, 38)])

    def test_all_cases_are_privacy_cases_and_prohibit_pass(self):
        for case_id, case in self.cases.items():
            with self.subTest(case=case_id):
                self.assertIn("privacy", case["domains"])
                self.assertEqual(case["expected"]["dispositions"]["PASS"], "prohibited")

    def test_proof_mechanism_case_requires_cryptographic_and_composition_evidence(self):
        case = self.cases["DTF-032"]
        categories = {x["category"] for x in case["evidence_required"]}
        self.assertTrue({"cryptographic", "composition", "provenance"} <= categories)
        self.assertIn("correlation", case["failure_classes"])

    def test_status_resolution_case_tests_observability_not_only_response_content(self):
        case = self.cases["DTF-033"]
        statement = case["proposition"]["statement"].lower()
        falsification = " ".join(x["condition"].lower() for x in case["falsification"])
        self.assertIn("act, target, timing", statement)
        self.assertIn("content of the status response", falsification)

    def test_post_presentation_case_preserves_policy_boundary(self):
        case = self.cases["DTF-034"]
        self.assertIn("policy-mismatch", case["failure_classes"])
        categories = {x["category"] for x in case["evidence_required"]}
        self.assertTrue({"policy", "temporal", "provenance"} <= categories)

    def test_authoritative_participant_does_not_get_privacy_inference_credit(self):
        case = self.cases["DTF-035"]
        falsification = " ".join(x["condition"].lower() for x in case["falsification"])
        self.assertIn("authoritative participant", falsification)
        self.assertIn("authorized to issue or operate", falsification)

    def test_minimal_parts_do_not_establish_minimal_composition(self):
        case = self.cases["DTF-036"]
        statement = case["proposition"]["statement"].lower()
        self.assertIn("combined disclosure", statement)
        self.assertIn("individually non-identifying", statement)

    def test_retention_case_requires_policy_provenance_composition_and_time(self):
        case = self.cases["DTF-037"]
        categories = {x["category"] for x in case["evidence_required"]}
        self.assertTrue({"policy", "provenance", "composition", "temporal"} <= categories)

    def test_w3c_reference_is_provenance_not_authority(self):
        for case_id, case in self.cases.items():
            with self.subTest(case=case_id):
                refs = case["references"]
                w3c = [r for r in refs if "w3.org/TR/vc-data-model-threat-model" in r["locator"]]
                self.assertEqual(len(w3c), 1)
                self.assertIn("not corpus authority", w3c[0].get("note", "").lower())


if __name__ == "__main__":
    unittest.main()
