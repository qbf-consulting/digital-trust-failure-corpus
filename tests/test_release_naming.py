from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "select_release_name.py"
POOL_PATH = ROOT / "release" / "national-flower-codenames.txt"

spec = importlib.util.spec_from_file_location("select_release_name", MODULE_PATH)
assert spec and spec.loader
release_names = importlib.util.module_from_spec(spec)
spec.loader.exec_module(release_names)


class ReleaseNamingTests(unittest.TestCase):
    def test_pool_is_substantial_and_unique(self) -> None:
        pool = release_names.load_pool(POOL_PATH)
        self.assertGreaterEqual(len(pool), 40)
        self.assertEqual(len(pool), len(set(pool)))

    def test_used_names_are_excluded_while_unused_names_remain(self) -> None:
        pool = ["Lotus", "Daffodil", "Edelweiss"]
        titles = ["Lotus — v0.1.0", "Unrelated title"]
        chosen = release_names.select_codename(
            pool,
            titles,
            chooser=lambda candidates: candidates[0],
        )
        self.assertEqual(chosen, "Daffodil")

    def test_pool_restarts_only_after_all_names_are_used(self) -> None:
        pool = ["Lotus", "Daffodil"]
        titles = ["Lotus — v0.1.0", "Daffodil — v0.2.0"]
        chosen = release_names.select_codename(
            pool,
            titles,
            chooser=lambda candidates: candidates[-1],
        )
        self.assertEqual(chosen, "Daffodil")

    def test_nonconforming_release_titles_do_not_consume_names(self) -> None:
        pool = ["Lotus", "Daffodil"]
        titles = ["Lotus experimental", "v0.1.0 — Lotus"]
        self.assertEqual(release_names.used_codenames(titles, pool), set())


if __name__ == "__main__":
    unittest.main()
