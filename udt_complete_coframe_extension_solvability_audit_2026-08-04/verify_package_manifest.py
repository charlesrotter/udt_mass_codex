#!/usr/bin/env python3
"""Render or verify the non-self-referential package manifest."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "PACKAGE_MANIFEST.tsv"


def render() -> str:
    lines = ["path\tbytes\tsha256"]
    for path in sorted(HERE.iterdir(), key=lambda item: item.name):
        if not path.is_file() or path == MANIFEST:
            continue
        data = path.read_bytes()
        lines.append(f"{path.name}\t{len(data)}\t{hashlib.sha256(data).hexdigest()}")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--render", action="store_true")
    args = parser.parse_args()
    current = render()
    if args.render:
        print(current, end="")
        return
    assert MANIFEST.read_text(encoding="utf-8") == current
    print(f"PASS: {len(current.splitlines()) - 1} package files")


if __name__ == "__main__":
    main()
