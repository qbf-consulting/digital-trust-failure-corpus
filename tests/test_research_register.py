"""Negative probes for bounded research-register integrity."""
import copy
import unittest
from tools.validate_research_register import validate_current, validate_register

CASES = {"DTF-001"}
GOOD = {"schema_version": "0.1.0", "records": [{
    "source": "MITRE CWE", "source_id": "CWE-863",
    "url": "https://cwe.mitre.org/data/definitions/863.html",
    "case_ids": ["DTF-001"]
}]}

class ResearchRegisterTests(unittest.TestCase):
    def test_repository_register_is_valid(self):
        self.assertEqual(validate_current(), [])

    def test_valid_minimal_register(self):
        self.assertEqual(validate_register(GOOD, CASES), [])

    def test_non_https_or_credential_url_rejected(self):
        for url in ("http://example.org/x", "https://user:password@example.org/x", "https://example.org/ bad"):
            data = copy.deepcopy(GOOD)
            data["records"][0]["url"] = url
            with self.subTest(url=url):
                self.assertTrue(validate_register(data, CASES))

    def test_duplicate_source_rejected(self):
        data = copy.deepcopy(GOOD)
        data["records"].append(copy.deepcopy(data["records"][0]))
        self.assertTrue(any("duplicate source" in e for e in validate_register(data, CASES)))

    def test_unknown_case_and_duplicate_case_rejected(self):
        for ids in (["DTF-999"], ["DTF-001", "DTF-001"]):
            data = copy.deepcopy(GOOD)
            data["records"][0]["case_ids"] = ids
            self.assertTrue(validate_register(data, CASES))

if __name__ == "__main__":
    unittest.main()
