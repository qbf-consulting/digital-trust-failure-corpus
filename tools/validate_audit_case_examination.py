"""Pinned, complete-case author research for audit list and verification."""
import json
from tools.validate_trust_tasks_inventory import MANIFEST, ROOT
from tools.validate_full_case_examination import check_family

PATH = ROOT / "research/external-sources/trust-tasks/audit-case-examination.json"
URI = "https://trusttasks.org/spec/"
TARGETS = {URI + v for v in ("audit/list/0.1", "audit/list/0.2", "audit/verify/0.1")}
DELTAS = {URI + "audit/list/0.2": (URI + "audit/list/0.1", ("nextCursor",))}

def check(data, inventory, cases=None):
    return check_family(data, inventory, "audit", TARGETS, DELTAS, cases)

if __name__ == "__main__":
    print(json.dumps(check(json.loads(PATH.read_text()), json.loads(MANIFEST.read_text())), indent=2))
