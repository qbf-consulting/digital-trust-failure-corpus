"""Representativeness and generated-navigation publication safeguards."""
import json
import unittest

from tools.validate_trust_tasks_inventory import MANIFEST, ROOT, PILOT
from tools.validate_acl_review import PATH as ACL
from tools.build_trust_tasks_pages import build_pages


class RepresentativeResearchPublicationTests(unittest.TestCase):
    def test_stable_github_entrypoint_and_published_nav_are_distinct(self):
        entry = ROOT / "docs/trust-tasks/index.md"
        self.assertTrue(entry.exists(), "tracked source landing page absent")
        text = entry.read_text()
        self.assertIn("https://qbf-consulting.github.io/digital-trust-failure-corpus/trust-tasks/", text)
        self.assertIn("generated", text.lower())
        inventory = json.loads(MANIFEST.read_text())
        pages = build_pages(inventory, json.loads(PILOT.read_text()), json.loads(ACL.read_text()))
        self.assertEqual(len(pages), 44)
        self.assertIn("index.md", pages)
        self.assertIn("consent.md", pages)
        self.assertIn("**Versioned tasks:** 1391", pages["index.md"])
        self.assertIn("**Full author-side case-examined:** 23", pages["index.md"])

    def test_representative_study_accounts_for_only_selected_family(self):
        doc = (ROOT / "docs/trust-tasks-representative-consent-study.md").read_text()
        family = json.loads((ROOT / "research/external-sources/trust-tasks/consent-case-examination.json").read_text())
        self.assertEqual(len(family["records"]), 8)
        decisions = [decision for r in family["records"] for decision in r["decisions"]]
        self.assertEqual(len(decisions), 296)
        self.assertEqual(sum(d["disposition"] == "conditional-candidate" for d in decisions), 61)
        self.assertIn("296 case/version judgments", doc)
        self.assertIn("not a statistically representative sample", doc)
        self.assertIn("No independent external reviewer", doc)
        self.assertIn("not** assert exhaustive applicability", doc)

    def test_navigation_and_readme_discover_the_study(self):
        self.assertIn("trust-tasks-representative-consent-study.md",
                      (ROOT / "mkdocs.yml").read_text())
        self.assertIn("trust-tasks-representative-consent-study.md",
                      (ROOT / "README.md").read_text())
        self.assertIn("trust-tasks-representative-consent-study.md",
                      (ROOT / "docs/index.md").read_text())


if __name__ == "__main__":
    unittest.main()
