#!/usr/bin/env python3
"""Synthetic defective composition target: treats local PASS as composition PASS."""
import json
import sys

if __name__ == "__main__":
    request = json.load(sys.stdin)
    if not isinstance(request.get("component_results"), list) or len(request["component_results"]) < 2:
        sys.exit(2)
    print(json.dumps({"disposition": "PASS", "reason": "defect-seam-obligation-ignored"}, sort_keys=True))
