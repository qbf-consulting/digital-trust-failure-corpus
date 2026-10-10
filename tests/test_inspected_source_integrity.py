"""Negative probes for inspected source research record integrity."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from tools.validate_inspected_sources import validate_inspected_records

ROOT = Path(__file__).resolve().parents[1]


class InspectedSourceIntegrityTests(unittest.TestCase):
    def test_repository_records_valid(self):
        self.assertEqual(validate_inspected_records(), [])

    def test_invalid_case_duplicate_identity_and_malformed_url_rejected(self):
        original = json.loads((ROOT / "research/external-sources/inspected-record-dispositions.json").read_text())
        for change in ("unknown_case", "duplicate", "bad_url", "missing_basis"):
            with self.subTest(change=change), tempfile.TemporaryDirectory() as tmp:
                target = Path(tmp)
                (target / "research/external-sources").mkdir(parents=True)
                (target / "corpus").symlink_to(ROOT / "corpus", target_is_directory=True)
                data = json.loads(json.dumps(original))
                if change == "unknown_case":
                    data["records"][0]["case_id"] = "DTF-999"
                elif change == "duplicate":
                    data["records"].append(dict(data["records"][0]))
                elif change == "bad_url":
                    data["records"][0]["url"] = "https://[broken"
                else:
                    data["records"][0]["basis"] = ""
                (target / "research/external-sources/inspected-record-dispositions.json").write_text(json.dumps(data))
                self.assertTrue(validate_inspected_records(target))


if __name__ == "__main__":
    unittest.main()
