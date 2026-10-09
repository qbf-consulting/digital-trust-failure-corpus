"""Eight-record x canonical corpus semantic-screening completeness checks."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class EightRecordCoverageTests(unittest.TestCase):
    def test_full_matrix_and_research_traceability(self):
        data = json.loads((ROOT / "research/external-sources/eight-record-coverage-matrix.json").read_text())
        inspected = json.loads((ROOT / "research/external-sources/inspected-record-dispositions.json").read_text())
        cases = {p.stem for p in (ROOT / "corpus").rglob("DTF-*.json")}
        ids = {r["id"] for r in inspected["records"]}
        self.assertEqual(len(ids), 8)
        self.assertEqual(len({r["family"] for r in inspected["records"]}), 3)
        self.assertEqual(len(cases), 37)
        self.assertEqual(len(data["judgments"]), 296)
        self.assertEqual({(j["source_id"], j["case_id"]) for j in data["judgments"]},
                         {(i, c) for i in ids for c in cases})
        self.assertEqual({r["id"] for r in data["source_records"]}, ids)
        for j in data["judgments"]:
            self.assertIn(j["classification"], ("mechanism-overlap", "adjacent", "not-established"))
            self.assertGreater(len(j["reason"]), 90)
            self.assertGreater(len(j["case_proposition_summary"]), 15)
        self.assertIn("not independently re-fetched", " ".join(data["limitations"]))

if __name__ == "__main__":
    unittest.main()
