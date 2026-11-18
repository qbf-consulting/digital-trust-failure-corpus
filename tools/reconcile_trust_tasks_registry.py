"""Reconcile pinned DTFC Trust Tasks inventory with an actual upstream checkout and built registry.

Use only read-only offline source inputs. This tool does NOT certify substantive applicability.
"""
import argparse
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path

from tools.validate_trust_tasks_inventory import MANIFEST, PIN, PILOT, check as check_inventory


STATUSES = {"draft", "candidate", "standard", "retired", "withdrawn"}
PREFIX = "https://trusttasks.org/spec/"


def git_blob_sha(content):
    return hashlib.sha1(b"blob " + str(len(content)).encode() + b"\\0" + content).hexdigest()


def discover(checkout):
    specs = checkout / "specs"
    if not specs.is_dir():
        raise ValueError("missing upstream specs directory")
    files = set()
    for file in specs.rglob("*"):
        if not file.is_file():
            continue
        rel = file.relative_to(specs)
        if any(part.startswith(("_", ".")) for part in rel.parts[:-1]):
            continue
        if file.name in {"spec.md", "payload.schema.json"}:
            files.add(rel.as_posix())
    directories = {str(Path(x).parent) for x in files}
    result = {}
    for directory in directories:
        prose = directory + "/spec.md"
        schema = directory + "/payload.schema.json"
        if (prose in files) != (schema in files):
            raise ValueError("incomplete spec/schema pair: " + directory)
        if prose not in files:
            continue
        parts = directory.split("/")
        if len(parts) < 2:
            raise ValueError("invalid spec identity " + directory)
        slug, version = "/".join(parts[:-1]), parts[-1]
        key = PREFIX + slug + "/" + version
        if key in result:
            raise ValueError("duplicate spec: " + key)
        result[key] = {
            "path": "specs/" + prose,
            "spec_blob": git_blob_sha((specs / prose).read_bytes()),
            "schema_blob": git_blob_sha((specs / schema).read_bytes()),
        }
    return result


def reconcile(inventory, checkout, registry):
    canonical = {PREFIX + x["slug"] + "/" + x["version"]: x for x in inventory["records"]}
    discovered = discover(checkout)
    if set(canonical) != set(discovered):
        missing = sorted(set(canonical) - set(discovered))
        extra = sorted(set(discovered) - set(canonical))
        raise ValueError(f"source-tree membership differs: missing={missing[:3]}, extra={extra[:3]}")
    for key, row in canonical.items():
        actual = discovered[key]
        if any(actual[field] != row[field] for field in ("path", "spec_blob", "schema_blob")):
            raise ValueError("source content or identity differs: " + key)
    tasks = registry.get("tasks")
    if not isinstance(tasks, list):
        raise ValueError("generated registry has no tasks array")
    published = {}
    statuses = Counter()
    for task in tasks:
        slug, version, status = task["slug"], task["version"], task["status"]
        key = PREFIX + slug + "/" + version
        if task.get("typeUri") != key or key in published or status not in STATUSES:
            raise ValueError("invalid, duplicated or unrecognized registry task: " + key)
        published[key] = status
        statuses[status] += 1
    if set(published) != set(discovered):
        missing = sorted(set(discovered) - set(published))
        extra = sorted(set(published) - set(discovered))
        raise ValueError(f"generated registry/source mismatch: missing={missing[:3]}, extra={extra[:3]}")
    return {
        "upstream_commit": inventory["source"]["commit"],
        "source_pairs": len(discovered),
        "registry_versions": len(published),
        "status_counts": dict(sorted(statuses.items())),
        "publication_reconciled": True,
        "semantic_review_complete": False,
        "independent_execution": False,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkout", type=Path, required=True,
                        help="clean checkout of pinned upstream Trust Tasks source")
    parser.add_argument("--registry", type=Path, default=None,
                        help="generated website/registry.json in that checkout")
    args = parser.parse_args()
    checkout = args.checkout.resolve()
    current = subprocess.run(["git", "-C", str(checkout), "rev-parse", "HEAD"],
                             text=True, capture_output=True, check=True).stdout.strip()
    if current != PIN:
        raise SystemExit(f"wrong upstream commit: {current}; required {PIN}")
    inventory = json.loads(MANIFEST.read_text())
    pilot = json.loads(PILOT.read_text())
    check_inventory(inventory, pilot)
    registry_path = args.registry or checkout / "website" / "registry.json"
    if not registry_path.is_file():
        raise SystemExit("generated registry missing; run upstream npm ci && npm run build")
    result = reconcile(inventory, checkout, json.loads(registry_path.read_text()))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
