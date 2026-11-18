"""Negative tests for false historical equivalence and missing version evidence."""
import copy
import json
import unittest

from tools.validate_acl_deltas import ACL, MANIFEST, validate


class ACLDeltaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.review = json.loads(ACL.read_text())
        cls.inventory = json.loads(MANIFEST.read_text())

    def test_pinned_family(self):
        v = validate(self.review, self.inventory)
        self.assertEqual(v["historical_delta_screened"], 13)
        self.assertFalse(v["semantic_review_complete"])

    def test_missing_source_version(self):
        obj = copy.deepcopy(self.review)
        obj["historical"].pop()
        with self.assertRaises(ValueError):
            validate(obj, self.inventory)

    def test_false_equivalence(self):
        obj = copy.deepcopy(self.review)
        obj["historical"][0]["version_delta_evidence"]["mapping_reuse"] = "equivalent"
        with self.assertRaises(ValueError):
            validate(obj, self.inventory)

    def test_forged_review_status(self):
        obj = copy.deepcopy(self.review)
        obj["historical"][0]["applicability_review"] = "independently-approved"
        with self.assertRaises(ValueError):
            validate(obj, self.inventory)

    def test_forged_source_revision(self):
        obj = copy.deepcopy(self.review)
        obj["historical"][0]["version_delta_evidence"]["source_commit"] = "main"
        with self.assertRaises(ValueError):
            validate(obj, self.inventory)

    def test_false_approved_history(self):
        obj = copy.deepcopy(self.review)
        obj["version_delta_review"]["historical_applicability_complete"] = True
        with self.assertRaises(ValueError):
            validate(obj, self.inventory)

    def test_missing_delta_rationale(self):
        obj = copy.deepcopy(self.review)
        obj["historical"][0]["version_delta_evidence"]["rationale"] = ""
        with self.assertRaises(ValueError):
            validate(obj, self.inventory)


if __name__ == "__main__":
    unittest.main()
