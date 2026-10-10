"""Conservative offline audit of external research source locators.

A URL is not a provenance attestation. Classifications are structural only.
"""
from __future__ import annotations
import json
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
REGISTER = ROOT / "research/external-sources/crosswalk.json"


def classify_locator(url: str) -> str:
    """Classify only well-understood immutable GitHub commit paths."""
    try:
        parsed = urlsplit(url)
        if parsed.scheme != "https" or not parsed.hostname:
            return "invalid"
        if parsed.hostname.lower() != "github.com":
            return "unverified-external"
        parts = parsed.path.strip("/").split("/")
        if len(parts) >= 5 and parts[2] in ("blob", "tree") and len(parts[3]) == 40 and all(c in "0123456789abcdefABCDEF" for c in parts[3]):
            return "commit-addressed-unverified"
        return "mutable-or-unpinned-github"
    except (ValueError, TypeError):
        return "invalid"


def audit_register(path: Path = REGISTER) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    records = []
    for item in data["records"]:
        records.append({
            "source": item["source"],
            "source_id": item["source_id"],
            "locator_class": classify_locator(item["url"]),
            "case_ids": item["case_ids"],
        })
    return {
        "scope": "offline locator classification; not independent source verification",
        "records": records,
        "counts": {kind: sum(r["locator_class"] == kind for r in records)
                   for kind in sorted(set(r["locator_class"] for r in records))},
    }


if __name__ == "__main__":
    print(json.dumps(audit_register(), indent=2, sort_keys=True))
