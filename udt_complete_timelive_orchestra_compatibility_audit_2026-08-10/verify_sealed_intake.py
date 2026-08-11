#!/usr/bin/env python3
"""Read-only verification of the exact 13-source repository or sealed-intake layout."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
PARENT = HERE.parent


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            value.update(block)
    return value.hexdigest()


with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
    rows = list(csv.DictReader(handle, delimiter="\t"))

assert len(rows) == 13
assert len({row["path"] for row in rows}) == 13
assert not any(
    "udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02" in row["path"]
    or "udt_native_onshell_timelive_reset_owner_audit_2026-08-10" in row["path"]
    for row in rows
)

sealed = PARENT / "sources"
repository = PARENT
if all((sealed / row["path"]).is_file() for row in rows):
    root = sealed
    layout = "sealed_sources"
elif all((repository / row["path"]).is_file() for row in rows):
    root = repository
    layout = "repository"
else:
    raise AssertionError("neither exact repository nor sealed source layout is complete")

for row in rows:
    source = root / row["path"]
    assert digest(source) == row["sha256"], row["path"]

print(f"PASS layout={layout} sources={len(rows)}")
