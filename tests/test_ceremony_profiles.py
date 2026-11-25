"""Regression checks for the provisional ceremony research contract."""
import copy
import unittest

from tools.validate_ceremony_profiles import (
    check, read, PROFILE_PATH, BASELINE_PATH, MANIFEST,
)


class CeremonyProfileTests(unittest.TestCase):
    def setUp(self):
        self.profiles = read(PROFILE_PATH)
        self.baseline = read(BASELINE_PATH)
        self.inventory = read(MANIFEST)

    def validate(self):
        return check(self.profiles, self.baseline, self.inventory)

    def test_frozen_population(self):
        result = self.validate()
        self.assertEqual(result["profiles"], 3)
        self.assertEqual(result["task_versions"], 13)
        self.assertEqual(result["canonical_cases"], 37)
        self.assertEqual(result["planned_comparisons"], 111)
        self.assertFalse(result["semantic_assessment_complete"])

    def test_duplicate_profile(self):
        self.profiles["profiles"].append(copy.deepcopy(self.profiles["profiles"][0]))
        with self.assertRaisesRegex(ValueError, "duplicate profile"):
            self.validate()

    def test_missing_case(self):
        self.baseline["cases"].pop()
        with self.assertRaisesRegex(ValueError, "baseline drift"):
            self.validate()

    def test_task_blob_drift(self):
        self.profiles["profiles"][0]["steps"][0]["schema_blob"] = "0" * 40
        with self.assertRaisesRegex(ValueError, "binding drift"):
            self.validate()

    def test_missing_task(self):
        self.profiles["profiles"][0]["steps"].pop()
        with self.assertRaisesRegex(ValueError, "membership drift"):
            self.validate()

    def test_missing_legitimacy(self):
        self.profiles["profiles"][0]["legitimacy"] = ""
        with self.assertRaisesRegex(ValueError, "missing legitimacy"):
            self.validate()

    def test_collapsed_predicates(self):
        profile = self.profiles["profiles"][0]
        profile["legitimacy"] = profile["execution"]
        with self.assertRaisesRegex(ValueError, "collapsed"):
            self.validate()

    def test_false_independent_review(self):
        self.profiles["independent_review"] = "accepted"
        with self.assertRaisesRegex(ValueError, "assurance promotion"):
            self.validate()

    def test_false_execution(self):
        self.profiles["target_execution"] = "passed"
        with self.assertRaisesRegex(ValueError, "assurance promotion"):
            self.validate()

    def test_catalog_blob_drift(self):
        self.baseline["catalogs"][0]["blob"] = "0" * 40
        with self.assertRaisesRegex(ValueError, "catalog blob drift"):
            self.validate()

    def test_missing_state_dimension(self):
        self.profiles["determination_model"]["effective_state"].remove("indeterminate")
        with self.assertRaisesRegex(ValueError, "determination state drift"):
            self.validate()

    def test_shared_source_drift(self):
        self.profiles["shared_sources"][0]["blob"] = "0" * 40
        with self.assertRaisesRegex(ValueError, "shared source binding drift"):
            self.validate()

    def test_unknown_path_task(self):
        self.profiles["profiles"][0]["paths"][0]["order"].append("consent/revoke/1.0")
        with self.assertRaisesRegex(ValueError, "invalid execution path"):
            self.validate()

    def test_missing_alternative_path(self):
        self.profiles["profiles"][0]["paths"].pop()
        with self.assertRaisesRegex(ValueError, "execution path membership drift"):
            self.validate()

    def test_missing_policy_owner(self):
        self.profiles["profiles"][0]["policy_owner"] = ""
        with self.assertRaisesRegex(ValueError, "missing policy_owner"):
            self.validate()


if __name__ == "__main__":
    unittest.main()
