#!/usr/bin/env python3
"""Deterministic illustrative DTFC consumer. Not an implementation conformance claim."""
import argparse
import json
from pathlib import Path
import jsonschema
import subprocess

ROOT = Path(__file__).resolve().parents[1]

def evaluate(binding, corpus_root=ROOT / "corpus"):
    schema = json.loads((ROOT / "schemas/execution-binding.schema.json").read_text())
    jsonschema.validate(binding, schema)
    revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    if binding["case_revision"] != revision:
        raise ValueError("Case revision must match checked-out repository HEAD")
    matches = [p for p in corpus_root.rglob("*.json") if json.loads(p.read_text()).get("id") == binding["case_id"]]
    if len(matches) != 1:
        raise ValueError("Case must resolve uniquely")
    case = json.loads(matches[0].read_text())
    if case["version"] != binding["case_version"]:
        raise ValueError("Case version mismatch")
    if case["expected"]["dispositions"][binding["expected"]] != "allowed":
        raise ValueError("Expected outcome is not allowed by case")
    observed = binding["observed"]
    allowed = case["expected"]["dispositions"][observed] == "allowed"
    result = dict(binding_version="0.1.0", case_id=binding["case_id"],
                  case_version=binding["case_version"], case_revision=binding["case_revision"],
                  scenario=binding["scenario"], target_disposition=observed,
                  test_verdict="SATISFIED" if allowed else "VIOLATED", evidence=binding["evidence"])
    jsonschema.validate(result, json.loads((ROOT / "schemas/execution-result.schema.json").read_text()))
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("binding", type=Path)
    args = parser.parse_args()
    result = evaluate(json.loads(args.binding.read_text()))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["test_verdict"] == "SATISFIED" else 1

if __name__ == "__main__":
    raise SystemExit(main())
