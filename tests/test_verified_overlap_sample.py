"""Check traceable, conservative multi-source overlap research."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class VerifiedOverlapSampleTests(unittest.TestCase):
    def test_references_and_case_resolution(self):
        data = json.loads((ROOT / "research/external-sources/verified-overlap-sample.json").read_text())
        self.assertEqual(data["schema_version"], "0.1.0")
        self.assertEqual({r["source"] for r in data["records"]},
                         {"MITRE CWE", "W3C VC Data Model Threat Model v2.1"})
        self.assertEqual(len(data["records"]), 4)
        keys = set()
        for record in data["records"]:
            key = (record["source"], record["id"])
            self.assertNotIn(key, keys)
            keys.add(key)
            self.assertTrue(record["url"].startswith("https://"))
            self.assertGreater(len(record["basis"]), 50)
            self.assertEqual(len(list((ROOT / "corpus").rglob(record["case_id"] + ".json"))), 1)

if __name__ == "__main__":
    unittest.main()
