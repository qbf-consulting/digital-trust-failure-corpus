import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
EVIDENCE_DIR = ROOT / "research/consumer-protection/cpc-001-agent-delegation-revocation/evidence"
MANIFEST = EVIDENCE_DIR / "evidence-manifest.yaml"
REPRODUCTION = EVIDENCE_DIR / "reproduction-instructions.md"


class CPC001EvidenceManifestTests(unittest.TestCase):
    def test_manifest_records_ci_and_source_context(self):
        text = MANIFEST.read_text(encoding="utf-8")
        self.assertIn("merged_pr: 112", text)
        self.assertIn("merged_commit_sha: 6723329668d1feb8815c9c1f74fcf3e9d928d891", text)
        self.assertIn("pr_head_sha: 4b6392c7f2e9916b428356c764732a688f7c936a", text)
        self.assertIn("run_id: 38332556409", text)
        self.assertIn("run_id: 38332556517", text)

    def test_manifest_does_not_promote_ci_to_full_assurance(self):
        text = MANIFEST.read_text(encoding="utf-8")
        self.assertIn("assurance_determination: INDETERMINATE", text)
        self.assertNotIn("assurance_determination: SUPPORTED", text)
        self.assertIn("Synthetic CI success is independent adoption evidence.", text)
        self.assertIn("RAHP has assessed CPC-001.", text)

    def test_reproduction_instructions_preserve_synthetic_boundary(self):
        text = REPRODUCTION.read_text(encoding="utf-8")
        self.assertIn("synthetic fixture reproduction path", text)
        self.assertIn("python tools/execute_cpc001.py --role paired", text)
        self.assertIn("python -m unittest discover -s tests -v", text)
        self.assertIn("independent-reproduction gate remains open", text)

    def test_manifest_and_reproduction_files_exist_together(self):
        self.assertTrue(MANIFEST.exists())
        self.assertTrue(REPRODUCTION.exists())


if __name__ == "__main__":
    unittest.main()
