"""Reconciliation must reject false-complete published inventories."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from tools.reconcile_trust_tasks_registry import PREFIX, discover, git_blob_sha, reconcile


class RegistryReconciliationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        directory = self.root / "specs" / "acl" / "grant" / "0.3"
        directory.mkdir(parents=True)
        (directory / "spec.md").write_bytes(b"---\\nslug: acl/grant\\n---\\n")
        (directory / "payload.schema.json").write_bytes(b"{}")
        self.key = PREFIX + "acl/grant/0.3"
        self.inventory = {"source": {"commit": "pinned"}, "records": [{
            "slug": "acl/grant", "version": "0.3",
            "path": "specs/acl/grant/0.3/spec.md",
            "spec_blob": git_blob_sha((directory / "spec.md").read_bytes()),
            "schema_blob": git_blob_sha((directory / "payload.schema.json").read_bytes()),
        }]}
        self.registry = {"tasks": [{"slug": "acl/grant", "version": "0.3",
                                    "status": "draft", "typeUri": self.key}]}

    def test_matching_source_and_registry(self):
        result = reconcile(self.inventory, self.root, self.registry)
        self.assertEqual(result["registry_versions"], 1)
        self.assertFalse(result["semantic_review_complete"])

    def test_missing_generated_entry(self):
        with self.assertRaises(ValueError):
            reconcile(self.inventory, self.root, {"tasks": []})

    def test_duplicate_published_entry(self):
        data = copy.deepcopy(self.registry)
        data["tasks"].append(copy.deepcopy(data["tasks"][0]))
        with self.assertRaises(ValueError):
            reconcile(self.inventory, self.root, data)

    def test_unexpected_status(self):
        data = copy.deepcopy(self.registry)
        data["tasks"][0]["status"] = "approved"
        with self.assertRaises(ValueError):
            reconcile(self.inventory, self.root, data)

    def test_mutated_upstream_bytes(self):
        (self.root / "specs/acl/grant/0.3/spec.md").write_text("changed")
        with self.assertRaises(ValueError):
            reconcile(self.inventory, self.root, self.registry)

    def test_incomplete_pair(self):
        (self.root / "specs/acl/grant/0.3/payload.schema.json").unlink()
        with self.assertRaises(ValueError):
            discover(self.root)

    def test_noninternal_additional_version(self):
        d = self.root / "specs/acl/grant/0.4"
        d.mkdir()
        (d / "spec.md").write_text("draft")
        (d / "payload.schema.json").write_text("{}")
        with self.assertRaises(ValueError):
            reconcile(self.inventory, self.root, self.registry)

    def test_internal_schemas_are_excluded(self):
        d = self.root / "specs/_framework/0.1"
        d.mkdir(parents=True)
        (d / "spec.md").write_text("internal")
        self.assertEqual(set(discover(self.root)), {self.key})


if __name__ == "__main__":
    unittest.main()
