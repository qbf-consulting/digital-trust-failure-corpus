#!/usr/bin/env python3
"""Portable, deterministic case-identity digest; no Git checkout required."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

def canonical_case_bytes(case: dict) -> bytes:
    """RFC 8785 is NOT claimed: this is DTFC's documented JSON normalization."""
    return json.dumps(case, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")

def case_sha256(case: dict) -> str:
    return hashlib.sha256(canonical_case_bytes(case)).hexdigest()

def load_unique_case(corpus_root: Path, case_id: str) -> dict:
    matches = []
    for path in corpus_root.rglob("DTF-*.json"):
        case = json.loads(path.read_text(encoding="utf-8"))
        if case.get("id") == case_id:
            matches.append(case)
    if len(matches) != 1:
        raise ValueError(f"Case {case_id} must resolve exactly once; found {len(matches)}")
    return matches[0]
