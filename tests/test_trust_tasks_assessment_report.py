"""Assurance false-success regression on actual pinned assessment inputs."""
import copy
import json
import unittest
from tools.trust_tasks_assessment_report import build_report, render, review_decision
from tools.validate_trust_tasks_inventory import MANIFEST, PILOT, ROOT
from tools.validate_acl_review import PATH as ACL_PATH

ATTEST = ROOT / "research/external-sources/trust-tasks/registry-reconciliation.json"

class AssessmentReportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inv = json.loads(MANIFEST.read_text())
        cls.pilot = json.loads(PILOT.read_text())
        cls.acl = json.loads(ACL_PATH.read_text())
        cls.att = json.loads(ATTEST.read_text())

    def report(self, i=None, p=None, a=None, att=None):
        return build_report(i or self.inv,p or self.pilot,a or self.acl,att or self.att)

    def test_real_source_report(self):
        r=self.report()
        s=r["summary"]
        self.assertEqual((s["registry_versions"],s["screened_versions"],s["pending_versions"]), (1391,51,1340))
        self.assertEqual(s["independently_reviewed_versions"],0)
        self.assertFalse(s["semantic_completion_claim"])
        self.assertEqual(len(r["records"]),1391)
        self.assertEqual(len(r["families"]),43)
        self.assertIn("not a complete semantic assessment",render(r))

    def test_author_case_dimensions_reconcile(self):
        r=self.report()
        s=r["summary"]
        self.assertEqual(r["schema_version"], "0.2.0")
        self.assertEqual((s["author_case_examined_versions"], s["author_case_comparisons"]),
                         (14, 518))
        self.assertEqual((s["author_conditional_candidates"],
                          s["author_not_established_from_task"]), (114, 404))
        complete=[x for x in r["records"] if x["author_case_examination"]["state"] == "author-case-examined"]
        self.assertEqual(len(complete), 14)
        self.assertEqual(sum(x["author_case_examination"]["canonical_case_count"] for x in complete), 518)
        self.assertEqual(sum(x["author_case_examination"]["state"] == "not-examined" for x in r["records"]), 1377)
        self.assertFalse(any(x["independent_review_state"] != "not-established" for x in complete))
        self.assertIn("Not established from task source", render(r))

    def test_author_review_cannot_claim_independent_approval(self):
        from jsonschema import Draft202012Validator, ValidationError
        schema=json.loads((ROOT / "schemas/trust-tasks-assessment-report.schema.json").read_text())
        report=self.report()
        examined=next(x for x in report["records"] if x["author_case_examination"]["state"] == "author-case-examined")
        examined["author_case_examination"]["independent_acceptance"] = "completed"
        with self.assertRaises(ValidationError):
            Draft202012Validator(schema).validate(report)

    def test_author_case_included_by_exact_version_not_by_slug(self):
        report=self.report()
        examined={x["type_uri"] for x in report["records"]
                  if x["author_case_examination"]["state"] == "author-case-examined"}
        self.assertIn("https://trusttasks.org/spec/audit/list/0.1",examined)
        self.assertIn("https://trusttasks.org/spec/audit/list/0.2",examined)
        self.assertNotIn("https://trusttasks.org/spec/acl/grant/0.3",examined)

    def test_unreviewed_is_not_no_match(self):
        r=self.report()
        self.assertEqual(sum(x["screening_state"]=="needs-review" for x in r["records"]),1340)
        self.assertFalse(any(x["independent_review_state"]=="reviewed-no-match" for x in r["records"]))

    def test_missing_source_is_rejected(self):
        i=copy.deepcopy(self.inv);i["records"].pop()
        with self.assertRaises(ValueError):self.report(i=i)

    def test_fake_independent_approval_fails(self):
        a=copy.deepcopy(self.acl);a["current"][0]["independent_review"]="completed"
        with self.assertRaises(ValueError):self.report(a=a)

    def test_fake_execution_fails(self):
        p=copy.deepcopy(self.pilot);p["judgments"][0]["execution_evidence"]="independent"
        with self.assertRaises(ValueError):self.report(p=p)

    def test_bad_registry_evidence_fails(self):
        a=copy.deepcopy(self.att);a["registry_versions"]=1200
        with self.assertRaises(ValueError):self.report(att=a)

    def test_unknown_case_fails(self):
        a=copy.deepcopy(self.acl);a["historical_screenings"][0]["case_id"]="DTF-999"
        with self.assertRaises(ValueError):self.report(a=a)

    def test_no_match_without_full_case_review_fails(self):
        with self.assertRaises(ValueError):review_decision({
            "decision":"reviewed-no-match","independent_review":"completed",
            "reviewer":"Reviewer A", "reviewed_source_blob":"1"*40,
            "case_ids":[],"cases_examined":["DTF-002"],
            "reasoning":"Source inspected.","challenge_record":"challenge #1"
        },{"DTF-002","DTF-003"})

    def test_independent_approval_without_challenge_fails(self):
        with self.assertRaises(ValueError):review_decision({
            "decision":"reviewed-mapped","independent_review":"completed",
            "reviewer":"Reviewer A","reviewed_source_blob":"1"*40,
            "case_ids":["DTF-002"],"reasoning":"source checked","challenge_record":""
        },{"DTF-002"})

    def test_blocked_evidence_does_not_count_as_review_complete(self):
        row=self.inv["records"][0]
        review={
            "task_type_uri":"https://trusttasks.org/spec/"+row["slug"]+"/"+row["version"],
            "decision":"blocked-evidence",
            "independent_review":"challenged-unresolved",
            "reviewer":"External reviewer (synthetic test only)",
            "reviewed_source_blob":row["spec_blob"],
            "case_ids":[],
            "reasoning":"The available source evidence supports contradictory interpretations.",
            "challenge_record":"Synthetic unresolved challenge test; not a real reviewer."
        }
        result=build_report(self.inv,self.pilot,self.acl,self.att,accepted=[review])
        self.assertEqual(result["summary"]["independently_reviewed_versions"],0)
        self.assertEqual(result["summary"]["blocked_review_versions"],1)
        self.assertFalse(result["summary"]["independent_review_complete"])

    def test_blocked_result_cannot_claim_completed_review(self):
        with self.assertRaises(ValueError):
            review_decision({
                "decision":"blocked-evidence","independent_review":"completed",
                "reviewer":"Reviewer A","reviewed_source_blob":"1"*40,
                "case_ids":[],"reasoning":"Contradiction still unresolved",
                "challenge_record":"Contradictory evidence"
            },{"DTF-002"})

    def test_machine_schema_accepts_source_report(self):
        from jsonschema import Draft202012Validator
        schema=json.loads((ROOT / "schemas/trust-tasks-assessment-report.schema.json").read_text())
        Draft202012Validator.check_schema(schema)
        Draft202012Validator(schema).validate(self.report())

    def test_machine_schema_rejects_false_review_state(self):
        from jsonschema import Draft202012Validator, ValidationError
        schema=json.loads((ROOT / "schemas/trust-tasks-assessment-report.schema.json").read_text())
        report=self.report()
        report["records"][0]["independent_review_state"]="safe"
        with self.assertRaises(ValidationError):
            Draft202012Validator(schema).validate(report)

    def test_machine_schema_rejects_missing_provenance(self):
        from jsonschema import Draft202012Validator, ValidationError
        schema=json.loads((ROOT / "schemas/trust-tasks-assessment-report.schema.json").read_text())
        report=self.report()
        report["records"][0]["source"].pop("spec_blob")
        with self.assertRaises(ValidationError):
            Draft202012Validator(schema).validate(report)
