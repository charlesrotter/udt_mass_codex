#!/usr/bin/env python3
"""Freeze the preregistered source packet without modifying source artifacts."""

from __future__ import annotations

import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


paths = [line for line in (HERE / "SOURCE_PATHS.txt").read_text().splitlines() if line.strip()]
assert len(paths) == len(set(paths)) == 28
rows = ["path\tbytes\tsha256"]
for relative in paths:
    target = ROOT / relative
    assert target.is_file(), relative
    rows.append(f"{relative}\t{target.stat().st_size}\t{digest(target)}")
manifest = "\n".join(rows) + "\n"
(HERE / "SOURCE_MANIFEST.tsv").write_text(manifest, encoding="utf-8")
(HERE / "SOURCE_MANIFEST.sha256").write_text(
    digest(HERE / "SOURCE_MANIFEST.tsv") + "  SOURCE_MANIFEST.tsv\n", encoding="utf-8"
)
print(f"PASS frozen_sources={len(paths)} manifest_sha256={digest(HERE / 'SOURCE_MANIFEST.tsv')}")
