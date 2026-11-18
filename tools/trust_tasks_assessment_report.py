"""Pinned, explainable research report generated from Trust Tasks and DTFC authorities.

Do not convert absence of a screening into a no-match, successful conformance,
or independent review. All values derive from committed research evidence.
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

from tools.validate_trust_tasks_inventory import MANIFEST, PILOT, ROOT
from tools.validate_acl_review import PATH as ACL_PATH
from tools.validate_consent_review import PATH as CONSENT_PATH, check as check_consent
from tools.validate_additional_screenings import PATH as ADDITIONAL_PATH, check as check_additional
from tools.validate_acl_deltas import validate as validate_deltas
from tools.validate_historical_acl_screening import check as check_history
from tools.trust_tasks_coverage import calculate
from tools.build_trust_tasks_pages import build_pages, case_versions

OUTPUT = ROOT / "docs" / "trust-tasks"
TYPE = "https://trusttasks.org/spec/"
CASE_COUNT = 37
REVIEW_STATUS = {"needs-review", "research-screened", "reviewed-mapped",
                 "reviewed-no-match", "blocked-evidence"}
PROVENANCE = {"pinned-spec-blob", "unverified"}
EXECUTION = {"none", "synthetic-local", "independent-target"}


def review_decision(record, case_ids):
    """Validate an additional admitted review; never infer approval from screening."""
    if record["decision"] not in {"reviewed-mapped", "reviewed-no-match", "blocked-evidence"}:
        raise ValueError("unrecognized semantic review outcome")
    if record["decision"] == "blocked-evidence":
        if record["independent_review"] != "challenged-unresolved":
            raise ValueError("blocked interpretation must stay unresolved")
    elif record["independent_review"] != "completed":
        raise ValueError("review cannot be admitted without independent challenge")
    if not record.get("reviewer") or not record.get("reviewed_source_blob"):
        raise ValueError("unbound reviewer or source version")
    if record["decision"] == "reviewed-mapped":
        if not record.get("case_ids") or not set(record["case_ids"]) <= case_ids:
            raise ValueError("invalid case mapping in independently accepted review")
    elif record["decision"] == "reviewed-no-match":
        if record.get("case_ids"):
            raise ValueError("a no-match cannot carry positive cases")
        if set(record.get("cases_examined", [])) != case_ids:
            raise ValueError("task-wide no-match requires full canonical-case examination")
    if not record.get("reasoning") or not record.get("challenge_record"):
        raise ValueError("semantic review lacks reasoned challenge evidence")
    return True


def build_report(inventory, pilot, acl, attestation, accepted=None, consent=None):
    consent = json.loads(CONSENT_PATH.read_text()) if consent is None else consent
    check_consent(consent, inventory)
    additional=json.loads(ADDITIONAL_PATH.read_text())
    check_additional(additional, inventory)
    accepted = [] if accepted is None else accepted
    coverage = calculate(inventory, pilot, acl)
    validate_deltas(acl, inventory)
    check_history(acl, inventory)
    # Exercise the actual versioned-navigation consumer path as an invariant.
    pages = build_pages(inventory, pilot, acl)
    if len(pages) != 44:
        raise ValueError("version navigator not reconciled")
    if (attestation["upstream_commit"] != inventory["source"]["commit"]
        or attestation["registry_versions"] != len(inventory["records"])
        or attestation["source_pairs"] != len(inventory["records"])
        or attestation["publication_membership_reconciled"] is not True
        or attestation["workflow_conclusion"] != "success"):
        raise ValueError("source-pinned publication census not verified")
    cases = case_versions()
    if len(cases) != CASE_COUNT:
        raise ValueError("canonical case baseline unexpectedly changed")
    indexed = {}
    for entry in inventory["records"]:
        uri = TYPE + entry["slug"] + "/" + entry["version"]
        if uri in indexed:
            raise ValueError("duplicate source task")
        indexed[uri] = {
            "type_uri": uri,
            "family": entry["slug"].split("/")[0],
            "slug": entry["slug"],
            "version": entry["version"],
            "source": {
                "commit": inventory["source"]["commit"],
                "path": entry["path"],
                "spec_blob": entry["spec_blob"],
                "schema_blob": entry["schema_blob"],
                "provenance_strength": "pinned-spec-blob",
            },
            "inventory_state": "registry-reconciled",
            "screening_state": "needs-review",
            "independent_review_state": "not-established",
            "execution_evidence_state": "none",
            "candidate_mappings": [],
            "author_case_examination": {"state": "not-examined"},
            "version_delta": "not-evaluated",
        }
    for record in pilot["judgments"]:
        uri = record["task_type_uri"]
        if uri not in indexed:
            raise ValueError("unknown original pilot task")
        if record["case_id"] not in cases:
            raise ValueError("unknown original pilot case")
        if record["assessment_state"] != "research-screened" or record["execution_evidence"] != "none":
            raise ValueError("pilot incorrectly promotes screening or execution")
        x = indexed[uri]
        x["screening_state"] = "research-screened"
        x["candidate_mappings"].append({
            "case_id": record["case_id"], "case_version": cases[record["case_id"]],
            "classification": record["classification"], "source": "pilot",
            "rationale": record["rationale"],
            "authority_boundary": record["authority_boundary"],
            "test_hypothesis": record["test_hypothesis"],
            "independent_review": "not-established",
            "execution_evidence": "none",
        })
    for record in acl["current"] + acl["historical_screenings"]:
        uri = record["task_type_uri"]
        if uri not in indexed:
            raise ValueError("unknown ACL source task")
        x = indexed[uri]
        if record["source_blob"] != x["source"]["spec_blob"] or record["source_path"] != x["source"]["path"]:
            raise ValueError("ACL source digest or path mismatch")
        if record["case_id"] not in cases or record["case_version"] != cases[record["case_id"]]:
            raise ValueError("unresolved or stale canonical case")
        if record["review_state"] != "research-screened" or record["execution_evidence"] != "none":
            raise ValueError("ACL screening incorrectly promoted to assurance")
        if record["independent_review"] != "not-established":
            raise ValueError("fabricated independent review")
        x["screening_state"] = "research-screened"
        x["candidate_mappings"].append({
            "case_id": record["case_id"], "case_version": record["case_version"],
            "classification": record["classification"], "source": "acl",
            "rationale": record["rationale"], "authority_boundary": record["authority_boundary"],
            "test_hypothesis": record["test_hypothesis"],
            "independent_review": "not-established",
            "execution_evidence": "none",
        })
    for record in consent["records"]:
        uri = record["task_type_uri"]
        if uri not in indexed:
            raise ValueError("unknown consent version")
        x = indexed[uri]
        if (record["source_blob"] != x["source"]["spec_blob"]
            or record["source_path"] != x["source"]["path"]
            or record["source_commit"] != x["source"]["commit"]):
            raise ValueError("consent source provenance mismatch")
        if record["case_id"] not in cases or record["case_version"] != cases[record["case_id"]]:
            raise ValueError("unresolved consent canonical case")
        if record["independent_review"] != "not-established" or record["execution_evidence"] != "none" or record["case_search_complete"] is not False:
            raise ValueError("consent research incorrectly promoted to assurance")
        x["screening_state"] = "research-screened"
        x["candidate_mappings"].append({
            "case_id": record["case_id"], "case_version": record["case_version"],
            "classification": record["classification"], "source": "consent",
            "rationale": record["rationale"], "authority_boundary": record["authority_boundary"],
            "test_hypothesis": record["test_hypothesis"],
            "independent_review": "not-established", "execution_evidence": "none",
        })
    for record in additional["records"]:
        uri = record["task_type_uri"]
        if uri not in indexed:
            raise ValueError("unknown additional research version")
        x = indexed[uri]
        if record["source_blob"] != x["source"]["spec_blob"] or record["source_path"] != x["source"]["path"]:
            raise ValueError("additional source provenance mismatch")
        if record["case_id"] not in cases or record["case_version"] != cases[record["case_id"]]:
            raise ValueError("invalid additional case reference")
        if record["independent_review"] != "not-established" or record["execution_evidence"] != "none":
            raise ValueError("unsupported assurance promotion")
        x["screening_state"] = "research-screened"
        x["candidate_mappings"].append({
            "case_id": record["case_id"], "case_version": record["case_version"],
            "classification": record["classification"], "source": "additional",
            "rationale": record["rationale"], "authority_boundary": record["authority_boundary"],
            "test_hypothesis": record["test_hypothesis"],
            "independent_review": "not-established", "execution_evidence": "none",
        })
    for record in acl["historical"]:
        uri = record["task_type_uri"]
        if uri not in indexed or record["source_blob"] != indexed[uri]["source"]["spec_blob"]:
            raise ValueError("unbound historical version delta")
        evidence = record["version_delta_evidence"]
        if evidence["mapping_reuse"] != "not-authorized":
            raise ValueError("historical version inheritance without evidence")
        indexed[uri]["version_delta"] = evidence["assessment"] + "-screened"
    # Review additions must be challengeable and source-pinned; no independent
    # assessments are presently committed to this repository.
    unique = set()
    for review in accepted:
        uri = review["task_type_uri"]
        if uri in unique or uri not in indexed:
            raise ValueError("missing or duplicated reviewed task")
        unique.add(uri)
        if review["reviewed_source_blob"] != indexed[uri]["source"]["spec_blob"]:
            raise ValueError("reviewed version differs from registered source")
        review_decision(review, set(cases))
        indexed[uri]["independent_review_state"] = review["decision"]
    from tools.trust_tasks_author_case_index import load as load_author_cases
    author_cases = load_author_cases(inventory)
    if not set(author_cases) <= set(indexed):
        raise ValueError("author case outside reconciled inventory")
    for uri, bundle in author_cases.items():
        source = bundle["record"]
        entry = indexed[uri]
        if entry["screening_state"] != "research-screened":
            raise ValueError("full author case review lacks separately recorded source screening")
        entry["author_case_examination"] = {
            "state": "author-case-examined",
            "canonical_case_count": len(source["decisions"]),
            "conditional_candidates": sum(d["disposition"] == "conditional-candidate" for d in source["decisions"]),
            "not_established_from_task": sum(d["disposition"] == "not-established-from-task" for d in source["decisions"]),
            "canonical_case_revision": bundle["case_revision"],
            "research_record_url": bundle["record_url"],
            "independent_acceptance": "not-established",
            "target_execution": "not-established",
        }
    rows = [indexed[key] for key in sorted(indexed)]
    covered = sum(x["screening_state"] == "research-screened" for x in rows)
    independent = sum(x["independent_review_state"] in {"reviewed-mapped", "reviewed-no-match"} for x in rows)
    blocked = sum(x["independent_review_state"] == "blocked-evidence" for x in rows)
    if covered != coverage["screened_unique"] or covered + (len(rows) - covered) != len(rows):
        raise ValueError("screening/report denominator mismatch")
    fam = defaultdict(lambda: Counter())
    for row in rows:
        c = fam[row["family"]]
        c["inventory"] += 1
        c["screened"] += row["screening_state"] == "research-screened"
        c["author_case_examined"] += row["author_case_examination"]["state"] == "author-case-examined"
        c["pending"] += row["screening_state"] == "needs-review"
        c["reviewed"] += row["independent_review_state"] in {"reviewed-mapped", "reviewed-no-match"}
        c["blocked"] += row["independent_review_state"] == "blocked-evidence"
    candidates = sum(len(x["candidate_mappings"]) for x in rows)
    return {
        "schema_version": "0.1.0",
        "report_type": "source-pinned-trust-tasks-dtfc-research",
        "objective": "Determine version-specific DTFC applicability or justified no-match at the consuming trust boundary, with falsification evidence and independent semantic challenge.",
        "authority": {
            "upstream_repository": inventory["source"]["repository"],
            "upstream_commit": inventory["source"]["commit"],
            "publication_evidence_url": attestation["workflow_run_url"],
            "canonical_dtfc_case_count": len(cases),
            "external_execution_evidenced": False,
        },
        "summary": {
            "registry_versions": len(rows),
            "draft_versions": attestation["status_counts"]["draft"],
            "retired_versions": attestation["status_counts"]["retired"],
            "families": len(fam),
            "screened_versions": covered,
            "pending_versions": len(rows) - covered,
            "candidate_judgments": candidates,
            "author_case_examined_versions": len(author_cases),
            "author_case_comparisons": sum(len(v["record"]["decisions"]) for v in author_cases.values()),
            "author_conditional_candidates": sum(
                sum(d["disposition"] == "conditional-candidate" for d in v["record"]["decisions"])
                for v in author_cases.values()),
            "author_not_established_from_task": sum(
                sum(d["disposition"] == "not-established-from-task" for d in v["record"]["decisions"])
                for v in author_cases.values()),
            "independently_reviewed_versions": independent,
            "blocked_review_versions": blocked,
            "independent_review_complete": independent == len(rows) and blocked == 0,
            "semantic_completion_claim": False,
            "publication_state": "research-checkpoint",
        },
        "review_dimensions": {
            "inventory": "registry-reconciled",
            "screening": ["needs-review", "research-screened"],
            "classification": ["mechanism-overlap", "adjacent"],
            "author_case_examination": ["not-examined", "author-case-examined"],
            "provenance": ["pinned-spec-blob"],
            "independent_review": ["not-established", "reviewed-mapped", "reviewed-no-match", "blocked-evidence"],
            "execution": ["none"],
        },
        "families": [{"family": family, **dict(counts)} for family, counts in sorted(fam.items())],
        "records": rows,
        "limitations": [
            "A preliminary mapping is not a defect report, conformance result or exhaustive consideration of all DTFC cases.",
            "Missing mapping means unreviewed, not no-match or safe.",
            "No independent semantic approvals or independently maintained execution are evidenced in this checkpoint.",
            "Historical version delta inspection does not authorize reuse of a different version's mapping.",
        ],
    }


def render(report):
    s = report["summary"]
    lines = [
        "# Trust Tasks × DTFC: technical assessment report", "",
        "**Research checkpoint, not an exhaustive semantic assurance report.**", "",
        "## Purpose", "",
        "For each versioned Trust Task, determine whether an existing DTFC failure",
        "proposition can apply when another system relies on the task's result.",
        "A mapping identifies a **possible mistake in the consuming system**,",
        "not a defect in the Trust Task itself.", "",
        "## What was checked", "",
        "| Measure | Result |", "|---|---:|",
        "| Pinned upstream task versions | " + str(s["registry_versions"]) + " |",
        "| Draft versions | " + str(s["draft_versions"]) + " |",
        "| Retired versions | " + str(s["retired_versions"]) + " |",
        "| Task families | " + str(s["families"]) + " |",
        "| Versions with preliminary DTFC screening | " + str(s["screened_versions"]) + " |",
        "| Versions awaiting screening | " + str(s["pending_versions"]) + " |",
        "| Conditional research judgments | " + str(s["candidate_judgments"]) + " |",
        "| Versions with full author-side 37-case examination | " + str(s["author_case_examined_versions"]) + " |",
        "| Author-side canonical case comparisons | " + str(s["author_case_comparisons"]) + " |",
        "| Conditional author-side candidate cells | " + str(s["author_conditional_candidates"]) + " |",
        "| Not established from task source | " + str(s["author_not_established_from_task"]) + " |",
        "| Independently reviewed task versions | " + str(s["independently_reviewed_versions"]) + " |",
        "| Blocked semantic reviews (unresolved) | " + str(s["blocked_review_versions"]) + " |",
        "",
        "The upstream source inventory and published registry were reconciled at",
        "[" + report["authority"]["upstream_commit"] + "](" +
        "https://github.com/trustoverip/dtgwg-trust-tasks-tf/tree/" +
        report["authority"]["upstream_commit"] + ").",
        "See [CI evidence](" + report["authority"]["publication_evidence_url"] + ").",
        "This establishes a complete **source census**, not a complete semantic assessment.", "",
        "## Source-qualified full-case research", "",
        "Four existing families have complete 37-case **author-side** matrices; these",
        "are not independently accepted semantic dispositions or implementation tests.",
        "Not established from task source is weaker than a reviewed no-match and",
        "must not be interpreted as evidence of universal safety.", "",
        "The version navigator links to the exact family examination for each",
        "examined task. The [research checkpoint](../trust-tasks-research-checkpoint.md)",
        "provides an actionable DTG/Trust Tasks negative-test agenda.", "",
        "## What the preliminary research shows", "",
        "**Authority:** A correctly signed or processed operation does not automatically",
        "give a relying system permission to act beyond the granting principal's scope.", "",
        "**Time:** Revocation, role change and policy activation can make an earlier",
        "valid observation unsuitable at a later decision.", "",
        "**Evidence:** A filtered, paginated or redacted ACL result is not proof",
        "of universal absence of an authorization.", "",
        "**Consent:** A signed prompt is not an approval; a bridge-attested answer is",
        "not interchangeable with a directly signed operator decision.", "",
        "**Versions:** Purpose, pagination and authority semantics changed across",
        "ACL versions. A mapping must refer to the actual version assessed.", "",
        "These are **testable hypotheses**, not observed implementation defects.", "",
        "## How to use the results", "",
        "1. Find a task in the [version navigator](index.md).",
        "2. Open its source-pinned specification and any candidate DTFC cases.",
        "3. Check the stated trust boundary, preconditions and negative test.",
        "4. Treat a missing mapping as **not reviewed**, not a safe/no-match outcome.",
        "5. Request substantive independent review before treating a mapping as accepted.", "",
        "The [machine-readable report](assessment-report.json) and",
        "[JSON Schema](assessment-report.schema.json) document the data contract. A record exists for"
        "every task version. The [review method](../trust-tasks-review-method.md)",
        "explains how to evaluate mappings and genuine no-matches.", "",
        "## Completion against the six work packages", "",
        "| Work package | Outcome |",
        "|---|---|",
        "| 1. Review contract | Evidence states, source linkage and negative tests defined |",
        "| 2. ACL reference family | Version-specific preliminary screening complete; independent full-case review pending |",
        "| 3. Other families | Consent family source-screened; " + str(s["pending_versions"]) + " versions require semantic screening |",
        "| 4. Independent challenge | No completed independent semantic review evidenced |",
        "| 5. Publication | Source-derived human and JSON reports generated with the existing documentation build |",
        "| 6. Close-out | Research checkpoint only; the final exhaustive acceptance gate is not met |",
        "",
        "## What this does *not* establish", "",
        "It does not determine that unreviewed tasks are safe. It does not establish",
        "complete applicability or justified no-match for every task. It does not",
        "prove upstream defects, independent conformance, deployment failures or adoption.", "",
        "**Release disposition:** publish a reproducible research checkpoint on GitHub",
        "Pages, but do **not** release or close issue #135 as an exhaustive assessment.", "",
        "See [issue #135](https://github.com/qbf-consulting/digital-trust-failure-corpus/issues/135)",
        "for unresolved acceptance criteria and evidence requirements.", "",
    ]
    return "\n".join(lines)


def generate(output=OUTPUT):
    inventory = json.loads(MANIFEST.read_text())
    pilot = json.loads(PILOT.read_text())
    acl = json.loads(ACL_PATH.read_text())
    att = json.loads((ROOT / "research/external-sources/trust-tasks/registry-reconciliation.json").read_text())
    report = build_report(inventory, pilot, acl, att)
    output.mkdir(parents=True, exist_ok=True)
    from jsonschema import Draft202012Validator
    schema_path = ROOT / "schemas" / "trust-tasks-assessment-report.schema.json"
    schema = json.loads(schema_path.read_text())
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(report)
    (output / "assessment-report.schema.json").write_text(json.dumps(schema, indent=2) + "\n", encoding="utf-8")
    (output / "assessment-report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    (output / "assessment-report.md").write_text(render(report), encoding="utf-8")
    print("Generated human and machine Trust Tasks assessment reports")


if __name__ == "__main__":
    generate()
