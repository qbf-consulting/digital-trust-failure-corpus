#!/usr/bin/env python3
"""Bounded actual subprocess execution for DTF-001; no independent-adoption claim."""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from tools.case_digest import case_sha256, load_unique_case

ROOT = Path(__file__).resolve().parents[1]
TARGETS = {
    "safe": ROOT / "examples/independent-consumer/authority_target.py",
    "defective": ROOT / "examples/independent-consumer/defective_authority_target.py",
}
REQUEST = {"authority_state": "revoked", "action": "read", "authorized_actions": ["read"]}

def execute(role: str, corpus_root: Path = ROOT / "corpus") -> dict:
    if role not in TARGETS:
        raise ValueError("Unknown target adapter")
    case = load_unique_case(corpus_root, "DTF-001")
    target = TARGETS[role]
    request_bytes = json.dumps(REQUEST, sort_keys=True, separators=(",", ":")).encode()
    cmd = [sys.executable, str(target)]
    completed = subprocess.run(cmd, input=request_bytes, capture_output=True, timeout=10, check=False)
    if completed.returncode != 0:
        raise ValueError("Target execution failed")
    try:
        output = json.loads(completed.stdout)
    except (ValueError, UnicodeDecodeError) as exc:
        raise ValueError("Malformed target response") from exc
    if not isinstance(output, dict) or output.get("disposition") not in ("PASS", "DENY", "INDETERMINATE"):
        raise ValueError("Unrecognized target disposition")
    disposition = output["disposition"]
    allowed = case["expected"]["dispositions"][disposition] == "allowed"
    return {
        "case_id": "DTF-001", "case_version": case["version"],
        "case_sha256": case_sha256(case), "adapter": "python-subprocess-v1",
        "execution_class": "executed-synthetic-target", "target_role": role,
        "target_path": str(target.relative_to(ROOT)),
        "target_sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
        "request_sha256": hashlib.sha256(request_bytes).hexdigest(),
        "response_sha256": hashlib.sha256(completed.stdout).hexdigest(),
        "request": REQUEST, "response": output,
        "target_disposition": disposition,
        "test_verdict": "SATISFIED" if allowed else "VIOLATED",
        "replay_command": f"{sys.executable} {target.relative_to(ROOT)}",
    }

def paired(corpus_root: Path = ROOT / "corpus") -> dict:
    safe, defective = execute("safe", corpus_root), execute("defective", corpus_root)
    if safe["test_verdict"] != "SATISFIED" or defective["test_verdict"] != "VIOLATED":
        raise ValueError("Paired target invariant failed")
    if safe["request_sha256"] != defective["request_sha256"]:
        raise ValueError("Paired requests differ")
    return {"execution_class": "executed-synthetic-target", "cases_executed_paired": 1,
            "total_canonical_cases": 37, "paired_executed_case_ids": ["DTF-001"],
            "independently_maintained_target_cases": 0,
            "independent_dtfc_consumer_cases": 0,
            "safe": safe, "defective": defective}

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--role", choices=("safe", "defective", "paired"), default="paired")
    args = parser.parse_args()
    result = paired() if args.role == "paired" else execute(args.role)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
