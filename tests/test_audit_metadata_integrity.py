"""Offline integrity tests for schema identifiers and licensing declarations.

These checks do not assert that public URLs resolve or that external legal
interpretations have been independently verified.
"""
import json
import unittest
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]


class AuditMetadataIntegrityTests(unittest.TestCase):
    def test_all_schema_ids_if_present_are_valid_https_uris_and_unique(self):
        ids = {}
        for path in sorted((ROOT / "schemas").glob("*.json")):
            with self.subTest(schema=path.name):
                data = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual(data.get("$schema"), "https://json-schema.org/draft/2020-12/schema")
                identifier = data.get("$id")
                if identifier is None:
                    continue  # Missing optional $id is not evidence of public resolvability.
                parsed = urlsplit(identifier)
                self.assertEqual(parsed.scheme, "https")
                self.assertTrue(parsed.hostname)
                self.assertFalse(parsed.username or parsed.password)
                self.assertFalse(parsed.fragment)
                self.assertNotIn(identifier, ids, f"Duplicate $id also in {ids.get(identifier)}")
                ids[identifier] = path.name

    def test_canonical_schema_id_is_not_silently_changed(self):
        data = json.loads((ROOT / "schemas/failure-case.schema.json").read_text(encoding="utf-8"))
        self.assertEqual(data["$id"], "https://qbfconsulting.digital/schemas/digital-trust-failure-case/0.1.0")

    def test_machine_readable_license_policy_files_and_classes(self):
        policy = json.loads((ROOT / "licensing/artifact-license-policy.json").read_text(encoding="utf-8"))
        self.assertEqual(policy["licenses"]["content"]["spdx"], "CC-BY-4.0")
        self.assertEqual(policy["licenses"]["software"]["spdx"], "Apache-2.0")
        for kind in ("content", "software"):
            self.assertTrue((ROOT / policy["licenses"][kind]["license_file"]).is_file())
        self.assertIn("explicit file-level license notice takes precedence", policy["default_rule"])
        self.assertTrue(any("corpus/**" in row["paths"] and row["license"] == "Apache-2.0"
                            for row in policy["path_guidance"]))

if __name__ == "__main__":
    unittest.main()
