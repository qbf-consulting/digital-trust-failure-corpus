import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "build_docs.py"


def load_generator():
    spec = importlib.util.spec_from_file_location("dtfc_build_docs", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class DocumentationSiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.docs = load_generator()
        cls.cases = cls.docs._load_cases()

    def test_documentation_config_and_landing_page_exist(self):
        self.assertTrue((ROOT / "mkdocs.yml").is_file())
        self.assertTrue((ROOT / "requirements-docs.txt").is_file())
        self.assertTrue((ROOT / "docs" / "index.md").is_file())
        self.assertTrue((ROOT / ".github" / "workflows" / "pages.yml").is_file())

    def test_generated_catalogue_source_covers_contiguous_corpus(self):
        ids = [case_id for case_id, _path, _case in self.cases]
        self.assertEqual(ids, [f"DTF-{n:03d}" for n in range(1, 32)])

    def test_every_case_renders_required_assurance_sections(self):
        for case_id, path, case in self.cases:
            with self.subTest(case=case_id):
                rendered = self.docs._render_case(path, case)
                for heading in (
                    "## Proposition",
                    "## Preconditions",
                    "## Trigger",
                    "## Expected dispositions",
                    "## Evidence required",
                    "## Falsification conditions",
                ):
                    self.assertIn(heading, rendered)
                self.assertIn("Canonical source", rendered)
                self.assertIn(
                    "generated from the canonical machine-readable corpus",
                    rendered,
                )

    def test_catalogue_index_contains_every_case(self):
        rendered = self.docs._render_index(self.cases)
        for case_id, _path, _case in self.cases:
            self.assertIn(f"[{case_id}]({case_id}.md)", rendered)

    def test_site_states_non_authoritative_boundary(self):
        landing = (ROOT / "docs" / "index.md").read_text(encoding="utf-8")
        self.assertIn("evidence, not authority", landing)
        self.assertIn("rendered views, not a second source of truth", landing)


if __name__ == "__main__":
    unittest.main()
