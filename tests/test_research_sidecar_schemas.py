"""Research sidecar schemas do not modify the canonical case contract."""
import copy
import json
import unittest
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SAMPLES = [
    ("schemas/research-external-crosswalk.schema.json", "research/external-sources/crosswalk.json"),
    ("schemas/research-tool-output-scenario.schema.json", "research/tool-output-boundary/scenario.json"),
]

class ResearchSidecarSchemaTests(unittest.TestCase):
    def test_valid_research_sidecars(self):
        for schema_path, sample_path in SAMPLES:
            with self.subTest(sample=sample_path):
                schema = json.loads((ROOT / schema_path).read_text())
                Draft202012Validator.check_schema(schema)
                instance = json.loads((ROOT / sample_path).read_text())
                Draft202012Validator(schema, format_checker=FormatChecker()).validate(instance)

    def test_reject_malformed_crosswalk(self):
        schema = json.loads((ROOT / SAMPLES[0][0]).read_text())
        original = json.loads((ROOT / SAMPLES[0][1]).read_text())
        for mutation in (lambda x: x["records"][0].update(confidence="verified"),
                         lambda x: x["records"][0].update(case_ids=["not-a-case"]),
                         lambda x: x.update(unexpected=True)):
            item = copy.deepcopy(original)
            mutation(item)
            with self.assertRaises(Exception):
                Draft202012Validator(schema, format_checker=FormatChecker()).validate(item)

    def test_reject_executed_claim_in_hypothetical_scenario(self):
        schema = json.loads((ROOT / SAMPLES[1][0]).read_text())
        item = json.loads((ROOT / SAMPLES[1][1]).read_text())
        item["status"] = "executed"
        with self.assertRaises(Exception):
            Draft202012Validator(schema).validate(item)

if __name__ == "__main__":
    unittest.main()
