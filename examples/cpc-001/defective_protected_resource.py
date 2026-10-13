#!/usr/bin/env python3
"""Deliberately defective CPC-001 protected resource.

This target is intentionally unsafe. It ignores revocation, stale authority
versions and replay in order to prove that CPC-001 tests detect failure.
"""
from __future__ import annotations

import json
import sys
from typing import Any


def decision(disposition: str, reason: str, request: dict[str, Any]) -> dict[str, Any]:
    return {
        "disposition": disposition,
        "reason": reason,
        "decision_evidence": {
            "case_id": "CPC-001",
            "target": "defective-synthetic-protected-resource",
            "agent_id": request.get("agent_id"),
            "consumer_id": request.get("consumer_id"),
            "action": request.get("action"),
            "resource": request.get("resource"),
            "evaluation_time": request.get("evaluation_time"),
            "authority_version": request.get("observed_authority_version"),
            "nonce": request.get("nonce"),
        },
    }


def evaluate(request: dict[str, Any]) -> dict[str, Any]:
    authority = request.get("authority") or {}
    if request.get("action") in authority.get("actions", []) and request.get("resource") in authority.get("resources", []):
        return decision("ALLOW", "defective target ignores lifecycle and replay state", request)
    return decision("DENY", "outside action/resource scope", request)


def main() -> int:
    try:
        request = json.loads(sys.stdin.read())
        if not isinstance(request, dict):
            raise ValueError("request must be object")
        result = evaluate(request)
    except Exception as exc:
        result = {
            "disposition": "INDETERMINATE",
            "reason": f"target error: {exc}",
            "decision_evidence": {"case_id": "CPC-001"},
        }
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
