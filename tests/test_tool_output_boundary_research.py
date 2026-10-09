"""Integrity tests for the hypothetical tool-output research fixture."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class ToolOutputBoundaryResearchTests(unittest.TestCase):
    def test_bounded_scenario(self):
        fixture = json.loads((ROOT / "research/tool-output-boundary/scenario.json").read_text())
        self.assertEqual(fixture["status"], "hypothetical-not-executed")
        self.assertEqual(fixture["disposition"], "covered-by-existing-cases")
        self.assertEqual(fixture["expected"]["safe"]["consequential_tool_called"], False)
        self.assertEqual(fixture["expected"]["unsafe"]["consequential_tool_called"], True)
        self.assertEqual(fixture["expected"]["safe"]["action"], "summarize_only")
        self.assertEqual(fixture["expected"]["unsafe"]["action"], "record_update")
        for case_id in fixture["existing_case_ids"]:
            self.assertEqual(len(list((ROOT / "corpus").rglob(case_id + ".json"))), 1)
        self.assertTrue(all(url.startswith("https://") for url in fixture["sources"]))
        self.assertGreaterEqual(len(fixture["evidence_needed"]), 3)

if __name__ == "__main__":
    unittest.main()
