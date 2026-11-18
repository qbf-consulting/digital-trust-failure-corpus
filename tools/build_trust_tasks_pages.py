"""Reproducible Trust Tasks version navigator; inventory is not semantic assurance."""
import json
from collections import defaultdict
from pathlib import Path
from tools.trust_tasks_coverage import calculate
from tools.validate_trust_tasks_inventory import MANIFEST, PILOT, ROOT
from tools.validate_acl_review import PATH as ACL_PATH, check as check_acl
from tools.validate_historical_acl_screening import check as check_history
from tools.validate_consent_review import PATH as CONSENT_PATH, check as check_consent
from tools.validate_additional_screenings import PATH as ADDITIONAL_PATH, check as check_additional

OUTPUT = ROOT / "docs" / "trust-tasks"
URI = "https://trusttasks.org/spec/"
GIT = "https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/"
TICK = chr(96)

def case_versions():
    found = {}
    for path in (ROOT / "corpus").rglob("DTF-*.json"):
        case = json.loads(path.read_text())
        if case["id"] in found:
            raise ValueError("duplicate canonical case")
        found[case["id"]] = case["version"]
    return found

def build_pages(inventory, pilot, acl, consent=None, additional=None):
    additional=json.loads(ADDITIONAL_PATH.read_text()) if additional is None else additional
    check_additional(additional, inventory)
    consent = json.loads(CONSENT_PATH.read_text()) if consent is None else consent
    check_consent(consent, inventory)
    from tools.trust_tasks_author_case_index import load as load_author_cases
    author_cases = load_author_cases(inventory)
    stats = calculate(inventory, pilot, acl)
    check_acl(acl, inventory)
    check_history(acl, inventory)
    rows = {URI + x["slug"] + "/" + x["version"]: x for x in inventory["records"]}
    if len(rows) != stats["source_versions"]:
        raise ValueError("duplicate inventory URI")
    versions = case_versions()
    screenings = defaultdict(list)
    for item in pilot["judgments"]:
        screenings[item["task_type_uri"]].append(("pilot", item))
    for item in acl["current"] + acl["historical_screenings"]:
        screenings[item["task_type_uri"]].append(("acl", item))
    for item in consent["records"]:
        screenings[item["task_type_uri"]].append(("consent", item))
    for item in additional["records"]:
        screenings[item["task_type_uri"]].append(("additional", item))
    for uri, entries in screenings.items():
        if uri not in rows:
            raise ValueError("unregistered mapped Type URI")
        for origin, item in entries:
            if item["case_id"] not in versions or item.get("case_version", versions[item["case_id"]]) != versions[item["case_id"]]:
                raise ValueError("invalid canonical case version")
            if item["classification"] not in {"mechanism-overlap", "adjacent"}:
                raise ValueError("unsupported classification")
            if item.get("review_state", item.get("assessment_state")) != "research-screened":
                raise ValueError("unjustified reviewed state")
            if item.get("independent_review", "not-established") != "not-established" or item["execution_evidence"] != "none":
                raise ValueError("false assurance evidence")
            for key in ("rationale", "test_hypothesis", "authority_boundary"):
                if not item.get(key):
                    raise ValueError("absent mapping evidence")
            if origin in {"acl","consent","additional"}:
                if item["source_blob"] != rows[uri]["spec_blob"] or item["source_path"] != rows[uri]["path"]:
                    raise ValueError("screened source digest mismatch")
            else:
                if not any(s["type_uri"] == uri and s["source_path"] == rows[uri]["path"] for s in pilot["specifications"]):
                    raise ValueError("pilot source provenance mismatch")
    if len(screenings) != stats["screened_unique"]:
        raise ValueError("screened numerator inconsistent")
    groups = defaultdict(list)
    for uri, row in rows.items():
        groups[row["slug"].split("/")[0]].append((uri, row))
    index = [
        "# Trust Tasks versioned navigator", "",
        "Derived from a pinned upstream registry and DTFC's research sidecars. A pending",
        "version is NOT a reviewed non-match. A candidate mapping is NOT a defect report.", "",
        "**Upstream:** " + TICK + inventory["source"]["commit"] + TICK + "  ",
        "**Versioned tasks:** " + str(len(rows)) + "  ",
        "**Research-screened:** " + str(len(screenings)) + "  ",
        "**Full author-side case-examined:** " + str(len(author_cases)) + "  ",
        "**Author case comparisons:** " + str(37 * len(author_cases)) + "  ",
        "**Pending:** " + str(len(rows)-len(screenings)) + "  ",
        "**Independently reviewed:** 0  ",
        "**Independent target executions:** 0", "",
        "| Family | Versions | Screened | Pending | Author case-examined |",
        "|---|---:|---:|---:|---:|",
    ]
    pages = {}
    for family, items in sorted(groups.items()):
        items.sort(key=lambda p: (p[1]["slug"], tuple(map(int, p[1]["version"].split(".")))))
        covered = sum(uri in screenings for uri, _ in items)
        index.append("| [" + family + "](" + family + ".md) | " + str(len(items)) + " | " + str(covered) + " | " + str(len(items)-covered) + " | " + str(sum(uri in author_cases for uri, _ in items)) + " |")
        lines = ["# " + family + " task versions", "",
                 "Pinned upstream sources and preliminary DTFC screening; not semantic assurance.", "",
                 "[Family index](index.md)", "",
                 "| Version | Screening | Conditional DTF cases | Full author case examination |",
                 "|---|---|---|---|"]
        for uri, row in items:
            label = row["slug"] + "/" + row["version"]
            link = GIT + inventory["source"]["commit"] + "/" + row["path"]
            ids = sorted({i["case_id"] for _, i in screenings.get(uri, [])})
            cases = ", ".join("[" + ident + "](../corpus/" + ident + ".md)" for ident in ids) if ids else "not assessed"
            status = "research-screened" if uri in screenings else "needs-review"
            deep = author_cases.get(uri)
            deep_link = ("[37-case author matrix](" + deep["report_page"] + ")" if deep else "not examined")
            lines.append("| [" + label + "](" + link + ") | " + TICK + status + TICK + " | " + cases + " | " + deep_link + " |")
        lines.extend(["", "## Research mapping rationale", ""])
        for uri, row in items:
            if uri not in screenings:
                continue
            lines.extend(["### " + row["slug"] + "/" + row["version"], "",
                          "Pinned source blob: " + TICK + row["spec_blob"] + TICK + "  ",
                          "Independent review: " + TICK + "not-established" + TICK + "  ",
                          "Execution evidence: " + TICK + "none" + TICK, ""])
            for origin, item in screenings[uri]:
                lines.extend(["**" + item["case_id"] + " / " + item["classification"] + " / " + origin + "**", "",
                              "Conditional rationale: " + item["rationale"], "",
                              "Authority boundary: " + item["authority_boundary"], "",
                              "Falsification hypothesis: " + item["test_hypothesis"], ""])
        lines.extend(["", "Unscreened versions are unresolved, not safe or no-match.",
                      "A screened version may have additional unexamined DTFC failures.", ""])
        pages[family + ".md"] = "\n".join(lines)
    index.extend(["", "## Interpretation", "",
                  "Full author case-examination covers 14 versions, not the entire inventory.",
                  "Each reviewed case is a qualified research decision, not independent",
                  "semantic approval or an execution verdict. Not-established-from-task",
                  "is not a deployment-level no-match. See the linked family reports.", "",
                  "Use the pinned task source, the canonical failure case, and the stated",
                  "negative-test hypothesis. A mapping is a candidate consuming-system seam.",
                  "It does not establish upstream defect, independently tested conformance,",
                  "complete applicability, or accepted semantic peer review.",
                  "See [technical report](assessment-report.md),",
                  "[machine-readable report](assessment-report.json),",
                  "[review method](../trust-tasks-review-method.md) and",
                  "[coverage](../trust-tasks-coverage.md).", ""])
    pages["index.md"] = "\n".join(index)
    if len(groups) != 43 or len(pages) != 44:
        raise ValueError("unexpected published family inventory")
    return pages

def generate(output=OUTPUT):
    inventory = json.loads(MANIFEST.read_text())
    pilot = json.loads(PILOT.read_text())
    acl = json.loads(ACL_PATH.read_text())
    pages = build_pages(inventory, pilot, acl)
    output.mkdir(parents=True, exist_ok=True)
    for path in output.glob("*.md"):
        path.unlink()
    for path, contents in pages.items():
        (output / path).write_text(contents, encoding="utf-8")
    print("Generated", len(pages), "Trust Tasks navigation pages")

if __name__ == "__main__":
    generate()
