#!/usr/bin/env python3
"""Synthetic CPC-001 protected resource.

This target is a deterministic local fixture. It is not an ARPA implementation,
not a production service, and not independent adoption evidence.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from typing import Any


def parse_time(value: str) -> datetime:
    if not isinstance(value, str):
        raise ValueError("timestamp must be a string")
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


def deny(reason: str, request: dict[str, Any]) -> dict[str, Any]:
    return decision("DENY", reason, request)


def indeterminate(reason: str, request: dict[str, Any]) -> dict[str, Any]:
    return decision("INDETERMINATE", reason, request)


def allow(reason: str, request: dict[str, Any]) -> dict[str, Any]:
    return decision("ALLOW", reason, request)


def decision(disposition: str, reason: str, request: dict[str, Any]) -> dict[str, Any]:
    return {
        "disposition": disposition,
        "reason": reason,
        "decision_evidence": {
            "case_id": "CPC-001",
            "target": "synthetic-protected-resource",
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
    required = ("consumer_id", "agent_id", "action", "resource", "evaluation_time", "authority")
    missing = [field for field in required if field not in request]
    if missing:
        return indeterminate(f"missing material field: {','.join(missing)}", request)

    authority = request["authority"]
    if not isinstance(authority, dict):
        return indeterminate("authority evidence is malformed", request)

    if request.get("authority_source_available") is False:
        return indeterminate("authority source unavailable", request)

    if authority.get("conflict") is True:
        return indeterminate("authority evidence is contradictory", request)

    current_version = authority.get("current_version")
    observed_version = request.get("observed_authority_version")
    if current_version is None or observed_version is None:
        return indeterminate("authority version evidence missing", request)
    if observed_version < current_version:
        return indeterminate("observed authority state is stale", request)

    evaluation_time = parse_time(request["evaluation_time"])
    effective_from = parse_time(authority["effective_from"])
    effective_until = parse_time(authority["effective_until"])
    if evaluation_time < effective_from or evaluation_time >= effective_until:
        return deny("authority outside validity interval", request)

    revoked_at = authority.get("revoked_at")
    if revoked_at is not None and evaluation_time >= parse_time(revoked_at):
        return deny("authority revoked at evaluation time", request)

    if request.get("nonce") in request.get("used_nonces", []):
        return deny("request replay detected", request)

    if request["action"] not in authority.get("actions", []):
        return deny("action outside delegated scope", request)

    if request["resource"] not in authority.get("resources", []):
        return deny("resource outside delegated scope", request)

    return allow("action authorized by current bounded authority", request)


def main() -> int:
    try:
        raw = sys.stdin.read()
        request = json.loads(raw)
        if not isinstance(request, dict):
            raise ValueError("request must be a JSON object")
        result = evaluate(request)
    except Exception as exc:  # fixture target: errors are indeterminate, not allow
        result = {
            "disposition": "INDETERMINATE",
            "reason": f"target error: {exc}",
            "decision_evidence": {"case_id": "CPC-001"},
        }
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
