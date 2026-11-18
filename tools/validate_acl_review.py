"""Evidence-gated ACL crosswalk slice for DTFC #135."""
import json
from pathlib import Path
from tools.validate_trust_tasks_inventory import MANIFEST, PIN

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "research/external-sources/trust-tasks/acl-review.json"
CLASSES = {"mechanism-overlap", "adjacent"}
KEYS = {"change-role": "0.3", "grant": "0.3", "list": "0.4", "revoke": "0.3",
        "show": "0.3", "swap-key": "0.1", "update": "0.3"}


def check(data, inventory):
    if data["schema_version"] != "0.1.0" or data["source_commit"] != PIN or data["family"] != "acl":
        raise ValueError("wrong source or slice contract")
    existing = {f"https://trusttasks.org/spec/{r['slug']}/{r['version']}": r
                for r in inventory["records"] if r["slug"].startswith("acl/")}
    reviewed = {}
    for entry in data["current"]:
        uri = entry["task_type_uri"]
        if uri not in existing or uri in reviewed:
            raise ValueError("unknown or duplicate source")
        reviewed[uri] = entry
        row = existing[uri]
        if entry["source_path"] != row["path"] or entry["source_blob"] != row["spec_blob"]:
            raise ValueError("source provenance mismatch")
        if entry["classification"] not in CLASSES or entry["review_state"] != "research-screened":
            raise ValueError("unjustified status promotion")
        if entry["execution_evidence"] != "none" or entry["independent_review"] != "not-established":
            raise ValueError("falsely asserted independent evidence")
        if entry["case_id"] not in {p.stem for p in (ROOT / "corpus").rglob("DTF-*.json")}:
            raise ValueError("unknown canonical case")
        for field in ("rationale", "test_hypothesis", "authority_boundary"):
            if len(entry[field]) < 65:
                raise ValueError("inadequate evidence-qualified mapping")
        case_path = next((ROOT / "corpus").rglob(entry["case_id"] + ".json"))
        case = json.loads(case_path.read_text())
        if entry["case_version"] != case["version"]:
            raise ValueError("stale canonical case version")
    expected = {f"https://trusttasks.org/spec/acl/{k}/{v}" for k, v in KEYS.items()}
    if set(reviewed) != expected:
        raise ValueError("current review scope incomplete")
    history = {}
    for entry in data["historical"]:
        uri = entry["task_type_uri"]
        if uri not in existing or uri in history or uri in reviewed:
            raise ValueError("unknown, duplicate or reviewed historical source")
        if entry["source_blob"] != existing[uri]["spec_blob"] or entry["review_state"] != "needs-version-delta-review":
            raise ValueError("historical equivalence not established")
        history[uri] = entry
    if set(history) != set(existing) - set(reviewed):
        raise ValueError("historical version dropped")
    for item in data["negative_controls"]:
        if item["classification"] != "not-established" or item["task_type_uri"] not in reviewed or len(item["rationale"]) < 80:
            raise ValueError("invalid no-overlap negative control")
    return {"acl_source_versions": len(existing), "current_screened": len(reviewed),
            "history_pending_delta": len(history), "semantic_review_complete": False}


def main():
    print(json.dumps(check(json.loads(PATH.read_text()), json.loads(MANIFEST.read_text())), indent=2))


if __name__ == "__main__":
    main()
