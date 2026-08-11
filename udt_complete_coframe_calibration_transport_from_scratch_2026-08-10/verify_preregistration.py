#!/usr/bin/env python3
"""Fail-closed preregistration and source-freeze verifier."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PKG = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    required = {
        "PREREGISTRATION.md",
        "PONDER_MAP.md",
        "PREMISE_LEDGER.tsv",
        "FAMILY_AXES.tsv",
        "FALSIFICATION_CONTRACT.tsv",
        "COMPLETENESS_MAP.md",
        "SOURCE_MANIFEST.tsv",
    }
    missing = sorted(name for name in required if not (PKG / name).is_file())
    assert not missing, f"missing preregistration files: {missing}"

    with (PKG / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    assert len(rows) == 15, f"expected 15 frozen sources, found {len(rows)}"
    assert len({row["path"] for row in rows}) == len(rows), "duplicate source path"
    for row in rows:
        path = ROOT / row["path"]
        assert path.is_file(), f"missing source: {row['path']}"
        actual = sha256(path)
        assert actual == row["sha256"], f"source hash mismatch: {row['path']}"
        assert "udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02" not in row["path"]

    with (PKG / "PREMISE_LEDGER.tsv").open(newline="", encoding="utf-8") as handle:
        premises = list(csv.DictReader(handle, delimiter="\t"))
    assert len(premises) == 10
    assert {row["premise_id"] for row in premises} == {f"P{i:02d}" for i in range(1, 11)}

    with (PKG / "FAMILY_AXES.tsv").open(newline="", encoding="utf-8") as handle:
        axes = list(csv.DictReader(handle, delimiter="\t"))
    assert len(axes) == 10

    with (PKG / "FALSIFICATION_CONTRACT.tsv").open(newline="", encoding="utf-8") as handle:
        falsifiers = list(csv.DictReader(handle, delimiter="\t"))
    assert len(falsifiers) == 15
    print("preregistration: PASS")
    print("frozen_sources: 15")
    print("premises: 10")
    print("classification_axes: 10")
    print("falsifiers: 15")


if __name__ == "__main__":
    main()

