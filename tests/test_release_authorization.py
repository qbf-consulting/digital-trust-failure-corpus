"""Release preflight negative probes; no GitHub release is created by tests."""
import json
import tempfile
import unittest
from pathlib import Path

from tools.check_release_request import check_request

class ReleaseAuthorizationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        self.version = root / "VERSION"
        self.request = root / "request.json"
        self.version.write_text("0.5.0\n")
        self.request.write_text(json.dumps({
            "version": "0.5.0", "requested_by": "someone",
            "reason": "Evidence-reviewed release"}))
        self.good = dict(request=self.request, version_file=self.version,
                         event="workflow_dispatch", ref="refs/heads/main",
                         actor="sankarshanmukhopadhyay",
                         authorization_mode="single-maintainer")

    def test_authorized_single_maintainer_manual_request_passes_preflight_only(self):
        check_request(**self.good)

    def test_unconfigured_or_mismatched_mode_fails_closed(self):
        for flag in ("", "false", "true", "reviewer-gated", "SINGLE-MAINTAINER"):
            with self.subTest(flag=flag), self.assertRaises(ValueError):
                check_request(**{**self.good, "authorization_mode": flag})

    def test_push_and_wrong_branch_fail(self):
        for delta in ({"event": "push"}, {"ref": "refs/heads/feature"}):
            with self.subTest(delta=delta), self.assertRaises(ValueError):
                check_request(**{**self.good, **delta})

    def test_unknown_actor_cannot_dispatch(self):
        with self.assertRaises(ValueError):
            check_request(**{**self.good, "actor": "untrusted-contributor"})

    def test_wrong_version_or_missing_reason_fails(self):
        for update in ({"version": "0.4.0"}, {"reason": ""}):
            original = json.loads(self.request.read_text())
            self.request.write_text(json.dumps({**original, **update}))
            with self.subTest(update=update), self.assertRaises(ValueError):
                check_request(**self.good)
            self.request.write_text(json.dumps(original))

    def test_requester_field_does_not_authenticate_actor(self):
        self.request.write_text(json.dumps({
            "version": "0.5.0", "requested_by": "sankarshanmukhopadhyay",
            "reason": "Impersonated metadata"}))
        with self.assertRaises(ValueError):
            check_request(**{**self.good, "actor": "untrusted-contributor"})

    def test_release_input_preflight_shell_continuations(self):
        workflow = (Path(__file__).resolve().parents[1] / ".github/workflows/release.yml").read_text()
        start = workflow.index("python -m tools.verify_release_inputs")
        end = workflow.index("--expected-sha", start)
        command = workflow[start:end]
        continuations = command.splitlines()[:3]
        self.assertEqual(len(continuations), 3)
        for line in continuations:
            self.assertTrue(line.rstrip().endswith(chr(92)))
            self.assertFalse(line.rstrip().endswith(chr(92) * 2))

    def test_workflow_requires_manual_dispatch_and_environment(self):
        workflow = (Path(__file__).resolve().parents[1] / ".github/workflows/release.yml").read_text()
        self.assertIn("workflow_dispatch:", workflow)
        self.assertNotIn("\n  push:", workflow)
        self.assertIn("environment: release-publication", workflow)
        self.assertIn("RELEASE_AUTHORIZATION_MODE: ${{ vars.RELEASE_AUTHORIZATION_MODE }}", workflow)

if __name__ == "__main__":
    unittest.main()
