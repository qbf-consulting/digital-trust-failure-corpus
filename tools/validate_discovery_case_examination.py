"""Pinned, complete-case author assessment for the discovery meta-task versions."""
import json
from tools.validate_trust_tasks_inventory import MANIFEST, ROOT
from tools.validate_full_case_examination import check_family

PATH = ROOT / "research/external-sources/trust-tasks/discovery-case-examination.json"
URI = "https://trusttasks.org/spec/trust-task-discovery/"
TARGETS = {URI + v for v in ("0.1", "0.2", "0.3", "0.4")}
DELTAS = {
    URI + "0.2": (URI + "0.1", ("MAJOR.MINOR.PATCH",)),
    URI + "0.3": (URI + "0.2", ("acceptanceWindow",)),
    URI + "0.4": (URI + "0.3", ("expiryHorizonSeconds",)),
}
def check(data, inventory):
    return check_family(data, inventory, "trust-task-discovery", TARGETS, DELTAS)

if __name__ == "__main__":
    print(json.dumps(check(json.loads(PATH.read_text()), json.loads(MANIFEST.read())), indent=2))
