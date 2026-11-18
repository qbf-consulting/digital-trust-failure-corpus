"""Validate historical ACL applicability screening without conflating source, review and execution."""
import json
from tools.validate_trust_tasks_inventory import MANIFEST
from tools.validate_acl_review import PATH

def check(data, inventory):
    known = {x["slug"] + "/" + x["version"]: x for x in inventory["records"]
             if x["slug"].startswith("acl/")}
    historical = {x["task_type_uri"].removeprefix("https://trusttasks.org/spec/"): x
                  for x in data["historical"]}
    if len(historical) != 13 or len(data["historical_screenings"]) != 13:
        raise ValueError("historical research scope incomplete")
    seen = set()
    for entry in data["historical_screenings"]:
        uri = entry["task_type_uri"]
        key = uri.removeprefix("https://trusttasks.org/spec/")
        if key in seen or key not in historical or key not in known:
            raise ValueError("duplicate or unknown historical mapping")
        seen.add(key)
        row = historical[key]
        if row["review_state"] != "source-delta-screened" or row["applicability_review"] != "research-screened":
            raise ValueError("unjustified assessment promotion")
        if entry["source_path"] != known[key]["path"] or entry["source_blob"] != known[key]["spec_blob"] or entry["source_commit"] != data["source_commit"]:
            raise ValueError("unverifiable source reference")
        if entry["classification"] not in {"adjacent","mechanism-overlap"} or entry["review_state"] != "research-screened":
            raise ValueError("invalid applicability classification")
        if entry["execution_evidence"] != "none" or entry["independent_review"] != "not-established" or entry["complete_case_exhaustiveness"] is not False:
            raise ValueError("false independent or exhaustive assurance")
        for name in ("local_proposition","unsupported_inference","test_hypothesis","authority_boundary"):
            if len(entry[name]) < 85:
                raise ValueError("insufficient semantic rationale: " + name)
        if len(entry["evidence_to_check"]) < 2 or not entry["source_section"]:
            raise ValueError("unsubstantiated test or source anchor")
        paths = list((MANIFEST.parents[3] / "corpus").rglob(entry["case_id"] + ".json"))
        # MANIFEST is rooted under research/external-sources/trust-tasks: parents[3] is repo root.
        if len(paths) != 1:
            raise ValueError("unresolved canonical case")
        case = json.loads(paths[0].read_text())
        if case["version"] != entry["case_version"]:
            raise ValueError("stale canonical case revision")
    if seen != set(historical) or data["version_delta_review"]["historical_applicability_screenings"] != 13 or data["version_delta_review"]["historical_applicability_reviews"] != 0:
        raise ValueError("historical screening count or review-status inconsistency")
    return {"source_screened": 13, "independent_reviewed": 0, "complete_case_exhaustiveness": False}
