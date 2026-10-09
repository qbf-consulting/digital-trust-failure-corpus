"""Conservative external-source to canonical case coverage checks."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class SemanticOverlapMatrixTests(unittest.TestCase):
    def test_full_cartesian_screening(self):
        data = json.loads((ROOT / "research/external-sources/semantic-overlap-matrix.json").read_text())
        source_ids = {s["id"] for s in data["source_records"]}
        case_ids = {p.stem for p in (ROOT / "corpus").rglob("DTF-*.json")}
        self.assertEqual(len(source_ids), 3)
        self.assertEqual(len(case_ids), 37)
        self.assertEqual(len(data["judgments"]), len(source_ids) * len(case_ids))
        self.assertEqual(
            {(j["source_id"], j["case_id"]) for j in data["judgments"]},
            {(s, c) for s in source_ids for c in case_ids})
        for j in data["judgments"]:
            self.assertIn(j["classification"], {"mechanism-overlap", "adjacent", "not-established"})
            self.assertGreater(len(j["reason"]), 75)
            self.assertGreater(len(j["case_proposition_summary"]), 15)
        for source in data["source_records"]:
            self.assertTrue(source["url"].startswith("https://"))
            self.assertTrue(source["proposition"])
        self.assertTrue(data["limitations"])

if __name__ == "__main__":
    unittest.main()
