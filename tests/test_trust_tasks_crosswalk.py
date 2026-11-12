"""Offline integrity tests for bounded, source-pinned Trust Tasks research."""
import copy
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "research/external-sources/trust-tasks/mapping.json"
PIN = "f21a98ec8383352d18629a08dd5dd23935456142"
FAMILIES = {"acl", "auth", "credential-exchange", "registry", "policy"}
CLASSES = {"mechanism-overlap", "adjacent", "not-established"}


def validate_mapping(data):
    if data["schema_version"] != "0.1.0" or data["source"]["commit"] != PIN:
        raise ValueError("unknown contract or unreviewed source revision")
    scope = data["scope"]
    if set(scope["families"]) != FAMILIES or scope["canonical_case_schema_changed"] is not False:
        raise ValueError("scope or canonical-schema boundary changed")
    if scope["independent_target_executions"] != 0 or scope["independent_consumer_replays"] != 0:
        raise ValueError("research artifact cannot claim external execution")
    specs = data["specifications"]
    if len(specs) != 12:
        raise ValueError("sample cardinality changed")
    by_uri = {}
    families = set()
    for s in specs:
        slug, version = s["slug"], s["version"]
        if not re.fullmatch(r"[a-z][a-z0-9-]*(?:/[a-z][a-z0-9-]*)+", slug):
            raise ValueError("invalid task slug")
        if not re.fullmatch(r"[0-9]+\.[0-9]+", version):
            raise ValueError("invalid version")
        if s["status"] != "draft":
            raise ValueError("unreviewed maturity promotion")
        if s["type_uri"] != f"https://trusttasks.org/spec/{slug}/{version}":
            raise ValueError("type URI not bound to source")
        path = f"specs/{slug}/{version}/spec.md"
        if s["source_path"] != path or s["source_url"] != (
            f"https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/{PIN}/{path}"
        ):
            raise ValueError("unpinned or incorrect source path")
        if s["type_uri"] in by_uri:
            raise ValueError("duplicate task")
        by_uri[s["type_uri"]] = s
        families.add(slug.split("/")[0])
    if families != FAMILIES:
        raise ValueError("family selection changed")
    case_ids = {p.stem for p in (ROOT / "corpus").rglob("DTF-*.json")}
    seen = set()
    touched = set()
    if len(data["judgments"]) < 12:
        raise ValueError("missing task judgments")
    for j in data["judgments"]:
        uri, case = j["task_type_uri"], j["case_id"]
        if uri not in by_uri or case not in case_ids:
            raise ValueError("missing task or canonical case")
        if (uri, case) in seen:
            raise ValueError("duplicate relation")
        seen.add((uri, case))
        touched.add(uri)
        if j["classification"] not in CLASSES:
            raise ValueError("unsupported classification")
        if j["assessment_state"] != "research-screened" or j["execution_evidence"] != "none":
            raise ValueError("research erroneously promoted to executed evidence")
        for key in ("rationale", "test_hypothesis", "authority_boundary"):
            if len(j[key]) < 65:
                raise ValueError(f"insufficient {key}")
    if touched != set(by_uri):
        raise ValueError("unscreened task")
    if len(data["limitations"]) < 4:
        raise ValueError("missing assurance boundaries")


class TrustTasksCrosswalkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(PATH.read_text(encoding="utf-8"))

    def test_canonical_mapping_valid(self):
        validate_mapping(self.data)

    def test_reject_unpinned_revision(self):
        d = copy.deepcopy(self.data)
        d["source"]["commit"] = "main"
        with self.assertRaises(ValueError):
            validate_mapping(d)

    def test_reject_forged_source_url(self):
        d = copy.deepcopy(self.data)
        d["specifications"][0]["source_url"] = "https://trusttasks.org/registry"
        with self.assertRaises(ValueError):
            validate_mapping(d)

    def test_reject_unknown_case(self):
        d = copy.deepcopy(self.data)
        d["judgments"][0]["case_id"] = "DTF-999"
        with self.assertRaises(ValueError):
            validate_mapping(d)

    def test_reject_duplicate_mapping(self):
        d = copy.deepcopy(self.data)
        d["judgments"].append(copy.deepcopy(d["judgments"][0]))
        with self.assertRaises(ValueError):
            validate_mapping(d)

    def test_reject_unsupported_claim(self):
        d = copy.deepcopy(self.data)
        d["judgments"][0]["execution_evidence"] = "verified"
        with self.assertRaises(ValueError):
            validate_mapping(d)

    def test_reject_maturity_promotion(self):
        d = copy.deepcopy(self.data)
        d["specifications"][0]["status"] = "stable"
        with self.assertRaises(ValueError):
            validate_mapping(d)


if __name__ == "__main__":
    unittest.main()
