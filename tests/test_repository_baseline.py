import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "corpus"


class RepositoryBaselineTests(unittest.TestCase):
    def test_adoption_files_exist(self):
        required = [
            ROOT / "CONTRIBUTING.md",
            ROOT / "SECURITY.md",
            ROOT / "docs" / "authoring-cases.md",
            ROOT / "docs" / "consuming-the-corpus.md",
            ROOT / "LICENSE",
            ROOT / "licensing" / "artifact-license-policy.json",
        ]
        for path in required:
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertTrue(path.is_file())

    def test_v0_1_initial_corpus_has_contiguous_twelve_case_ids(self):
        cases = []
        for path in sorted(CORPUS.rglob("DTF-*.json")):
            cases.append(json.loads(path.read_text(encoding="utf-8")))
        self.assertEqual(
            sorted(case["id"] for case in cases),
            [f"DTF-{number:03d}" for number in range(1, 13)],
        )


if __name__ == "__main__":
    unittest.main()
