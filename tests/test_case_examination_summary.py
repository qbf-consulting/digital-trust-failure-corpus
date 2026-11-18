"""Keep author research checkpoint totals derived from exact pinned case records."""
import json
import re
import unittest
from tools.validate_trust_tasks_inventory import ROOT, MANIFEST
from tools.validate_audit_case_examination import PATH as AUDIT, check as audit_check
from tools.validate_governance_case_examination import PATH as GOVERNANCE, check as governance_check
from tools.validate_task_consent_case_examination import PATH as CONSENT, check as consent_check
from tools.validate_discovery_case_examination import PATH as DISCOVERY, check as discovery_check

class CaseExaminationSummaryTests(unittest.TestCase):
    def test_checkpoint_reconciles_all_family_records(self):
        inventory = json.loads(MANIFEST.read_text())
        packages = [
            audit_check(json.loads(AUDIT.read_text()), inventory),
            governance_check(json.loads(GOVERNANCE.read_text()), inventory),
            consent_check(json.loads(CONSENT.read_text()), inventory),
            discovery_check(json.loads(DISCOVERY.read_text()), inventory),
        ]
        total = lambda k: sum(package[k] for package in packages)
        checkpoint = (ROOT / "docs/trust-tasks-research-checkpoint.md").read_text()
        measures = {
            "Fully case-examined pinned task versions": str(total("versions")) + " of 1,391",
            "Explicit case comparisons": str(total("comparisons")),
            "Conditional candidate applicability cells": str(total("conditional_candidates")),
            "Case comparisons not established by task semantics": str(total("not_established_from_task")),
            "Previously source-screened versions still lacking full case comparison": str(51 - total("versions")),
            "Versions not yet source-screened": "1,340",
            "Independently accepted 37-case dispositions": "0",
        }
        for label, value in measures.items():
            self.assertIn("| " + label + " | " + value + " |", checkpoint)
        self.assertEqual(total("comparisons"), 37 * total("versions"))
        self.assertEqual(total("comparisons"), total("conditional_candidates") + total("not_established_from_task"))
        self.assertEqual(total("independently_accepted"), 0)

if __name__ == "__main__":
    unittest.main()
