#!/usr/bin/env python3
"""Synthetic safe composition decision; local component PASS is insufficient."""
import json
import sys

def decide(request):
    if not isinstance(request.get("component_results"), list) or len(request["component_results"]) < 2:
        raise ValueError("missing component results")
    if any(value != "PASS" for value in request["component_results"]):
        return {"disposition": "DENY", "reason": "component-not-valid"}
    if request.get("seam_obligation") != "established":
        return {"disposition": "INDETERMINATE", "reason": "seam-evidence-not-established"}
    return {"disposition": "PASS", "reason": "composition-obligations-established"}

if __name__ == "__main__":
    try:
        print(json.dumps(decide(json.load(sys.stdin)), sort_keys=True))
    except (ValueError, TypeError, KeyError) as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(2)
