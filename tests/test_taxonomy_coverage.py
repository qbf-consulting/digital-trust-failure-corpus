"""Coverage report counts and negative duplicate-ID probe."""
import json
import tempfile
import unittest
from pathlib import Path
from tools.taxonomy_coverage import build_report

class TaxonomyCoverageTests(unittest.TestCase):
    def test_current_corpus_is_deterministic(self):
        report = build_report()
        self.assertEqual(report, build_report())
        self.assertEqual(report["case_count"], 37)
        self.assertEqual(len(report["case_ids"]), 37)
        self.assertEqual(sum(report["statuses"].values()), 37)
        self.assertTrue(report["domains"])
        self.assertTrue(report["failure_classes"])
        self.assertIn("no independent execution", report["interpretation"])

    def test_duplicate_id_fails_closed(self):
        case = {"id": "DTF-999", "domains": ["evidence"],
                "failure_classes": ["stale-evidence"], "status": "draft"}
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for directory in ("a", "b"):
                path = root / directory / "DTF-999.json"
                path.parent.mkdir()
                path.write_text(json.dumps(case))
            with self.assertRaisesRegex(ValueError, "Duplicate"):
                build_report(root)

if __name__ == "__main__":
    unittest.main()
