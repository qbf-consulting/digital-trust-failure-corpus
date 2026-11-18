"""Validated author-side full-case records for published Trust Tasks consumers.

A complete author case matrix is not an independently accepted semantic assessment.
"""
import json
from tools.validate_trust_tasks_inventory import ROOT

SOURCES = (
    ("audit", "audit-case-examination.json", "trust-tasks-audit-case-examination.md"),
    ("consent", "consent-case-examination.json", "trust-tasks-consent-case-examination.md"),
    ("governance", "governance-case-examination.json", "trust-tasks-governance-case-examination.md"),
    ("task-consent", "task-consent-case-examination.json", "trust-tasks-task-consent-case-examination.md"),
    ("trust-task-discovery", "discovery-case-examination.json", "trust-tasks-discovery-case-examination.md"),
)
DIR = ROOT / "research/external-sources/trust-tasks"


def load(inventory):
    # Defer imports so the existing navigator/case-version authority remains
    # importable without cycles in report generation.
    from tools.validate_full_case_examination import check_family
    from tools.validate_audit_case_examination import TARGETS as A, DELTAS as AD
    from tools.validate_consent_case_examination import TARGETS as C, DELTAS as CD
    from tools.validate_governance_case_examination import TARGETS as G
    from tools.validate_task_consent_case_examination import TARGETS as T, DELTAS as TD
    from tools.validate_discovery_case_examination import TARGETS as D, DELTAS as DD
    gates = {"audit": (A, AD), "consent": (C, CD), "governance": (G, {}),
             "task-consent": (T, TD), "trust-task-discovery": (D, DD)}
    seen = {}
    for family, filename, page in SOURCES:
        data = json.loads((DIR / filename).read_text())
        check_family(data, inventory, family, *gates[family])
        for row in data["records"]:
            uri = row["type_uri"]
            if uri in seen:
                raise ValueError("overlapping author-side case examination")
            seen[uri] = {
                "record": row,
                "case_revision": data["dtfc_case_revision"],
                "record_url": "https://github.com/qbf-consulting/digital-trust-failure-corpus/blob/main/research/external-sources/trust-tasks/" + filename,
                "report_page": "../" + page,
            }
    return seen
