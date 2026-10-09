"""Positive and negative subprocess consumer integration tests."""
import json
import subprocess
import unittest
from pathlib import Path
from tools.execute_binding import ROOT
from tools.run_independent_consumer import run, verify_capture

TARGET = ROOT / "examples/independent-consumer/authority_target.py"
DEFECTIVE_TARGET = ROOT / "examples/independent-consumer/defective_authority_target.py"

def case_version():
    for p in (ROOT / "corpus").rglob("*.json"):
        data = json.loads(p.read_text())
        if data.get("id") == "DTF-001":
            return data["version"]
    raise AssertionError("DTF-001 missing")

def revision():
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()

class IndependentConsumerTests(unittest.TestCase):
    def test_stale_authority_denied(self):
        result = run(TARGET, dict(authority_state="revoked", action="commit",
                                  authorized_actions=["commit"]), case_version(), revision())
        self.assertEqual(result["result"]["test_verdict"], "SATISFIED")
        self.assertEqual(result["result"]["target_disposition"], "DENY")
        self.assertEqual(len(result["evidence"]["response_sha256"]), 64)

    def test_revoked_authority_wrongly_permitted_is_violation(self):
        result = run(DEFECTIVE_TARGET, dict(authority_state="revoked", action="commit",
                                  authorized_actions=["commit"]), case_version(), revision())
        self.assertEqual(result["result"]["test_verdict"], "VIOLATED")

    def test_capture_integrity_and_tampering(self):
        request = dict(authority_state="revoked", action="commit",
                       authorized_actions=["commit"])
        capture = run(TARGET, request, case_version(), revision())
        self.assertTrue(verify_capture(capture, TARGET, request))
        changed_request = dict(request, authority_state="active")
        self.assertFalse(verify_capture(capture, TARGET, changed_request))
        capture["evidence"]["response"]["disposition"] = "PASS"
        self.assertFalse(verify_capture(capture, TARGET, request))

    def test_missing_input_fails_closed(self):
        with self.assertRaises(RuntimeError):
            run(TARGET, {}, case_version(), revision())

    def test_nonexistent_target_fails(self):
        with self.assertRaises((RuntimeError, OSError)):
            run(TARGET.with_name("missing_target.py"), {}, case_version(), revision())

    def test_wrong_case_revision_rejected(self):
        with self.assertRaises(ValueError):
            run(TARGET, dict(authority_state="revoked", action="commit",
                             authorized_actions=["commit"]), case_version(), "0" * 40)

    def test_wrong_case_version_rejected(self):
        with self.assertRaises(ValueError):
            run(TARGET, dict(authority_state="revoked", action="commit",
                             authorized_actions=["commit"]), "999.0.0", revision())

if __name__ == "__main__":
    unittest.main()
