#!/usr/bin/env python3
"""Fail-closed preflight for manually approved DTFC release publication.

GitHub environment required reviewers are enforced by GitHub settings, not by
this script. RELEASE_APPROVAL_CONFIGURED must be supplied as an environment-
scoped variable *after* a maintainer verifies those settings.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

AUTHORIZED_DISPATCHERS = frozenset({"sankarshanmukhopadhyay"})


def check_request(*, request: Path, version_file: Path, event: str,
                  ref: str, actor: str, approval_configured: str) -> None:
    if event != "workflow_dispatch":
        raise ValueError("Release publication requires an explicit manual workflow dispatch")
    if ref != "refs/heads/main":
        raise ValueError("Release publication must run on main")
    if actor not in AUTHORIZED_DISPATCHERS:
        raise ValueError("Dispatching GitHub actor is not authorized to request publication")
    if approval_configured != "true":
        raise ValueError(
            "release-publication environment approval is not attested; "
            "configure required reviewers and set environment variable "
            "RELEASE_APPROVAL_CONFIGURED=true only after verifying protection"
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
                      approval_configured=os.environ.get("RELEASE_APPROVAL_CONFIGURED", ""))
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        parser.exit(1, f"Release preflight rejected: {exc}\n")
    print("Release request preflight passed; GitHub environment approval is separately required.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
