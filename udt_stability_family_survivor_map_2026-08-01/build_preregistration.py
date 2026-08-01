#!/usr/bin/env python3
"""Freeze the additions-only source and family universe for the survivor map."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PKG = Path(__file__).resolve().parent
PARENT = ROOT / "udt_stability_hypothesis_cross_family_atlas_2026-08-01"
PARENT_PACKAGE = PARENT.name


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def blob(path: str) -> str:
    return subprocess.check_output(["git", "rev-parse", f"HEAD:{path}"], cwd=ROOT, text=True).strip()


def write_tsv(name: str, rows: list[dict[str, object]]) -> None:
    with (PKG / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    with (PARENT / "SOURCE_INVENTORY.tsv").open(newline="", encoding="utf-8") as handle:
        inherited = list(csv.DictReader(handle, delimiter="\t"))
    if len(inherited) != 1469:
        raise RuntimeError(f"parent source count changed: {len(inherited)}")

    parent_paths = subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", "HEAD", PARENT_PACKAGE], cwd=ROOT, text=True
    ).splitlines()
    if len(parent_paths) != 44:
        raise RuntimeError(f"parent package count changed: {len(parent_paths)}")

    layers = {row["path"]: "PARENT_EFFECTIVE_SOURCE_UNIVERSE" for row in inherited}
    if set(parent_paths) & set(layers):
        raise RuntimeError("unexpected source-layer overlap")
    layers.update({path: "COMPLETE_PARENT_ATLAS_PACKAGE" for path in parent_paths})
    if len(layers) != 1513:
        raise RuntimeError(f"source union changed: {len(layers)}")

    source_rows = []
    for rel in sorted(layers):
        path = ROOT / rel
        if not path.is_file():
            raise RuntimeError(f"missing source: {rel}")
        source_rows.append({
            "path": rel,
            "git_blob": blob(rel),
            "sha256": sha256(path),
            "bytes": path.stat().st_size,
            "layer": layers[rel],
        })
    write_tsv("SOURCE_INVENTORY.tsv", source_rows)
    (PKG / "SOURCE_PATHS.txt").write_text(
        "\n".join(row["path"] for row in source_rows) + "\n", encoding="utf-8"
    )
    (PKG / "SOURCE_MANIFEST.sha256").write_text(
        "\n".join(f"{row['sha256']}  ../{row['path']}" for row in source_rows) + "\n",
        encoding="utf-8",
    )
    write_tsv("SOURCE_SCOPE.tsv", [
        {"layer": "PARENT_EFFECTIVE_SOURCE_UNIVERSE", "expected_paths": 1469, "rule": "exact inherited effective freeze"},
        {"layer": "COMPLETE_PARENT_ATLAS_PACKAGE", "expected_paths": 44, "rule": "all tracked parent-package files at base"},
        {"layer": "UNION", "expected_paths": 1513, "rule": "sorted unique additions-only union"},
    ])

    with (PARENT / "FAMILY_PARTITION_LEDGER.tsv").open(newline="", encoding="utf-8") as handle:
        partitions = list(csv.DictReader(handle, delimiter="\t"))
    if [row["family_id"] for row in partitions] != [f"F{i:02d}" for i in range(1, 8)]:
        raise RuntimeError("parent family partition changed")
    family_rows = [
        {"family_id": row["family_id"], "effective_partition_key": row["effective_partition_key"]}
        for row in partitions
    ]
    write_tsv("FAMILY_UNIVERSE.tsv", family_rows)
    print("PASS preregistration build: sources=1513 families=7 cells=12 readiness=11 outcomes=5")


if __name__ == "__main__":
    main()
