from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

EXPERIMENT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EXPERIMENT_ROOT))

from graph_report import generate_report, load_graph, write_report


class GraphReportTests(unittest.TestCase):
    def test_generates_deterministic_markdown_report(self) -> None:
        graph = {
            "nodes": [
                {"id": "case:DTF-999", "type": "case", "label": "DTF-999: fixture"},
                {"id": "domain:evidence", "type": "domain", "label": "evidence"},
                {"id": "failure_class:stale-evidence", "type": "failure_class", "label": "stale-evidence"},
                {"id": "evidence_category:freshness", "type": "evidence_category", "label": "freshness"},
                {"id": "reference_type:issue", "type": "reference_type", "label": "issue"},
                {"id": "disposition:pass:prohibited", "type": "disposition", "label": "PASS=prohibited"},
            ],
            "edges": [
                {"source": "case:DTF-999", "target": "domain:evidence", "type": "classified_as_domain"},
                {"source": "case:DTF-999", "target": "failure_class:stale-evidence", "type": "classified_as_failure_class"},
                {"source": "case:DTF-999", "target": "evidence_category:freshness", "type": "requires_evidence_category"},
                {"source": "case:DTF-999", "target": "reference_type:issue", "type": "cites_reference_type"},
                {"source": "case:DTF-999", "target": "disposition:pass:prohibited", "type": "has_expected_disposition"},
            ],
        }

        first = generate_report(graph)
        second = generate_report(graph)

        self.assertEqual(first, second)
        self.assertIn("| Case nodes | 1 |", first)
        self.assertIn("| Total nodes | 6 |", first)
        self.assertIn("| Total edges | 5 |", first)
        self.assertIn("not corpus authority", first)
        self.assertIn("No isolated nodes", first)

    def test_loads_graph_and_writes_report(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            graph_path = Path(directory) / "graph.json"
            report_path = Path(directory) / "report.md"
            graph_path.write_text(json.dumps({"nodes": [], "edges": []}), encoding="utf-8")

            report = generate_report(load_graph(graph_path))
            write_report(report, report_path)

            self.assertTrue(report_path.exists())
            self.assertIn("| Total nodes | 0 |", report_path.read_text(encoding="utf-8"))

    def test_rejects_malformed_graph_json(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            graph_path = Path(directory) / "graph.json"
            graph_path.write_text(json.dumps({"nodes": []}), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "nodes\[\] and edges\[\]"):
                load_graph(graph_path)


if __name__ == "__main__":
    unittest.main()
