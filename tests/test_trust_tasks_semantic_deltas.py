"""Adversarial regression tests for source-pinned delta controls, issue #135."""
import copy
import json
import unittest

from tools.validate_trust_tasks_semantic_deltas import PATH, check


class SemanticDeltaControlsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(PATH.read_text())

    def test_live_controls_are_pinned_but_do_not_authorize_inheritance(self):
        summary = check(self.data)
        self.assertEqual(summary["material_delta_controls"], 6)
        self.assertEqual(summary["challenged_predicate_pairs"], 16)
        self.assertEqual(summary["inheritance_authorized"], 0)
        self.assertEqual(summary["independently_accepted"], 0)

    def test_altered_normative_source_blob_fails_closed(self):
        data = copy.deepcopy(self.data)
        data["controls"][0]["source_binding"]["successor_spec_blob"] = "0" * 40
        with self.assertRaisesRegex(ValueError, "fingerprint drift"):
            check(data)

    def test_changed_case_proposition_version_reopens_controls(self):
        cases = {f"DTF-{i:03}": "0.1.0" for i in range(1, 38)}
        cases["DTF-010"] = "0.2.0"
        with self.assertRaisesRegex(ValueError, "canonical case revision drift"):
            check(self.data, cases=cases)

    def test_synthetic_editorial_only_claim_cannot_erase_a_known_delta(self):
        data = copy.deepcopy(self.data)
        data["controls"][0]["change_domain"] = "editorial"
        with self.assertRaisesRegex(ValueError, "missing material contract change"):
            check(data)

    def test_missing_normative_anchor_rejected(self):
        data = copy.deepcopy(self.data)
        data["controls"][0]["source_sections"] = []
        with self.assertRaisesRegex(ValueError, "unanchored"):
            check(data)

    def test_fabricated_semantic_marker_rejected(self):
        data = copy.deepcopy(self.data)
        data["controls"][0]["required_delta_tokens"] = ["thisDoesNotExistInSourceDelta"]
        with self.assertRaisesRegex(ValueError, "marker absent"):
            check(data)

    def test_out_of_scope_predicate_rejected(self):
        data = copy.deepcopy(self.data)
        data["controls"][0]["candidate_predicates_to_recheck"].append("DTF-999")
        with self.assertRaisesRegex(ValueError, "unknown canonical"):
            check(data)

    def test_unjustified_inheritance_rejected_even_if_both_cases_match(self):
        data = copy.deepcopy(self.data)
        data["controls"][0]["inheritance"] = [{"case_id": "DTF-009", "mode": "inherited"}]
        with self.assertRaisesRegex(ValueError, "inheritance not approved"):
            check(data)

    def test_cannot_cross_direct_consent_and_bridge_attestation(self):
        data = copy.deepcopy(self.data)
        data["controls"][0]["predecessor"] = (
            "https://trusttasks.org/spec/consent/decision/1.0")
        with self.assertRaisesRegex(ValueError, "cross-contract"):
            check(data)

    def test_missing_version_and_fabricated_review_rejected(self):
        data = copy.deepcopy(self.data)
        data["controls"][0]["successor"] += "-unpublished"
        with self.assertRaisesRegex(ValueError, "unknown pinned"):
            check(data)
        data = copy.deepcopy(self.data)
        data["controls"][0]["independent_acceptance"] = "accepted"
        with self.assertRaisesRegex(ValueError, "fabricated independent"):
            check(data)

    def test_duplicate_control_rejected(self):
        data = copy.deepcopy(self.data)
        data["controls"].append(copy.deepcopy(data["controls"][0]))
        with self.assertRaisesRegex(ValueError, "duplicate"):
            check(data)


if __name__ == "__main__":
    unittest.main()
