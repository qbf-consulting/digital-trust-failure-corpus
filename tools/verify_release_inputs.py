"""Offline fail-closed release input checks; never publish tags or releases."""
from pathlib import Path

def verify_release_inputs(version_file: Path, notes: Path, existing_tags: set[str], checked_out_sha: str, expected_sha: str) -> str:
    version = version_file.read_text().strip()
    if not version or not all(part.isdigit() for part in version.split(".")) or len(version.split(".")) != 3:
        raise ValueError("Invalid release version")
    if not notes.is_file() or not notes.read_text().strip():
        raise ValueError("Release notes missing or empty")
    tag = "v" + version
    if tag in existing_tags:
        raise ValueError("Release tag already exists")
    if not expected_sha or len(expected_sha) != 40 or any(c not in "0123456789abcdef" for c in expected_sha):
        raise ValueError("Invalid expected commit SHA")
    if checked_out_sha != expected_sha:
        raise ValueError("Stale or mismatched commit SHA")
    return tag
