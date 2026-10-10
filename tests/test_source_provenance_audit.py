"""Negative checks for conservative external source locator classifications."""
import unittest
from tools.audit_source_provenance import audit_register, classify_locator


class SourceProvenanceAuditTests(unittest.TestCase):
    def test_unpinned_and_external_urls_never_claim_attestation(self):
        self.assertEqual(classify_locator("https://github.com/w3c/vc-data-model-2.0-test-suite"),
                         "mutable-or-unpinned-github")
        self.assertEqual(classify_locator("https://cwe.mitre.org/data/definitions/863.html"),
                         "unverified-external")
        self.assertEqual(classify_locator("https://github.com/acme/repo/blob/main/README.md"),
                         "mutable-or-unpinned-github")

    def test_commit_path_is_only_commit_addressed_not_verified(self):
        sha = "a" * 40
        self.assertEqual(classify_locator(f"https://github.com/acme/repo/blob/{sha}/README.md"),
                         "commit-addressed-unverified")
        self.assertEqual(classify_locator("https://github.com/acme/repo/blob/1234/README.md"),
                         "mutable-or-unpinned-github")

    def test_invalid_urls_are_not_classified_as_sources(self):
        for url in ("http://example.org", "https://[broken", "not-a-url"):
            with self.subTest(url=url):
                self.assertEqual(classify_locator(url), "invalid")

    def test_register_is_fully_accounted_for(self):
        report = audit_register()
        self.assertEqual(sum(report["counts"].values()), len(report["records"]))
        self.assertTrue(all(r["locator_class"] != "verified" for r in report["records"]))


if __name__ == "__main__":
    unittest.main()
