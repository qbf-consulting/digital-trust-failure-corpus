"""Fail-closed method-validation ledger for pinned Trust Tasks semantic deltas.

This validates author-record provenance and known delta controls, NOT normative
equivalence of arbitrary upstream specifications. No inherited case judgment is
authorized by this module. Existing family validators remain authoritative.
"""
import json
from pathlib import Path

from tools.validate_trust_tasks_inventory import MANIFEST, ROOT
from tools.trust_tasks_author_case_index import load as load_author_cases
from tools.build_trust_tasks_pages import case_versions

PATH = ROOT / "research/external-sources/trust-tasks/semantic-delta-controls.json"
PREFIX = "https://trusttasks.org/spec/"
ALLOWED_DOMAINS = {
    "pagination", "incremental-sync", "action-binding",
    "framework-version", "acceptance-window", "expiry-horizon",
}


def check(data, inventory=None, author_cases=None, cases=None):
    inventory = json.loads(MANIFEST.read_text()) if inventory is None else inventory
    author_cases = load_author_cases(inventory) if author_cases is None else author_cases
    cases = case_versions() if cases is None else cases
    if data.get("schema_version") != "0.1.0":
        raise ValueError("unsupported delta control schema")
    upstream = inventory["source"]
    if data.get("upstream") != {
        "repository": upstream["repository"], "commit": upstream["commit"]
    }:
        raise ValueError("stale upstream revision")
    if data.get("assessment_kind") != "author-side-method-control-no-inheritance":
        raise ValueError("invalid assurance claim")
    source = {PREFIX + r["slug"] + "/" + r["version"]: r
              for r in inventory["records"]}
    controls = data.get("controls", [])
    if not controls:
        raise ValueError("no material delta controls")
    seen = set()
    for row in controls:
        old, new = row.get("predecessor"), row.get("successor")
        if (old, new) in seen or old == new:
            raise ValueError("duplicate or self-comparison")
        seen.add((old, new))
        if old not in source or new not in source or old not in author_cases or new not in author_cases:
            raise ValueError("unknown pinned author-examined version")
        # Exclude similarly named but different authorities (e.g. bridge-attested
        # consent/decision versus approver-signed task-consent/decision).
        if old.rsplit("/", 1)[0] != new.rsplit("/", 1)[0]:
            raise ValueError("cross-contract comparison cannot inherit")
        previous, current = source[old], source[new]
        if row.get("source_binding") != {
            "predecessor_spec_blob": previous["spec_blob"],
            "predecessor_schema_blob": previous["schema_blob"],
            "successor_spec_blob": current["spec_blob"],
            "successor_schema_blob": current["schema_blob"],
        }:
            raise ValueError("source/spec/schema fingerprint drift")
        old_record = author_cases[old]["record"]
        new_record = author_cases[new]["record"]
        if old_record["source_blob"] != previous["spec_blob"] or new_record["source_blob"] != current["spec_blob"]:
            raise ValueError("author source binding drift")
        delta = new_record.get("version_delta") or {}
        if delta.get("compared_with") != old:
            raise ValueError("missing validated predecessor delta")
        known_sections = delta.get("reviewed_sections", delta.get("source_sections", []))
        if not row.get("source_sections") or not set(row["source_sections"]).issubset(set(known_sections)):
            raise ValueError("unanchored semantic delta")
        if row.get("change_domain") not in ALLOWED_DOMAINS or len(row.get("change_claim", "")) < 75:
            raise ValueError("missing material contract change")
        for token in row.get("required_delta_tokens", []):
            if not token or token not in delta.get("claim", ""):
                raise ValueError("material delta marker absent")
        if not row.get("required_delta_tokens"):
            raise ValueError("no semantic change markers")
        inherited = row.get("inheritance", [])
        if not isinstance(inherited, list):
            raise ValueError("inheritance not approved without case-specific evidence")
        affected = row.get("candidate_predicates_to_recheck", [])
        if not affected or len(affected) != len(set(affected)) or not set(affected) <= set(cases):
            raise ValueError("missing or unknown canonical challenge predicate")
        # Every challenge ID must be bound to the same live canonical proposition
        # version in both existing author-side case examinations.
        prior = {d["case_id"]: d for d in old_record["decisions"]}
        latter = {d["case_id"]: d for d in new_record["decisions"]}
        if set(prior) != set(cases) or set(latter) != set(cases):
            raise ValueError("incomplete prior case accounting")
        if any(prior[c]["case_version"] != cases[c] or latter[c]["case_version"] != cases[c]
               for c in cases):
            raise ValueError("canonical case revision drift")
        inherited_ids = set()
        for assertion in inherited:
            cid = assertion.get("case_id")
            if cid in inherited_ids or cid not in cases or cid in affected:
                raise ValueError("inheritance not approved for affected, duplicated or unknown case")
            inherited_ids.add(cid)
            if assertion.get("mode") != "source-justified-inherited":
                raise ValueError("inheritance not approved without scoped provenance")
            if any(len(assertion.get(k, "")) < 75 for k in
                   ("unchanged_normative_requirement", "semantic_justification", "negative_control")):
                raise ValueError("inheritance not approved without substantive source argument")
            if (assertion.get("predecessor_section") != prior[cid].get("source_section")
                or assertion.get("successor_section") != latter[cid].get("source_section")
                or not assertion.get("predecessor_section")):
                raise ValueError("inheritance not approved without source-specific sections")
            # Literal judgment preservation is necessary, but not sufficient,
            # for semantic equivalence. The positive source claim is author-side
            # evidence, never independent review or proof of source equality.
            semantic_fields = ("disposition", "rationale", "authority_boundary",
                               "test_hypothesis", "case_version")
            if any(prior[cid].get(key) != latter[cid].get(key)
                   for key in semantic_fields):
                raise ValueError("inheritance not approved after changed case judgment")
        if row.get("independent_acceptance") != "not-established":
            raise ValueError("fabricated independent acceptance")
        if row.get("target_execution") != "not-established":
            raise ValueError("fabricated target execution")
    return {
        "material_delta_controls": len(controls),
        "challenged_predicate_pairs": sum(len(r["candidate_predicates_to_recheck"]) for r in controls),
        "inheritance_authorized": sum(len(r["inheritance"]) for r in controls),
        "independently_accepted": 0,
    }


if __name__ == "__main__":
    print(json.dumps(check(json.loads(PATH.read_text())), indent=2))
