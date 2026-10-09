#!/usr/bin/env python3
"""Evaluate portable 0.2 fixture bindings without git; never invoke a target."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import jsonschema
from tools.case_digest import case_sha256, load_unique_case

ROOT = Path(__file__).resolve().parents[1]

def evaluate(binding: dict, corpus_root: Path = ROOT / "corpus") -> dict:
    schema = json.loads((ROOT / "schemas/execution-binding-v0.2.schema.json").read_text())
    jsonschema.validate(binding, schema)
    case = load_unique_case(corpus_root, binding["case_id"])
    if case["version"] != binding["case_version"]:
        raise ValueError("Case version mismatch")
    digest = case_sha256(case)
    if digest != binding["case_sha256"]:
        raise ValueError("Canonical case SHA-256 mismatch")
    if case["expected"]["dispositions"][binding["expected"]] != "allowed":
        raise ValueError("Expected safe disposition is not allowed")
    observed = binding["observed"]
    permitted = case["expected"]["dispositions"][observed] == "allowed"
    result = {
        "binding_version": "0.2.0",
        "case_id": binding["case_id"],
        "case_version": binding["case_version"],
        "case_sha256": digest,
        "adapter": "fixture-v1",
        "execution_class": "author-supplied-fixture",
        "scenario": binding["scenario"],
        "target_disposition": observed,
        "test_verdict": "SATISFIED" if permitted else "VIOLATED",
        "evidence": binding["evidence"],
    }
    result_schema = json.loads((ROOT / "schemas/execution-result-v0.2.schema.json").read_text())
    jsonschema.validate(result, result_schema)
    return result

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("binding", type=Path)
    parser.add_argument("--corpus-root", type=Path, default=ROOT / "corpus")
    args = parser.parse_args()
    result = evaluate(json.loads(args.binding.read_text()), args.corpus_root)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["test_verdict"] == "SATISFIED" else 1

if __name__ == "__main__":
    raise SystemExit(main())
