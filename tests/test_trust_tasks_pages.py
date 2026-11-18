"""End-to-end source-derived task navigation and false-success tests."""
import copy
import json
import unittest
from tools.build_trust_tasks_pages import build_pages
from tools.validate_trust_tasks_inventory import MANIFEST, PILOT
from tools.validate_acl_review import PATH as ACL_PATH

class NavigationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inventory=json.loads(MANIFEST.read_text())
        cls.pilot=json.loads(PILOT.read_text())
        cls.acl=json.loads(ACL_PATH.read_text())

    def test_complete_documented_version_path(self):
        pages=build_pages(self.inventory,self.pilot,self.acl)
        self.assertEqual(len(pages),44)
        self.assertIn("1391",pages["index.md"])
        self.assertIn("1340",pages["index.md"])
        self.assertIn("Independently reviewed:** 0",pages["index.md"])
        self.assertEqual(sum(s.count(" | "+chr(96)+"needs-review"+chr(96)+" |") for n,s in pages.items() if n!="index.md"),1340)
        self.assertEqual(sum(s.count(" | "+chr(96)+"research-screened"+chr(96)+" |") for n,s in pages.items() if n!="index.md"),51)

    def test_examined_version_navigates_to_complete_case_matrix(self):
        pages=build_pages(self.inventory,self.pilot,self.acl)
        self.assertIn("Full author-side case-examined:** 22",pages["index.md"])
        self.assertIn("Author case comparisons:** 814",pages["index.md"])
        self.assertIn("[37-case author matrix](../trust-tasks-audit-case-examination.md)",pages["audit.md"])
        self.assertIn("[37-case author matrix](../trust-tasks-discovery-case-examination.md)",pages["trust-task-discovery.md"])
        self.assertIn("[37-case author matrix](../trust-tasks-consent-case-examination.md)",pages["consent.md"])
        self.assertIn("not examined",pages["vta.md"])

    def test_no_match_is_not_implicit(self):
        self.assertIn("Unscreened versions are unresolved",build_pages(self.inventory,self.pilot,self.acl)["vta.md"])

    def test_false_independent_review(self):
        data=copy.deepcopy(self.acl)
        data["historical_screenings"][0]["independent_review"]="approved"
        with self.assertRaises(ValueError): build_pages(self.inventory,self.pilot,data)

    def test_unknown_case(self):
        data=copy.deepcopy(self.pilot)
        data["judgments"][0]["case_id"]="DTF-999"
        with self.assertRaises(ValueError): build_pages(self.inventory,data,self.acl)

    def test_forged_execution(self):
        data=copy.deepcopy(self.pilot)
        data["judgments"][0]["execution_evidence"]="external"
        with self.assertRaises(ValueError): build_pages(self.inventory,data,self.acl)

    def test_invented_version(self):
        data=copy.deepcopy(self.pilot)
        data["judgments"][0]["task_type_uri"] += "/invented"
        with self.assertRaises(ValueError): build_pages(self.inventory,data,self.acl)

    def test_stale_source(self):
        data=copy.deepcopy(self.inventory)
        data["records"][0]["spec_blob"]="0"*40
        with self.assertRaises(ValueError): build_pages(data,self.pilot,self.acl)
