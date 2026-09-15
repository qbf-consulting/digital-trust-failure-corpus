import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "failure-case.schema.json"
CORPUS = ROOT / "corpus"


class ReleaseBaselineTests(unittest.TestCase):
    def test_repository_version_is_v0_1_0(self):
        self.assertEqual((ROOT / "VERSION").read_text(encoding="utf-8").strip(), "0.1.0")

    def test_schema_identifier_matches_release_version(self):
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        self.assertTrue(schema["$id"].endswith("/0.1.0"))

    def test_release_contains_exactly_twelve_initial_cases(self):
        cases = [
            json.loads(path.read_text(encoding="utf-8"))
            for path in sorted(CORPUS.rglob("DTF-*.json"))
        ]
        self.assertEqual(len(cases), 12)
        self.assertEqual(
            sorted(case["id"] for case in cases),
            [f"DTF-{number:03d}" for number in range(1, 13)],
        )

    def test_initial_cases_match_release_version_and_remain_draft(self):
        for path in sorted(CORPUS.rglob("DTF-*.json")):
            case = json.loads(path.read_text(encoding="utf-8"))
            with self.subTest(case=case["id"]):
                self.assertEqual(case["version"], "0.1.0")
                self.assertEqual(case["status"], "draft")

    def test_release_documentation_exists(self):
        self.assertTrue((ROOT / "CHANGELOG.md").is_file())
        self.assertTrue((ROOT / "docs" / "release-notes-v0.1.0.md").is_file())


if __name__ == "__main__":
    unittest.main()
