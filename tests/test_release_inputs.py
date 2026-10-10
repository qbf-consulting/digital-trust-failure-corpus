"""Negative release-input tests; no publication."""
import tempfile
import unittest
from pathlib import Path
from tools.verify_release_inputs import verify_release_inputs

SHA = "a" * 40

class ReleaseInputsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        self.version = root / "VERSION"
        self.notes = root / "notes.md"
        self.version.write_text("0.5.0\n")
        self.notes.write_text("Documented evidence review\n")

    def check(self, **changes):
        args = dict(version_file=self.version, notes=self.notes, existing_tags=set(),
                    checked_out_sha=SHA, expected_sha=SHA)
        args.update(changes)
        return verify_release_inputs(**args)

    def test_valid_inputs_do_not_publish(self):
        self.assertEqual(self.check(), "v0.5.0")

    def test_existing_tag_rejected(self):
        with self.assertRaisesRegex(ValueError, "already exists"):
            self.check(existing_tags={"v0.5.0"})

    def test_missing_and_empty_notes_rejected(self):
        self.notes.unlink()
        with self.assertRaisesRegex(ValueError, "notes"):
            self.check()
        self.notes.write_text("")
        with self.assertRaisesRegex(ValueError, "notes"):
            self.check()

    def test_stale_and_invalid_sha_rejected(self):
        with self.assertRaisesRegex(ValueError, "mismatched"):
            self.check(checked_out_sha="b" * 40)
        with self.assertRaisesRegex(ValueError, "Invalid expected"):
            self.check(expected_sha="not-a-sha")

    def test_invalid_version_rejected(self):
        self.version.write_text("0.5.0; rm -rf /")
        with self.assertRaisesRegex(ValueError, "Invalid"):
            self.check()

if __name__ == "__main__":
    unittest.main()
