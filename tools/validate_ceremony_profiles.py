"""Structural checks for #168; not semantic acceptance or target execution."""
import json

from tools.validate_trust_tasks_inventory import ROOT, MANIFEST, PIN
from tools.validate_trust_tasks_predicate_catalog import (
    DIR, check as check_catalog, git_blob, load as load_catalog,
)

RESEARCH = MANIFEST.parent
PROFILE_PATH = RESEARCH / "ceremony-profiles.json"
BASELINE_PATH = RESEARCH / "ceremony-case-baseline.json"
PREFIX = "https://trusttasks.org/spec/"
TARGETS = {
    "joining": {"vtc/join-requests/manifest/0.4", "vtc/join-requests/submit/0.3",
                "vtc/join-requests/decide/0.1", "vtc/members/admit/0.1"},
    "separation": {"vtc/members/self-remove/0.1", "vtc/members/self-remove-receipt/0.1",
                   "vtc/members/admin-remove/0.1"},
    "consent": {"consent/approver-set/1.0", "consent/request/1.0",
                "consent/approve-request/0.1", "consent/decision/1.0",
                "consent/list/1.1", "consent/revoke/1.0"},
}
CASE_FIELDS = ("case_id", "case_version", "source_path", "source_blob")


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def require_text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("missing " + label)


def check(profiles, baseline, inventory):
    if (profiles.get("issue") != 168 or profiles.get("registry_commit") != PIN
            or inventory["source"]["commit"] != PIN
            or inventory["source"]["repository"] != "trustoverip/dtgwg-trust-tasks-tf"):
        raise ValueError("source pin mismatch")
    if (profiles.get("framework_commit") != "bdf2cdd9256f9d7b98fe8b40c776124fc27a6084"
            or profiles.get("vti_commit") != "83e88fcf8760f6bd159bbac09a27b002f5b656c2"):
        raise ValueError("framework or VTI pin drift")
    if (profiles.get("status") != "provisional-author-profile"
            or profiles.get("independent_review") != "not-established"
            or profiles.get("target_execution") != "not-established"):
        raise ValueError("unsupported assurance promotion")
    if not profiles.get("limitations"):
        raise ValueError("missing limitations")
    lookup = {PREFIX + x["slug"] + "/" + x["version"]: x for x in inventory["records"]}
    seen = set()
    for profile in profiles["profiles"]:
        pid = profile["id"]
        if pid not in TARGETS or pid in seen:
            raise ValueError("unexpected or duplicate profile")
        seen.add(pid)
        for field in ("initial", "target", "execution", "legitimacy", "effective", "control"):
            require_text(profile.get(field), field)
        if len({profile[k] for k in ("execution", "legitimacy", "effective")}) != 3:
            raise ValueError("collapsed assurance predicates")
        if not profile.get("actors"):
            raise ValueError("missing actors")
        tasks = set()
        for step in profile["steps"]:
            uri = step["type_uri"]
            if uri in tasks or uri not in lookup:
                raise ValueError("duplicate or unknown task")
            tasks.add(uri)
            row = lookup[uri]
            if any(step[k] != row[v] for k, v in (
                ("spec_path", "path"), ("spec_blob", "spec_blob"), ("schema_blob", "schema_blob")
            )):
                raise ValueError("task source binding drift")
            require_text(step.get("dependency"), "dependency")
            require_text(step.get("proposition"), "proposition")
        if tasks != {PREFIX + x for x in TARGETS[pid]}:
            raise ValueError("profile task membership drift")
    if seen != set(TARGETS):
        raise ValueError("missing profile")
    if (baseline.get("kind") != "ceremony-study-canonical-baseline"
            or baseline.get("issue") != 168
            or baseline.get("revision") != "1eda75842cf3b268361dc47ce8ade23b6a99c5cb"):
        raise ValueError("canonical baseline metadata drift")
    catalog = load_catalog()
    check_catalog(catalog)
    expected = sorted(
        [{k: row[k] for k in CASE_FIELDS} for family in catalog.values()
         for row in family["records"]], key=lambda row: row["case_id"])
    if baseline.get("cases") != expected:
        raise ValueError("canonical case baseline drift")
    pins = sorted((x["family"], x["blob"]) for x in baseline["catalogs"])
    actual = sorted((p.stem, git_blob(p.read_bytes())) for p in DIR.glob("*.json"))
    if pins != actual:
        raise ValueError("predicate catalog blob drift")
    return {"profiles": len(seen), "task_versions": sum(map(len, TARGETS.values())),
            "canonical_cases": len(expected), "planned_comparisons": len(seen) * len(expected),
            "semantic_assessment_complete": False, "independent_review": "not-established",
            "target_execution": "not-established"}


if __name__ == "__main__":
    print(json.dumps(check(read(PROFILE_PATH), read(BASELINE_PATH), read(MANIFEST)), indent=2))
