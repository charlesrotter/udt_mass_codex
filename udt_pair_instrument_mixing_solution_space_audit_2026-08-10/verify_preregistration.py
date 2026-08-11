#!/usr/bin/env python3
"""Fail-closed preregistration and source-manifest verifier."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


required = {
    "PREREGISTRATION.md",
    "PONDER_MAP.md",
    "PREMISE_LEDGER.tsv",
    "INSTRUMENT_AXES.tsv",
    "FALSIFICATION_CONTRACT.tsv",
    "COMPLETENESS_MAP.md",
    "SOURCE_MANIFEST.tsv",
}
missing = sorted(name for name in required if not (HERE / name).is_file())
assert not missing, f"missing preregistration files: {missing}"

with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
    rows = list(csv.DictReader(handle, delimiter="\t"))

assert len(rows) == 15, f"expected 15 frozen sources, found {len(rows)}"
paths = [row["path"] for row in rows]
assert len(paths) == len(set(paths)), "duplicate source path"
for row in rows:
    source = ROOT / row["path"]
    assert source.is_file(), f"missing source: {row['path']}"
    actual = digest(source)
    assert actual == row["sha256"], (
        f"source hash mismatch: {row['path']} expected={row['sha256']} actual={actual}"
    )

premise_text = (HERE / "PREREGISTRATION.md").read_text(encoding="utf-8")
for token in (
    "metric-led solution-space map",
    "No time, angular, shift, or mixing component is frozen",
    "strong local CSN",
    "c_E",
    "UNIQUE_POSITIVE_MIXING_LAW",
    "SPLIT_RELATIVE_SIGNED_ORCHESTRA_ATLAS",
):
    assert token in premise_text, f"missing scope guard: {token}"

print(f"PASS preregistration files={len(required)} sources={len(rows)}")
