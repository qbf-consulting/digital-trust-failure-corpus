"""Pinned, complete-case author research for capability governance."""
import json
from tools.validate_trust_tasks_inventory import MANIFEST, ROOT
from tools.validate_full_case_examination import check_family

PATH = ROOT / "research/external-sources/trust-tasks/governance-case-examination.json"
URI = "https://trusttasks.org/spec/governance/capability/"
TARGETS = {URI + op + "/0.1" for op in ("disable", "enable", "list")}

def check(data, inventory):
    return check_family(data, inventory, "governance", TARGETS)

if __name__ == "__main__":
    print(json.dumps(check(json.loads(PATH.read_text()), json.loads(MANIFEST.read_text())), indent=2))
