"""Evidence-gated ACL historical version-delta screening for #135.

Source-delta inspection is not an approval of historical DTFC applicability.
"""
import json
from pathlib import Path
from tools.validate_trust_tasks_inventory import MANIFEST, PIN

ROOT = Path(__file__).resolve().parents[1]
ACL = ROOT / "research/external-sources/trust-tasks/acl-review.json"

BASELINES = {"acl/change-role/0.1", "acl/grant/0.1", "acl/list/0.1",
             "acl/revoke/0.1", "acl/show/0.1", "acl/update/0.1"}


def validate(data, inventory):
    source = {r["slug"] + "/" + r["version"]: r for r in inventory["records"]
              if r["slug"].startswith("acl/")}
    if data["source_commit"] != PIN or len(source) != 20:
        raise ValueError("unexpected pinned family scope")
    currents = {r["task_type_uri"].removeprefix("https://trusttasks.org/spec/"): r
                for r in data["current"]}
    history = {}
    for row in data["historical"]:
        key = row["task_type_uri"].removeprefix("https://trusttasks.org/spec/")
        if key in history or key in currents or key not in source:
            raise ValueError("invalid or duplicate historical spec")
        history[key] = row
        d = row["version_delta_evidence"]
        if row["review_state"] != "needs-version-delta-review" or row["applicability_review"] != "needs-review":
            raise ValueError("semantic review status incorrectly promoted")
        if d["source_commit"] != PIN or d["source_path"] != source[key]["path"] or row["source_blob"] != source[key]["spec_blob"]:
            raise ValueError("historical source evidence does not match pinned source")
        if d["assessment"] != ("baseline" if key in BASELINES else "material-change"):
            raise ValueError("unsupported or missing version-delta assessment")
        if d["mapping_reuse"] != "not-authorized" or d["scope"] != "source-version semantics only":
            raise ValueError("historical semantic mapping inheritance incorrectly claimed")
        if len(d["rationale"]) < 85 or not d["source_section"]:
            raise ValueError("incomplete evidence for historical delta")
    if set(source) != set(currents) | set(history) or len(currents) != 7 or len(history) != 13:
        raise ValueError("ACL family version inventory not reconciled")
    result = data["version_delta_review"]
    if result["historical_version_delta_records"] != len(history) or result["historical_applicability_reviews"] != 0 or result["historical_applicability_complete"] is not False or result["independent_semantic_peer_review"] is not False:
        raise ValueError("false historical applicability or independent review claim")
    return {"family_versions": len(source), "current_screened": len(currents),
            "historical_delta_screened": len(history), "historical_applicability_reviewed": 0,
            "semantic_review_complete": False}


def main():
    print(json.dumps(validate(json.loads(ACL.read_text()), json.loads(MANIFEST.read_text())), indent=2))


if __name__ == "__main__":
    main()
