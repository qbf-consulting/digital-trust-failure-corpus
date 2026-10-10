#!/usr/bin/env python3
"""Fail-closed manual release preflight for a named single-maintainer model.

GitHub actor and branch checks are enforced here; GitHub environment branch
restrictions and any additional reviewer protection are configured externally.
A configuration variable is not independent human approval.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

AUTHORIZED_DISPATCHERS = frozenset({"sankarshanmukhopadhyay"})


def check_request(*, request: Path, version_file: Path, event: str,
                  ref: str, actor: str, authorization_mode: str) -> None:
    if event != "workflow_dispatch":
        raise ValueError("Release publication requires an explicit manual workflow dispatch")
    if ref != "refs/heads/main":
        raise ValueError("Release publication must run on main")
    if actor not in AUTHORIZED_DISPATCHERS:
        raise ValueError("Dispatching GitHub actor is not authorized to request publication")
    if authorization_mode != "single-maintainer":
        raise ValueError(
            "Release authorization mode must be explicitly set to single-maintainer "
            "in the release-publication environment after verifying main restriction"
        )
    data = json.loads(request.read_text(encoding="utf-8"))
    version = version_file.read_text(encoding="utf-8").strip()
    if not version or data.get("version") != version:
        raise ValueError("Release request version must match VERSION")
    if not isinstance(data.get("reason"), str) or not data["reason"].strip():
        raise ValueError("Release request must contain a nonempty rationale")
    # requested_by is non-authoritative provenance, not a credential or approval.
    if not isinstance(data.get("requested_by"), str) or not data["requested_by"].strip():
        raise ValueError("Release request must identify its recorded requester")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument("--version-file", type=Path, required=True)
    parser.add_argument("--event", required=True)
    parser.add_argument("--ref", required=True)
    parser.add_argument("--actor", required=True)
    args = parser.parse_args()
    try:
        check_request(request=args.request, version_file=args.version_file,
                      event=args.event, ref=args.ref, actor=args.actor,
                      authorization_mode=os.environ.get("RELEASE_AUTHORIZATION_MODE", ""))
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        parser.exit(1, f"Release preflight rejected: {exc}\n")
    print("Single-maintainer release preflight passed; no independent human approval is asserted.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
