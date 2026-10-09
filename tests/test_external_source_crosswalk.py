"""Validate the non-normative external-source research crosswalk."""
import json
import re
import unittest
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
REGISTER = ROOT / "research/external-sources/crosswalk.json"

class ExternalSourceCrosswalkTests(unittest.TestCase):
    def test_register_shape_and_references(self):
        data = json.loads(REGISTER.read_text())
        self.assertEqual(data["schema_version"], "0.1.0")
        self.assertGreaterEqual(len(data["records"]), 4)
        seen = set()
        allowed = {"cross-reference", "inspect-overlap", "coverage-gap", "test-pattern", "method-reference"}
        for record in data["records"]:
            with self.subTest(source=record["source_id"]):
                self.assertTrue(record["source"].strip())
                self.assertTrue(record["rationale"].strip())
                self.assertTrue(record["reuse"].strip())
                self.assertIn(record["confidence"], {"high", "medium", "low"})
                self.assertIn(record["disposition"], allowed)
                self.assertEqual(urlparse(record["url"]).scheme, "https")
                self.assertTrue(urlparse(record["url"]).netloc)
                key = (record["source"], record["source_id"])
                self.assertNotIn(key, seen)
                seen.add(key)
                self.assertEqual(len(record["case_ids"]), len(set(record["case_ids"])))
                for case_id in record["case_ids"]:
                    self.assertRegex(case_id, r"^DTF-\d{3}$")
                    self.assertEqual(len(list((ROOT / "corpus").rglob(case_id + ".json"))), 1)

    def test_informative_mapping_is_in_canonical_case(self):
        case = json.loads((ROOT / "corpus/authority/DTF-001.json").read_text())
        refs = [ref for ref in case["references"] if ref["locator"] == "https://cwe.mitre.org/data/definitions/863.html"]
        self.assertEqual(len(refs), 1)
        self.assertIn("Informative", refs[0]["note"])

if __name__ == "__main__":
    unittest.main()
