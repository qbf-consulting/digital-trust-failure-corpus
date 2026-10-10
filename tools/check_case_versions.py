#!/usr/bin/env python3
"""Check changed canonical case content against a trusted base revision."""
from __future__ import annotations
import argparse
import json
import subprocess
from pathlib import Path
from tools.case_digest import canonical_case_bytes

ROOT = Path(__file__).resolve().parents[1]

def is_version_bump(old: str, new: str) -> bool:
    try:
        a, b = tuple(int(x) for x in old.split(".")), tuple(int(x) for x in new.split("."))
    except ValueError:
        return False
    return len(a) == len(b) == 3 and b > a

def check_case_changes(before: dict, after: dict) -> None:
    if before["id"] != after["id"]:
        raise ValueError("Canonical case ID changed")
    if canonical_case_bytes(before) != canonical_case_bytes(after):
        if not is_version_bump(before["version"], after["version"]):
            raise ValueError("Canonical case changed without case-version bump")

def check_git_diff(base: str) -> list[str]:
    if not base or base.startswith("-"):
        raise ValueError("Invalid base revision")
    paths = subprocess.check_output(
        ["git", "diff", "--name-only", "--diff-filter=AM", base, "HEAD", "--", "corpus"],
        cwd=ROOT, text=True).splitlines()
    checked = []
    for path in paths:
        if not path.endswith(".json"):
            continue
        current = ROOT / path
        if not current.is_file():
            continue
        try:
            old = subprocess.check_output(["git", "show", f"{base}:{path}"], cwd=ROOT)
        except subprocess.CalledProcessError:
            continue  # New cases have no previous version.
        check_case_changes(json.loads(old), json.loads(current.read_text(encoding="utf-8")))
        checked.append(path)
    return checked

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", required=True)
    args = parser.parse_args()
    checked = check_git_diff(args.base)
    print(json.dumps({"checked_changed_cases": checked}, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
