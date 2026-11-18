"""Fail-closed structural checks for the pinned Trust Tasks source inventory.

Structural coverage is NOT semantic review or upstream conformance.
"""
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "research/external-sources/trust-tasks/inventory.json"
PILOT = ROOT / "research/external-sources/trust-tasks/mapping.json"
PIN = "f21a98ec8383352d18629a08dd5dd23935456142"
HEX = re.compile(r"^[0-9a-f]{40}$")
VERSION = re.compile(r"^[0-9]+\.[0-9]+$")
STATES = {"sample-screened", "needs-review", "reviewed-no-match", "reviewed-mapped", "blocked-evidence"}


def check(data, pilot):
    source = data["source"]
    if data["schema_version"] != "0.1.0" or source["commit"] != PIN:
        raise ValueError("unreviewed source pin or inventory contract")
    if source["repository"] != "trustoverip/dtgwg-trust-tasks-tf":
        raise ValueError("incorrect upstream authority")
    if not HEX.fullmatch(source["git_tree_sha"]):
        raise ValueError("invalid pinned tree")
    if source["status_metadata_verified"] is not False:
        raise ValueError("unsubstantiated status verification")
    records = data["records"]
    if len(records) != 1391:
        raise ValueError("snapshot cardinality changed; regenerate and review source")
    seen = set()
    selected = set()
    for row in records:
        slug, version = row["slug"], row["version"]
        key = (slug, version)
        if key in seen:
            raise ValueError("duplicate versioned task")
        seen.add(key)
        if not VERSION.fullmatch(version) or not re.fullmatch(r"[a-z0-9-]+(?:/[a-z0-9-]+)*", slug):
            raise ValueError("invalid slug or version")
        if row["path"] != f"specs/{slug}/{version}/spec.md":
            raise ValueError("path does not match task identity")
        if not HEX.fullmatch(row["spec_blob"]) or not HEX.fullmatch(row["schema_blob"]):
            raise ValueError("missing source blob provenance")
        if row["review_state"] not in STATES:
            raise ValueError("unsupported review state")
        if row["review_state"] == "sample-screened":
            selected.add(key)
        if row["review_state"] in {"reviewed-no-match", "reviewed-mapped"}:
            raise ValueError("new substantive review must have a separate evidence-qualified record")
    expected = {(x["slug"], x["version"]) for x in pilot["specifications"]}
    if pilot["source"]["commit"] != PIN or selected != expected:
        raise ValueError("sample screening not reconciled with original pilot")
    if len({x[0] for x in seen}) < 1:
        raise ValueError("no inventory")
    return Counter(x["review_state"] for x in records)


def main():
    counts = check(json.loads(MANIFEST.read_text()), json.loads(PILOT.read_text()))
    print(json.dumps({"source_commit": PIN, "inventory_count": sum(counts.values()),
                      "review_states": dict(sorted(counts.items())),
                      "semantic_review_complete": False}, indent=2))


if __name__ == "__main__":
    main()
