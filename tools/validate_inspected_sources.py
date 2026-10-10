"""Offline structural checks for individually inspected source research records.

Does not assert source reachability, authenticity, copyright clearance or independent review.
"""
from __future__ import annotations

import json
from pathlib import Path
from tools.validate_research_register import validate_register

ROOT = Path(__file__).resolve().parents[1]


def validate_inspected_records(root: Path = ROOT) -> list[str]:
    path = root / "research/external-sources/inspected-record-dispositions.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    errors = []
    records = data.get("records")
    if not isinstance(records, list):
        return ["inspected records must be a list"]
    cases = {json.loads(p.read_text(encoding="utf-8"))["id"] for p in (root / "corpus").rglob("DTF-*.json")}
    seen = set()
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            errors.append(f"record {index}: not an object")
            continue
        family, identifier = record.get("family"), record.get("id")
        if not all(isinstance(v, str) and v.strip() for v in (family, identifier)):
            errors.append(f"record {index}: missing source identity")
        else:
            key = (family, identifier)
            if key in seen:
                errors.append(f"record {index}: duplicate source identity")
            seen.add(key)
        case_id = record.get("case_id")
        if case_id not in cases:
            errors.append(f"record {index}: unknown case ID {case_id!r}")
        for field in ("disposition", "basis", "inspected", "source_status", "reproduction", "rights"):
            if not isinstance(record.get(field), str) or not record[field].strip():
                errors.append(f"record {index}: missing {field}")
        # Reuse the shared conservative URL syntax validator, not a network check.
        synthetic = {"schema_version": "0.1.0", "records": [{
            "source": family, "source_id": identifier, "url": record.get("url"),
            "case_ids": [case_id] if case_id in cases else [],
        }]}
        errors.extend(f"record {index}: {msg}" for msg in validate_register(synthetic, cases))
    return errors


if __name__ == "__main__":
    for error in (errors := validate_inspected_records()):
        print(error)
    raise SystemExit(bool(errors))
