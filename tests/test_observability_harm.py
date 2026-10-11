"""Falsification fixtures for synthetic observability harm. Run: python -m unittest discover -s tests."""
import unittest
from tools.observability_harm import evaluate_observability

class ObservabilityHarmTests(unittest.TestCase):
    def test_cross_context_join_fails(self):
        events = [{"context": c, "trace_id": "shared", "evidence_state": "verified"} for c in ("verifier-a", "verifier-b")]
        self.assertEqual(evaluate_observability(events)["reason"], "cross-context-trace-correlation")

    def test_missing_event_never_passes(self):
        self.assertEqual(evaluate_observability([{"context": "a", "trace_id": "x", "evidence_state": "missing"}])["state"], "INDETERMINATE")

    def test_telemetry_cannot_authorize_adverse_action(self):
        events = [{"context": "a", "trace_id": "x", "evidence_state": "verified", "decision_source": "telemetry", "consequential_action": "suspend"}]
        self.assertEqual(evaluate_observability(events)["reason"], "telemetry-promoted-to-authority")

    def test_no_incident_does_not_prove_safety(self):
        events = [{"context": "a", "trace_id": "x", "evidence_state": "verified"}]
        self.assertEqual(evaluate_observability(events)["state"], "INDETERMINATE")

    def test_malformed_event_rejected(self):
        with self.assertRaises(ValueError):
            evaluate_observability([None])
