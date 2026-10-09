"""Corpus-wide invariant tests: new families cannot bypass PASS prohibition."""
import json
import tempfile
import unittest
from pathlib import Path

from tools.validate import validate_case_files

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas/failure-case.schema.json"
VALID = ROOT / "tests/fixtures/valid/DTF-000.json"

class CorpusInvariantsTests(unittest.TestCase):
    def test_all_canonical_cases_prohibit_pass(self):
        paths = sorted((ROOT / "corpus").rglob("DTF-*.json"))
        self.assertGreater(len(paths), 0)
        for path in paths:
            with self.subTest(path=path):
                case = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual(case["expected"]["dispositions"]["PASS"], "prohibited")
        self.assertEqual(validate_case_files(paths, SCHEMA), [])

    def test_new_family_cannot_bypass_validator(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "new-uncovered-family" / "DTF-999.json"
            path.parent.mkdir()
            case = json.loads(VALID.read_text(encoding="utf-8"))
            case["id"] = "DTF-999"
            case["title"] = "new-family-unsafe-pass-probe"
            case["expected"]["dispositions"]["PASS"] = "allowed"
            path.write_text(json.dumps(case), encoding="utf-8")
            findings = validate_case_files([path], SCHEMA)
            self.assertTrue(any("must prohibit PASS" in f.message for f in findings), findings)

    def test_schema_version_is_unchanged(self):
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        self.assertIn("0.1.0", schema.get("$id", ""))

if __name__ == "__main__":
    unittest.main()
