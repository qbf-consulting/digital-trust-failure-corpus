"""Derived, non-normative coverage for pinned Trust Tasks applicability research."""
import json
from collections import Counter
from pathlib import Path

from tools.validate_trust_tasks_inventory import MANIFEST, PILOT, check as check_inventory
from tools.validate_acl_review import PATH as ACL_PATH, check as check_acl

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "trust-tasks-coverage.md"
PREFIX = "https://trusttasks.org/spec/"


def calculate(inventory, pilot, acl):
    check_inventory(inventory, pilot)
    check_acl(acl, inventory)
    original = {x["slug"] + "/" + x["version"] for x in pilot["specifications"]}
    reviewed_acl = {x["task_type_uri"].removeprefix(PREFIX) for x in acl["current"] + acl["historical_screenings"]}
    all_ids = {x["slug"] + "/" + x["version"] for x in inventory["records"]}
    if not reviewed_acl <= all_ids or not original <= all_ids:
        raise ValueError("crosswalk refers to absent inventory task")
    screened = original | reviewed_acl
    counts = {}
    for row in inventory["records"]:
        family = row["slug"].split("/")[0]
        c = counts.setdefault(family, Counter())
        key = row["slug"] + "/" + row["version"]
        c["all_versions"] += 1
        if key in original:
            c["original_pilot"] += 1
        if key in reviewed_acl:
            c["acl_screening"] += 1
        if key in screened:
            c["screened_unique"] += 1
        else:
            c["pending"] += 1
    return {
        "upstream_commit": inventory["source"]["commit"],
        "source_versions": len(all_ids),
        "original_pilot": len(original),
        "acl_screening": len(reviewed_acl),
        "overlapping_source_versions": len(original & reviewed_acl),
        "screened_unique": len(screened),
        "pending": len(all_ids - screened),
        "families": counts,
        "inventory_publication_reconciled": True,
        "semantic_review_complete": False,
        "independent_execution": False,
    }


def render(stats):
    lines = [
        "# Trust Tasks applicability coverage (derived research)",
        "",
        "Generated from the pinned DTFC inventory, the original 12-task screening and the bounded ACL review.",
        "Registry membership and statuses are source-pinned and CI-reconciled; this page does not establish independent semantic review or execution evidence.",
        "",
        f"**Upstream revision:** `{stats['upstream_commit']}`  ",
        f"**Versioned source pairs:** {stats['source_versions']}  ",
        f"**Original pilot:** {stats['original_pilot']}  ",
        f"**ACL source screening:** {stats['acl_screening']}  ",
        f"**Overlap:** {stats['overlapping_source_versions']}  ",
        f"**Distinct source-screened versions:** {stats['screened_unique']}  ",
        f"**Not yet source-screened:** {stats['pending']}  ",
        "",
        "Screened means DTFC-authored research mapping, **not** independent verification or all-case semantic completeness.",
        "Historical versions do not inherit screened status from a later version.",
        "",
        "| Family | Source versions | Original pilot | ACL screening | Distinct screened | Pending |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for family, c in sorted(stats["families"].items()):
        lines.append(f"| `{family}` | {c['all_versions']} | {c['original_pilot']} | {c['acl_screening']} | {c['screened_unique']} | {c['pending']} |")
    lines += [
        "",
        "## Interpretation and reproduction",
        "",
        "Each row is an inventory item, not an assurance result. Version-delta equivalence and substantive",
        "DTFC applicability remain unverified despite successful upstream registry reconciliation.",
        "A screened task may have more applicable DTFC cases than currently documented; a pending task",
        "is not a reviewed no-match. A mapping hypothesis is not evidence that an implementation failed.",
        "",
        "Run `python -m tools.trust_tasks_coverage` to emit this page's content or",
        "`python -m tools.trust_tasks_coverage --check` to reject documentation drift.",
        "The repository unit tests independently exercise false-success and missing-input conditions.",
        "",
    ]
    return "\n".join(lines).replace("\\`", "`")


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    inventory = json.loads(MANIFEST.read_text())
    pilot = json.loads(PILOT.read_text())
    acl = json.loads(ACL_PATH.read_text())
    rendered = render(calculate(inventory, pilot, acl))
    if args.check:
        if DOC.read_text() != rendered:
            raise SystemExit("coverage document differs from source-derived metrics")
        print("coverage document matches pinned sources")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
