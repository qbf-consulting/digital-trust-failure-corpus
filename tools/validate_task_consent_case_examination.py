"""Pinned, complete-case author research for delegated task consent."""
import json
from tools.validate_trust_tasks_inventory import MANIFEST, ROOT
from tools.validate_full_case_examination import check_family

PATH = ROOT / "research/external-sources/trust-tasks/task-consent-case-examination.json"
URI = "https://trusttasks.org/spec/task-consent/"
TARGETS = {URI + x for x in ("request/0.1", "decision/0.1", "decision/0.2", "granted/0.1")}
DELTAS = {URI + "decision/0.2": (URI + "decision/0.1", ("evidence", "actionId", "assertionMethod"))}

def check(data, inventory):
    return check_family(data, inventory, "task-consent", TARGETS, DELTAS)

if __name__ == "__main__":
    print(json.dumps(check(json.loads(PATH.read_text()), json.loads(MANIFEST.read_text())), indent=2))
