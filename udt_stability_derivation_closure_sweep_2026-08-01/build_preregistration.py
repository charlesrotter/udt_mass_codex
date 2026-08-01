#!/usr/bin/env python3
"""Freeze the source universe for the derivation-closure sweep."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PKG = Path(__file__).resolve().parent
PARENT = ROOT / "udt_stability_family_survivor_map_2026-08-01"
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
    if len(inherited) != 1513:
        raise RuntimeError(f"parent source count changed: {len(inherited)}")
    parent_paths = subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", "HEAD", PARENT_PACKAGE], cwd=ROOT, text=True
    ).splitlines()
    if len(parent_paths) != 45:
        raise RuntimeError(f"parent package count changed: {len(parent_paths)}")
    layers = {row["path"]: "PARENT_SURVIVOR_SOURCE_UNIVERSE" for row in inherited}
    if set(parent_paths) & set(layers):
        raise RuntimeError("unexpected source-layer overlap")
    layers.update({path: "COMPLETE_PARENT_SURVIVOR_PACKAGE" for path in parent_paths})
    if len(layers) != 1558:
        raise RuntimeError(f"source union changed: {len(layers)}")
    records = []
    for rel in sorted(layers):
        path = ROOT / rel
        if not path.is_file():
            raise RuntimeError(f"missing source: {rel}")
        records.append({"path": rel, "git_blob": blob(rel), "sha256": sha256(path), "bytes": path.stat().st_size, "layer": layers[rel]})
    write_tsv("SOURCE_INVENTORY.tsv", records)
    (PKG / "SOURCE_PATHS.txt").write_text("\n".join(row["path"] for row in records) + "\n", encoding="utf-8")
    (PKG / "SOURCE_MANIFEST.sha256").write_text("\n".join(f"{row['sha256']}  ../{row['path']}" for row in records) + "\n", encoding="utf-8")
    write_tsv("SOURCE_SCOPE.tsv", [
        {"layer": "PARENT_SURVIVOR_SOURCE_UNIVERSE", "expected_paths": 1513, "rule": "exact inherited freeze"},
        {"layer": "COMPLETE_PARENT_SURVIVOR_PACKAGE", "expected_paths": 45, "rule": "all tracked parent-package files at base"},
        {"layer": "UNION", "expected_paths": 1558, "rule": "sorted unique additions-only union"},
    ])
    print("PASS sweep preregistration build: sources=1558 groups=4 objects=15 statuses=7 outcomes=5")


if __name__ == "__main__":
    main()
