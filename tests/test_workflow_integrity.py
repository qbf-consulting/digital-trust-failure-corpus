"""Regression guards for workflow supply-chain references and permission boundaries."""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / ".github" / "workflows"
ACTION = re.compile(r"^\s*-?\s*uses:\s*([^\s#]+)", re.MULTILINE)
SHA_PIN = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+@[a-f0-9]{40}$")


class WorkflowIntegrityTests(unittest.TestCase):
    def test_all_remote_actions_are_pinned_to_full_commit_sha(self):
        for workflow in sorted(ROOT.glob("*.yml")):
            with self.subTest(workflow=workflow.name):
                refs = ACTION.findall(workflow.read_text())
                self.assertTrue(refs, "No Actions found; inspect the workflow")
                for ref in refs:
                    if ref.startswith("./"):
                        continue
                    self.assertRegex(ref, SHA_PIN, f"Unpinned Action in {workflow.name}: {ref}")

    def test_read_only_diagnostic_has_no_publication_privilege(self):
        workflow = (ROOT / "release-safety-preflight.yml").read_text()
        self.assertIn("contents: read", workflow)
        self.assertNotIn("contents: write", workflow)
        self.assertNotIn("environment: release-publication", workflow)
        self.assertNotIn("gh release create", workflow)
        self.assertNotIn("gh release edit", workflow)

    def test_release_is_explicitly_manual_only(self):
        workflow = (ROOT / "release.yml").read_text()
        self.assertIn("workflow_dispatch:", workflow)
        self.assertNotIn("\n  push:", workflow)
        self.assertNotIn("\n  pull_request:", workflow)
        self.assertIn("environment: release-publication", workflow)
        self.assertIn("contents: write", workflow)


if __name__ == "__main__":
    unittest.main()
