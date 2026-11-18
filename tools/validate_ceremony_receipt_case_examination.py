"""Case-pinned full author assessment for trust-ceremony-receipt/0.1."""
import json
from tools.validate_trust_tasks_inventory import MANIFEST, ROOT
from tools.validate_full_case_examination import check_family

PATH = ROOT / "research/external-sources/trust-tasks/ceremony-receipt-case-examination.json"
URI = "https://trusttasks.org/spec/trust-ceremony-receipt/0.1"
TARGETS = {URI}

def check(data, inventory):
    return check_family(data, inventory, "trust-ceremony-receipt", TARGETS)

if __name__ == "__main__":
    print(json.dumps(check(json.loads(PATH.read_text()), json.loads(MANIFEST.read_text())), indent=2))
