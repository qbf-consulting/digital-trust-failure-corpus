"""Source-derived index of the 37 existing canonical DTFC predicates.

This is a mechanically checked research index, not a second canonical case
definition. Canonical corpus JSON remains authoritative for every field.
"""
from __future__ import annotations

import hashlib
import json

from tools.validate_trust_tasks_inventory import ROOT

DIR = ROOT / "research/external-sources/trust-tasks/predicate-catalog"
FIELDS = (
    "case_id", "case_version", "title", "source_path", "source_blob",
    "proposition", "preconditions", "trigger", "evidence_required",
    "falsification", "expected",
)
SOURCE_FIELDS = {
    "case_id": "id", "case_version": "version", "title": "title",
    "proposition": "proposition", "preconditions": "preconditions",
    "trigger": "trigger", "evidence_required": "evidence_required",
    "falsification": "falsification", "expected": "expected",
}


def git_blob(content):
    header = b"blob " + str(len(content)).encode("ascii") + bytes([0])
    return hashlib.sha1(header + content).hexdigest()


def derive(root=ROOT):
    """Derive exact predicate entries from canonical files, without paraphrase."""
    catalog = {}
    for group in sorted((root / "corpus").iterdir()):
        if not group.is_dir():
            continue
        records = []
        for path in sorted(group.glob("DTF-*.json")):
            raw = path.read_bytes()
            case = json.loads(raw.decode("utf-8"))
            row = {field: case[source] for field, source in SOURCE_FIELDS.items()}
            row["source_path"] = path.relative_to(root).as_posix()
            row["source_blob"] = git_blob(raw)
            records.append({k: row[k] for k in FIELDS})
        catalog[group.name] = {
            "schema_version": "0.1.0",
            "catalog_kind": "derived-canonical-predicate-index",
            "family": group.name,
            "records": records,
        }
    return catalog


def load():
    return {p.stem: json.loads(p.read_text())
            for p in sorted(DIR.glob("*.json"))}


def check(catalog=None, expected=None):
    catalog = load() if catalog is None else catalog
    expected = derive() if expected is None else expected
    if set(catalog) != set(expected):
        raise ValueError("canonical predicate family membership drift")
    all_cases = set()
    for family, reference in expected.items():
        actual = catalog[family]
        if actual.get("schema_version") != "0.1.0" or actual.get("catalog_kind") != "derived-canonical-predicate-index" or actual.get("family") != family:
            raise ValueError("predicate catalog metadata or family mismatch")
        rows = actual.get("records")
        if not isinstance(rows, list) or rows != reference["records"]:
            raise ValueError("canonical proposition, version, blob, or precondition drift")
        for case in rows:
            cid = case["case_id"]
            if cid in all_cases:
                raise ValueError("duplicate canonical predicate")
            all_cases.add(cid)
    if all_cases != {f"DTF-{i:03d}" for i in range(1, 38)}:
        raise ValueError("incomplete canonical proposition population")
    return {"canonical_predicates": len(all_cases), "families": len(catalog),
            "authority": "corpus/", "independent_acceptance": "not-established"}


if __name__ == "__main__":
    print(json.dumps(check(), indent=2))
