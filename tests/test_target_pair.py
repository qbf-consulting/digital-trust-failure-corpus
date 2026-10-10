"""Executed synthetic DTF-001 pair; never conflate with independent adoption."""
import unittest
from tools.execute_target_pair import execute, paired

class TargetPairTests(unittest.TestCase):
    def test_actual_safe_and_defective_processes(self):
        result = paired()
        self.assertEqual(result["cases_executed_paired"], 1)
        self.assertEqual(result["total_canonical_cases"], 37)
        self.assertEqual(result["independently_maintained_target_cases"], 0)
        self.assertEqual(result["independent_dtfc_consumer_cases"], 0)
        self.assertEqual(result["safe"]["test_verdict"], "SATISFIED")
        self.assertEqual(result["defective"]["test_verdict"], "VIOLATED")
        self.assertEqual(result["safe"]["request_sha256"], result["defective"]["request_sha256"])
        self.assertEqual(result["defective"]["target_disposition"], "PASS")

    def test_unknown_target_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "Unknown target adapter"):
            execute("untrusted")

if __name__ == "__main__":
    unittest.main()
