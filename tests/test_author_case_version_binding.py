"""Adversarial case-version drift checks on all full-case author research families."""
import copy
import json
import unittest

from tools.validate_trust_tasks_inventory import MANIFEST
from tools.validate_audit_case_examination import PATH as AUDIT, check as audit
from tools.validate_consent_case_examination import PATH as CONSENT, check as consent
from tools.validate_governance_case_examination import PATH as GOV, check as gov
from tools.validate_task_consent_case_examination import PATH as TASK, check as task
from tools.validate_discovery_case_examination import PATH as DISC, check as disc

FAMILIES = ((AUDIT, audit), (CONSENT, consent), (GOV, gov), (TASK, task), (DISC, disc))

class AuthorCaseVersionBindingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inventory = json.loads(MANIFEST.read_text())

    def test_exact_versions_reconciled(self):
        total = 0
        for path, check in FAMILIES:
            with self.subTest(path=path.name):
                data = json.loads(path.read_text())
                summary = check(data, self.inventory)
                self.assertEqual(data["schema_version"], "0.2.0")
                self.assertEqual(
                    sum(len(r["decisions"]) for r in data["records"]),
                    summary["comparisons"])
                total += summary["comparisons"]
        self.assertEqual(total, 814)

    def test_missing_case_semantic_version_is_rejected(self):
        for path, check in FAMILIES:
            with self.subTest(path=path.name):
                data = json.loads(path.read_text())
                data["records"][0]["decisions"][0].pop("case_version")
                with self.assertRaisesRegex(ValueError, "canonical case semantic version"):
                    check(data, self.inventory)

    def test_mismatched_case_semantic_version_is_rejected(self):
        for path, check in FAMILIES:
            with self.subTest(path=path.name):
                data = json.loads(path.read_text())
                data["records"][0]["decisions"][0]["case_version"] = "9.9.9"
                with self.assertRaisesRegex(ValueError, "canonical case semantic version"):
                    check(data, self.inventory)

    def test_case_source_upgrade_is_not_silently_accepted(self):
        # Challenge the authoritative case-version mapping itself rather than
        # only a malformed record, simulating a new canonical case proposition.
        data = json.loads(AUDIT.read_text())
        original = audit(data, self.inventory)
        self.assertEqual(original["versions"], 3)
        from tools.build_trust_tasks_pages import case_versions
        versions = case_versions()
        versions["DTF-013"] = "0.2.0"
        with self.assertRaisesRegex(ValueError, "canonical case semantic version"):
            audit(data, self.inventory, cases=versions)

if __name__ == "__main__":
    unittest.main()
