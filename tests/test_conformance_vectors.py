"""Vector runner tests: execution and fail-closed controls."""
import copy
import json
import tempfile
import unittest
from unittest.mock import patch
import subprocess
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

    def test_unavailable_and_timed_out_target_fail_closed(self):
        for failure in (OSError("unavailable"), subprocess.TimeoutExpired("python", 10)):
            with self.subTest(failure=type(failure).__name__):
                with patch("tools.run_conformance.subprocess.run", side_effect=failure):
                    with self.assertRaisesRegex(ValueError, "unavailable or timed out"):
                        execute_vector(self.vector)

    def test_pair_executes_and_reports_real_denominator(self):
        report = run()
        self.assertEqual(report["total_canonical_cases"], 37)
        self.assertEqual(report["paired_executed_cases"], 3)
        self.assertEqual(report["independent_target_cases"], 0)
        self.assertEqual(report["independent_consumer_cases"], 0)
        self.assertEqual(set(report["paired_executed_case_ids"]), {"DTF-001", "DTF-023", "DTF-027"})
        for result in report["results"]:
            self.assertEqual(result["outcomes"]["safe"]["test_verdict"], "SATISFIED")
            self.assertEqual(result["outcomes"]["defective"]["test_verdict"], "VIOLATED")
        outcomes = report["results"][0]["outcomes"]
        self.assertEqual(outcomes["safe"]["test_verdict"], "SATISFIED")
        self.assertEqual(outcomes["defective"]["test_verdict"], "VIOLATED")
        self.assertEqual(outcomes["safe"]["request_sha256"], outcomes["defective"]["request_sha256"])

    def test_worked_evidence_is_observed_and_hashed_for_seam_cases(self):
        report = run()
        by_id = {result["case_id"]: result for result in report["results"]}
        for case_id in ("DTF-023", "DTF-027"):
            with self.subTest(case_id=case_id):
                result = by_id[case_id]
                safe = result["outcomes"]["safe"]
                defective = result["outcomes"]["defective"]
                self.assertEqual(safe["disposition"], "INDETERMINATE")
                self.assertEqual(defective["disposition"], "PASS")
                self.assertEqual(safe["test_verdict"], "SATISFIED")
                self.assertEqual(defective["test_verdict"], "VIOLATED")
                self.assertEqual(safe["request_sha256"], defective["request_sha256"])
                for outcome in (safe, defective):
                    self.assertEqual(json.loads(outcome["raw_response"])["disposition"], outcome["disposition"])
                    self.assertEqual(len(outcome["target_sha256"]), 64)
                    self.assertEqual(len(outcome["response_sha256"]), 64)

    def test_target_revision_pin_tampering_fails_before_execution(self):
        vector = copy.deepcopy(self.vector)
        vector["target_git_blob_sha1"]["safe"] = "0" * 40
        with patch("tools.run_conformance.subprocess.run") as launched:
            with self.assertRaisesRegex(ValueError, "pinned Git blob"):
                execute_vector(vector)
            launched.assert_not_called()

    def test_target_revision_pin_contract_rejects_missing_and_invalid(self):
        for update in (None, {"safe": "invalid", "defective": self.vector["target_git_blob_sha1"]["defective"]}):
            vector = copy.deepcopy(self.vector)
            if update is None:
                del vector["target_git_blob_sha1"]
            else:
                vector["target_git_blob_sha1"] = update
            with self.assertRaises(ValueError):
                execute_vector(vector)

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
