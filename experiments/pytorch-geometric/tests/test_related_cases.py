from __future__ import annotations
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from related_cases import related_cases, render_report

def fixture():
    return {
        "nodes": [
            {"id": "case:DTF-002", "type": "case"},
            {"id": "case:DTF-003", "type": "case"},
            {"id": "case:DTF-001", "type": "case"},
            {"id": "case:DTF-004", "type": "case"},
        ],
        "edges": [
            {"source": "case:DTF-001", "target": "failure_class:stale", "type": "classified_as_failure_class"},
            {"source": "case:DTF-002", "target": "failure_class:stale", "type": "classified_as_failure_class"},
            {"source": "case:DTF-003", "target": "failure_class:stale", "type": "classified_as_failure_class"},
            {"source": "case:DTF-001", "target": "domain:authority", "type": "classified_as_domain"},
            {"source": "case:DTF-002", "target": "domain:authority", "type": "classified_as_domain"},
            {"source": "case:DTF-001", "target": "evidence_category:proof", "type": "requires_evidence_category"},
            {"source": "case:DTF-003", "target": "evidence_category:proof", "type": "requires_evidence_category"},
        ],
    }

class RelatedCasesTests(unittest.TestCase):
    def test_weights_and_tie_break(self):
        result = related_cases(fixture())
        self.assertEqual([(x["case_id"], x["score"]) for x in result["DTF-001"]], [("DTF-002", 8), ("DTF-003", 7)])
        self.assertEqual(result["DTF-004"], [])

    def test_stable_across_order_and_repetition(self):
        graph = fixture()
        result = related_cases(graph)
        self.assertEqual(result, related_cases(graph))
        graph["nodes"].reverse()
        graph["edges"].reverse()
        self.assertEqual(result, related_cases(graph))
        self.assertEqual(render_report(result), render_report(related_cases(graph)))

    def test_limit_and_unique_features(self):
        graph = fixture()
        graph["edges"].append(dict(graph["edges"][0]))
        self.assertEqual(related_cases(graph, 1)["DTF-001"][0]["score"], 8)
        self.assertEqual(len(related_cases(graph, 1)["DTF-001"]), 1)

    def test_negative_inputs(self):
        with self.assertRaisesRegex(ValueError, "positive integer"):
            related_cases(fixture(), 0)
        with self.assertRaisesRegex(ValueError, "duplicate"):
            graph = fixture()
            graph["nodes"].append({"id": "case:DTF-001", "type": "case"})
            related_cases(graph)
        with self.assertRaisesRegex(ValueError, "unknown case feature"):
            graph = fixture()
            graph["edges"].append({"source": "case:DTF-001", "target": "x", "type": "unknown"})
            related_cases(graph)

    def test_output_declares_boundary(self):
        markdown = render_report(related_cases(fixture()))
        self.assertIn("not equivalence", markdown)
        self.assertIn("### DTF-004", markdown)
        self.assertIn("No overlapping case features", markdown)

if __name__ == "__main__":
    unittest.main()
