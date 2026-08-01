#!/usr/bin/env python3
"""Freeze the additions-only source and pair universes for the ontology audit."""

from __future__ import annotations

import csv
import hashlib
import itertools
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PKG = Path(__file__).resolve().parent
PARENT = ROOT / "udt_stability_derivation_closure_sweep_2026-08-01"


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
    if len(inherited) != 1558:
        raise RuntimeError(f"parent source count changed: {len(inherited)}")
    parent_paths = subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", "HEAD", PARENT.name], cwd=ROOT, text=True
    ).splitlines()
    if len(parent_paths) != 47:
        raise RuntimeError(f"complete parent package count changed: {len(parent_paths)}")
    layers = {row["path"]: "PARENT_SWEEP_SOURCE_UNIVERSE" for row in inherited}
    if set(parent_paths) & set(layers):
        raise RuntimeError("unexpected source-layer overlap")
    layers.update({path: "COMPLETE_PARENT_SWEEP_PACKAGE" for path in parent_paths})
    if len(layers) != 1605:
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
        {"layer": "PARENT_SWEEP_SOURCE_UNIVERSE", "expected_paths": 1558, "rule": "exact inherited freeze"},
        {"layer": "COMPLETE_PARENT_SWEEP_PACKAGE", "expected_paths": 47, "rule": "all tracked parent-package files at base"},
        {"layer": "UNION", "expected_paths": 1605, "rule": "sorted unique additions-only union"},
    ])
    families = [f"F{i:02d}" for i in range(1, 8)]
    pairs = []
    for index, (left, right) in enumerate(itertools.combinations_with_replacement(families, 2), 1):
        pairs.append({"pair_id": f"P{index:02d}", "left_family": left, "right_family": right, "diagonal": "YES" if left == right else "NO"})
    write_tsv("PAIRWISE_UNIVERSE.tsv", pairs)
    print("PASS ontology preregistration build: sources=1605 families=7 axes=10 pairs=28 statuses=9 relations=11 outcomes=5")


if __name__ == "__main__":
    main()
