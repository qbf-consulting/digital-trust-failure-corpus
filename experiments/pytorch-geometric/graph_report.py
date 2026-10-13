#!/usr/bin/env python3
"""Generate a deterministic Markdown report from a DTFC graph JSON file."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping, Sequence


@dataclass(frozen=True)
class CountRow:
    name: str
    count: int


def load_graph(path: Path) -> Mapping[str, object]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path}: graph JSON root must be an object")
    nodes = value.get("nodes")
    edges = value.get("edges")
    if not isinstance(nodes, list) or not isinstance(edges, list):
        raise ValueError(f"{path}: graph JSON must contain nodes[] and edges[]")
    return value


def _counter_rows(counter: Counter[str]) -> list[CountRow]:
    return [
        CountRow(name=name, count=count)
        for name, count in sorted(counter.items(), key=lambda item: (-item[1], item[0]))
    ]


def _table(title: str, rows: Iterable[CountRow]) -> list[str]:
    output = [f"## {title}", "", "| Value | Count |", "|---|---:|"]
    row_list = list(rows)
    if not row_list:
        output.append("| _none_ | 0 |")
    else:
        for row in row_list:
            output.append(f"| `{row.name}` | {row.count} |")
    output.append("")
    return output


def generate_report(graph: Mapping[str, object]) -> str:
    nodes = graph["nodes"]
    edges = graph["edges"]
    assert isinstance(nodes, list)
    assert isinstance(edges, list)

    node_types: Counter[str] = Counter()
    edge_types: Counter[str] = Counter()
    labels_by_type: dict[str, Counter[str]] = {
        "domain": Counter(),
        "failure_class": Counter(),
        "evidence_category": Counter(),
        "reference_type": Counter(),
        "disposition": Counter(),
    }

    case_node_ids: set[str] = set()
    connected_node_ids: set[str] = set()

    for node in nodes:
        if not isinstance(node, Mapping):
            continue
        node_type = str(node.get("type", ""))
        node_id = str(node.get("id", ""))
        label = str(node.get("label", ""))
        node_types[node_type] += 1
        if node_type == "case":
            case_node_ids.add(node_id)
        if node_type in labels_by_type:
            labels_by_type[node_type][label] += 1

    for edge in edges:
        if not isinstance(edge, Mapping):
            continue
        edge_type = str(edge.get("type", ""))
        edge_types[edge_type] += 1
        connected_node_ids.add(str(edge.get("source", "")))
        connected_node_ids.add(str(edge.get("target", "")))

    isolated_nodes = sorted(
        str(node.get("id", ""))
        for node in nodes
        if isinstance(node, Mapping) and str(node.get("id", "")) not in connected_node_ids
    )

    lines: list[str] = [
        "# DTFC experimental graph baseline report",
        "",
        "This report is a deterministic research sidecar generated from the experimental graph JSON projection. It is not corpus authority, normative coverage evidence, external adoption evidence, assurance certification, or a machine-learning result.",
        "",
        "## Summary",
        "",
        "| Metric | Count |",
        "|---|---:|",
        f"| Case nodes | {len(case_node_ids)} |",
        f"| Total nodes | {len(nodes)} |",
        f"| Total edges | {len(edges)} |",
        f"| Isolated nodes | {len(isolated_nodes)} |",
        "",
        "## Evidence boundary",
        "",
        "- These counts are deterministic graph facts derived from `corpus/**/*.json` through the experimental projection code.",
        "- They are not learned embeddings, clusters, predictions, maturity assessments, conformance results, or assurance decisions.",
        "- PyTorch/PyG conversion remains an optional runtime validation path and is not required for this report.",
        "",
    ]

    lines.extend(_table("Node types", _counter_rows(node_types)))
    lines.extend(_table("Edge relation types", _counter_rows(edge_types)))
    lines.extend(_table("Domains", _counter_rows(labels_by_type["domain"])))
    lines.extend(_table("Failure classes", _counter_rows(labels_by_type["failure_class"])))
    lines.extend(_table("Evidence categories", _counter_rows(labels_by_type["evidence_category"])))
    lines.extend(_table("Reference types", _counter_rows(labels_by_type["reference_type"])))
    lines.extend(_table("Expected dispositions", _counter_rows(labels_by_type["disposition"])))

    lines.append("## Isolated nodes")
    lines.append("")
    if isolated_nodes:
        for node_id in isolated_nodes:
            lines.append(f"- `{node_id}`")
    else:
        lines.append("No isolated nodes were present in the generated graph.")
    lines.append("")

    return "\n".join(lines)


def write_report(report: str, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--graph", type=Path, required=True, help="Graph JSON input path")
    parser.add_argument("--output", type=Path, required=True, help="Markdown report output path")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    report = generate_report(load_graph(args.graph))
    write_report(report, args.output)
    print(f"Wrote baseline graph report to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
