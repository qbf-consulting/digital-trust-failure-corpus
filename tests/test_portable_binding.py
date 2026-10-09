"""Portable v0.2 fixture evaluation, digest tamper rejection and honest coverage."""
import json
import tempfile
import unittest
from pathlib import Path

from tools.case_digest import case_sha256, load_unique_case
from tools.execute_portable_binding import ROOT, evaluate

class PortableBindingTests(unittest.TestCase):
    def binding(self, case_id="DTF-001", observed="DENY"):
        case = load_unique_case(ROOT / "corpus", case_id)
        expected = next(k for k in ("DENY", "INDETERMINATE")
                        if case["expected"]["dispositions"][k] == "allowed")
        return dict(binding_version="0.2.0", case_id=case_id,
                    case_version=case["version"], case_sha256=case_sha256(case),
                    adapter="fixture-v1", scenario="synthetic", expected=expected,
                    observed=observed, evidence=["synthetic:unverified"])

    def test_three_fixture_pairs_are_not_target_executions(self):
        for case_id in ("DTF-001", "DTF-023", "DTF-027"):
            with self.subTest(case_id=case_id):
                b = self.binding(case_id)
                b["observed"] = b["expected"]
                safe = evaluate(b)
                self.assertEqual(safe["test_verdict"], "SATISFIED")
                self.assertEqual(safe["execution_class"], "author-supplied-fixture")
                b["observed"] = "PASS"
                unsafe = evaluate(b)
                self.assertEqual(unsafe["test_verdict"], "VIOLATED")
                self.assertEqual(unsafe["execution_class"], "author-supplied-fixture")

    def test_digest_detects_case_mutation_in_vendored_archive(self):
        b = self.binding()
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            case = load_unique_case(ROOT / "corpus", b["case_id"])
            p = root / "DTF-001.json"
            p.write_text(json.dumps(case))
            self.assertEqual(evaluate(b, root)["test_verdict"], "SATISFIED")
            case["title"] += "-changed"
            p.write_text(json.dumps(case))
            with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
                evaluate(b, root)

    def test_bad_digest_rejected(self):
        b = self.binding()
        b["case_sha256"] = "0" * 64
        with self.assertRaises(ValueError):
            evaluate(b)

    def test_v01_contract_still_available(self):
        self.assertTrue((ROOT / "schemas/execution-binding.schema.json").exists())
        self.assertTrue((ROOT / "tools/execute_binding.py").exists())

if __name__ == "__main__":
    unittest.main()
