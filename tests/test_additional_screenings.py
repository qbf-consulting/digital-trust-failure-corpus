import copy,json,unittest
from tools.validate_additional_screenings import PATH,MANIFEST,check
class AdditionalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=json.loads(PATH.read_text());cls.inv=json.loads(MANIFEST.read_text())
    def test_pinned(self):self.assertEqual(check(self.data,self.inv)["screened"],14)
    def test_missing(self):
        d=copy.deepcopy(self.data);d["records"].pop()
        with self.assertRaises(ValueError):check(d,self.inv)
    def test_forged_source(self):
        d=copy.deepcopy(self.data);d["records"][0]["source_blob"]="0"*40
        with self.assertRaises(ValueError):check(d,self.inv)
    def test_unknown_case(self):
        d=copy.deepcopy(self.data);d["records"][0]["case_id"]="DTF-999"
        with self.assertRaises(ValueError):check(d,self.inv)
    def test_false_review(self):
        d=copy.deepcopy(self.data);d["records"][0]["independent_review"]="completed"
        with self.assertRaises(ValueError):check(d,self.inv)
    def test_false_inheritance(self):
        d=copy.deepcopy(self.data);d["records"][0]["version_inheritance"]="equivalent"
        with self.assertRaises(ValueError):check(d,self.inv)
