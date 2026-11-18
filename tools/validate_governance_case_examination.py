"""Fail-closed checks for governance-capability family author case examination.

This checks the full source/case review *record*, not independent semantic truth.
"""
import json
from tools.validate_trust_tasks_inventory import MANIFEST, ROOT
from tools.build_trust_tasks_pages import case_versions

PATH = ROOT / "research/external-sources/trust-tasks/governance-case-examination.json"
TYPE = "https://trusttasks.org/spec/governance/capability/"
TARGETS = {TYPE + op + "/0.1" for op in ("disable", "enable", "list")}

def check(data, inventory):
    cases = case_versions()
    source = {
        "https://trusttasks.org/spec/" + r["slug"] + "/" + r["version"]: r
        for r in inventory["records"] if r["slug"].startswith("governance/")
    }
    if data.get("schema_version") != "0.1.0" or data.get("scope") != "governance-family-case-examination":
        raise ValueError("unsupported review record contract")
    if data.get("upstream") != {
        "repository": inventory["source"]["repository"],
        "commit": inventory["source"]["commit"],
    } or len(data.get("dtfc_case_revision", "")) != 40:
        raise ValueError("source or case revision not pinned")
    if set(source) != TARGETS or set(cases) != {
        "DTF-" + str(i).zfill(3) for i in range(1, 38)
    } or data.get("dtfc_case_count") != 37:
        raise ValueError("incorrect complete family/case denominator")
    records = data.get("records", [])
    if len(records) != 3 or {r["type_uri"] for r in records} != TARGETS:
        raise ValueError("missing, repeated or extra governance task")
    candidates = 0
    for record in records:
        original = source[record["type_uri"]]
        if (record["source_path"], record["source_blob"], record["schema_blob"]) != (
            original["path"], original["spec_blob"], original["schema_blob"]):
            raise ValueError("source spec or schema provenance mismatch")
        if record["assessment_state"] != "author-case-examined" or record["independent_acceptance"] != "not-established" or record["target_execution"] != "not-established":
            raise ValueError("unsupported assurance or execution promotion")
        decisions = record.get("decisions", [])
        if len(decisions) != 37 or {x["case_id"] for x in decisions} != set(cases):
            raise ValueError("missing or duplicate canonical case")
        for item in decisions:
            if item["disposition"] not in ("conditional-candidate", "not-established-from-task") or len(item.get("rationale", "")) < 45:
                raise ValueError("non-admissible case disposition")
            if item["disposition"] == "conditional-candidate":
                if (any(len(item.get(k, "")) < 35 for k in ("test_hypothesis", "authority_boundary"))
                    or len(item.get("source_section", "")) < 5):
                    raise ValueError("incomplete candidate falsification evidence")
                candidates += 1
            elif item.get("test_hypothesis") or item.get("authority_boundary"):
                raise ValueError("unadmitted positive-test evidence")
    return {"versions": 3, "comparisons": 111, "conditional_candidates": candidates,
            "not_established_from_task": 111 - candidates, "independently_accepted": 0}

if __name__ == "__main__":
    print(json.dumps(check(json.loads(PATH.read_text()), json.loads(MANIFEST.read_text())), indent=2))
