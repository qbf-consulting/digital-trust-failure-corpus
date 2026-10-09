#!/usr/bin/env python3
"""Standalone example decision target: no DTFC imports, deliberately non-production."""
import json
import sys

def decide(request):
    if request["authority_state"] != "active":
        return {"disposition": "DENY", "reason": "authority-not-active"}
    if request["action"] not in request["authorized_actions"]:
        return {"disposition": "DENY", "reason": "out-of-scope"}
    return {"disposition": "PASS", "reason": "active-in-scope"}

if __name__ == "__main__":
    try:
        request = json.load(sys.stdin)
        if not isinstance(request, dict) or not all(k in request for k in ("authority_state", "action", "authorized_actions")):
            raise ValueError("missing required request fields")
        print(json.dumps(decide(request), sort_keys=True))
    except (ValueError, KeyError, TypeError) as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(2)
