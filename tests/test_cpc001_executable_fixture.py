import unittest

from tools.execute_cpc001 import SCENARIOS, execute, paired


class CPC001ExecutableFixtureTests(unittest.TestCase):
    def test_safe_target_satisfies_all_contract_scenarios(self):
        for scenario in SCENARIOS:
            with self.subTest(scenario=scenario):
                result = execute("safe", scenario)
                self.assertEqual(result["test_verdict"], "SATISFIED")
                self.assertEqual(result["observed_disposition"], result["expected_disposition"])
                self.assertEqual(result["execution_class"], "executed-synthetic-target")
                self.assertTrue(result["contract_ids"])

    def test_defective_target_is_detected(self):
        result = paired()
        self.assertTrue(result["known_defect_detected"])
        self.assertGreater(result["defective_target_violations"], 0)
        self.assertEqual(result["safe_target_satisfied"], len(SCENARIOS))

    def test_post_revocation_defect_is_visible(self):
        result = execute("defective", "post_revocation_deny")
        self.assertEqual(result["expected_disposition"], "DENY")
        self.assertEqual(result["observed_disposition"], "ALLOW")
        self.assertEqual(result["test_verdict"], "VIOLATED")

    def test_stale_authority_defect_is_visible(self):
        result = execute("defective", "stale_authority_indeterminate")
        self.assertEqual(result["expected_disposition"], "INDETERMINATE")
        self.assertEqual(result["observed_disposition"], "ALLOW")
        self.assertEqual(result["test_verdict"], "VIOLATED")


if __name__ == "__main__":
    unittest.main()
