"""Vector runner tests: execution and fail-closed controls."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from tools.run_conformance import ROOT, execute_vector, run

class ConformanceVectorTests(unittest.TestCase):
    def setUp(self):
        self.vector = json.loads((ROOT / "conformance/vectors/DTF-001.json").read_text())

    def test_vector_schema_rejects_wrong_types_before_execution(self):
        for change in ({"case_id": 1}, {"request": []}, {"targets": []},
                       {"vector_version": "9.0.0"}, {"expected_safe": "DENY"}):
            vector = copy.deepcopy(self.vector)
            vector.update(change)
            with self.subTest(change=change), self.assertRaises(ValueError):
                execute_vector(vector)

    def test_pair_executes_and_reports_real_denominator(self):
        report = run()
        self.assertEqual(report["total_canonical_cases"], 37)
        self.assertEqual(report["paired_executed_cases"], 1)
        self.assertEqual(report["independent_target_cases"], 0)
        self.assertEqual(report["independent_consumer_cases"], 0)
        outcomes = report["results"][0]["outcomes"]
        self.assertEqual(outcomes["safe"]["test_verdict"], "SATISFIED")
        self.assertEqual(outcomes["defective"]["test_verdict"], "VIOLATED")
        self.assertEqual(outcomes["safe"]["request_sha256"], outcomes["defective"]["request_sha256"])

    def test_unknown_adapter_and_path_fail_closed(self):
        for change in ({"adapter": "shell-v1"}, {"targets": {"safe": "../../tmp/malicious.py",
                         "defective": self.vector["targets"]["defective"]}}):
            v = copy.deepcopy(self.vector)
            v.update(change)
            with self.assertRaises(ValueError):
                execute_vector(v)

    def test_missing_request_and_case_version_fail_closed(self):
        for change in ({"request": {}}, {"case_version": "9.9.9"}):
            v = copy.deepcopy(self.vector)
            v.update(change)
            with self.assertRaises(ValueError):
                execute_vector(v)

    def test_malformed_vector_contract_fails_closed(self):
        malformed = [
            {"extra": "unrecognized"},
            {"expected_safe": []},
            {"expected_safe": ["DENY", "DENY"]},
            {"expected_safe": ["ALLOW"]},
            {"expected_safe": [{"unexpected": "object"}]},
            {"targets": {"safe": self.vector["targets"]["safe"],
                         "defective": self.vector["targets"]["safe"]}},
            {"targets": {"safe": self.vector["targets"]["safe"]}},
        ]
        for change in malformed:
            vector = copy.deepcopy(self.vector)
            vector.update(change)
            with self.subTest(change=change), self.assertRaises(ValueError):
                execute_vector(vector)

    def test_empty_vector_directory_has_zero_coverage(self):
        with tempfile.TemporaryDirectory() as d:
            report = run(Path(d))
            self.assertEqual(report["paired_executed_cases"], 0)
            self.assertEqual(report["total_canonical_cases"], 37)

if __name__ == "__main__":
    unittest.main()
