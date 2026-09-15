#!/usr/bin/env python3
"""Select a human-facing release codename from the committed flower pool."""

from __future__ import annotations

import argparse
import random
from pathlib import Path
from typing import Callable, Iterable, Sequence


def load_pool(path: Path) -> list[str]:
    names: list[str] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        name = raw.strip()
        if not name or name.startswith("#"):
            continue
        names.append(name)
    if not names:
        raise ValueError("release codename pool is empty")
    if len(names) != len(set(names)):
        raise ValueError("release codename pool contains duplicate names")
    return names


def used_codenames(release_titles: Iterable[str], pool: Sequence[str]) -> set[str]:
    titles = [title.strip() for title in release_titles if title.strip()]
    used: set[str] = set()
    for flower in pool:
        prefix = f"{flower} — v"
        if any(title.startswith(prefix) for title in titles):
            used.add(flower)
    return used


def select_codename(
    pool: Sequence[str],
    release_titles: Iterable[str] = (),
    chooser: Callable[[Sequence[str]], str] | None = None,
) -> str:
    if not pool:
        raise ValueError("release codename pool is empty")
    used = used_codenames(release_titles, pool)
    available = [name for name in pool if name not in used]
    candidates = available or list(pool)
    choose = chooser or random.SystemRandom().choice
    return choose(candidates)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pool", type=Path, required=True)
    parser.add_argument(
        "--used-titles",
        type=Path,
        help="Optional file containing one prior GitHub Release title per line.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    pool = load_pool(args.pool)
    titles: list[str] = []
    if args.used_titles and args.used_titles.exists():
        titles = args.used_titles.read_text(encoding="utf-8").splitlines()
    print(select_codename(pool, titles))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
