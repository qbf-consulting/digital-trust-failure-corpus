"""Actual external OPA engine integration; requires DTFC_OPA_BIN in CI."""
import json
import os
import unittest
from pathlib import Path
from tools.run_opa_consumer import ROOT, evaluate_opa

class RealOpaIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.opa = os.environ.get("DTFC_OPA_BIN")
        if not cls.opa:
            raise unittest.SkipTest("OPA executable not configured; CI dedicated job requires it")
        if not Path(cls.opa).is_file():
            raise AssertionError("Configured OPA binary missing")

    def test_revoked_authority_safe_and_defective(self):
        request = json.loads((ROOT / "examples/independent-consumer/stale-authority.json").read_text())
        safe = evaluate_opa(self.opa, ROOT / "examples/opa-consumer/safe.rego", request)
        defective = evaluate_opa(self.opa, ROOT / "examples/opa-consumer/defective.rego", request)
        self.assertEqual(safe["disposition"], "DENY")
        self.assertEqual(defective["disposition"], "PASS")
        self.assertEqual(safe["input_sha256"], defective["input_sha256"])
        self.assertEqual(safe["target_sha256"], defective["target_sha256"])
        self.assertNotEqual(safe["policy_sha256"], defective["policy_sha256"])
        self.assertIn("Version: 1.9.0", safe["target_version"])
        for result in (safe, defective):
            self.assertEqual(len(result["output_sha256"]), 64)
            self.assertEqual(result["exit_code"], 0)

if __name__ == "__main__":
    unittest.main()
