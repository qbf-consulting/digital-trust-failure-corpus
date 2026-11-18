"""Negative / false-success regression for eight source-pinned consent versions."""
import copy
import json
import unittest
from tools.validate_trust_tasks_inventory import MANIFEST
from tools.validate_consent_case_examination import PATH, check

class ConsentCaseExaminationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(PATH.read_text())
        cls.inventory = json.loads(MANIFEST.read_text())
    def invalid(self, data):
        with self.assertRaises(ValueError):
            check(data,self.inventory)
    def test_complete_canonical_case_set(self):
        result=check(self.data,self.inventory)
        self.assertEqual((result["versions"],result["comparisons"]), (8,296))
        self.assertEqual((result["conditional_candidates"],result["not_established_from_task"]),(61,235))
        self.assertEqual(result["independently_accepted"],0)
    def test_omit_version_fails(self):
        d=copy.deepcopy(self.data);d["records"].pop();self.invalid(d)
    def test_omit_case_fails(self):
        d=copy.deepcopy(self.data);d["records"][0]["decisions"].pop();self.invalid(d)
    def test_duplicate_case_fails(self):
        d=copy.deepcopy(self.data);d["records"][0]["decisions"][0]["case_id"]=d["records"][0]["decisions"][1]["case_id"];self.invalid(d)
    def test_wrong_schema_digest_fails(self):
        d=copy.deepcopy(self.data);d["records"][5]["schema_blob"]="0"*40;self.invalid(d)
    def test_false_review_acceptance_fails(self):
        d=copy.deepcopy(self.data);d["records"][5]["independent_acceptance"]="completed";self.invalid(d)
    def test_false_target_execution_fails(self):
        d=copy.deepcopy(self.data);d["records"][5]["target_execution"]="independent-target";self.invalid(d)
    def test_unjustified_no_match_fails(self):
        d=copy.deepcopy(self.data);d["records"][0]["decisions"][0]["disposition"]="reviewed-no-match";self.invalid(d)
    def test_without_test_hypothesis_fails(self):
        d=copy.deepcopy(self.data)
        next(x for x in d["records"][1]["decisions"] if x["disposition"]=="conditional-candidate")["test_hypothesis"]=""
        self.invalid(d)
    def test_missing_version_delta_fails(self):
        d=copy.deepcopy(self.data);d["records"][5].pop("version_delta");self.invalid(d)
    def test_cursor_sync_token_version_mismatch_fails(self):
        d=copy.deepcopy(self.data);d["records"][5]["version_delta"]["claim"]="The two variants are byte-for-byte equivalent.";self.invalid(d)
    def test_direct_vs_bridge_attested_decision_boundary(self):
        decision=next(r for r in self.data["records"] if r["type_uri"].endswith("/decision/1.0"))
        row=next(x for x in decision["decisions"] if x["case_id"]=="DTF-013")
        self.assertEqual(row["disposition"],"conditional-candidate")
        self.assertIn("bridge",row["rationale"].lower())
    def test_cache_lifecycle_under_revocation(self):
        for suffix in ("list/1.0","list/1.1","revoke/1.0"):
            record=next(r for r in self.data["records"] if r["type_uri"] == "https://trusttasks.org/spec/consent/" + suffix)
            self.assertEqual(next(x for x in record["decisions"] if x["case_id"]=="DTF-021")["disposition"],"conditional-candidate")

if __name__=="__main__":
    unittest.main()
