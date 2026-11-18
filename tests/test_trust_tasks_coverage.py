"""Source-derived completeness and generated-doc false-success tests."""
import copy
import json
import unittest
from tools.trust_tasks_coverage import calculate, render, DOC
from tools.validate_trust_tasks_inventory import MANIFEST, PILOT
from tools.validate_acl_review import PATH as ACL_PATH


class CoverageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inventory = json.loads(MANIFEST.read_text())
        cls.pilot = json.loads(PILOT.read_text())
        cls.acl = json.loads(ACL_PATH.read_text())

    def test_unique_screening_not_double_counted(self):
        stats = calculate(self.inventory, self.pilot, self.acl)
        self.assertEqual((stats["source_versions"], stats["original_pilot"], stats["acl_screening"],
                          stats["overlapping_source_versions"], stats["screened_unique"], stats["pending"]),
                         (1391, 12, 20, 3, 37, 1354))
        self.assertFalse(stats["semantic_review_complete"])
        self.assertTrue(stats["inventory_publication_reconciled"])

    def test_generated_docs_are_derived(self):
        self.assertEqual(render(calculate(self.inventory, self.pilot, self.acl)), DOC.read_text())

    def test_missing_inventory_row_is_not_coverage(self):
        changed = copy.deepcopy(self.inventory)
        changed["records"].pop()
        with self.assertRaises(ValueError):
            calculate(changed, self.pilot, self.acl)

    def test_forged_additional_mapping_is_rejected(self):
        changed = copy.deepcopy(self.acl)
        changed["current"].append(copy.deepcopy(changed["current"][0]))
        with self.assertRaises(ValueError):
            calculate(self.inventory, self.pilot, changed)


if __name__ == "__main__":
    unittest.main()
