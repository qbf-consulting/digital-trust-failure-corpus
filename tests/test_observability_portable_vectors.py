import json
import unittest
from pathlib import Path
from tools.observability_harm import evaluate_observability

class PortableObservabilityVectors(unittest.TestCase):
    def test_canonical_synthetic_vectors(self):
        path = Path(__file__).resolve().parents[1] / "research" / "observability" / "synthetic-vectors-v1.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(payload["contract"], "dtfc-observability-synthetic-vectors/v1")
        self.assertFalse(payload["provenance"]["deployment_evidence"])
        self.assertEqual(payload["provenance"]["evidence_class"], "author-supplied-synthetic")
        self.assertEqual(len({v["id"] for v in payload["vectors"]}), len(payload["vectors"]))
        for vector in payload["vectors"]:
            with self.subTest(vector=vector["id"]):
                self.assertEqual(evaluate_observability(vector["events"]), vector["expected"])
                self.assertNotEqual(vector["expected"]["state"], "PASS")
