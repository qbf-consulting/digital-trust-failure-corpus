"""Positive and negative regression coverage for the additive fixture adapter."""
import json
import unittest
import subprocess
from pathlib import Path
from tools.execute_binding import ROOT, evaluate

def load_case(case_id):
    matches = [json.loads(p.read_text()) for p in (ROOT / "corpus").rglob("*.json")
               if json.loads(p.read_text()).get("id") == case_id]
    if len(matches) != 1:
        raise AssertionError("case lookup failed")
    return matches[0]

def binding(case_id, observed="DENY"):
    case = load_case(case_id)
    expected = next(k for k in ("DENY", "INDETERMINATE")
                    if case["expected"]["dispositions"][k] == "allowed")
    return dict(binding_version="0.1.0", case_id=case_id, case_version=case["version"],
                case_revision=subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(), adapter="fixture-v1",
                scenario="synthetic adverse condition", expected=expected,
                observed=observed, evidence=["synthetic:observation-1"])

class ExecutionBindingTests(unittest.TestCase):
    def test_safe_outcomes(self):
        for case_id in ("DTF-001", "DTF-023", "DTF-027"):
            with self.subTest(case=case_id):
                b = binding(case_id)
                b["observed"] = b["expected"]
                self.assertEqual(evaluate(b)["test_verdict"], "SATISFIED")

    def test_unsafe_pass_is_violation(self):
        for case_id in ("DTF-001", "DTF-023", "DTF-027"):
            with self.subTest(case=case_id):
                self.assertEqual(evaluate(binding(case_id, "PASS"))["test_verdict"], "VIOLATED")

    def test_missing_evidence_rejected(self):
        b = binding("DTF-001")
        b["evidence"] = []
        with self.assertRaises(Exception):
            evaluate(b)

    def test_mismatched_case_version_rejected(self):
        b = binding("DTF-001")
        b["case_version"] = "999.0.0"
        with self.assertRaises(ValueError):
            evaluate(b)

    def test_unknown_adapter_rejected(self):
        b = binding("DTF-001")
        b["adapter"] = "unsupported"
        with self.assertRaises(Exception):
            evaluate(b)

    def test_wrong_revision_rejected(self):
        b = binding("DTF-001")
        b["case_revision"] = "0" * 40
        with self.assertRaises(ValueError):
            evaluate(b)

    def test_malformed_revision_rejected(self):
        b = binding("DTF-001")
        b["case_revision"] = "main"
        with self.assertRaises(Exception):
            evaluate(b)

    def test_missing_case_rejected(self):
        b = binding("DTF-001")
        b["case_id"] = "DTF-99999"
        with self.assertRaises(ValueError):
            evaluate(b)

    def test_invalid_disposition_rejected(self):
        b = binding("DTF-001")
        b["observed"] = "UNKNOWN"
        with self.assertRaises(Exception):
            evaluate(b)


    def test_invalid_expected_outcome_rejected(self):
        b = binding("DTF-001")
        case = load_case("DTF-001")
        invalid = next((k for k in ("DENY", "INDETERMINATE")
                        if case["expected"]["dispositions"][k] != "allowed"), None)
        if invalid is None:
            self.skipTest("case permits both safe dispositions")
        b["expected"] = invalid
        with self.assertRaises(ValueError):
            evaluate(b)

    def test_binding_additional_property_rejected(self):
        b = binding("DTF-001")
        b["untrusted_override"] = "PASS"
        with self.assertRaises(Exception):
            evaluate(b)

    def test_repeated_evaluation_is_deterministic(self):
        b = binding("DTF-023")
        b["observed"] = b["expected"]
        self.assertEqual(evaluate(b), evaluate(b))

if __name__ == "__main__":
    unittest.main()
