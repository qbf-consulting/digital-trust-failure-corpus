import contextlib
import io
import json
import pathlib
import tempfile
import unittest

from tools.validate import discover_case_files, main, validate_case_files

ROOT = pathlib.Path(__file__).resolve().parents[1]
VALID = ROOT / "tests" / "fixtures" / "valid" / "DTF-000.json"
INVALID_DIR = ROOT / "tests" / "fixtures" / "invalid"
SCHEMA = ROOT / "schemas" / "failure-case.schema.json"


class CorpusValidatorTests(unittest.TestCase):
    def test_valid_collection_passes(self):
        self.assertEqual(validate_case_files([VALID], SCHEMA), [])

    def test_each_negative_fixture_fails(self):
        invalid_files = discover_case_files([INVALID_DIR])
        self.assertGreaterEqual(len(invalid_files), 4)
        for path in invalid_files:
            with self.subTest(path=path.name):
                self.assertTrue(validate_case_files([path], SCHEMA))

    def test_duplicate_ids_are_rejected(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = pathlib.Path(temp_dir)
            case = json.loads(VALID.read_text(encoding="utf-8"))
            first = temp / "one.json"
            second = temp / "two.json"
            first.write_text(json.dumps(case), encoding="utf-8")
            case["title"] = "second-title"
            second.write_text(json.dumps(case), encoding="utf-8")
            findings = validate_case_files([first, second], SCHEMA)
            self.assertTrue(any("duplicate case id" in item.message for item in findings))

    def test_duplicate_titles_are_rejected(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = pathlib.Path(temp_dir)
            case = json.loads(VALID.read_text(encoding="utf-8"))
            first = temp / "one.json"
            second = temp / "two.json"
            first.write_text(json.dumps(case), encoding="utf-8")
            case["id"] = "DTF-999"
            second.write_text(json.dumps(case), encoding="utf-8")
            findings = validate_case_files([first, second], SCHEMA)
            self.assertTrue(any("duplicate case title" in item.message for item in findings))

    def test_empty_directory_is_valid_but_reports_zero_cases(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                result = main([temp_dir])
            self.assertEqual(result, 0)
            self.assertIn("Validated 0 case file(s).", output.getvalue())

    def test_cli_returns_nonzero_and_file_context_for_invalid_case(self):
        target = INVALID_DIR / "missing-evidence.json"
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            result = main([str(target)])
        self.assertEqual(result, 1)
        self.assertIn(str(target), stderr.getvalue())
        self.assertIn("schema violation", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
