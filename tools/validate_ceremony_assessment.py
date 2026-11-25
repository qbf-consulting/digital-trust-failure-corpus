"""Validate #168 research bindings, not semantic correctness or execution."""
from collections import Counter
import json

from tools.validate_ceremony_profiles import (
    check as check_profiles, read, PROFILE_PATH, BASELINE_PATH, MANIFEST,
    RESEARCH, CASE_FIELDS, require_text,
)
from tools.validate_trust_tasks_predicate_catalog import load as load_catalog, git_blob

FAMILIES = ("authority", "composition", "evidence", "lifecycle", "privacy")
CONTROL_PROFILES = {
    "NC-JOIN-01": {"joining"},
    "NC-SEPARATION-01": {"separation"},
    "NC-CONSENT-01": {"consent"},
    "NC-CROSS-01": {"joining", "separation"},
}
DISPOSITIONS = {"conditional-candidate", "not-established-within-profile", "unresolved-evidence"}
ATTRIBUTIONS = {"task-local", "ceremony-compositional", "cross-ceremony"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unique_index(rows, key, label):
    result = {}
    for row in rows:
        value = key(row)
        require(value not in result, "duplicate " + label)
        result[value] = row
    return result


def load_inputs():
    return {
        "profiles": read(PROFILE_PATH),
        "baseline": read(BASELINE_PATH),
        "inventory": read(MANIFEST),
        "catalog": load_catalog(),
        "profile_blob": git_blob(PROFILE_PATH.read_bytes()),
        "matrix": {f: read(RESEARCH / ("ceremony-" + f + "-assessment.json")) for f in FAMILIES},
        "controls": read(RESEARCH / "ceremony-negative-controls.json"),
        "comparison": read(RESEARCH / "ceremony-consent-comparison.json"),
        "prior": read(RESEARCH / "consent-case-examination.json"),
        "prior_blob": git_blob((RESEARCH / "consent-case-examination.json").read_bytes()),
    }


def check(data):
    profiles, baseline = data["profiles"], data["baseline"]
    check_profiles(profiles, baseline, data["inventory"])
    catalog = data["catalog"]
    # The profile validator checks the on-disk canonical catalog against corpus bytes.
    require(catalog == load_catalog(), "canonical catalog drift")
    tasks = {p["id"]: {s["type_uri"]: s for s in p["steps"]} for p in profiles["profiles"]}
    canonical = {f: {x["case_id"]: x for x in catalog[f]["records"]} for f in FAMILIES}
    all_cases = {cid: row for group in canonical.values() for cid, row in group.items()}
    pins = {x["family"]: x["blob"] for x in baseline["catalogs"]}
    require(set(data["matrix"]) == set(FAMILIES), "matrix family drift")
    all_rows = {}
    for family, artifact in data["matrix"].items():
        require(artifact.get("kind") == "ceremony-comparative-author-assessment-increment"
                and artifact.get("issue") == 168 and artifact.get("family") == family
                and artifact.get("status") == "provisional-author-judgments"
                and artifact.get("registry_commit") == profiles["registry_commit"]
                and artifact.get("profile_blob") == data["profile_blob"]
                and artifact.get("canonical_catalog_blob") == pins[family],
                "matrix metadata or source pin drift")
        require(bool(artifact.get("limitations")), "missing matrix limitations")
        require(artifact.get("case_count") == len(canonical[family])
                and artifact.get("profile_count") == len(tasks), "matrix count drift")
        rows = unique_index(artifact["dispositions"],
                            lambda x: (x["profile"], x["case_id"]), "matrix cell")
        require(set(rows) == {(p, c) for p in tasks for c in canonical[family]},
                "missing or extra matrix cell")
        for (pid, cid), row in rows.items():
            case = canonical[family][cid]
            require(all(row.get(k) == case[k] for k in CASE_FIELDS), "canonical binding drift")
            require(row.get("trigger") == case["trigger"]["statement"]
                    and row.get("falsification") == [x["condition"] for x in case["falsification"]],
                    "canonical trigger or falsification drift")
            uris = row.get("task_versions", [])
            require(isinstance(uris, list) and len(uris) == len(set(uris))
                    and set(uris) <= set(tasks[pid]), "unknown or duplicate task reference")
            if row.get("disposition") == "conditional-candidate":
                require(bool(uris), "conditional candidate without task anchor")
            require(row.get("disposition") in DISPOSITIONS, "invalid disposition")
            require(row.get("attribution") in ATTRIBUTIONS, "invalid attribution")
            for field in ("sections", "local_proposition", "relying_proposition",
                          "precondition_analysis", "authority", "expected_safe_outcome",
                          "potential_impact", "comparison"):
                require_text(row.get(field), field)
            require(row["local_proposition"] != row["relying_proposition"],
                    "collapsed local and relying propositions")
            require(row.get("observed_failure") is False
                    and row.get("independent_review") == "not-established",
                    "unsupported assurance promotion")
        all_rows.update(rows)

    controls = data["controls"]
    require(controls.get("kind") == "ceremony-negative-control-designs"
            and controls.get("issue") == 168
            and controls.get("status") == "unexecuted-author-hypotheses"
            and controls.get("profile_source_blob") == data["profile_blob"]
            and all(controls.get(k) == profiles[k] for k in
                    ("registry_commit", "framework_commit", "vti_commit")),
            "control source or evidence status drift")
    designs = unique_index(controls["designs"], lambda x: x["id"], "control design")
    require(set(designs) == set(CONTROL_PROFILES)
            and controls.get("design_count") == len(designs), "control coverage drift")
    require(bool(controls.get("limitations")), "missing control limitations")
    for cid, design in designs.items():
        pids = CONTROL_PROFILES[cid]
        expected_profile = next(iter(pids)) if len(pids) == 1 else "cross-ceremony:joining+separation"
        require(design.get("profile") == expected_profile, "control profile drift")
        require(design.get("observed_failure") is False
                and design.get("independent_review") == "not-established"
                and design.get("evidence_status") == "hypothetical-unexecuted-author-design",
                "unsupported control assurance")
        case_ids = design.get("case_ids", [])
        require(bool(case_ids) and len(set(case_ids)) == len(case_ids)
                and set(case_ids) <= set(all_cases), "bad control case reference")
        allowed = {uri: task for pid in pids for uri, task in tasks[pid].items()}
        refs = unique_index(design.get("task_refs", []), lambda x: x["type_uri"], "control task")
        require(bool(refs) and set(refs) <= set(allowed), "bad control task reference")
        for uri, ref in refs.items():
            require(all(ref.get(k) == allowed[uri][k] for k in ("spec_blob", "schema_blob")),
                    "control task blob drift")
        for field in ("initial_state", "policy", "intervention", "identical_local_observations",
                      "relying_proposition", "observation_point", "task_only_vs_ceremony",
                      "falsifier", "evaluation_contract"):
            require_text(design.get(field), field)
        for field in ("actors", "required_evidence"):
            require(isinstance(design.get(field), list) and bool(design[field]), "missing " + field)
            for value in design[field]:
                require_text(value, field)
        for variant in ("negative", "control"):
            outcome = design[variant]
            for field in ("execution", "legitimacy", "effective_state", "safe"):
                require_text(outcome.get(field), variant + " " + field)
            require(len({outcome[k] for k in ("execution", "legitimacy", "effective_state")}) == 3,
                    "collapsed control determinations")
        require(design["negative"] != design["control"], "identical negative and control")

    comparison, prior = data["comparison"], data["prior"]
    require(comparison.get("kind") == "consent-comparative-reconciliation"
            and comparison.get("issue") == 168
            and comparison.get("prior_blob") == data["prior_blob"]
            and comparison.get("profile_blob") == data["profile_blob"]
            and comparison.get("registry_commit") == profiles["registry_commit"] == prior["upstream"]["commit"]
            and comparison.get("prior_case_revision") == prior["dtfc_case_revision"],
            "prior comparison source drift")
    prior_tasks = unique_index(prior["records"], lambda x: x["type_uri"], "prior task")
    consent = tasks["consent"]
    require(set(consent) <= set(prior_tasks), "missing prior task")
    previous = {uri: unique_index(prior_tasks[uri]["decisions"], lambda x: x["case_id"],
                                  "prior judgment") for uri in consent}
    rows = unique_index(comparison["rows"], lambda x: x["case_id"], "comparison case")
    require(set(rows) == set(all_cases) and comparison.get("comparison_rows") == len(rows)
            and comparison.get("prior_judgments") == len(rows) * len(consent),
            "prior comparison coverage drift")
    require(bool(comparison.get("limitations")), "missing comparison limitations")
    for cid, row in rows.items():
        case = all_cases[cid]
        require(row.get("case_version") == case["case_version"]
                and row.get("case_blob") == case["source_blob"]
                and row.get("ceremony_disposition") == all_rows["consent", cid]["disposition"],
                "comparison case or disposition drift")
        require(row.get("category") in {"overlap", "conditional-extension", "not-established",
                                        "scope-narrowing"}, "invalid comparison category")
        require_text(row.get("rationale"), "comparison rationale")
        refs = unique_index(row["prior_decisions"], lambda x: x["type_uri"], "prior decision ref")
        require(set(refs) == set(consent), "prior decision coverage drift")
        for uri, ref in refs.items():
            old = previous[uri][cid]
            require(old["case_version"] == case["case_version"]
                    and ref.get("spec_blob") == prior_tasks[uri]["source_blob"] == consent[uri]["spec_blob"]
                    and ref.get("schema_blob") == prior_tasks[uri]["schema_blob"] == consent[uri]["schema_blob"]
                    and all(ref.get(k) == old[k] for k in ("disposition", "source_section")),
                    "prior judgment binding drift")
    reconciliation = comparison["case_reconciliation"]
    require(reconciliation.get("prior_revision") == prior["dtfc_case_revision"]
            and reconciliation.get("current_revision") == baseline["revision"],
            "reconciliation revision drift")
    links = unique_index(reconciliation["cases"], lambda x: x["case_id"], "reconciled case")
    require(set(links) == set(all_cases), "reconciliation coverage drift")
    for cid, link in links.items():
        case = all_cases[cid]
        require(link.get("prior_path") == link.get("current_path") == case["source_path"]
                and link.get("prior_blob") == link.get("current_blob") == case["source_blob"]
                and link.get("case_version") == case["case_version"]
                and link.get("status") == "unchanged-by-commit-comparison",
                "reconciliation binding drift")
    return {"cells": len(all_rows), "dispositions": dict(Counter(x["disposition"] for x in all_rows.values())),
            "controls": len(designs), "comparison_rows": len(rows),
            "prior_judgment_references": len(rows) * len(consent),
            "semantic_acceptance": "not-established", "target_execution": "not-established"}


if __name__ == "__main__":
    print(json.dumps(check(load_inputs()), indent=2))
