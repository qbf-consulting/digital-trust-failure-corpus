"""Regression checks for the bounded external-record triage and maturity note."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class ResearchGatesTests(unittest.TestCase):
    def test_record_triage(self):
        data = json.loads((ROOT / "research/external-sources/record-triage.json").read_text())
        self.assertEqual(data["schema_version"], "0.1.0")
        self.assertEqual(len(data["records"]), 8)
        ids = set()
        for record in data["records"]:
            with self.subTest(id=record["id"]):
                self.assertNotIn(record["id"], ids)
                ids.add(record["id"])
                self.assertTrue(record["url"].startswith("https://cwe.mitre.org/data/definitions/"))
                self.assertTrue(record["note"])
                self.assertTrue(record["rights"])
                self.assertEqual(len(list((ROOT / "corpus").rglob(record["candidate_case_id"] + ".json"))), 1)
        self.assertEqual(ids, {"CWE-862", "CWE-287", "CWE-345", "CWE-294",
                               "CWE-613", "CWE-200", "CWE-863", "CWE-841"})

    def test_maturity_gate_is_not_automatic(self):
        note = (ROOT / "docs/case-maturity-and-release-gates.md").read_text()
        self.assertIn("Current maturity decision: Draft", note)
        self.assertIn("do not cut a release", note)
        self.assertIn("no core schema or taxonomy revision", note)

if __name__ == "__main__":
    unittest.main()
