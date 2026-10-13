#!/usr/bin/env python3
"""Execute the CPC-001 synthetic protected-resource fixture.

The runner emits reproducible local evidence for the CPC-001 protection
contracts. It is executed-synthetic-target evidence only; it is not production
assurance and not independent adoption evidence.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TARGETS = {
    "safe": ROOT / "examples/cpc-001/protected_resource.py",
    "defective": ROOT / "examples/cpc-001/defective_protected_resource.py",
}

BASE_REQUEST: dict[str, Any] = {
    "consumer_id": "consumer:example:alice",
    "agent_id": "agentreg:example:shopping-agent",
    "action": "purchase.approve",
    "resource": "cart:123",
    "evaluation_time": "2026-10-13T01:00:00Z",
    "observed_authority_version": 2,
    "authority_source_available": True,
    "nonce": "nonce-001",
    "used_nonces": [],
    "authority": {
        "delegation_id": "delegation:cpc-001:001",
        "current_version": 2,
        "effective_from": "2026-10-13T00:00:00Z",
        "effective_until": "2026-10-14T00:00:00Z",
        "revoked_at": None,
        "actions": ["purchase.approve"],
        "resources": ["cart:123"],
        "conflict": False,
    },
}

SCENARIOS: dict[str, dict[str, Any]] = {
    "in_scope_allow": {"expected": "ALLOW", "mutations": {}},
    "out_of_scope_action_deny": {"expected": "DENY", "mutations": {"action": "purchase.refund"}},
    "out_of_scope_resource_deny": {"expected": "DENY", "mutations": {"resource": "cart:999"}},
    "post_revocation_deny": {
        "expected": "DENY",
        "mutations": {"authority.revoked_at": "2026-10-13T00:30:00Z"},
    },
    "stale_authority_indeterminate": {
        "expected": "INDETERMINATE",
        "mutations": {"observed_authority_version": 1},
    },
    "unavailable_authority_indeterminate": {
        "expected": "INDETERMINATE",
        "mutations": {"authority_source_available": False},
    },
    "conflicting_authority_indeterminate": {
        "expected": "INDETERMINATE",
        "mutations": {"authority.conflict": True},
    },
    "replay_deny": {
        "expected": "DENY",
        "mutations": {"used_nonces": ["nonce-001"]},
    },
}


def set_path(obj: dict[str, Any], dotted: str, value: Any) -> None:
    current: Any = obj
    parts = dotted.split(".")
    for part in parts[:-1]:
        current = current[part]
    current[parts[-1]] = value


def request_for(scenario_id: str) -> dict[str, Any]:
    if scenario_id not in SCENARIOS:
        raise ValueError(f"unknown scenario: {scenario_id}")
    request = deepcopy(BASE_REQUEST)
    for dotted, value in SCENARIOS[scenario_id]["mutations"].items():
        set_path(request, dotted, value)
    return request


def execute(role: str, scenario_id: str) -> dict[str, Any]:
    if role not in TARGETS:
        raise ValueError("unknown target role")
    target = TARGETS[role]
    request = request_for(scenario_id)
    request_bytes = json.dumps(request, sort_keys=True, separators=(",", ":")).encode("utf-8")
    completed = subprocess.run(
        [sys.executable, "-S", str(target)],
        input=request_bytes,
        capture_output=True,
        timeout=10,
        check=False,
    )
    if completed.returncode != 0:
        raise ValueError(f"target execution failed: {completed.stderr.decode('utf-8', 'replace')}")
    try:
        response = json.loads(completed.stdout)
    except (ValueError, UnicodeDecodeError) as exc:
        raise ValueError("malformed target response") from exc
    if not isinstance(response, dict) or response.get("disposition") not in {"ALLOW", "DENY", "INDETERMINATE"}:
        raise ValueError("unrecognized target disposition")
    expected = SCENARIOS[scenario_id]["expected"]
    observed = response["disposition"]
    return {
        "case_id": "CPC-001",
        "scenario_id": scenario_id,
        "contract_ids": scenario_contracts(scenario_id),
        "execution_class": "executed-synthetic-target",
        "target_role": role,
        "target_path": str(target.relative_to(ROOT)),
        "target_sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
        "request_sha256": hashlib.sha256(request_bytes).hexdigest(),
        "response_sha256": hashlib.sha256(completed.stdout).hexdigest(),
        "expected_disposition": expected,
        "observed_disposition": observed,
        "test_verdict": "SATISFIED" if observed == expected else "VIOLATED",
        "request": request,
        "response": response,
        "replay_command": f"{sys.executable} -S {target.relative_to(ROOT)}",
    }


def scenario_contracts(scenario_id: str) -> list[str]:
    return {
        "in_scope_allow": ["CPC-PROT-001", "CPC-PROT-002", "CPC-PROT-008"],
        "out_of_scope_action_deny": ["CPC-PROT-002", "CPC-PROT-003"],
        "out_of_scope_resource_deny": ["CPC-PROT-001", "CPC-PROT-003"],
        "post_revocation_deny": ["CPC-PROT-004"],
        "stale_authority_indeterminate": ["CPC-PROT-005"],
        "unavailable_authority_indeterminate": ["CPC-PROT-005"],
        "conflicting_authority_indeterminate": ["CPC-PROT-005"],
        "replay_deny": ["CPC-PROT-006"],
    }[scenario_id]


def paired() -> dict[str, Any]:
    safe_results = [execute("safe", scenario) for scenario in SCENARIOS]
    defective_results = [execute("defective", scenario) for scenario in SCENARIOS]
    if any(result["test_verdict"] != "SATISFIED" for result in safe_results):
        raise ValueError("safe target failed one or more CPC-001 scenarios")
    defect_detected = any(result["test_verdict"] == "VIOLATED" for result in defective_results)
    if not defect_detected:
        raise ValueError("defective target was not detected")
    return {
        "case_id": "CPC-001",
        "execution_class": "executed-synthetic-target",
        "scenario_count": len(SCENARIOS),
        "safe_target_satisfied": sum(result["test_verdict"] == "SATISFIED" for result in safe_results),
        "defective_target_violations": sum(result["test_verdict"] == "VIOLATED" for result in defective_results),
        "known_defect_detected": defect_detected,
        "independently_maintained_target_cases": 0,
        "independent_dtfc_consumer_cases": 0,
        "safe": safe_results,
        "defective": defective_results,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--role", choices=("safe", "defective", "paired"), default="paired")
    parser.add_argument("--scenario", choices=tuple(SCENARIOS.keys()), default="in_scope_allow")
    args = parser.parse_args()
    result = paired() if args.role == "paired" else execute(args.role, args.scenario)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
