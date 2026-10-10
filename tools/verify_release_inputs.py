"""Fail-closed release input validation; no publication side effects."""
from __future__ import annotations
import argparse
import subprocess
from pathlib import Path

def verify_release_inputs(version_file: Path, notes: Path, existing_tags: set[str], checked_out_sha: str, expected_sha: str) -> str:
    version = version_file.read_text(encoding="utf-8").strip()
    if not version or not all(part.isdigit() for part in version.split(".")) or len(version.split(".")) != 3:
        raise ValueError("Invalid release version")
    if not notes.is_file() or not notes.read_text(encoding="utf-8").strip():
        raise ValueError("Release notes missing or empty")
    tag = "v" + version
    if tag in existing_tags:
        raise ValueError("Release tag already exists")
    if not expected_sha or len(expected_sha) != 40 or any(c not in "0123456789abcdef" for c in expected_sha):
        raise ValueError("Invalid expected commit SHA")
    if checked_out_sha != expected_sha:
        raise ValueError("Stale or mismatched commit SHA")
    return tag

def verify_checkout(version_file: Path, notes_dir: Path, expected_sha: str) -> str:
    """Read checkout and remote tags; do not rely on potentially shallow local tags."""
    checkout = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    version = version_file.read_text(encoding="utf-8").strip()
    if not version or "/" in version or "\\" in version:
        raise ValueError("Invalid release version")
    notes = notes_dir / f"release-notes-v{version}.md"
    remote_tags = subprocess.check_output(["git", "ls-remote", "--tags", "--refs", "origin"], text=True)
    tags = {line.split("refs/tags/", 1)[1].strip() for line in remote_tags.splitlines() if "refs/tags/" in line}
    return verify_release_inputs(version_file, notes, tags, checkout, expected_sha)

def main() -> int:
    parser = argparse.ArgumentParser(description="Verify release inputs against checked-out SHA and remote tags")
    parser.add_argument("--version-file", type=Path, required=True)
    parser.add_argument("--notes-dir", type=Path, required=True)
    parser.add_argument("--expected-sha", required=True)
    args = parser.parse_args()
    try:
        tag = verify_checkout(args.version_file, args.notes_dir, args.expected_sha)
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        parser.exit(1, f"Release input preflight rejected: {exc}\n")
    print(f"Release input preflight passed for {tag}; this does not authorize publication.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
