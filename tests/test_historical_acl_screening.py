"""Historical version research screening rejects forged assurance and false-positive case claims."""
import copy
import json
import unittest
from tools.validate_historical_acl_screening import check
from tools.validate_acl_review import PATH
from tools.validate_trust_tasks_inventory import MANIFEST

class TestHistoricalScreening(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=json.loads(PATH.read_text())
        cls.inventory=json.loads(MANIFEST.read_text())

    def test_valid(self):
        self.assertEqual(check(self.data,self.inventory)["source_screened"],13)

    def test_duplicate(self):
        x=copy.deepcopy(self.data);x["historical_screenings"][1]=copy.deepcopy(x["historical_screenings"][0])
        with self.assertRaises(ValueError):check(x,self.inventory)

    def test_incorrect_case(self):
        x=copy.deepcopy(self.data);x["historical_screenings"][0]["case_id"]="DTF-999"
        with self.assertRaises(ValueError):check(x,self.inventory)

    def test_false_assurance(self):
        x=copy.deepcopy(self.data);x["historical_screenings"][0]["independent_review"]="approved"
        with self.assertRaises(ValueError):check(x,self.inventory)

    def test_unsubstantiated_mapping(self):
        x=copy.deepcopy(self.data);x["historical_screenings"][0]["test_hypothesis"]=""
        with self.assertRaises(ValueError):check(x,self.inventory)

    def test_source_revision_mismatch(self):
        x=copy.deepcopy(self.data);x["historical_screenings"][0]["source_blob"]="0"*40
        with self.assertRaises(ValueError):check(x,self.inventory)
