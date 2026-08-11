#!/usr/bin/env python3
"""Build the additions-only current package manifest after review adjudication."""

from __future__ import annotations

import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "POSTREVIEW_MANIFEST.tsv"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def main() -> None:
    excluded = {OUTPUT.name, "POSTREVIEW_VERIFICATION.json"}
    paths = sorted(p for p in HERE.iterdir() if p.is_file() and p.name not in excluded and "__pycache__" not in p.parts)
    lines = ["path\tsha256"]
    for path in paths:
        lines.append(f"{path.relative_to(HERE.parent)}\t{sha256(path)}")
    OUTPUT.write_text("\n".join(lines) + "\n")
    print(f"rows={len(paths)}")


if __name__ == "__main__":
    main()
