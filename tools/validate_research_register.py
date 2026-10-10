"""Conservative research-register integrity checks, not semantic correctness."""
from __future__ import annotations
import json
from pathlib import Path
from urllib.parse import urlsplit
import re

ROOT = Path(__file__).resolve().parents[1]

def validate_register(data: dict, case_ids: set[str]) -> list[str]:
    errors = []
    if data.get("schema_version") != "0.1.0":
        errors.append("Unsupported register schema_version")
    records = data.get("records")
    if not isinstance(records, list):
        return errors + ["Missing records list"]
    seen = set()
    for i, item in enumerate(records):
        if not isinstance(item, dict):
            errors.append(f"Record {i}: not an object")
            continue
        source = item.get("source")
        identifier = item.get("source_id")
        if not isinstance(source, str) or not source.strip() or not isinstance(identifier, str) or not identifier.strip():
            errors.append(f"Record {i}: missing source identity")
        else:
            key = (source, identifier)
            if key in seen:
                errors.append(f"Record {i}: duplicate source identity")
            seen.add(key)
        url = item.get("url")
        if not isinstance(url, str):
            errors.append(f"Record {i}: missing URL")
        else:
            # Structural check only; URL reachability and authorship are not asserted.
            try:
                parsed = urlsplit(url)
                host = parsed.hostname
                port = parsed.port
                valid = (
                    parsed.scheme == "https"
                    and bool(host)
                    and not parsed.username
                    and not parsed.password
                    and not any(ord(c) < 33 or ord(c) == 127 for c in url)
                    and not re.search(r"%(?![0-9a-fA-F]{2})", url)
                    and (port is None or 1 <= port <= 65535)
                )
            except (ValueError, TypeError):
                valid = False
            if not valid:
                errors.append(f"Record {i}: invalid HTTPS URL")
        ids = item.get("case_ids")
        if not isinstance(ids, list) or any(not isinstance(v, str) or v not in case_ids for v in ids):
            errors.append(f"Record {i}: invalid case references")
        elif len(ids) != len(set(ids)):
            errors.append(f"Record {i}: duplicate case references")
    return errors

def validate_current(root: Path = ROOT) -> list[str]:
    register = json.loads((root / "research/external-sources/crosswalk.json").read_text(encoding="utf-8"))
    case_ids = set()
    for path in (root / "corpus").rglob("DTF-*.json"):
        case_ids.add(json.loads(path.read_text(encoding="utf-8"))["id"])
    return validate_register(register, case_ids)

if __name__ == "__main__":
    errors = validate_current()
    for error in errors:
        print(error)
    raise SystemExit(bool(errors))
