"""Canonical case changes require monotonically increased case version."""
import copy
import unittest
from tools.check_case_versions import check_case_changes, is_version_bump

class CaseVersionGateTests(unittest.TestCase):
    def setUp(self):
        self.before = {"id": "DTF-001", "version": "0.1.0", "proposition": {"statement": "original"}}

    def test_semantic_change_without_bump_rejected(self):
        after = copy.deepcopy(self.before)
        after["proposition"]["statement"] = "changed"
        with self.assertRaisesRegex(ValueError, "version bump"):
            check_case_changes(self.before, after)

    def test_semantic_change_with_bump_accepted(self):
        after = copy.deepcopy(self.before)
        after["proposition"]["statement"] = "changed"
        after["version"] = "0.1.1"
        check_case_changes(self.before, after)

    def test_formatting_and_key_order_do_not_require_bump(self):
        after = {"proposition": {"statement": "original"}, "version": "0.1.0", "id": "DTF-001"}
        check_case_changes(self.before, after)

    def test_id_change_rejected(self):
        after = copy.deepcopy(self.before)
        after["id"] = "DTF-999"
        after["version"] = "0.2.0"
        with self.assertRaisesRegex(ValueError, "ID changed"):
            check_case_changes(self.before, after)

    def test_versions_must_increase(self):
        self.assertFalse(is_version_bump("0.2.0", "0.1.9"))
        self.assertFalse(is_version_bump("0.1.0", "0.1.0"))
        self.assertTrue(is_version_bump("0.1.0", "0.1.1"))

if __name__ == "__main__":
    unittest.main()
