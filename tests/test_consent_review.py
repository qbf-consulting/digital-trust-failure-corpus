"""Consent family evidence and false-assurance regression tests."""
import json
import copy
import unittest
from tools.validate_consent_review import PATH, MANIFEST, check

class ConsentReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=json.loads(PATH.read_text())
        cls.inventory=json.loads(MANIFEST.read_text())

    def test_family_complete_for_initial_screening(self):
        self.assertEqual(check(self.data,self.inventory)["research_screened"],8)

    def test_missing_version(self):
        x=copy.deepcopy(self.data);x["records"].pop()
        with self.assertRaises(ValueError):check(x,self.inventory)

    def test_duplicate_version(self):
        x=copy.deepcopy(self.data);x["records"][1]=copy.deepcopy(x["records"][0])
        with self.assertRaises(ValueError):check(x,self.inventory)

    def test_wrong_blob(self):
        x=copy.deepcopy(self.data);x["records"][0]["source_blob"]="0"*40
        with self.assertRaises(ValueError):check(x,self.inventory)

    def test_claimed_independent_review(self):
        x=copy.deepcopy(self.data);x["records"][0]["independent_review"]="completed"
        with self.assertRaises(ValueError):check(x,self.inventory)

    def test_false_case_completeness(self):
        x=copy.deepcopy(self.data);x["records"][0]["case_search_complete"]=True
        with self.assertRaises(ValueError):check(x,self.inventory)

    def test_false_version_equivalence(self):
        x=copy.deepcopy(self.data);x["version_delta"]["equivalence_asserted"]=True
        with self.assertRaises(ValueError):check(x,self.inventory)

    def test_unknown_case(self):
        x=copy.deepcopy(self.data);x["records"][0]["case_id"]="DTF-999"
        with self.assertRaises(ValueError):check(x,self.inventory)
