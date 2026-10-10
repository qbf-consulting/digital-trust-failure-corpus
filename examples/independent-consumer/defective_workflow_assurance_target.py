#!/usr/bin/env python3
"""Synthetic defective assurance target: green workflow implies PASS."""
import json
import sys

if __name__ == "__main__":
    request = json.load(sys.stdin)
    if request.get("workflow_status") != "success":
        sys.exit(2)
    print(json.dumps({"disposition": "PASS", "reason": "defect-process-success-conflated"}, sort_keys=True))
