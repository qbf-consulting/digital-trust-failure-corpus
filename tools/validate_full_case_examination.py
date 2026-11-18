"""Shared fail-closed validation for source-pinned complete-case author research.

A complete case-examination record is not independent semantic approval.
"""
from __future__ import annotations

import re
from tools.build_trust_tasks_pages import case_versions

PREFIX = "https://trusttasks.org/spec/"
VALID_DISPOSITIONS = {"conditional-candidate", "not-established-from-task"}

def check_family(data, inventory, family, targets, version_deltas=None, cases=None):
    """Validate exact family census, all cases and explicit assurance boundaries.

    version_deltas maps type URI to (prior URI, required semantic change markers).
    """
    cases = case_versions() if cases is None else cases
    source = {
        PREFIX + r["slug"] + "/" + r["version"]: r
        for r in inventory["records"]
        if r["slug"].split("/")[0] == family
    }
    targets = set(targets)
    if data.get("schema_version") != "0.1.0" or data.get("scope") != family + "-family-case-examination":
        raise ValueError("unsupported source-qualified case-examination contract")
    if data.get("upstream") != {
        "repository": inventory["source"]["repository"],
        "commit": inventory["source"]["commit"],
    }:
        raise ValueError("wrong upstream repository or source revision")
    if not re.fullmatch(r"[0-9a-f]{40}", data.get("dtfc_case_revision", "")):
        raise ValueError("unbound DTFC case source revision")
    if (set(source) != targets or set(cases) != {
        "DTF-" + str(i).zfill(3) for i in range(1, 38)
    } or data.get("dtfc_case_count") != 37):
        raise ValueError("pinned task family and case population disagree")
    records = data.get("records", [])
    if len(records) != len(targets) or {r["type_uri"] for r in records} != targets:
        raise ValueError("missing, duplicated or extra task version")
    indexed = {r["type_uri"]: r for r in records}
    candidates = 0
    for uri, row in indexed.items():
        ref = source[uri]
        if (row["source_path"], row["source_blob"], row["schema_blob"]) != (
            ref["path"], ref["spec_blob"], ref["schema_blob"]):
            raise ValueError("source path or Git blob mismatch")
        if row.get("assessment_state") != "author-case-examined":
            raise ValueError("author case review status not established")
        if row.get("independent_acceptance") != "not-established" or row.get("target_execution") != "not-established":
            raise ValueError("fabricated independent approval or target execution")
        decisions = row.get("decisions", [])
        if len(decisions) != 37 or {d["case_id"] for d in decisions} != set(cases):
            raise ValueError("missing, duplicated or unrelated canonical case")
        for d in decisions:
            if d.get("disposition") not in VALID_DISPOSITIONS or len(d.get("rationale", "")) < 45:
                raise ValueError("unsupported classification or missing rationale")
            if d["disposition"] == "conditional-candidate":
                if (any(len(d.get(k, "")) < 35 for k in ("authority_boundary", "test_hypothesis"))
                    or len(d.get("source_section", "")) < 5):
                    raise ValueError("source-anchored candidate lacks a falsification test or authority boundary")
                candidates += 1
            elif d.get("test_hypothesis") or d.get("authority_boundary"):
                raise ValueError("unadmitted positive evidence in a non-established case")
    for uri, expected in (version_deltas or {}).items():
        if uri not in indexed:
            raise ValueError("version delta refers to an absent task")
        delta = indexed[uri].get("version_delta")
        if (not delta or delta.get("compared_with") != expected[0]
            or any(token not in delta.get("claim", "") for token in expected[1])
            or not delta.get("source_sections")):
            raise ValueError("missing source-specific semantic version delta")
    return {
        "versions": len(records),
        "comparisons": 37 * len(records),
        "case_comparisons": 37 * len(records),
        "conditional_candidates": candidates,
        "not_established_from_task": 37 * len(records) - candidates,
        "independently_accepted": 0,
    }
