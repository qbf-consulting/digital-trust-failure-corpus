import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "failure-case.schema.json"
CORPUS = ROOT / "corpus"


class ReleaseBaselineTests(unittest.TestCase):
    def test_repository_version_is_v0_4_0(self):
        self.assertEqual((ROOT / "VERSION").read_text(encoding="utf-8").strip(), "0.4.0")

    def test_schema_contract_remains_v0_1_0_when_unchanged(self):
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        self.assertTrue(schema["$id"].endswith("/0.1.0"))

    def test_v0_4_release_preserves_prior_cases_and_is_contiguous(self):
        cases = [
            json.loads(path.read_text(encoding="utf-8"))
            for path in sorted(CORPUS.rglob("DTF-*.json"))
        ]
        ids = sorted(case["id"] for case in cases)
        released_v0_3_ids = [f"DTF-{number:03d}" for number in range(1, 32)]

        self.assertTrue(set(released_v0_3_ids) <= set(ids))
        self.assertEqual(ids, [f"DTF-{number:03d}" for number in range(1, 38)])

    def test_cases_remain_draft_and_use_case_level_semver(self):
        for path in sorted(CORPUS.rglob("DTF-*.json")):
            case = json.loads(path.read_text(encoding="utf-8"))
            with self.subTest(case=case["id"]):
                self.assertRegex(case["version"], r"^[0-9]+\.[0-9]+\.[0-9]+$")
                self.assertEqual(case["status"], "draft")

    def test_release_documentation_exists(self):
        self.assertTrue((ROOT / "CHANGELOG.md").is_file())
        self.assertTrue((ROOT / "docs" / "release-notes-v0.4.0.md").is_file())


if __name__ == "__main__":
    unittest.main()
