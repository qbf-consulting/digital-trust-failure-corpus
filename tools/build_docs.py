#!/usr/bin/env python3
"""Generate human-readable DTFC case pages from the canonical JSON corpus."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "corpus"
OUTPUT = ROOT / "docs" / "corpus"
REPO_BLOB = "https://github.com/qbf-consulting/digital-trust-failure-corpus/blob/main"


def _load_cases():
    cases = []
    for path in sorted(CORPUS.rglob("DTF-*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        cases.append((data["id"], path, data))
    return sorted(cases, key=lambda item: item[0])


def _text(value):
    return str(value).replace("|", "\\|").strip()


def _code_list(values):
    return ", ".join(f"`{_text(value)}`" for value in values)


def _render_case(path: Path, case: dict) -> str:
    rel = path.relative_to(ROOT).as_posix()
    lines = [
        f"# {case['id']} — {case['title'].replace('-', ' ')}",
        "",
        f"**Status:** `{case['status']}`  ",
        f"**Case version:** `{case['version']}`  ",
        f"**Canonical source:** [{rel}]({REPO_BLOB}/{rel})",
        "",
        "## Proposition",
        "",
        case["proposition"]["statement"],
        "",
        "## Classification",
        "",
        "| Dimension | Values |",
        "|---|---|",
        f"| Domains | {_code_list(case['domains'])} |",
        f"| Failure classes | {_code_list(case['failure_classes'])} |",
        "",
        "## Preconditions",
        "",
    ]
    lines.extend(f"- {item}" for item in case["preconditions"])
    lines.extend([
        "",
        "## Trigger",
        "",
        case["trigger"]["statement"],
        "",
        "## Expected dispositions",
        "",
        "| Disposition | Treatment |",
        "|---|---|",
    ])
    for disposition in ("PASS", "DENY", "INDETERMINATE"):
        lines.append(
            f"| `{disposition}` | `{case['expected']['dispositions'][disposition]}` |"
        )

    lines.extend([
        "",
        "## Evidence required",
        "",
        "| Category | Requirement |",
        "|---|---|",
    ])
    for item in case["evidence_required"]:
        lines.append(f"| `{_text(item['category'])}` | {_text(item['statement'])} |")

    lines.extend(["", "## Falsification conditions", ""])
    lines.extend(f"- {item['condition']}" for item in case["falsification"])

    refs = case.get("references", [])
    if refs:
        lines.extend(["", "## References and provenance", ""])
        for ref in refs:
            note = ref.get("note", "")
            suffix = f" — {note}" if note else ""
            lines.append(
                f"- **{_text(ref['type'])}:** [{ref['locator']}]({ref['locator']}){suffix}"
            )

    lines.extend([
        "",
        "---",
        "",
        "This page is generated from the canonical machine-readable corpus. "
        "If this rendered page and the JSON differ, the committed JSON case is authoritative for DTFC repository content.",
        "",
    ])
    return "\n".join(lines)


def _render_index(cases) -> str:
    lines = [
        "# Corpus catalogue",
        "",
        "This catalogue is generated from the committed machine-readable DTFC corpus.",
        "",
        f"**Cases:** {len(cases)}  ",
        f"**Range:** {cases[0][0]}–{cases[-1][0]}",
        "",
        "| Case | Title | Status | Domains |",
        "|---|---|---|---|",
    ]
    for case_id, _path, case in cases:
        page = f"{case_id}.md"
        title = case["title"].replace("-", " ")
        domains = _code_list(case["domains"])
        lines.append(
            f"| [{case_id}]({page}) | {title} | `{case['status']}` | {domains} |"
        )

    lines.extend([
        "",
        "## Interpretation boundary",
        "",
        "A case records a falsifiable failure proposition and its evidence requirements. "
        "Inclusion does not establish universal severity, external normative authority, implementation conformance, or assurance approval.",
        "",
    ])
    return "\n".join(lines)


def main() -> None:
    cases = _load_cases()
    if not cases:
        raise SystemExit("No corpus cases found.")

    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    OUTPUT.mkdir(parents=True)

    seen = set()
    for case_id, path, case in cases:
        if case_id in seen:
            raise SystemExit(f"Duplicate case ID while generating docs: {case_id}")
        seen.add(case_id)
        (OUTPUT / f"{case_id}.md").write_text(
            _render_case(path, case), encoding="utf-8"
        )

    (OUTPUT / "index.md").write_text(_render_index(cases), encoding="utf-8")
    print(f"Generated {len(cases)} case pages in {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
