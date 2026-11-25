"""Regression and false-success checks for the ceremony research sidecars."""
import copy
import unittest

from tools.validate_ceremony_assessment import check, load_inputs


class CeremonyAssessmentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inputs = load_inputs()

    def setUp(self):
        self.data = copy.deepcopy(self.inputs)
        self.rows = self.data["matrix"]["authority"]["dispositions"]

    def reject(self, pattern):
        with self.assertRaisesRegex(ValueError, pattern):
            check(self.data)

    def test_actual_research_population(self):
        result = check(self.data)
        self.assertEqual(result["cells"], 111)
        self.assertEqual(result["controls"], 4)
        self.assertEqual(result["comparison_rows"], 37)
        self.assertEqual(result["prior_judgment_references"], 222)
        self.assertEqual(result["semantic_acceptance"], "not-established")
        self.assertEqual(result["target_execution"], "not-established")
        self.assertEqual(sum(result["dispositions"].values()), 111)

    def test_missing_cell(self):
        self.rows.pop()
        self.reject("missing or extra matrix cell")

    def test_duplicate_cell(self):
        self.rows.append(copy.deepcopy(self.rows[0]))
        self.reject("duplicate matrix cell")

    def test_extra_case(self):
        self.rows[0]["case_id"] = "DTF-999"
        self.reject("missing or extra matrix cell")

    def test_wrong_family(self):
        self.data["matrix"]["authority"]["family"] = "privacy"
        self.reject("matrix metadata")

    def test_case_blob_drift(self):
        self.rows[0]["source_blob"] = "0" * 40
        self.reject("canonical binding drift")

    def test_case_version_drift(self):
        self.rows[0]["case_version"] = "9.9.9"
        self.reject("canonical binding drift")

    def test_trigger_drift(self):
        self.rows[0]["trigger"] = "A different trigger"
        self.reject("canonical trigger")

    def test_falsification_drift(self):
        self.rows[0]["falsification"].pop()
        self.reject("canonical trigger")

    def test_unknown_task(self):
        self.rows[0]["task_versions"] = ["https://trusttasks.org/spec/unknown/0.1"]
        self.reject("unknown or duplicate task")

    def test_candidate_without_anchor(self):
        self.rows[0]["disposition"] = "conditional-candidate"
        self.rows[0]["task_versions"] = []
        self.reject("without task anchor")

    def test_missing_rationale(self):
        self.rows[0]["precondition_analysis"] = " "
        self.reject("missing precondition_analysis")

    def test_collapsed_propositions(self):
        self.rows[0]["relying_proposition"] = self.rows[0]["local_proposition"]
        self.reject("collapsed local and relying")

    def test_false_observed_failure(self):
        self.rows[0]["observed_failure"] = True
        self.reject("unsupported assurance promotion")

    def test_false_independent_review(self):
        self.rows[0]["independent_review"] = "accepted"
        self.reject("unsupported assurance promotion")

    def test_missing_control(self):
        self.data["controls"]["designs"].pop()
        self.reject("control coverage drift")

    def test_unknown_control_case(self):
        self.data["controls"]["designs"][0]["case_ids"].append("DTF-999")
        self.reject("bad control case reference")

    def test_control_task_pin_drift(self):
        self.data["controls"]["designs"][0]["task_refs"][0]["schema_blob"] = "0" * 40
        self.reject("control task blob drift")

    def test_control_collapsed_states(self):
        outcome = self.data["controls"]["designs"][0]["negative"]
        outcome["legitimacy"] = outcome["execution"]
        self.reject("collapsed control determinations")

    def test_false_executed_control(self):
        self.data["controls"]["designs"][0]["evidence_status"] = "executed"
        self.reject("unsupported control assurance")

    def test_prior_decision_drift(self):
        ref = self.data["comparison"]["rows"][0]["prior_decisions"][0]
        ref["source_section"] = "Different section"
        self.reject("prior judgment binding drift")

    def test_reconciliation_drift(self):
        self.data["comparison"]["case_reconciliation"]["cases"][0]["prior_blob"] = "0" * 40
        self.reject("reconciliation binding drift")


if __name__ == "__main__":
    unittest.main()
