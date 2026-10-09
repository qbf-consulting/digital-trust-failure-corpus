"""OPA adapter parsing tests use a fake executable; not external-engine evidence."""
import json
import tempfile
import unittest
from pathlib import Path
from tools.run_opa_consumer import ROOT, evaluate_opa

class OpaAdapterTests(unittest.TestCase):
    def test_malformed_result_shapes_rejected(self):
        malformed = ["null", "{}", '{"result":null}', '{"result":{}}',
                     '{"result":[null]}', '{"result":[{}]}',
                     '{"result":[{"expressions":null}]}',
                     '{"result":[{"expressions":[null]}]}',
                     '{"result":[{"expressions":[{"value":"false"}]}]}']
        for payload in malformed:
            with self.subTest(payload=payload):
                with tempfile.TemporaryDirectory() as temp:
                    binary = Path(temp) / "fake-opa"
                    binary.write_text('#!/usr/bin/env python3\nimport sys\nif "version" in sys.argv: print("test-only")\nelse: print(' + repr(payload) + ')\n')
                    binary.chmod(0o755)
                    with self.assertRaises(ValueError):
                        evaluate_opa(binary, ROOT / "examples/opa-consumer/safe.rego", {})

    def test_missing_binary_is_execution_failure(self):
        with self.assertRaises(OSError):
            evaluate_opa("/nonexistent/opa", ROOT / "examples/opa-consumer/safe.rego", {})

    def test_fake_cli_parses_boolean_but_is_not_opa_evidence(self):
        with tempfile.TemporaryDirectory() as temp:
            binary = Path(temp) / "fake-opa"
            binary.write_text('#!/usr/bin/env python3\nimport json,sys\nif "version" in sys.argv: print("test-only")\nelse: print(json.dumps({"result":[{"expressions":[{"value":False}]}]}))\n')
            binary.chmod(0o755)
            result = evaluate_opa(binary, ROOT / "examples/opa-consumer/safe.rego", {})
            self.assertEqual(result["disposition"], "DENY")
            self.assertEqual(len(result["target_sha256"]), 64)
            self.assertEqual(result["target_version"], "test-only")

    def test_fake_cli_missing_decision_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            binary = Path(temp) / "fake-opa"
            binary.write_text('#!/usr/bin/env python3\nimport json,sys\nif "version" in sys.argv: print("test-only")\nelse: print(json.dumps({"result":[]}))\n')
            binary.chmod(0o755)
            with self.assertRaises(ValueError):
                evaluate_opa(binary, ROOT / "examples/opa-consumer/safe.rego", {})

if __name__ == "__main__":
    unittest.main()
