"""Fail-closed provenance tests for the canonical DTF predicate index."""
import copy
import unittest

from tools.validate_trust_tasks_predicate_catalog import check, load, derive


class PredicateCatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = load()

    def test_all_canonical_source_predicates_reconciled(self):
        result = check(self.catalog)
        self.assertEqual(result["canonical_predicates"], 37)
        self.assertEqual(result["families"], 5)
        self.assertEqual(result["authority"], "corpus/")

    def test_missing_case_does_not_become_no_match(self):
        changed = copy.deepcopy(self.catalog)
        changed["authority"]["records"].pop()
        with self.assertRaisesRegex(ValueError, "canonical proposition"):
            check(changed)

    def test_stale_git_blob_is_rejected(self):
        changed = copy.deepcopy(self.catalog)
        changed["authority"]["records"][0]["source_blob"] = "0" * 40
        with self.assertRaisesRegex(ValueError, "blob"):
            check(changed)

    def test_unchanged_case_version_cannot_hide_changed_precondition(self):
        # Model a canonical corpus edit that omitted a version bump. The
        # source-derived expected predicates must still invalidate the index.
        authoritative = derive()
        altered = copy.deepcopy(authoritative)
        altered["authority"]["records"][0]["preconditions"][0] += " altered"
        with self.assertRaisesRegex(ValueError, "precondition drift"):
            check(self.catalog, expected=altered)

    def test_edited_falsification_is_rejected(self):
        changed = copy.deepcopy(self.catalog)
        changed["evidence"]["records"][0]["falsification"] = []
        with self.assertRaisesRegex(ValueError, "canonical proposition"):
            check(changed)

    def test_unrecognized_extra_case_is_rejected(self):
        changed = copy.deepcopy(self.catalog)
        item = copy.deepcopy(changed["privacy"]["records"][-1])
        item["case_id"] = "DTF-999"
        changed["privacy"]["records"].append(item)
        with self.assertRaisesRegex(ValueError, "canonical proposition"):
            check(changed)

    def test_missing_family_is_rejected(self):
        changed = copy.deepcopy(self.catalog)
        changed.pop("composition")
        with self.assertRaisesRegex(ValueError, "family membership"):
            check(changed)


if __name__ == "__main__":
    unittest.main()
