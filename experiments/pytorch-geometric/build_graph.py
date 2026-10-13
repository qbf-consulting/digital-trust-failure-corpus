#!/usr/bin/env python3
"""Command-line graph exporter for the experimental DTFC PyG sidecar."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from graph_builder import build_from_corpus, graph_to_pyg_data, write_graph_json


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--corpus",
        type=Path,
        default=Path("corpus"),
        help="Corpus directory or single case JSON file",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("experiments/pytorch-geometric/out/dtfc-graph.json"),
        help="Output graph JSON path",
    )
    parser.add_argument(
        "--check-pyg",
        action="store_true",
        help="Also verify optional PyTorch Geometric conversion",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    graph = build_from_corpus(args.corpus)
    write_graph_json(graph, args.output)
    print(f"Wrote {len(graph.nodes)} node(s) and {len(graph.edges)} edge(s) to {args.output}")

    if args.check_pyg:
        data = graph_to_pyg_data(graph)
        print(f"PyG Data: x={tuple(data.x.shape)} edge_index={tuple(data.edge_index.shape)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
