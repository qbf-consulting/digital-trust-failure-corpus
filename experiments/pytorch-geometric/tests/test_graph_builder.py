from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

EXPERIMENT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EXPERIMENT_ROOT))

from graph_builder import build_from_corpus, graph_to_pyg_data, write_graph_json


class GraphBuilderTests(unittest.TestCase):
    def test_builds_deterministic_case_graph(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            corpus = Path(directory) / "corpus"
            corpus.mkdir()
            case_path = corpus / "DTF-999.json"
            case_path.write_text(
                json.dumps(
                    {
                        "id": "DTF-999",
                        "title": "fixture-case",
                        "domains": ["evidence", "authorization"],
                        "failure_classes": ["stale-evidence"],
                        "expected": {
                            "dispositions": {
                                "PASS": "prohibited",
                                "DENY": "allowed",
                            }
                        },
                        "evidence_required": [
                            {"category": "freshness", "statement": "freshness evidence"},
                            {"category": "authority-state", "statement": "authority evidence"},
                        ],
                        "references": [
                            {"type": "issue", "locator": "https://example.test/issue/1"}
                        ],
                    }
                ),
                encoding="utf-8",
            )

            first = build_from_corpus(corpus)
            second = build_from_corpus(corpus)

        self.assertEqual(first.as_dict(), second.as_dict())
        node_ids = {node["id"] for node in first.as_dict()["nodes"]}
        edge_types = {edge["type"] for edge in first.as_dict()["edges"]}

        self.assertIn("case:DTF-999", node_ids)
        self.assertIn("domain:authorization", node_ids)
        self.assertIn("evidence_category:freshness", node_ids)
        self.assertIn("reference_type:issue", node_ids)
        self.assertIn("disposition:pass:prohibited", node_ids)
        self.assertIn("classified_as_domain", edge_types)
        self.assertIn("requires_evidence_category", edge_types)
        self.assertIn("has_expected_disposition", edge_types)

    def test_writes_sorted_graph_json(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            corpus = Path(directory) / "corpus"
            output = Path(directory) / "out" / "graph.json"
            corpus.mkdir()
            (corpus / "DTF-001.json").write_text(
                json.dumps(
                    {
                        "id": "DTF-001",
                        "title": "a",
                        "domains": [],
                        "failure_classes": [],
                        "expected": {"dispositions": {"PASS": "prohibited"}},
                    }
                ),
                encoding="utf-8",
            )
            graph = build_from_corpus(corpus)
            write_graph_json(graph, output)
            loaded = json.loads(output.read_text(encoding="utf-8"))

        self.assertEqual(loaded, graph.as_dict())

    def test_pyg_dependency_is_optional_and_explicit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            corpus = Path(directory) / "corpus"
            corpus.mkdir()
            (corpus / "DTF-001.json").write_text(
                json.dumps(
                    {
                        "id": "DTF-001",
                        "title": "a",
                        "domains": [],
                        "failure_classes": [],
                        "expected": {"dispositions": {"PASS": "prohibited"}},
                    }
                ),
                encoding="utf-8",
            )
            graph = build_from_corpus(corpus)

        real_import = __import__

        def blocked_import(name, *args, **kwargs):
            if name == "torch" or name.startswith("torch_geometric"):
                raise ImportError(name)
            return real_import(name, *args, **kwargs)

        with mock.patch("builtins.__import__", side_effect=blocked_import):
            with self.assertRaisesRegex(RuntimeError, "optional experiment dependencies"):
                graph_to_pyg_data(graph)


if __name__ == "__main__":
    unittest.main()
