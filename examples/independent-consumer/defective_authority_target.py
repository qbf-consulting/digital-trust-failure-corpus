#!/usr/bin/env python3
"""Intentionally defective external-process fixture: ignores revocation. Test only."""
import json
import sys

if __name__ == "__main__":
    request = json.load(sys.stdin)
    if not all(k in request for k in ("authority_state", "action", "authorized_actions")):
        sys.exit(2)
    print(json.dumps({"disposition": "PASS", "reason": "defect-revocation-ignored"}, sort_keys=True))
