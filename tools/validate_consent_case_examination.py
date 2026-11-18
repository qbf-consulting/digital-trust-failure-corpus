"""Complete canonical-case author examination of every pinned consent family version."""
import json
from tools.validate_trust_tasks_inventory import MANIFEST, ROOT
from tools.validate_full_case_examination import check_family

PATH = ROOT / "research/external-sources/trust-tasks/consent-case-examination.json"
URI = "https://trusttasks.org/spec/consent/"
VERSIONS = ("approve-request/0.1", "approver-list/1.0",
            "approver-set/1.0", "decision/1.0", "list/1.0",
            "list/1.1", "request/1.0", "revoke/1.0")
TARGETS = {URI + version for version in VERSIONS}
DELTAS = {URI + "list/1.1": (URI + "list/1.0", ("syncToken", "nextSyncToken"))}

def check(data, inventory):
    return check_family(data, inventory, "consent", TARGETS, DELTAS)

if __name__ == "__main__":
    print(json.dumps(check(json.loads(PATH.read_text()), json.loads(MANIFEST.read())), indent=2))
