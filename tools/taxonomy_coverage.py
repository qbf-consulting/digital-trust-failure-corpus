#!/usr/bin/env python3
"""Deterministic descriptive taxonomy coverage; not assurance scoring."""
from __future__ import annotations
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def build_report(corpus_root: Path = ROOT / "corpus") -> dict:
    cases = [json.loads(path.read_text(encoding="utf-8")) for path in sorted(corpus_root.rglob("DTF-*.json"))]
    ids = [case["id"] for case in cases]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate case IDs")
    domains = Counter(value for case in cases for value in case["domains"])
    classes = Counter(value for case in cases for value in case["failure_classes"])
    statuses = Counter(case["status"] for case in cases)
    return {
        "report_type": "descriptive-taxonomy-coverage",
        "case_count": len(cases),
        "domains": dict(sorted(domains.items())),
        "failure_classes": dict(sorted(classes.items())),
        "statuses": dict(sorted(statuses.items())),
        "case_ids": sorted(ids),
        "interpretation": "Counts of labels in draft cases; no independent execution, completeness, risk score, certification or maturity inference.",
    }

if __name__ == "__main__":
    print(json.dumps(build_report(), indent=2, sort_keys=True))
