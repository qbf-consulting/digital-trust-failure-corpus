#!/usr/bin/env python3
"""Deterministic related-case baseline over the non-authoritative DTFC graph projection."""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

WEIGHTS = {
    "classified_as_failure_class": 5,
    "classified_as_domain": 3,
    "requires_evidence_category": 2,
    "cites_reference_type": 1,
    "has_expected_disposition": 1,
}

def related_cases(graph: dict, limit: int = 5) -> dict[str, list[dict]]:
    if not isinstance(limit, int) or isinstance(limit, bool) or limit < 1:
        raise ValueError("limit must be a positive integer")
    nodes, edges = graph.get("nodes"), graph.get("edges")
    if not isinstance(nodes, list) or not isinstance(edges, list):
        raise ValueError("graph must contain nodes[] and edges[]")
    ids = [n["id"] for n in nodes if isinstance(n, dict) and n.get("type") == "case"]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate case node")
    cases = set(ids)
    features: dict[str, set[tuple[str, str]]] = {c: set() for c in ids}
    for edge in edges:
        if not isinstance(edge, dict):
            raise ValueError("edge must be an object")
        source, relation, target = edge.get("source"), edge.get("type"), edge.get("target")
        if source in cases:
            if relation not in WEIGHTS:
                raise ValueError(f"unknown case feature relation: {relation}")
            if not isinstance(target, str) or not target:
                raise ValueError("invalid feature target")
            features[source].add((relation, target))
    result = {}
    for source in sorted(cases):
        candidates = []
        for target in sorted(cases - {source}):
            shared = features[source] & features[target]
            score = sum(WEIGHTS[relation] for relation, _ in shared)
            if not score:
                continue
            matches = [{"relation": relation, "target": feature} for relation, feature in sorted(shared)]
            candidates.append({"case_id": target.removeprefix("case:"), "score": score, "shared": matches})
        result[source.removeprefix("case:")] = sorted(candidates, key=lambda item: (-item["score"], item["case_id"]))[:limit]
    return result

def render_report(results: dict[str, list[dict]]) -> str:
    lines = [
        "# DTFC deterministic related-case baseline", "",
        "This report is a non-ML authoring and review aid derived from the canonical corpus graph.",
        "Similarity reflects shared taxonomy and evidence metadata, not equivalence, independent validation, assurance, conformance, or case correctness.", "",
        "## Method", "",
        "Score is a sum over **distinct shared (relation, target) pairs**: failure class 5, domain 3, evidence category 2, reference type 1, expected disposition 1.",
        "Pairs with zero overlap are omitted. Ordering is descending score, then ascending case ID; the maximum number of neighbours per case is configurable (default five).",
        "Broad shared attributes may dominate; scores are not normalized for feature prevalence and are not probabilities.", "",
        "## Related cases", ""
    ]
    for case_id, neighbours in sorted(results.items()):
        lines += [f"### {case_id}", ""]
        if not neighbours:
            lines += ["No overlapping case features.", ""]
            continue
        for item in neighbours:
            evidence = ", ".join(f"`{x['relation']}:{x['target']}`" for x in item["shared"])
            lines += [f"- **{item['case_id']}** (score {item['score']}): {evidence}"]
        lines.append("")
    return "\n".join(lines)

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--graph", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()
    graph = json.loads(args.graph.read_text(encoding="utf-8"))
    rendered = render_report(related_cases(graph, args.limit))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(rendered, encoding="utf-8")
    print(f"Wrote deterministic related-case report to {args.output}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
