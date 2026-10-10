#!/usr/bin/env python3
"""Synthetic safe workflow assurance decision; CI green is not substantive evidence."""
import json
import sys

def decide(request):
    if request.get("workflow_status") != "success":
        return {"disposition": "INDETERMINATE", "reason": "workflow-not-complete"}
    if request.get("substantive_evidence") != "established":
        return {"disposition": "INDETERMINATE", "reason": "substantive-evidence-missing"}
    return {"disposition": "PASS", "reason": "substantive-evidence-established"}

if __name__ == "__main__":
    try:
        print(json.dumps(decide(json.load(sys.stdin)), sort_keys=True))
    except (ValueError, TypeError, KeyError) as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(2)
