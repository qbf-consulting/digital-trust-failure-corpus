#!/usr/bin/env python3
"""Build a deterministic DTFC assurance graph from failure-case JSON files.

This module is intentionally dependency-light. It derives an inspectable graph from
canonical corpus files and can be used without PyTorch or PyTorch Geometric. The
optional PyG conversion lives behind an explicit import boundary so the core DTFC
validation path does not inherit machine-learning dependencies.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping


CASE_FILE_GLOB = "DTF-*.json"


@dataclass(frozen=True, order=True)
class GraphNode:
    """A typed graph node derived from corpus content."""

    id: str
    type: str
    label: str

    def as_dict(self) -> dict[str, str]:
        return {"id": self.id, "type": self.type, "label": self.label}


@dataclass(frozen=True, order=True)
class GraphEdge:
    """A typed directed graph edge derived from corpus content."""

    source: str
    target: str
    type: str

    def as_dict(self) -> dict[str, str]:
        return {"source": self.source, "target": self.target, "type": self.type}


@dataclass(frozen=True)
class AssuranceGraph:
    """Deterministic graph projection over DTFC case files."""

    nodes: tuple[GraphNode, ...]
    edges: tuple[GraphEdge, ...]

    def as_dict(self) -> dict[str, list[dict[str, str]]]:
        return {
            "nodes": [node.as_dict() for node in self.nodes],
            "edges": [edge.as_dict() for edge in self.edges],
        }


def slug(value: str) -> str:
    """Return a stable lowercase identifier fragment for graph node ids."""
    return "-".join(value.strip().lower().replace("_", "-").split())


def load_case(path: Path) -> Mapping[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path}: case JSON root must be an object")
    return value


def discover_case_files(corpus_path: Path) -> list[Path]:
    if corpus_path.is_file():
        return [corpus_path]
    return sorted(corpus_path.rglob(CASE_FILE_GLOB), key=lambda path: str(path))


def _add_node(nodes: dict[str, GraphNode], node_id: str, node_type: str, label: str) -> None:
    nodes.setdefault(node_id, GraphNode(id=node_id, type=node_type, label=label))


def _add_edge(edges: set[GraphEdge], source: str, target: str, edge_type: str) -> None:
    edges.add(GraphEdge(source=source, target=target, type=edge_type))


def build_graph(case_files: Iterable[Path]) -> AssuranceGraph:
    """Build an assurance graph from DTFC failure-case JSON files.

    The graph is a derived research artifact. It does not change corpus authority
    or validate normative correctness of any case.
    """

    nodes: dict[str, GraphNode] = {}
    edges: set[GraphEdge] = set()

    for path in sorted((Path(p) for p in case_files), key=lambda item: str(item)):
        case = load_case(path)
        case_id = str(case.get("id", "")).strip()
        if not case_id:
            raise ValueError(f"{path}: missing case id")

        title = str(case.get("title", case_id))
        case_node = f"case:{case_id}"
        _add_node(nodes, case_node, "case", f"{case_id}: {title}")

        for domain in sorted(str(item) for item in case.get("domains", [])):
            domain_node = f"domain:{slug(domain)}"
            _add_node(nodes, domain_node, "domain", domain)
            _add_edge(edges, case_node, domain_node, "classified_as_domain")

        for failure_class in sorted(str(item) for item in case.get("failure_classes", [])):
            class_node = f"failure_class:{slug(failure_class)}"
            _add_node(nodes, class_node, "failure_class", failure_class)
            _add_edge(edges, case_node, class_node, "classified_as_failure_class")

        evidence_required = case.get("evidence_required", [])
        if isinstance(evidence_required, list):
            for evidence in evidence_required:
                if not isinstance(evidence, Mapping):
                    continue
                category = str(evidence.get("category", "")).strip()
                if not category:
                    continue
                evidence_node = f"evidence_category:{slug(category)}"
                _add_node(nodes, evidence_node, "evidence_category", category)
                _add_edge(edges, case_node, evidence_node, "requires_evidence_category")

        references = case.get("references", [])
        if isinstance(references, list):
            for reference in references:
                if not isinstance(reference, Mapping):
                    continue
                reference_type = str(reference.get("type", "")).strip()
                if not reference_type:
                    continue
                reference_node = f"reference_type:{slug(reference_type)}"
                _add_node(nodes, reference_node, "reference_type", reference_type)
                _add_edge(edges, case_node, reference_node, "cites_reference_type")

        dispositions = case.get("expected", {}).get("dispositions", {})
        if isinstance(dispositions, Mapping):
            for disposition, status in sorted(dispositions.items()):
                disposition_node = f"disposition:{slug(str(disposition))}:{slug(str(status))}"
                label = f"{disposition}={status}"
                _add_node(nodes, disposition_node, "disposition", label)
                _add_edge(edges, case_node, disposition_node, "has_expected_disposition")

    return AssuranceGraph(
        nodes=tuple(sorted(nodes.values(), key=lambda node: (node.type, node.id))),
        edges=tuple(sorted(edges, key=lambda edge: (edge.source, edge.type, edge.target))),
    )


def write_graph_json(graph: AssuranceGraph, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(graph.as_dict(), handle, indent=2, sort_keys=True)
        handle.write("\n")


def graph_to_pyg_data(graph: AssuranceGraph):
    """Convert the derived graph to a PyTorch Geometric Data object.

    Node features are intentionally minimal one-hot node-type indicators. This is
    a smoke-test bridge, not a production embedding strategy.
    """

    try:
        import torch
        from torch_geometric.data import Data
    except ImportError as exc:  # pragma: no cover - exercised through dependency absence tests
        raise RuntimeError(
            "PyTorch and PyTorch Geometric are optional experiment dependencies. "
            "Install experiments/pytorch-geometric/requirements-experimental.txt "
            "to enable graph_to_pyg_data()."
        ) from exc

    node_index = {node.id: index for index, node in enumerate(graph.nodes)}
    node_types = sorted({node.type for node in graph.nodes})
    type_index = {node_type: index for index, node_type in enumerate(node_types)}

    features = []
    for node in graph.nodes:
        vector = [0.0] * len(node_types)
        vector[type_index[node.type]] = 1.0
        features.append(vector)

    edge_pairs = [
        (node_index[edge.source], node_index[edge.target])
        for edge in graph.edges
        if edge.source in node_index and edge.target in node_index
    ]
    if edge_pairs:
        edge_index = torch.tensor(edge_pairs, dtype=torch.long).t().contiguous()
    else:
        edge_index = torch.empty((2, 0), dtype=torch.long)

    return Data(x=torch.tensor(features, dtype=torch.float), edge_index=edge_index)


def build_from_corpus(corpus_path: Path) -> AssuranceGraph:
    return build_graph(discover_case_files(corpus_path))
