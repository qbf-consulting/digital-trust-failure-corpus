"""Fail closed on the source-pinned, author-side audit case-examination record.

Structural validity and complete candidate accounting are not semantic peer review.
"""
from __future__ import annotations

import json
from pathlib import Path
from tools.validate_trust_tasks_inventory import MANIFEST, ROOT
from tools.build_trust_tasks_pages import case_versions

PATH = ROOT / "research/external-sources/trust-tasks/audit-case-examination.json"
PREFIX = "https://trusttasks.org/spec/"
STATES = {"conditional-candidate", "not-established-from-task"}
TARGETS = {
    PREFIX + "audit/list/0.1",
    PREFIX + "audit/list/0.2",
    PREFIX + "audit/verify/0.1",
}

def check(data, inventory, cases=None):
    cases = case_versions() if cases is None else cases
    indexed = {
        PREFIX + item["slug"] + "/" + item["version"]: item
        for item in inventory["records"]
        if item["slug"].startswith("audit/")
    }
    if data.get("schema_version") != "0.1.0" or data.get("scope") != "audit-family-case-examination":
        raise ValueError("unsupported audit research contract")
    if not data.get("dtfc_case_revision") or len(data["dtfc_case_revision"]) != 40:
        raise ValueError("unbound DTFC case baseline revision")
    if data["upstream"] != {
        "repository": inventory["source"]["repository"],
        "commit": inventory["source"]["commit"]
    }:
        raise ValueError("wrong pinned upstream source")
    if set(indexed) != TARGETS or set(cases) != {
        "DTF-" + str(i).zfill(3) for i in range(1, 38)
    } or data.get("dtfc_case_count") != len(cases):
        raise ValueError("inconsistent pinned family or canonical case inventory")
    rows = data.get("records", [])
    if len(rows) != len(TARGETS) or {r["type_uri"] for r in rows} != TARGETS:
        raise ValueError("missing, duplicate or unexpected task version")
    candidates = 0
    for row in rows:
        ref = indexed[row["type_uri"]]
        if row["source_path"] != ref["path"] or row["source_blob"] != ref["spec_blob"] or row["schema_blob"] != ref["schema_blob"]:
            raise ValueError("source revision or schema mismatch")
        if row["assessment_state"] != "author-case-examined" or row["independent_acceptance"] != "not-established" or row["target_execution"] != "not-established":
            raise ValueError("unsupported assurance promotion")
        decisions = row.get("decisions", [])
        if len(decisions) != len(cases) or {d["case_id"] for d in decisions} != set(cases):
            raise ValueError("missing, duplicated or unrelated canonical case comparison")
        for item in decisions:
            if item["disposition"] not in STATES or len(item.get("rationale", "")) < 45:
                raise ValueError("missing evidence-grounded bounded judgment")
            if item["disposition"] == "conditional-candidate":
                if (any(len(item.get(k, "")) < 35 for k in ("test_hypothesis", "authority_boundary"))
                    or len(item.get("source_section", "")) < 5):
                    raise ValueError("conditional candidate lacks a test, source section or boundary")
                candidates += 1
            else:
                if item.get("test_hypothesis") or item.get("authority_boundary"):
                    raise ValueError("unadmitted test or boundary on non-established comparison")
    if "audit/list/0.2" not in rows[1]["type_uri"]:
        raise ValueError("task-version order changed unexpectedly")
    delta = rows[1].get("version_delta")
    if not delta or delta.get("compared_with") != PREFIX + "audit/list/0.1" or "nextCursor" not in delta.get("claim", ""):
        raise ValueError("missing specific semantic version delta")
    return {"versions": len(rows), "case_comparisons": len(rows)*len(cases),
            "conditional_candidates": candidates,
            "not_established_from_task": len(rows)*len(cases)-candidates,
            "independently_accepted": 0}

if __name__ == "__main__":
    print(json.dumps(check(json.loads(PATH.read_text()), json.loads(MANIFEST.read_text())), indent=2))
