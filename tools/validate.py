#!/usr/bin/env python3
"""Validate Digital Trust Failure Corpus case files.

The validator proves structural conformance to the repository schema and a small
set of collection-level invariants. It does not establish normative correctness,
severity, applicability, or completeness of any case.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCHEMA = ROOT / "schemas" / "failure-case.schema.json"
DEFAULT_CORPUS = ROOT / "corpus"


@dataclass(frozen=True)
class ValidationFinding:
    path: Path
    message: str

    def render(self) -> str:
        return f"{self.path}: {self.message}"


def discover_case_files(inputs: Sequence[Path]) -> list[Path]:
    files: set[Path] = set()
    for item in inputs:
        if item.is_file():
            if item.suffix.lower() == ".json":
                files.add(item.resolve())
            continue
        if item.is_dir():
            files.update(path.resolve() for path in item.rglob("*.json"))
    return sorted(files, key=lambda path: str(path))


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_case_files(
    case_files: Iterable[Path], schema_path: Path = DEFAULT_SCHEMA
) -> list[ValidationFinding]:
    schema = load_json(schema_path)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)

    findings: list[ValidationFinding] = []
    seen_ids: dict[str, Path] = {}
    seen_titles: dict[str, Path] = {}

    for path in sorted((Path(p) for p in case_files), key=lambda p: str(p)):
        try:
            case = load_json(path)
        except (OSError, json.JSONDecodeError) as exc:
            findings.append(ValidationFinding(path, f"cannot load JSON: {exc}"))
            continue

        errors = sorted(validator.iter_errors(case), key=lambda error: list(error.absolute_path))
        if errors:
            for error in errors:
                location = ".".join(str(part) for part in error.absolute_path) or "<root>"
                findings.append(
                    ValidationFinding(path, f"schema violation at {location}: {error.message}")
                )
            continue

        assert isinstance(case, dict)  # guaranteed by schema
        case_id = str(case["id"])
        title = str(case["title"])

        if case_id in seen_ids:
            findings.append(
                ValidationFinding(
                    path,
                    f"duplicate case id {case_id!r}; first seen in {seen_ids[case_id]}",
                )
            )
        else:
            seen_ids[case_id] = path

        if title in seen_titles:
            findings.append(
                ValidationFinding(
                    path,
                    f"duplicate case title {title!r}; first seen in {seen_titles[title]}",
                )
            )
        else:
            seen_titles[title] = path

    return findings


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        help="JSON files or directories to validate (default: corpus/)",
    )
    parser.add_argument(
        "--schema",
        type=Path,
        default=DEFAULT_SCHEMA,
        help="Schema path (default: schemas/failure-case.schema.json)",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    inputs = args.paths or [DEFAULT_CORPUS]
    case_files = discover_case_files(inputs)
    findings = validate_case_files(case_files, args.schema)

    if findings:
        for finding in findings:
            print(f"ERROR: {finding.render()}", file=sys.stderr)
        return 1

    print(f"Validated {len(case_files)} case file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
