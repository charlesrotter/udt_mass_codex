#!/usr/bin/env python3
"""Build the recursive G236 final evidence manifest without persistent runtime byproducts."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "FINAL_EVIDENCE_MANIFEST.tsv"


def main() -> None:
    rows: list[tuple[str, str]] = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path == OUTPUT or "__pycache__" in path.parts:
            continue
        relative = path.relative_to(ROOT).as_posix()
        rows.append((hashlib.sha256(path.read_bytes()).hexdigest(), relative))
    body = "sha256\tpath\n" + "".join(f"{digest}\t{relative}\n" for digest, relative in rows)
    OUTPUT.write_text(body, encoding="utf-8")


if __name__ == "__main__":
    main()
