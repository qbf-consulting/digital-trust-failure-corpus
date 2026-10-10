#!/usr/bin/env python3
"""Versioned, allowlisted subprocess conformance vectors; no external adoption claim."""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from tools.case_digest import case_sha256, load_unique_case

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_TARGETS = frozenset({
    "examples/independent-consumer/authority_target.py",
    "examples/independent-consumer/defective_authority_target.py",
})

def execute_vector(vector: dict, corpus_root: Path = ROOT / "corpus") -> dict:
    if vector.get("vector_version") != "0.1.0" or vector.get("adapter") != "python-subprocess-v1":
        raise ValueError("Unknown vector version or adapter")
    if vector.get("execution_class") != "executed-synthetic-target":
        raise ValueError("Unverified execution class")
    case_id = vector["case_id"]
    case = load_unique_case(corpus_root, case_id)
    if vector.get("case_version") != case["version"]:
        raise ValueError("Case version mismatch")
    request = vector["request"]
    if not isinstance(request, dict) or not request:
        raise ValueError("Missing request")
    payload = json.dumps(request, sort_keys=True, separators=(",", ":")).encode()
    expected = {"safe": "SATISFIED", "defective": "VIOLATED"}
    if set(vector["targets"]) != set(expected):
        raise ValueError("Exactly two target roles required")
    outcomes = {}
    for role in ("safe", "defective"):
        relative = vector["targets"][role]
        if relative not in ALLOWED_TARGETS:
            raise ValueError("Unknown or unsafe target path")
        target = ROOT / relative
        process = subprocess.run([sys.executable, str(target)], input=payload,
                                 capture_output=True, timeout=10, check=False)
        if process.returncode != 0:
            raise ValueError("Target exited unsuccessfully")
        try:
            response = json.loads(process.stdout)
        except (UnicodeDecodeError, ValueError) as exc:
            raise ValueError("Invalid target JSON") from exc
        if not isinstance(response, dict) or response.get("disposition") not in ("PASS", "DENY", "INDETERMINATE"):
            raise ValueError("Unknown target disposition")
        disposition = response["disposition"]
        if disposition not in vector["expected_" + role]:
            raise ValueError("Target disagrees with vector oracle")
        allowed = case["expected"]["dispositions"][disposition] == "allowed"
        verdict = "SATISFIED" if allowed else "VIOLATED"
        if verdict != expected[role]:
            raise ValueError("Paired safe/defective invariant failed")
        outcomes[role] = {
            "target": relative,
            "target_sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
            "request_sha256": hashlib.sha256(payload).hexdigest(),
            "response_sha256": hashlib.sha256(process.stdout).hexdigest(),
            "raw_response": process.stdout.decode("utf-8"),
            "disposition": disposition, "test_verdict": verdict,
            "replay_command": [sys.executable, relative],
        }
    return {"case_id": case_id, "case_version": case["version"],
            "case_sha256": case_sha256(case),
            "execution_class": "executed-synthetic-target",
            "request": request, "outcomes": outcomes}

def run(vector_dir: Path = ROOT / "conformance/vectors", corpus_root: Path = ROOT / "corpus") -> dict:
    files = sorted(vector_dir.glob("DTF-*.json"))
    canonical = sorted(corpus_root.rglob("DTF-*.json"))
    case_ids = [json.loads(p.read_text())["id"] for p in canonical]
    if len(case_ids) != len(set(case_ids)):
        raise ValueError("Duplicate canonical case IDs")
    results = []
    for file in files:
        vector = json.loads(file.read_text())
        if file.stem != vector.get("case_id"):
            raise ValueError("Vector filename/case mismatch")
        results.append(execute_vector(vector, corpus_root))
    ids = [r["case_id"] for r in results]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate vectors")
    return {"total_canonical_cases": len(case_ids),
            "paired_executed_cases": len(ids),
            "paired_executed_case_ids": ids,
            "independent_target_cases": 0,
            "independent_consumer_cases": 0,
            "results": results}

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vector-dir", type=Path, default=ROOT / "conformance/vectors")
    args = parser.parse_args()
    print(json.dumps(run(args.vector_dir), sort_keys=True, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
